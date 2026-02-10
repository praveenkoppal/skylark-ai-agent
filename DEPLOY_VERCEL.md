# Vercel Deployment Guide

This guide walks you through deploying the Skylark Drone Agent to Vercel.

## Prerequisites

- **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
- **GitHub Account**: Push your code to GitHub (Vercel deploys from Git repos)
- **Google Sheets API Credentials**: JSON service account key file

## Step 1: Prepare Your Credentials

1. **Get your Google Service Account credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable **Google Sheets API** and **Google Drive API**
   - Create a **Service Account**:
     - Navigate to "Service Accounts"
     - Click "Create Service Account"
     - Grant it "Editor" role for simplicity (or custom minimal permissions)
     - Create a JSON key and download it
   
2. **Prepare the credentials string**:
   - Open your downloaded `credentials.json` file
   - Copy its **entire contents** as a single-line JSON string
   - You'll paste this into Vercel environment variables in Step 4

## Step 2: Push Code to GitHub

1. Initialize git (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Skylark Drone Agent"
   ```

2. Create a new repo on GitHub and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/skylark-agent.git
   git push -u origin main
   ```

## Step 3: Connect Vercel to GitHub

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click **"Import Git Repository"**
3. Select your GitHub account and the `skylark-agent` repo
4. Click **"Import"**

## Step 4: Configure Environment Variables

**Important**: Before deploying, add the environment variable:

1. In Vercel dashboard, go to your project → **Settings** → **Environment Variables**
2. Add:
   - **Name**: `GOOGLE_CREDENTIALS`
   - **Value**: Paste your entire `credentials.json` contents (as a single-line JSON string)
   - **Environments**: Select all (Production, Preview, Development)
3. Click **"Save"**

## Step 5: Deploy

1. Click the **"Deploy"** button (or it may auto-deploy on push)
2. Vercel will build and deploy your app
3. Once complete, you'll get a live URL like: `https://skylark-agent.vercel.app`

## Step 6: Test Your Deployment

```bash
# Test the UI
curl https://your-app.vercel.app/

# Test the API
curl -X POST https://your-app.vercel.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "assign PRJ001"}'
```

## Troubleshooting

### "GOOGLE_CREDENTIALS not found"
- Ensure environment variable is set in Vercel **Settings → Environment Variables**
- Redeploy after adding variables (`git push` or manual redeploy)

### "Module not found" errors
- Check `requirements.txt` includes all dependencies
- Vercel should auto-install via `pip install -r requirements.txt`

### Builds taking too long or timing out
- Vercel has a 45-second build limit for free tier
- Upgrade plan if needed

### Still getting Sheets API errors
- Verify the Service Account has access to your Google Sheets
- Ensure the sheet name (e.g., "Pilot_Roster") exists and is shared with the service account email

## Local Testing Before Deployment

Test locally with environment variable:

```bash
# PowerShell
$env:GOOGLE_CREDENTIALS = Get-Content credentials.json -Raw
python -m uvicorn app:app --reload

# Bash/Linux/Mac
export GOOGLE_CREDENTIALS=$(cat credentials.json)
python -m uvicorn app:app --reload
```

## Updating After Deployment

Any push to your GitHub repository will **auto-deploy** to Vercel (configurable in Settings).

To push updates:
```bash
git add .
git commit -m "Update: [description]"
git push
```

Vercel will automatically rebuild and redeploy.

## Next Steps

- Monitor logs: Vercel Dashboard → **Deployments** → Click deployment → **Logs**
- Set up custom domain (optional): Settings → **Domains**
- Configure CI/CD: GitHub should auto-trigger rebuilds on push
