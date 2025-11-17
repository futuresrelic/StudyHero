# StudyHero Windows Setup Script
# Run this in PowerShell to set everything up automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   StudyHero Setup for Windows 11" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker is running!" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and run this script again." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (!(Test-Path "backend\.env")) {
    Write-Host ""
    Write-Host "Creating environment file..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"

    # Generate secret key
    $secret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
    (Get-Content "backend\.env") -replace 'SECRET_KEY=.*', "SECRET_KEY=$secret" | Set-Content "backend\.env"

    Write-Host "✓ Environment file created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: You need to add your Anthropic API key!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Get a free API key from: https://console.anthropic.com/" -ForegroundColor Cyan
    Write-Host "2. Open the file: backend\.env" -ForegroundColor Cyan
    Write-Host "3. Replace 'your_anthropic_api_key_here' with your actual key" -ForegroundColor Cyan
    Write-Host ""

    $response = Read-Host "Do you want to open the .env file now to add your API key? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        notepad "backend\.env"
        Write-Host ""
        Read-Host "Press Enter after you've saved your API key in the file"
    } else {
        Write-Host ""
        Write-Host "Please edit backend\.env and add your API key before continuing." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Environment file already exists!" -ForegroundColor Green
}

# Check if API key is set
$envContent = Get-Content "backend\.env" -Raw
if ($envContent -match "ANTHROPIC_API_KEY=sk-ant-") {
    Write-Host "✓ Anthropic API key is configured!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️  WARNING: Anthropic API key might not be set correctly!" -ForegroundColor Yellow
    Write-Host "The app won't work without a valid API key." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Do you want to open the .env file to check? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        notepad "backend\.env"
        Read-Host "Press Enter after you've checked the API key"
    }
}

Write-Host ""
Write-Host "Starting StudyHero with Docker..." -ForegroundColor Yellow
Write-Host "This might take a few minutes on first run..." -ForegroundColor Yellow
Write-Host ""

# Start docker compose
docker-compose up -d

Write-Host ""
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check if backend is running
Write-Host ""
Write-Host "Checking if backend is running..." -ForegroundColor Yellow
$maxAttempts = 12
$attempt = 0
$running = $false

while ($attempt -lt $maxAttempts -and -not $running) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
        $running = $true
        Write-Host "✓ Backend is running!" -ForegroundColor Green
    } catch {
        $attempt++
        Write-Host "Waiting... ($attempt/$maxAttempts)" -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($running) {
    Write-Host "✓ StudyHero is running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Open these URLs in your browser:" -ForegroundColor Cyan
    Write-Host "  • API Status:  http://localhost:8000" -ForegroundColor White
    Write-Host "  • API Docs:    http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  • View logs:          docker-compose logs -f" -ForegroundColor White
    Write-Host "  • Stop app:           docker-compose down" -ForegroundColor White
    Write-Host "  • Restart app:        docker-compose restart" -ForegroundColor White
    Write-Host "  • Check status:       docker-compose ps" -ForegroundColor White
    Write-Host ""

    # Ask if they want to open browser
    $response = Read-Host "Do you want to open the API documentation in your browser? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Start-Process "http://localhost:8000/docs"
    }
} else {
    Write-Host "⚠️  Backend might not be running correctly." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To check what went wrong, run:" -ForegroundColor Cyan
    Write-Host "  docker-compose logs backend" -ForegroundColor White
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Cyan
    Write-Host "  1. Make sure you added your Anthropic API key to backend\.env" -ForegroundColor White
    Write-Host "  2. Make sure Docker Desktop is running" -ForegroundColor White
    Write-Host "  3. Try restarting: docker-compose restart" -ForegroundColor White
}

Write-Host ""
