# Investify - Stock Market Simulation Game

A modern, interactive stock market simulation game built with Python Flask, MySQL, and modern web technologies. Learn trading with virtual money in a risk-free environment.

## Features

- 🎮 **Virtual Trading**: Start with $10,000 virtual money
- 📊 **Real-time Data**: Live stock prices and market data
- 🏆 **Competition**: Global leaderboards and friend competitions
- 🎯 **Achievements**: Unlock badges and rewards
- 📚 **Educational**: Interactive tutorials and learning resources
- 🎨 **Modern UI**: Dark theme with beautiful gradients and animations

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with gradients and animations
- **Icons**: Font Awesome
- **Authentication**: Flask-Login

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd investify
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   ```sql
   CREATE DATABASE investify;
   CREATE USER 'investify_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON investify.* TO 'investify_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Configure database connection**
   Edit `app.py` and update the database URI:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://investify_user:your_password@localhost/investify'
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Project Structure

```
investify/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── dashboard.html    # User dashboard
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # Main JavaScript file
│   └── images/           # Image assets
```

## Features Implemented

### ✅ Authentication System
- User registration with email validation
- Secure login with password hashing
- Password visibility toggle
- Session management

### ✅ Homepage/Landing Page
- Modern hero section with call-to-action
- Feature highlights with animated badges
- Responsive design
- Smooth scrolling navigation

### ✅ Dashboard
- Portfolio overview with key metrics
- Quick stats sidebar
- Action buttons for trading
- Market insights and tips
- Recent trades section

### ✅ User Interface
- Dark theme with neon accents
- Gradient backgrounds and animations
- Responsive design for mobile devices
- Modern card-based layout
- Interactive hover effects

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `portfolio_value`: Current portfolio value
- `cash_balance`: Available cash
- `global_rank`: User's global ranking
- `friends_count`: Number of friends
- `achievements_count`: Achievements earned
- `total_achievements`: Total available achievements
- `created_at`: Account creation timestamp

## Security Features

- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Input validation and sanitization
- Secure password requirements

## Customization

### Colors and Theme
The application uses a custom color scheme defined in `static/css/style.css`:
- Primary: `#00b8ff` (Blue)
- Secondary: `#00ff88` (Green)
- Accent: `#9d4edd` (Purple)
- Background: Dark gradient from `#0a0a0a` to `#16213e`

### Adding New Features
1. Create new routes in `app.py`
2. Add corresponding templates in `templates/`
3. Update navigation in templates
4. Add any required JavaScript in `static/js/`

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Database Migrations
The application uses Flask-SQLAlchemy for database management. Tables are automatically created when the app starts.

### Adding New Models
1. Define the model in `app.py`
2. Import and register with the database
3. Tables will be created automatically on app startup

## Deployment

### Production Considerations
1. Change the secret key in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up a reverse proxy (Nginx)
4. Use environment variables for sensitive data
5. Enable HTTPS
6. Set up proper logging

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
export DATABASE_URL=mysql://user:password@host/database
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## Roadmap

### Phase 2 Features (Next Steps)
- [ ] Stock trading functionality
- [ ] Real-time stock data integration
- [ ] Leaderboard system
- [ ] Achievement system
- [ ] Friend system
- [ ] Tutorial system
- [ ] Market research tools
- [ ] Portfolio analytics
- [ ] Mobile app version

### Phase 3 Features
- [ ] Advanced trading features
- [ ] Social features
- [ ] Educational content
- [ ] API for third-party integrations
- [ ] Advanced analytics
- [ ] Multi-language support 