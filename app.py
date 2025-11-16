from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_
try:
    import requests
except ImportError:
    requests = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Database configuration - supports both SQLite (local) and PostgreSQL (production)
database_url = os.environ.get('DATABASE_URL', '').strip()
if database_url:
    # Render and other services use postgres://, but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    # For Python 3.13+, try to use psycopg instead of psycopg2
    if database_url.startswith('postgresql://') and not database_url.startswith('postgresql+psycopg://'):
        try:
            import sys
            if sys.version_info >= (3, 13):
                # Try to import psycopg, if available use it
                try:
                    import psycopg
                    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
                except ImportError:
                    # Fall back to psycopg2 if psycopg not available
                    pass
        except:
            pass
    # Validate the URL is not empty after processing
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Fallback to SQLite if DATABASE_URL is invalid
        os.makedirs(app.instance_path, exist_ok=True)
        default_sqlite_path = os.path.join(app.instance_path, 'investify.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{default_sqlite_path}'
else:
    # Default to SQLite for local development
    os.makedirs(app.instance_path, exist_ok=True)
    default_sqlite_path = os.path.join(app.instance_path, 'investify.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{default_sqlite_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.unauthorized_handler
def unauthorized():
    # Return JSON for API calls and redirect otherwise
    if request.path.startswith('/execute_trade') or request.path.startswith('/get_portfolio_data'):
        return jsonify({'success': False, 'message': 'Please log in to continue'}), 401
    return redirect(url_for('login'))

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    portfolio_value = db.Column(db.Float, default=10000.0)
    cash_balance = db.Column(db.Float, default=10000.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    global_rank = db.Column(db.Integer, default=0)
    friends_count = db.Column(db.Integer, default=0)
    achievements_count = db.Column(db.Integer, default=0)
    total_achievements = db.Column(db.Integer, default=25)
    bio = db.Column(db.String(500), default="")
    avatar_color = db.Column(db.String(20), default="#00b8ff")
    # Analytics columns
    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, default=0)
    total_time_spent = db.Column(db.Integer, default=0)  # in minutes
    trades_made = db.Column(db.Integer, default=0)
    total_trades_value = db.Column(db.Float, default=0.0)
    achievements_unlocked = db.Column(db.Integer, default=0)
    tutorial_completed = db.Column(db.Boolean, default=False)
    profile_views = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

# Friends Model
class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Achievement Model
class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    xp_reward = db.Column(db.Integer, default=0)
    icon = db.Column(db.String(50), default="fas fa-star")

# User Achievement Model
class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

# Holding Model
class Holding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(16), nullable=False)
    company_name = db.Column(db.String(120), nullable=False)
    shares = db.Column(db.Integer, default=0)
    avg_price = db.Column(db.Float, default=0.0)
    last_price = db.Column(db.Float, default=0.0)  # last known market price used for portfolio valuation

# Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(16), nullable=False)
    action = db.Column(db.String(4), nullable=False)  # BUY or SELL
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def update_user_rankings():
    """Update global rankings based on portfolio value"""
    users = User.query.order_by(User.portfolio_value.desc()).all()
    for i, user in enumerate(users, 1):
        user.global_rank = i
    db.session.commit()

def get_user_friends_count(user_id):
    """Get the number of friends for a user"""
    return Friendship.query.filter_by(user_id=user_id).count()

def get_user_achievements_count(user_id):
    """Get the number of achievements earned by a user"""
    return UserAchievement.query.filter_by(user_id=user_id).count()

def init_database():
    """Create all tables and seed initial data when needed.

    This runs at app startup so tables exist regardless of how the server is started
    (flask run, gunicorn, etc.).
    """
    db.create_all()
    # Create default achievements if they don't exist
    if not Achievement.query.first():
        achievements = [
            Achievement(name="First Trade", description="Complete your first trade", category="trading", xp_reward=50, icon="fas fa-star"),
            Achievement(name="Doubled Money", description="Double your starting portfolio", category="milestones", xp_reward=200, icon="fas fa-rocket"),
            Achievement(name="Risk Taker", description="Make 10 high-risk trades", category="risk", xp_reward=150, icon="fas fa-bullseye"),
            Achievement(name="Streak Master", description="Maintain a 7-day trading streak", category="streaks", xp_reward=100, icon="fas fa-bolt"),
            Achievement(name="Diversifier", description="Own stocks from 5 different industries", category="trading", xp_reward=75, icon="fas fa-chart-pie"),
            Achievement(name="Profit Hunter", description="Make 5 consecutive profitable trades", category="profit", xp_reward=125, icon="fas fa-chart-line"),
            Achievement(name="Millionaire", description="Reach $1,000,000 portfolio value", category="milestones", xp_reward=500, icon="fas fa-crown"),
            Achievement(name="Social Trader", description="Add 10 friends", category="social", xp_reward=50, icon="fas fa-users"),
            Achievement(name="Quick Learner", description="Complete the tutorial", category="education", xp_reward=25, icon="fas fa-graduation-cap"),
            Achievement(name="Market Master", description="Trade 50 different stocks", category="trading", xp_reward=300, icon="fas fa-trophy"),
        ]
        for achievement in achievements:
            db.session.add(achievement)
        db.session.commit()

# Initialize the database at import/startup time
with app.app_context():
    init_database()

@app.route('/init_db', methods=['POST'])
def init_db():
    with app.app_context():
        db.create_all()
        return jsonify({'success': True})

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        identifier = data.get('username')  # Can be username or email
        password = data.get('password')
        
        # Allow login by username or email
        user = User.query.filter(or_(User.username == identifier, User.email == identifier)).first()
        if user and check_password_hash(user.password_hash, password):
            # Update login analytics
            user.login_count = (user.login_count or 0) + 1
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            login_user(user)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            return jsonify({'success': False, 'message': 'Invalid username/email or password'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'})
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        # Update rankings after adding new user
        update_user_rankings()
        
        return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Update user stats
    current_user.friends_count = get_user_friends_count(current_user.id)
    current_user.achievements_count = get_user_achievements_count(current_user.id)
    db.session.commit()
    
    return render_template('dashboard.html', user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    data = request.get_json()
    bio = data.get('bio', '')
    avatar_color = data.get('avatar_color', '#00b8ff')
    
    current_user.bio = bio
    current_user.avatar_color = avatar_color
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile updated successfully!'})

@app.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    data = request.get_json()
    friend_username = data.get('username')
    
    if not friend_username:
        return jsonify({'success': False, 'message': 'Please enter a username'})
    
    if friend_username == current_user.username:
        return jsonify({'success': False, 'message': 'You cannot add yourself as a friend'})
    
    friend = User.query.filter_by(username=friend_username).first()
    if not friend:
        return jsonify({'success': False, 'message': 'User not found'})
    
    # Check if already friends
    existing_friendship = Friendship.query.filter_by(
        user_id=current_user.id, 
        friend_id=friend.id
    ).first()
    
    if existing_friendship:
        return jsonify({'success': False, 'message': 'Already friends with this user'})
    
    # Add friendship
    friendship = Friendship(user_id=current_user.id, friend_id=friend.id)
    db.session.add(friendship)
    db.session.commit()
    
    # Update friend counts
    current_user.friends_count = get_user_friends_count(current_user.id)
    friend.friends_count = get_user_friends_count(friend.id)
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'Successfully added {friend_username} as a friend!'})

@app.route('/market')
@login_required
def market():
    return render_template('market.html', user=current_user)

@app.route('/portfolio')
@login_required
def portfolio():
    return render_template('portfolio.html', user=current_user)

@app.route('/leaderboard')
@login_required
def leaderboard():
    # Get all users ordered by portfolio value
    users = User.query.order_by(User.portfolio_value.desc()).all()
    return render_template('leaderboard.html', user=current_user, users=users)

@app.route('/achievements')
@login_required
def achievements():
    # Get all achievements
    all_achievements = Achievement.query.all()
    
    # Get user's earned achievements
    user_achievements = UserAchievement.query.filter_by(user_id=current_user.id).all()
    earned_achievement_ids = [ua.achievement_id for ua in user_achievements]
    
    # Update user's achievement count
    current_user.achievements_count = len(earned_achievement_ids)
    db.session.commit()
    
    return render_template('achievements.html', 
                         user=current_user, 
                         all_achievements=all_achievements,
                         earned_achievement_ids=earned_achievement_ids)

@app.route('/tutorial')
@login_required
def tutorial():
    return render_template('tutorial.html', user=current_user)

@app.route('/get_portfolio_data')
@login_required
def get_portfolio_data():
    """Get portfolio data for dashboard and portfolio pages"""
    user_holdings = Holding.query.filter_by(user_id=current_user.id).all()
    user_txns = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()

    holdings_payload = []
    total_stocks_value = 0.0
    for h in user_holdings:
        current_price = h.last_price or h.avg_price
        total_value = current_price * h.shares
        gain_loss = (current_price - h.avg_price) * h.shares
        gain_loss_percent = 0.0 if h.avg_price == 0 else ((current_price - h.avg_price) / h.avg_price) * 100
        holdings_payload.append({
            'symbol': h.symbol,
            'company_name': h.company_name,
            'shares': h.shares,
            'avg_price': h.avg_price,
            'current_price': current_price,
            'total_value': total_value,
            'gain_loss': gain_loss,
            'gain_loss_percent': gain_loss_percent,
        })
        total_stocks_value += total_value

    portfolio_stats = {
        'total_value': current_user.cash_balance + total_stocks_value,
        'total_gain_loss': 0.0,
        'total_gain_loss_percent': 0.0,
        'holdings_count': len(user_holdings)
    }

    transactions_payload = [{
        'symbol': t.symbol,
        'action': t.action,
        'shares': t.shares,
        'price': t.price,
        'timestamp': t.timestamp.isoformat()
    } for t in user_txns]
    
    return jsonify({
        'portfolio_stats': portfolio_stats,
        'holdings': holdings_payload,
        'transactions': transactions_payload
    })

@app.route('/execute_trade', methods=['POST'])
@login_required
def execute_trade():
    try:
        # Ensure tables exist (helps if DB was created before new models)
        db.create_all()
        data = request.get_json(silent=True) or {}
        app.logger.info(f"/execute_trade payload: {data}")
        symbol = data.get('symbol')
        action = data.get('action')  # BUY or SELL
        shares = int(data.get('shares', 0))
        price = float(data.get('price', 0))
        company_name = data.get('company_name', symbol)

        if not symbol or shares <= 0 or price <= 0 or action not in ('BUY', 'SELL'):
            return jsonify({'success': False, 'message': 'Invalid trade request'})

        holding = Holding.query.filter_by(user_id=current_user.id, symbol=symbol).first()

        if action == 'BUY':
            cost = shares * price
            if current_user.cash_balance < cost:
                return jsonify({'success': False, 'message': 'Insufficient cash balance'})

            if not holding:
                holding = Holding(user_id=current_user.id, symbol=symbol, company_name=company_name, shares=0, avg_price=0.0, last_price=price)
                db.session.add(holding)

            total_cost_existing = holding.avg_price * holding.shares
            total_cost_new = shares * price
            new_total_shares = holding.shares + shares
            holding.avg_price = (total_cost_existing + total_cost_new) / new_total_shares
            holding.shares = new_total_shares
            holding.last_price = price
            current_user.cash_balance -= cost
            db.session.add(Transaction(user_id=current_user.id, symbol=symbol, action='BUY', shares=shares, price=price))

        elif action == 'SELL':
            if not holding or holding.shares < shares:
                return jsonify({'success': False, 'message': 'Not enough shares to sell'})
            proceeds = shares * price
            holding.shares -= shares
            holding.last_price = price
            if holding.shares == 0:
                holding.avg_price = 0.0
            current_user.cash_balance += proceeds
            db.session.add(Transaction(user_id=current_user.id, symbol=symbol, action='SELL', shares=shares, price=price))

        user_holdings = Holding.query.filter_by(user_id=current_user.id).all()
        stocks_value = sum(h.shares * (h.last_price or h.avg_price) for h in user_holdings)
        current_user.portfolio_value = current_user.cash_balance + stocks_value

        db.session.commit()
        # Award achievements
        try:
            first_trade = Achievement.query.filter_by(name="First Trade").first()
            if first_trade and not UserAchievement.query.filter_by(user_id=current_user.id, achievement_id=first_trade.id).first():
                db.session.add(UserAchievement(user_id=current_user.id, achievement_id=first_trade.id))
                db.session.commit()
        except Exception:
            db.session.rollback()

        # Update rankings after portfolio update
        update_user_rankings()

        return jsonify({
            'success': True,
            'message': 'Trade executed successfully!',
            'new_portfolio_value': current_user.portfolio_value,
            'cash_balance': current_user.cash_balance
        })
    except Exception as e:
        db.session.rollback()
        app.logger.exception("Trade failed")
        # Return 200 with success:false so the frontend reliably shows the message
        return jsonify({'success': False, 'message': f'Trade failed: {str(e)}'})

@app.route('/refresh_prices', methods=['POST'])
@login_required
def refresh_prices():
    try:
        if not requests:
            return jsonify({'success': False, 'message': 'requests library not installed. Run: pip install requests'})
        user_holdings = Holding.query.filter_by(user_id=current_user.id).all()
        if not user_holdings:
            return jsonify({'success': True, 'message': 'No holdings to refresh.', 'portfolio_value': current_user.portfolio_value, 'updated': 0})

        symbols = ','.join([h.symbol for h in user_holdings])
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}"
        r = requests.get(url, timeout=6)
        data = r.json()
        result = (data.get('quoteResponse', {}).get('result', []))
        symbol_to_price = {item.get('symbol'): float(item.get('regularMarketPrice', 0) or 0) for item in result}

        updates = 0
        for h in user_holdings:
            new_price = symbol_to_price.get(h.symbol)
            if new_price is not None and new_price > 0 and abs(new_price - (h.last_price or 0)) > 1e-9:
                h.last_price = new_price
                updates += 1

        # Recompute portfolio
        stocks_value = sum(h.shares * (h.last_price or h.avg_price) for h in user_holdings)
        current_user.portfolio_value = current_user.cash_balance + stocks_value
        db.session.commit()

        # Rankings refresh
        update_user_rankings()

        return jsonify({'success': True, 'message': 'Prices refreshed', 'portfolio_value': current_user.portfolio_value, 'updated': updates})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Price refresh failed: {str(e)}'})

@app.route('/get_user_data')
@login_required
def get_user_data():
    """Get current user data"""
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'portfolio_value': current_user.portfolio_value,
        'cash_balance': current_user.cash_balance,
        'global_rank': current_user.global_rank,
        'friends_count': current_user.friends_count,
        'achievements_count': current_user.achievements_count
    })

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=False, host='0.0.0.0', port=port)
