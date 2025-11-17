# 🏗️ StudyHero Architecture Documentation

Complete technical architecture and design decisions for StudyHero.

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Mobile App (React Native + Expo)      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Camera  │  │   Quiz   │  │  Tutor  │  │Progress │ │
│  │  Scan    │  │Generator │  │  Chat   │  │Tracking │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         State Management (Zustand + React Query)   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS / REST API
                           ▼
┌─────────────────────────────────────────────────────────┐
│                FastAPI Backend (Python)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │   Auth   │  │Homework  │  │  Quiz    │  │Progress │ │
│  │  Router  │  │  Router  │  │ Router   │  │ Router  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              AI Engine & Solvers                   │ │
│  │   ┌──────────┐  ┌───────────┐  ┌───────────────┐  │ │
│  │   │   OCR    │  │   Math    │  │  AI Tutor     │  │ │
│  │   │Tesseract │  │  Solver   │  │ (Claude API)  │  │ │
│  │   └──────────┘  └───────────┘  └───────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                           │
                           │ SQL
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                     │
│  ┌───────┐  ┌──────────┐  ┌──────┐  ┌────────────────┐ │
│  │ Users │  │ Homework │  │Quiz  │  │Progress/Stats  │ │
│  └───────┘  └──────────┘  └──────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────┘

External Services:
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│  Anthropic  │  │   Stripe    │  │   Expo       │
│  Claude API │  │  Payments   │  │  Push Notif  │
└─────────────┘  └─────────────┘  └──────────────┘
```

## 🎯 Key Design Decisions

### 1. Mobile-First Approach
- **React Native + Expo**: Cross-platform development (iOS & Android from one codebase)
- **Expo Router**: File-based routing, simplifies navigation
- **Why**: Faster development, single codebase, easier maintenance

### 2. FastAPI Backend
- **Python FastAPI**: High performance, automatic API docs, async support
- **Why**: Python has excellent ML/AI libraries, FastAPI is modern and fast
- **Alternatives considered**: Node.js/Express, Django

### 3. AI Provider - Anthropic Claude
- **Claude API**: For explanations, chat, text generation
- **Why**: Better reasoning, safer outputs, good for education
- **Alternatives**: OpenAI GPT-4, Google PaLM

### 4. State Management
- **Zustand**: Lightweight, simple, performant
- **React Query**: Server state, caching, automatic refetching
- **Why**: Simpler than Redux, better DX, handles async well

### 5. Database Choice
- **PostgreSQL**: Relational database
- **SQLAlchemy ORM**: Python ORM with migrations
- **Why**: Reliable, ACID compliant, good for structured data
- **Alternatives**: MongoDB (NoSQL), MySQL

### 6. Authentication
- **JWT tokens**: Stateless authentication
- **bcrypt**: Password hashing
- **Expo SecureStore**: Secure token storage on device
- **Why**: Industry standard, scalable, secure

## 📊 Data Models

### User
```python
- id: int (PK)
- email: string (unique)
- password_hash: string
- school_level: string
- subscription_status: string
- trial_ends_at: datetime
- subscription_expires_at: datetime
```

### HomeworkScan
```python
- id: int (PK)
- user_id: int (FK)
- question_text: text
- image_url: string
- subject: string
- solution_text: text
- explanation_steps: json
- created_at: datetime
```

### Quiz
```python
- id: int (PK)
- user_id: int (FK)
- topic: string
- difficulty: string
- questions: json
- score: float
- completed: boolean
```

### Progress
```python
- id: int (PK)
- user_id: int (FK)
- current_streak: int
- total_questions_solved: int
- level: int
- experience_points: int
- weekly_breakdown: json
```

## 🔄 Request Flow

### Example: Scanning Homework

```
1. User taps camera button
   └─> Frontend: Camera screen opens

2. User takes photo
   └─> Frontend: Image captured, shown for confirmation

3. User confirms
   └─> Frontend: Upload image via multipart/form-data
       POST /homework/scan

4. Backend receives image
   └─> Save to temp storage
   └─> Run OCR (Tesseract)
   └─> Extract text
   └─> Classify subject
   └─> Save to database
   └─> Return scan ID + question text

5. User taps "Solve"
   └─> Frontend: POST /homework/solve/{id}

6. Backend solves problem
   └─> Route to appropriate solver (math/science/history)
   └─> Generate step-by-step solution
   └─> Update database with solution
   └─> Return solution + steps

7. Frontend displays solution
   └─> Render steps with formatting
   └─> Show "Create Notes" option
   └─> Update user progress
```

## 🧩 Core Components

### Frontend Components

**Base Components:**
- `Button`: Reusable button with variants
- `Card`: Container with shadow and padding
- `Input`: Text input with validation
- `Badge`: Status/label display

**Feature Components:**
- `CameraView`: Camera capture interface
- `QuizCard`: Quiz question display
- `SolutionSteps`: Step-by-step solution renderer
- `ProgressRing`: Circular progress indicator
- `ChatBubble`: Chat message display

### Backend Modules

**Core Modules:**
- `ocr.py`: Image text extraction
- `solver/math_engine.py`: Math problem solving
- `solver/science_engine.py`: Science explanations
- `ai_tutor.py`: AI chat and explanations
- `quizgen.py`: Quiz generation
- `notes_builder.py`: Study notes creation

**API Routers:**
- `auth.py`: Registration, login, JWT
- `homework.py`: Scan, solve, history
- `quiz.py`: Generate, submit, grade
- `notes.py`: Create, retrieve notes
- `tutor.py`: Chat, rewrite, explain
- `subscription.py`: Stripe integration
- `progress.py`: Stats, achievements

## 🔐 Security Measures

### Authentication
- Password hashing (bcrypt, 12 rounds)
- JWT tokens (30-day expiration)
- Secure token storage (SecureStore on mobile)
- Authorization middleware on protected routes

### Data Protection
- HTTPS only (enforced)
- Input validation (Pydantic models)
- SQL injection prevention (ORM)
- XSS prevention (sanitized outputs)
- CORS configuration (whitelist origins)

### Rate Limiting
- Free tier: 5 scans/day
- Premium: unlimited
- API rate limiting per user
- Stored in database

### Payment Security
- Stripe handles card processing (PCI compliant)
- Webhook signature verification
- Server-side validation
- No card data stored

## ⚡ Performance Optimizations

### Frontend
- React Query caching (5min stale time)
- Lazy loading of screens
- Image optimization (expo-image-manipulator)
- Optimistic updates
- Virtualized lists for long content

### Backend
- Database connection pooling
- Index on foreign keys
- Query optimization (select specific fields)
- Async request handling
- Response compression (gzip)

### Database
- Indexes on:
  - user_id (all tables)
  - created_at (for sorting)
  - subject (for filtering)
- Regular VACUUM and ANALYZE
- Connection pooling (10 connections)

## 📈 Scalability Considerations

### Horizontal Scaling
- Stateless backend (JWT, no sessions)
- Database connection pooling
- Ready for load balancer
- Separate worker processes for AI tasks

### Vertical Scaling
- Async/await throughout
- Database indexes
- Caching strategy
- CDN for static assets

### Future Improvements
- Redis for caching and rate limiting
- Celery for background tasks
- Elasticsearch for search
- CDN for uploaded images
- Microservices architecture

## 🧪 Testing Strategy

### Unit Tests
- Math solver functions
- OCR processing
- API endpoints
- State management

### Integration Tests
- Complete user flows
- Payment processing
- AI API calls
- Database operations

### E2E Tests
- User registration → homework scan → solution
- Quiz generation → completion → grading
- Subscription purchase → feature unlock

## 📱 Mobile App Features

### Required Permissions
- **Camera**: For homework scanning
- **Photos**: For selecting existing images
- **Notifications**: For reminders and updates

### Offline Support
- Homework history cached
- Notes available offline
- Sync when online
- Optimistic UI updates

### Platform-Specific
- iOS: Touch ID/Face ID for login
- Android: Fingerprint auth
- Deep linking: `studyhero://`
- Push notifications

## 🎨 Design System

### Colors
- Primary: #4A6FFF (blue)
- Secondary: #7F56D9 (purple)
- Accent: #00E676 (neon green)
- Consistent across platform

### Typography
- System fonts (SF Pro on iOS, Roboto on Android)
- Consistent sizing scale
- Clear hierarchy

### Components
- Reusable, composable
- Props for customization
- TypeScript for type safety

## 🔮 Future Enhancements

### Phase 2
- Voice input for questions
- Handwriting recognition (Apple Pencil)
- Video explanations
- Study groups/collaboration

### Phase 3
- Parent/teacher dashboard
- School/district integrations
- Advanced analytics
- AI study recommendations

### Phase 4
- Multiple languages
- Accessibility improvements
- Offline AI (on-device models)
- AR features for 3D visualization

---

This architecture is designed for:
✅ **Scalability**: Can handle 100K+ users
✅ **Maintainability**: Clean code, separation of concerns
✅ **Performance**: Fast response times, optimized queries
✅ **Security**: Industry best practices
✅ **Extensibility**: Easy to add new features
