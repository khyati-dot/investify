# ⚡ Quick Start - Make Your Site Public in 10 Minutes

## 🗑️ Step 1: Delete Old Repo (2 minutes)

1. Go to [github.com](https://github.com) → Your repositories
2. Click **"investify"** → **"Settings"** → Scroll down
3. **"Danger Zone"** → **"Delete this repository"**
4. Type `investify` and confirm

---

## 📦 Step 2: Create New Repo (3 minutes)

1. GitHub → **"+"** → **"New repository"**
2. Name: `investify`
3. Make it **PUBLIC** ✅
4. **Don't** add README, .gitignore, or license
5. Click **"Create repository"**

---

## 💻 Step 3: Push Code (2 minutes)

Run these commands in Terminal:

```bash
cd /Users/Khyati/Desktop/investify
git init
git add .
git commit -m "Ready to deploy"
git remote add origin https://github.com/YOUR_USERNAME/investify.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

---

## 🚀 Step 4: Deploy on Render (3 minutes)

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. **"New +"** → **"Web Service"** → Select `investify`
3. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Add `SECRET_KEY`: Run `python3 generate_secret_key.py` and copy the key
4. Click **"Create Web Service"**
5. **"New +"** → **"PostgreSQL"** → Free plan
6. Copy Internal Database URL
7. Web Service → Environment → Add `DATABASE_URL` with the URL

**Done!** Your site is live at `https://investify.onrender.com` 🎉

---

## 📖 Need More Details?

See `STEP_BY_STEP_DEPLOY.md` for detailed instructions with screenshots guidance.

