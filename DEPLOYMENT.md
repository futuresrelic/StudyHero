# 🚀 Deployment Guide for StudyHero

Complete guide to deploy StudyHero to production.

## 📋 Prerequisites

### Required Accounts
- [ ] Railway or Render account (backend hosting)
- [ ] Expo EAS account (mobile app builds)
- [ ] PostgreSQL database (Railway/Render provides)
- [ ] Anthropic API key
- [ ] Stripe account (for payments)
- [ ] Apple Developer Account (for iOS - $99/year)
- [ ] Google Play Developer Account (for Android - $25 one-time)

### Required Tools
- [ ] Node.js 18+
- [ ] Python 3.10+
- [ ] Expo CLI
- [ ] EAS CLI
- [ ] Git

## 🔧 Backend Deployment

### Option 1: Railway (Recommended)

1. **Create Railway account** at https://railway.app

2. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

3. **Login to Railway**
```bash
railway login
```

4. **Initialize project**
```bash
cd backend
railway init
```

5. **Add PostgreSQL**
```bash
railway add postgresql
```

6. **Set environment variables**
```bash
railway variables set ANTHROPIC_API_KEY=your_key_here
railway variables set STRIPE_SECRET_KEY=sk_live_xxx
railway variables set STRIPE_PUBLISHABLE_KEY=pk_live_xxx
railway variables set STRIPE_WEBHOOK_SECRET=whsec_xxx
railway variables set SECRET_KEY=$(openssl rand -hex 32)
```

7. **Deploy**
```bash
railway up
```

8. **Get deployment URL**
```bash
railway status
# Copy your deployment URL (e.g., https://studyhero-api.railway.app)
```

### Option 2: Render

1. **Create Render account** at https://render.com

2. **Connect GitHub repository**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure service**
   - Name: `studyhero-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add PostgreSQL**
   - Click "New +" → "PostgreSQL"
   - Name: `studyhero-db`
   - Copy connection string

5. **Set environment variables**
   - Add all variables from `.env.example`
   - Set `DATABASE_URL` to PostgreSQL connection string

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Stripe Webhook Setup

1. **Get deployment URL** (e.g., `https://studyhero-api.railway.app`)

2. **Configure Stripe webhook**
   - Go to Stripe Dashboard → Developers → Webhooks
   - Click "Add endpoint"
   - URL: `https://your-api-url.com/subscription/webhook`
   - Events to send:
     - `checkout.session.completed`
     - `customer.subscription.updated`
     - `customer.subscription.deleted`
   - Copy webhook secret

3. **Update environment variable**
```bash
railway variables set STRIPE_WEBHOOK_SECRET=whsec_xxx
# or update in Render dashboard
```

## 📱 Frontend Deployment

### Setup EAS Build

1. **Install EAS CLI**
```bash
npm install -g eas-cli
```

2. **Login to Expo**
```bash
cd frontend
eas login
```

3. **Initialize EAS**
```bash
eas init
```

4. **Update configuration**

Edit `eas.json` and set your production API URL:
```json
{
  "build": {
    "production": {
      "env": {
        "API_URL": "https://your-production-api.com"
      }
    }
  }
}
```

### Build for iOS

1. **Configure Apple credentials**
```bash
eas credentials
```

2. **Build for iOS**
```bash
eas build --platform ios --profile production
```

3. **Submit to App Store**
```bash
eas submit --platform ios
```

4. **Monitor build**
- Check build status on https://expo.dev
- Download build to test locally
- Submit for App Store review

### Build for Android

1. **Generate keystore** (first time only)
```bash
eas credentials
```

2. **Build for Android**
```bash
eas build --platform android --profile production
```

3. **Submit to Play Store**
```bash
eas submit --platform android
```

4. **Monitor build**
- Download APK/AAB from Expo dashboard
- Test on device
- Submit for Play Store review

### App Store Submission Checklist

#### iOS App Store

- [ ] App icons (all sizes)
- [ ] Screenshots (iPhone, iPad)
- [ ] App description
- [ ] Keywords
- [ ] Privacy policy URL
- [ ] Support URL
- [ ] Age rating
- [ ] App Store Connect filled out
- [ ] TestFlight beta testing completed

#### Google Play Store

- [ ] App icons (all sizes)
- [ ] Feature graphic (1024x500)
- [ ] Screenshots (phone, tablet)
- [ ] App description (short & long)
- [ ] Privacy policy URL
- [ ] Content rating questionnaire
- [ ] Store listing complete
- [ ] Internal testing completed

## 🔐 Security Checklist

Before going live:

- [ ] All environment variables are set
- [ ] SECRET_KEY is randomly generated
- [ ] Database has strong password
- [ ] CORS is configured properly
- [ ] Rate limiting is enabled
- [ ] HTTPS is enabled (automatic on Railway/Render)
- [ ] API keys are not exposed in frontend
- [ ] Stripe is in live mode (not test mode)
- [ ] Webhook secrets are configured
- [ ] Error logging is set up

## 📊 Monitoring

### Backend Monitoring

**Railway:**
- View logs: `railway logs`
- View metrics: Railway dashboard

**Render:**
- View logs: Render dashboard → Logs tab
- View metrics: Render dashboard → Metrics tab

### Crash Reporting

Add Sentry for error tracking:

```bash
# Backend
pip install sentry-sdk[fastapi]

# Frontend
npx expo install sentry-expo
```

## 🔄 Updates and Maintenance

### Backend Updates

```bash
cd backend
git pull
railway up  # or push to GitHub for Render
```

### Frontend Updates

#### Over-The-Air (OTA) Updates
For small changes (JS/assets only):
```bash
eas update --branch production
```

#### Full Rebuild
For native code changes:
```bash
eas build --platform all --profile production
eas submit --platform all
```

## 💾 Database Backups

### Railway
- Automatic daily backups
- Manual backup: Railway dashboard → Database → Backups

### Render
- Automatic daily backups (paid plans)
- Manual backup:
```bash
pg_dump $DATABASE_URL > backup.sql
```

## 🆘 Troubleshooting

### Backend Issues

**500 errors:**
- Check logs: `railway logs` or Render dashboard
- Verify environment variables
- Check database connection

**Database connection failed:**
- Verify `DATABASE_URL` is correct
- Check database is running
- Verify firewall rules

**Stripe webhook not working:**
- Verify webhook URL is correct
- Check webhook secret matches
- Test with Stripe CLI: `stripe listen --forward-to localhost:8000/subscription/webhook`

### Frontend Issues

**Build failed:**
- Check `eas.json` configuration
- Verify credentials
- Check package.json dependencies

**App crashes on startup:**
- Check API_URL is correct
- Verify backend is running
- Check Expo logs: `npx expo start --dev-client`

**Stripe payment not working:**
- Verify `STRIPE_PUBLISHABLE_KEY` is correct
- Check Stripe is in live mode
- Test with Stripe test cards first

## 📈 Scaling

### Backend Scaling

**Railway:**
- Automatic scaling based on traffic
- Upgrade plan for more resources

**Render:**
- Scale manually: Dashboard → Settings → Instance Type
- Enable autoscaling (paid plans)

### Database Scaling

- Monitor query performance
- Add indexes for slow queries
- Consider connection pooling (PgBouncer)
- Upgrade database plan as needed

### CDN for Images

Consider using Cloudinary or AWS S3 for uploaded images:
- Reduces server load
- Faster image delivery
- Automatic image optimization

## ✅ Launch Checklist

Before public launch:

- [ ] Backend deployed and running
- [ ] Database set up with backups
- [ ] All environment variables configured
- [ ] Stripe live mode enabled
- [ ] Webhook configured
- [ ] iOS app approved and live
- [ ] Android app approved and live
- [ ] Privacy policy page live
- [ ] Terms of service page live
- [ ] Support email set up
- [ ] Analytics configured
- [ ] Error monitoring active
- [ ] Load testing completed
- [ ] Beta testing feedback addressed
- [ ] Marketing website live
- [ ] Social media accounts created

---

🎉 **You're ready to launch StudyHero!**

For support, email: dev@studyhero.app
