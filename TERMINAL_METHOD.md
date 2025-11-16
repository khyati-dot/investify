# 💻 Terminal Method - Step by Step

Use the **Terminal** app on your Mac (it's in Applications → Utilities, or press Cmd+Space and type "Terminal")

---

## Step 1: Open Terminal

1. Press `Cmd + Space` (Command + Spacebar)
2. Type: `Terminal`
3. Press Enter

---

## Step 2: Navigate to Your Project

Copy and paste this command (one line at a time, press Enter after each):

```bash
cd /Users/Khyati/Desktop/investify
```

Press Enter. You should see your prompt change.

---

## Step 3: Check if Git is Installed

```bash
git --version
```

If you see a version number (like `git version 2.x.x`), you're good! If not, you may need to install Xcode Command Line Tools.

---

## Step 4: Initialize Git (If Not Already Done)

```bash
git init
```

---

## Step 5: Add All Files

```bash
git add .
```

This adds all your files to be committed.

---

## Step 6: Create First Commit

```bash
git commit -m "Initial commit - Investify app"
```

---

## Step 7: Add Your GitHub Repository

**IMPORTANT:** Replace `YOUR_USERNAME` with your actual GitHub username!

```bash
git remote add origin https://github.com/YOUR_USERNAME/investify.git
```

**Example:** If your GitHub username is `khyati123`, the command would be:
```bash
git remote add origin https://github.com/khyati123/investify.git
```

---

## Step 8: Set Main Branch

```bash
git branch -M main
```

---

## Step 9: Push to GitHub

```bash
git push -u origin main
```

**You'll be asked for:**
- **Username:** Your GitHub username
- **Password:** You'll need a **Personal Access Token** (not your regular password)

---

## Step 10: Get Personal Access Token (If Needed)

If GitHub asks for a password and your regular password doesn't work:

1. Go to [github.com](https://github.com) → Sign in
2. Click your profile picture (top right) → **"Settings"**
3. Scroll down → **"Developer settings"** (left sidebar)
4. Click **"Personal access tokens"** → **"Tokens (classic)"**
5. Click **"Generate new token"** → **"Generate new token (classic)"**
6. Name it: `investify-deploy`
7. Select scopes: Check **"repo"** (this gives full control of private repositories)
8. Click **"Generate token"** at the bottom
9. **COPY THE TOKEN** (you won't see it again!)
10. Use this token as your password when pushing

---

## Step 11: Verify Upload

After pushing, go to your GitHub repository page. You should see all your files!

---

## Troubleshooting

### "fatal: not a git repository"
- Make sure you're in the right folder: `cd /Users/Khyati/Desktop/investify`
- Run `git init` first

### "remote origin already exists"
- Run: `git remote remove origin`
- Then run Step 7 again

### "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- See Step 10 above

### "Permission denied"
- Check your GitHub username is correct
- Make sure the repository exists on GitHub

---

## After Successfully Pushing

Once you see "Enumerating objects... Writing objects... done", your files are on GitHub!

Then proceed to deploy on Render (see deployment guides).

---

## Quick Copy-Paste Commands

Here are all commands in order (replace YOUR_USERNAME):

```bash
cd /Users/Khyati/Desktop/investify
git init
git add .
git commit -m "Initial commit - Investify app"
git remote add origin https://github.com/YOUR_USERNAME/investify.git
git branch -M main
git push -u origin main
```

**That's it!** 🚀

