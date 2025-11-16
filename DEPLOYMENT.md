# Deploy Investify to Render (Free)

This guide will help you deploy your Investify website to Render for free.

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in (or create an account)
2. Click the "+" icon in the top right → "New repository"
3. Name it `investify` (or any name you prefer)
4. Make it **Public** (required for free Render)
5. Click "Create repository"

## Step 2: Push Your Code to GitHub

Open terminal in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Investify app"

# Add your GitHub repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/investify.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Render

1. Go to [Render.com](https://render.com) and sign up (use GitHub to sign in - it's easier)
2. Click "New +" → "Web Service"
3. Connect your GitHub account if prompted
4. Select your `investify` repository
5. Configure the service:
   - **Name**: `investify` (or any name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Advanced" and add Environment Variables:
   - `SECRET_KEY`: Generate a random string (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DATABASE_URL`: Leave empty (Render will create a PostgreSQL database)
7. Click "Create Web Service"

## Step 4: Add PostgreSQL Database (Free)

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it: `investify-db`
3. Select "Free" plan
4. Click "Create Database"
5. Copy the **Internal Database URL**
6. Go back to your Web Service → Environment
7. Add/Update `DATABASE_URL` with the Internal Database URL from PostgreSQL

## Step 5: Update Database Connection

Your app already uses SQLite by default, but for production you'll want PostgreSQL. The app should automatically use the `DATABASE_URL` environment variable if set.

## Step 6: Deploy!

1. Render will automatically start building and deploying
2. Wait 2-3 minutes for the build to complete
3. Your site will be live at: `https://your-app-name.onrender.com`

## Alternative: Railway (Also Free)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python apps
6. Add PostgreSQL database from the dashboard
7. Your app will be live automatically!

## Troubleshooting

- **Build fails**: Check the build logs in Render dashboard
- **Database errors**: Make sure `DATABASE_URL` is set correctly
- **App crashes**: Check the logs tab in Render dashboard
- **Static files not loading**: Make sure all files are committed to GitHub

## Your Live URL

Once deployed, your website will be accessible at:
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.up.railway.app`

Both services offer free tiers perfect for personal projects!
