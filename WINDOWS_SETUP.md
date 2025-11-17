# 🪟 StudyHero Setup Guide for Windows 11

**Complete beginner-friendly guide to run StudyHero on Windows 11**

## 📋 What You Need

1. **Docker Desktop** - Download from https://www.docker.com/products/docker-desktop/
2. **PowerShell** - Already built into Windows 11
3. **Anthropic API Key** - Get free at https://console.anthropic.com/

## 🚀 Step-by-Step Setup

### Step 1: Install Docker Desktop

1. Go to https://www.docker.com/products/docker-desktop/
2. Click "Download for Windows"
3. Run the installer
4. Restart your computer when prompted
5. Open Docker Desktop (search for it in Start menu)
6. Wait for Docker to start (you'll see a green icon in the system tray)

### Step 2: Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up for a free account
3. Go to "API Keys" section
4. Click "Create Key"
5. Copy the API key (starts with `sk-ant-`)
6. Keep this safe - you'll need it soon!

### Step 3: Open PowerShell

1. Press `Windows Key + X`
2. Click "Windows PowerShell" or "Terminal"
3. You should see a blue window

### Step 4: Navigate to the Project

In PowerShell, type:
```powershell
cd C:\Users\YourUsername\StudyHero
```
Replace `YourUsername` with your actual Windows username.

Or if you know the path, navigate there:
```powershell
cd "path\to\StudyHero"
```

### Step 5: Set Up Environment Variables

We'll create the configuration file with your API key.

Copy the example file:
```powershell
Copy-Item backend\.env.example backend\.env
```

Now edit the file with Notepad:
```powershell
notepad backend\.env
```

**Replace these values:**
```
# REPLACE THIS with your actual Anthropic API key
ANTHROPIC_API_KEY=sk-ant-your_actual_key_here

# These are already set correctly - don't change them
DATABASE_URL=postgresql://studyhero:studyhero123@db:5432/studyhero
SECRET_KEY=your_secret_key_will_be_generated_automatically
STRIPE_SECRET_KEY=sk_test_placeholder
STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
STRIPE_WEBHOOK_SECRET=whsec_placeholder
```

**Important:** Only change the `ANTHROPIC_API_KEY` line. Leave everything else as is.

Save and close Notepad (File → Save, then close).

### Step 6: Generate Secret Key

Run this command to generate a secure secret key:
```powershell
$secret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
(Get-Content backend\.env) -replace 'SECRET_KEY=.*', "SECRET_KEY=$secret" | Set-Content backend\.env
Write-Host "Secret key generated!"
```

### Step 7: Start the Application

Now let's start everything with Docker:
```powershell
docker-compose up -d
```

This will:
- Download required software (first time takes 5-10 minutes)
- Set up the database
- Start the backend server
- Everything runs automatically!

**Wait about 2 minutes** for everything to start.

### Step 8: Check if It's Running

Open your web browser and go to:
```
http://localhost:8000
```

You should see:
```json
{
  "app": "StudyHero",
  "version": "1.0.0",
  "status": "running"
}
```

🎉 **Success!** The backend is running!

### Step 9: View API Documentation

To see all the available features, go to:
```
http://localhost:8000/docs
```

This shows you all the API endpoints you can use.

## 🛠️ Common Commands

### See if containers are running:
```powershell
docker-compose ps
```

### View logs (to see what's happening):
```powershell
docker-compose logs -f
```
Press `Ctrl+C` to stop viewing logs.

### Stop the application:
```powershell
docker-compose down
```

### Start the application again:
```powershell
docker-compose up -d
```

### Restart everything (if something goes wrong):
```powershell
docker-compose restart
```

### Delete everything and start fresh:
```powershell
docker-compose down -v
docker-compose up -d
```

## 🧪 Test the API

Let's test if the homework solver works!

### Test 1: Register a User

Open PowerShell and run:
```powershell
$body = @{
    email = "test@example.com"
    password = "test123456"
    full_name = "Test Student"
    school_level = "high"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/auth/register" -Method Post -Body $body -ContentType "application/json"
```

You should get back an access token!

### Test 2: Solve a Math Problem

First, save your token from the previous step:
```powershell
$token = "paste_your_token_here"
```

Then test the math solver:
```powershell
# This will test solving "2x + 5 = 15"
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/homework/history" -Method Get -Headers $headers
```

## 📱 Setting Up the Mobile App (Optional)

If you want to run the mobile app:

### Install Node.js:
1. Go to https://nodejs.org/
2. Download "LTS" version
3. Run installer
4. Restart PowerShell

### Install Expo:
```powershell
npm install -g expo-cli
```

### Set up the frontend:
```powershell
cd frontend
npm install
Copy-Item .env.example .env
notepad .env
```

In the .env file, set:
```
API_URL=http://localhost:8000
STRIPE_PUBLISHABLE_KEY=pk_test_placeholder
```

### Start the mobile app:
```powershell
npx expo start
```

You can then:
- Press `w` to open in web browser
- Scan QR code with Expo Go app on your phone
- Press `a` for Android emulator (if installed)
- Press `i` for iOS simulator (Mac only)

## 🐛 Troubleshooting

### "Docker is not running"
- Open Docker Desktop from Start menu
- Wait for it to say "Docker Desktop is running"

### "Port 8000 is already in use"
Stop anything using port 8000:
```powershell
$process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($process) { Stop-Process -Id $process -Force }
```

### "Database connection failed"
Make sure the database container is running:
```powershell
docker-compose ps
```
All services should show "Up".

### Need to see detailed error messages:
```powershell
docker-compose logs backend
```

### Start completely fresh:
```powershell
docker-compose down -v
Remove-Item -Recurse -Force backend\__pycache__ -ErrorAction SilentlyContinue
docker-compose up -d --build
```

## ✅ What's Working Now

Once everything is running, you have:
- ✅ Full REST API at `http://localhost:8000`
- ✅ API documentation at `http://localhost:8000/docs`
- ✅ PostgreSQL database (automatically managed)
- ✅ Math solver (algebra, calculus, arithmetic)
- ✅ Science helper (physics, chemistry, biology)
- ✅ History helper
- ✅ AI tutor powered by Claude
- ✅ Quiz generator
- ✅ Study notes builder
- ✅ User authentication
- ✅ Progress tracking

## 📞 Need Help?

If something doesn't work:
1. Check Docker Desktop is running (green icon in system tray)
2. Run `docker-compose logs` to see error messages
3. Make sure you put your real Anthropic API key in `.env`
4. Try restarting: `docker-compose restart`

---

**You're all set! 🎉 The backend is running and ready to help students with homework!**
