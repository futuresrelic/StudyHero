# 🔥 StudyHero — AI Homework & Study Assistant

A complete, production-ready mobile app that helps students complete homework and learn faster using AI-powered features.

## 📱 Features

### Core Functionality
- ✅ **Homework Scanning**: Take a photo of any homework question
- ✅ **Step-by-Step Solutions**: Get detailed explanations for math, science, history, and more
- ✅ **AI Tutor Chat**: Ask questions and get personalized help
- ✅ **Quiz Generator**: Create practice quizzes on any topic
- ✅ **Study Notes Builder**: Automatically generate study notes and flashcards
- ✅ **Progress Tracking**: Track streaks, XP, levels, and achievements
- ✅ **Multi-Subject Support**: Math (Algebra, Geometry, Calculus), Science (Physics, Chemistry, Biology), History, English
- ✅ **Premium Subscriptions**: Stripe-powered subscription system
- ✅ **Offline Support**: Local storage for homework history

### Tech Stack

**Frontend** (React Native + Expo)
- Expo Router for navigation
- TypeScript for type safety
- Zustand for state management
- React Query for API calls
- React Native Vision Camera for photo capture
- Stripe for payments

**Backend** (Python FastAPI)
- FastAPI for REST API
- PostgreSQL for database
- SQLAlchemy ORM
- Anthropic Claude AI for explanations
- Tesseract OCR for text extraction
- SymPy for math solving
- Stripe for subscriptions
- JWT authentication

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- PostgreSQL 14+
- Expo CLI (`npm install -g expo-cli`)
- Tesseract OCR
- Anthropic API key

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `ANTHROPIC_API_KEY`: Your Claude API key
- `SECRET_KEY`: Generate with `openssl rand -hex 32`
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `STRIPE_WEBHOOK_SECRET`: Your Stripe webhook secret

4. **Initialize database**
```bash
# Database will be created automatically on first run
python main.py
```

5. **Run backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required variables:
- `API_URL`: Your backend URL (e.g., `http://localhost:8000`)
- `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key

3. **Run the app**
```bash
# iOS
npm run ios

# Android
npm run android

# Web
npm run web
```

## 📚 API Documentation

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

### Homework
- `POST /homework/scan` - Upload and scan homework image
- `POST /homework/solve/{id}` - Solve a scanned problem
- `GET /homework/{id}` - Get homework details
- `GET /homework/history` - Get user's homework history

### Quiz
- `POST /quiz/generate` - Generate a new quiz
- `POST /quiz/submit` - Submit quiz answers
- `GET /quiz/{id}` - Get quiz details
- `GET /quiz/history` - Get quiz history

### Study Notes
- `POST /notes/create` - Create study notes
- `POST /notes/from-scan/{id}` - Create notes from homework scan
- `POST /notes/flashcards` - Generate flashcards
- `GET /notes/` - Get all notes
- `GET /notes/{id}` - Get specific note

### AI Tutor
- `POST /tutor/chat` - Chat with AI tutor
- `GET /tutor/conversations` - Get conversation history
- `POST /tutor/rewrite` - Rewrite text in different styles
- `POST /tutor/explain-simple` - Explain concepts simply
- `POST /tutor/study-plan` - Generate study plan

### Subscription
- `POST /subscription/create-checkout-session` - Create Stripe checkout
- `GET /subscription/status` - Get subscription status
- `GET /subscription/plans` - Get available plans

### Progress
- `GET /progress/` - Get user progress
- `POST /progress/log-study-time` - Log study time
- `GET /progress/achievements` - Get achievements
- `GET /progress/stats` - Get detailed statistics

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Deployment

### Backend Deployment (Railway/Render)

1. **Create account** on Railway or Render

2. **Add environment variables** in dashboard

3. **Deploy**
```bash
# Railway
railway up

# Render - connect GitHub repo and auto-deploy
```

4. **Set up database**
```bash
# Will auto-initialize on first request
```

### Frontend Deployment (Expo EAS)

1. **Install EAS CLI**
```bash
npm install -g eas-cli
```

2. **Configure EAS**
```bash
cd frontend
eas init
```

3. **Build for stores**
```bash
# iOS
eas build --platform ios

# Android
eas build --platform android
```

4. **Submit to stores**
```bash
# iOS App Store
eas submit --platform ios

# Google Play Store
eas submit --platform android
```

## 💳 Subscription Plans

- **Free**: 5 scans/day, basic features
- **Weekly**: $3.99/week - Unlimited scans, all features
- **Monthly**: $9.99/month - Save 17%
- **Yearly**: $49/year - Save 60%, best value!

**Free Trial**: 3 days included with first subscription

## 🎯 Key Features Breakdown

### Math Solver
- Linear equations
- Quadratic equations
- Expression simplification
- Fractions
- Basic arithmetic
- Word problems

### Science Helper
- Physics (kinematics, forces, energy)
- Chemistry (equation balancing, concepts)
- Biology (photosynthesis, mitosis, cells)

### Study Tools
- Auto-generated notes
- Flashcards with spaced repetition
- Quiz creation (multiple choice, true/false, fill-in-blank)
- Practice problems
- Study plans

### Progress System
- Daily streaks
- Experience points and levels
- Achievements and badges
- Subject breakdown
- Weekly analytics
- Leaderboard

## 🔒 Security

- JWT authentication
- Password hashing with bcrypt
- Secure token storage (Expo SecureStore)
- API rate limiting
- Input validation and sanitization
- CORS protection

## 📈 Performance

- React Query for caching
- Optimistic updates
- Image optimization
- Lazy loading
- Database indexing
- API response compression

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Anthropic Claude** for AI-powered explanations
- **Tesseract OCR** for text extraction
- **Expo** for React Native tooling
- **FastAPI** for backend framework
- **Stripe** for payment processing

## 📞 Support

- Email: support@studyhero.app
- Discord: [Join our community](https://discord.gg/studyhero)
- Documentation: [docs.studyhero.app](https://docs.studyhero.app)

## 🗺️ Roadmap

- [ ] Voice input for questions
- [ ] Handwriting recognition
- [ ] Collaborative study groups
- [ ] Parent/teacher dashboard
- [ ] More languages support
- [ ] Offline AI mode
- [ ] Video explanations
- [ ] Study timer and pomodoro

---

Made with ❤️ for students worldwide
