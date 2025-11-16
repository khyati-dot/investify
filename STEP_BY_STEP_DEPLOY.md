# 🚀 Step-by-Step: Make Your Investify Website Public

Follow these steps exactly to deploy your website for FREE!

---

## PART 1: Delete Old Repository (If Not Done Yet)

1. Go to [github.com](https://github.com) and sign in
2. Click your profile picture → **"Your repositories"**
3. Click on **"investify"** repository
4. Click **"Settings"** tab
5. Scroll to bottom → **"Danger Zone"**
6. Click **"Delete this repository"**
7. Type: `investify` and confirm deletion

---

## PART 2: Create New GitHub Repository

### Step 1: Create Repository on GitHub
1. Go to [github.com](https://github.com)
2. Click the **"+"** icon (top right) → **"New repository"**
3. Repository name: `investify`
4. Description: `Stock Market Simulation Game - Learn trading with virtual money`
5. Make it **PUBLIC** ✅ (Required for free hosting)
6. **DO NOT** check "Add a README file"
7. **DO NOT** add .gitignore or license
8. Click **"Create repository"**

### Step 2: Push Your Code to GitHub

Open Terminal in your project folder (`/Users/Khyati/Desktop/investify`) and run:

```bash
# Navigate to your project (if not already there)
cd /Users/Khyati/Desktop/investify

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Investify stock trading game"

# Add your GitHub repository (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/investify.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

Example: If your GitHub username is `khyati123`, the command would be:
```bash
git remote add origin https://github.com/khyati123/investify.git
```

---

## PART 3: Deploy to Render (FREE Hosting)

### Step 1: Sign Up on Render
1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Click **"Sign up with GitHub"** (easiest way)
4. Authorize Render to access your GitHub account

### Step 2: Create Web Service
1. In Render dashboard, click **"New +"** button (top right)
2. Click **"Web Service"**
3. You'll see your GitHub repositories listed
4. Find and click **"investify"** repository
5. Click **"Connect"**

### Step 3: Configure Web Service
Fill in these settings:

- **Name**: `investify` (or any name you like)
- **Region**: Choose closest to you (e.g., "Oregon" for US)
- **Branch**: `main` (should be selected by default)
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### Step 4: Add Environment Variables
1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"**
3. Add this variable:
   - **Key**: `SECRET_KEY`
   - **Value**: Run this command in your terminal to generate one:
     ```bash
     python3 generate_secret_key.py
     ```
     Copy the generated key and paste it as the value

4. Click **"Create Web Service"**

### Step 5: Add PostgreSQL Database
1. In Render dashboard, click **"New +"** again
2. Click **"PostgreSQL"**
3. Name: `investify-db` (or any name)
4. Plan: Select **"Free"** (it's free!)
5. Region: Same as your web service
6. Click **"Create Database"**
7. Wait for database to be created (30 seconds)

### Step 6: Connect Database to Your App
1. Go back to your Web Service (click on it in dashboard)
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Go to your PostgreSQL database → Click **"Connections"** tab → Copy the **"Internal Database URL"** → Paste it here
5. Click **"Save Changes"**

### Step 7: Deploy!
1. Render will automatically start building your app
2. Watch the build logs (it takes 2-3 minutes)
3. When you see "Your service is live", you're done! 🎉

---

## PART 4: Your Website is Live!

Your website will be available at:
**`https://investify.onrender.com`** (or whatever name you chose)

You can share this URL with anyone! It's publicly accessible.

---

## Troubleshooting

### Build Fails?
- Check the build logs in Render dashboard
- Make sure all files are committed to GitHub
- Verify `requirements.txt` has all dependencies

### Database Errors?
- Make sure `DATABASE_URL` is set correctly
- Check that PostgreSQL database is running
- Verify the Internal Database URL is copied correctly

### App Crashes?
- Check the logs tab in Render dashboard
- Look for error messages
- Make sure `SECRET_KEY` is set

### Can't Push to GitHub?
- Make sure you're logged into GitHub
- Check your GitHub username is correct
- Try: `git remote -v` to see your remote URL

---

## Need Help?

If you get stuck at any step, let me know which step number and what error you're seeing!

---

## Summary Checklist

- [ ] Deleted old GitHub repository
- [ ] Created new public GitHub repository
- [ ] Pushed code to GitHub
- [ ] Signed up on Render
- [ ] Created Web Service
- [ ] Added SECRET_KEY environment variable
- [ ] Created PostgreSQL database
- [ ] Added DATABASE_URL environment variable
- [ ] Website is live! 🎉

---

**Your website is now PUBLIC and FREE!** 🌐✨

