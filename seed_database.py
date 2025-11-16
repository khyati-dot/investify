#!/usr/bin/env python3
"""
Seed the database with 29 users and friendships
Run this script to populate your database with sample data
"""
from app import app, db, User, Friendship
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def seed_database():
    """Add 29 users and create friendships"""
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing users)
        # Friendship.query.delete()
        # User.query.filter(User.id > 1).delete()  # Keep first user if exists
        
        # List of realistic usernames
        usernames = [
            "alex_trader", "sarah_invests", "mike_wallstreet", "emma_stocks", "james_market",
            "lisa_portfolio", "david_trades", "olivia_finance", "chris_investor", "sophia_wealth",
            "ryan_trading", "mia_stocks", "noah_market", "ava_invests", "ethan_portfolio",
            "isabella_trader", "lucas_finance", "amelia_stocks", "henry_market", "charlotte_invests",
            "benjamin_trades", "harper_portfolio", "mason_finance", "ella_stocks", "jackson_market",
            "luna_invests", "aiden_trader", "zoe_portfolio", "carter_finance"
        ]
        
        # Create 29 users
        users = []
        for i, username in enumerate(usernames):
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                users.append(existing_user)
                continue
            
            user = User(
                username=username,
                email=f"{username}@example.com",
                password_hash=generate_password_hash("password123"),  # Default password
                portfolio_value=random.uniform(8000, 15000),
                cash_balance=random.uniform(5000, 12000),
                global_rank=i + 1,
                friends_count=0,
                achievements_count=random.randint(0, 10),
                total_achievements=25,
                created_at=datetime.now() - timedelta(days=random.randint(1, 90)),
                login_count=random.randint(5, 50),
                trades_made=random.randint(0, 30),
                total_trades_value=random.uniform(1000, 5000),
                achievements_unlocked=random.randint(0, 10),
                tutorial_completed=random.choice([True, False]),
                profile_views=random.randint(0, 100),
                is_active=True
            )
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create friendships (each user has 2-5 friends)
        friendships_created = 0
        for user in users:
            # Each user will have 2-5 random friends
            num_friends = random.randint(2, 5)
            potential_friends = [u for u in users if u.id != user.id]
            friends = random.sample(potential_friends, min(num_friends, len(potential_friends)))
            
            for friend in friends:
                # Check if friendship already exists (either direction)
                existing = Friendship.query.filter(
                    ((Friendship.user_id == user.id) & (Friendship.friend_id == friend.id)) |
                    ((Friendship.user_id == friend.id) & (Friendship.friend_id == user.id))
                ).first()
                
                if not existing:
                    friendship = Friendship(
                        user_id=user.id,
                        friend_id=friend.id,
                        created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                    )
                    db.session.add(friendship)
                    friendships_created += 1
        
        db.session.commit()
        print(f"✅ Created {friendships_created} friendships")
        
        # Update friend counts
        for user in users:
            user.friends_count = Friendship.query.filter_by(user_id=user.id).count()
        
        db.session.commit()
        print("✅ Updated friend counts")
        
        # Update rankings
        users_sorted = User.query.order_by(User.portfolio_value.desc()).all()
        for i, user in enumerate(users_sorted, 1):
            user.global_rank = i
        
        db.session.commit()
        print("✅ Updated global rankings")
        
        print("\n🎉 Database seeded successfully!")
        print(f"📊 Total users: {User.query.count()}")
        print(f"👥 Total friendships: {Friendship.query.count()}")
        print("\nAll users have password: password123")

if __name__ == '__main__':
    seed_database()

