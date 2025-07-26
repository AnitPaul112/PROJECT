অপরিচিতা RAG Chatbot

A modern Bengali Retrieval-Augmented Generation (RAG) chatbot built with React TypeScript frontend and FastAPI backend, designed to answer questions about Rabindranath Tagore's "Oporichita" story.

 About

This project implements an intelligent conversational AI system that can understand and respond to questions in both Bengali and Banglish (Bengali written in English script) about the classic Bengali story "Oporichita" by Rabindranath Tagore.

## ✨ Features

### 🎯 Core Functionality
- **Multilingual Support**: Query in Bengali (বাংলা) or Banglish (English script)
- **Advanced Search Methods**:
  - 🔍 Hybrid Search (Vector + Keyword combination)
  - 🧠 Semantic Search (Meaning-based understanding)
  - 🔤 Keyword Search (Exact word matching)
- **Intelligent RAG System**: Context-aware responses with source attribution
- **Real-time Processing**: Instant query processing and response generation

### 🎨 User Interface
- **Modern React Frontend**: Built with TypeScript for type safety
- **Responsive Design**: Works seamlessly on mobile and desktop
- **Conversation History**: Maintains chat history during session
- **Live Status Indicators**: Real-time API connection status
- **Interactive Elements**: Clickable sample questions and search method selection
- **Beautiful Gradients**: Modern UI with smooth animations and transitions

### � Technical Features
- **RESTful API**: Clean FastAPI backend with comprehensive endpoints
- **Vector Embeddings**: Advanced semantic understanding using sentence transformers
- **CORS Support**: Proper cross-origin resource sharing configuration
- **Error Handling**: Robust error management and user feedback
- **Debug Mode**: Comprehensive logging and debugging capabilities

## 🏗️ Architecture

```
PROJECT/
├── 📄 README.md              # Project documentation
├── 🐍 api.py                 # FastAPI backend server
├── 🤖 basic_rag.py          # RAG system implementation
├── � text_processor.py      # Text processing and chunking
├── 🔄 txt_convert.py         # PDF to text conversion using OCR
├── 📊 processed_data.json    # Processed story data chunks
├── 🗂️ embeddings.pkl        # Vector embeddings cache
├── 📋 requirements.txt      # Python dependencies
├── 📑 bangla_output.txt     # OCR output from PDF
├── 📚 HSC26-Bangla1st-Paper (1).pdf # Source PDF document
├── 🖥️ frontend/             # React TypeScript frontend
│   ├── 📦 package.json      # Node.js dependencies
│   ├── ⚙️ tsconfig.json     # TypeScript configuration
│   ├── 🌐 public/           # Static assets
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   └── 💻 src/              # Source code
│       ├── App.tsx          # Main React component
│       ├── App.css          # Styling and animations
│       ├── index.tsx        # Application entry point
│       └── react-app-env.d.ts # TypeScript definitions
└── 🗃️ __pycache__/          # Python bytecode cache
```

## � Quick Start

### Prerequisites
- **Python 3.12+** with pip
- **Node.js 16+** with npm
- **OpenAI API Key** (optional, for enhanced responses)

### 🔧 Backend Setup

```bash
# Clone the repository
git clone https://github.com/AnitPaul112/PROJECT
cd PROJECT

# Install Python dependencies
pip install -r requirements.txt

# Install additional FastAPI dependencies
pip install fastapi uvicorn

# Start the FastAPI backend
python api.py
```

✅ Backend will be available at: `http://localhost:8000`

### 🎨 Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

✅ Frontend will be available at: `http://localhost:3000`

## 🎯 Usage Guide

### Step-by-Step Instructions

1. **🚀 Start Backend Server**
   ```bash
   python api.py
   ```

2. **🎨 Launch Frontend**
   ```bash
   cd frontend && npm start
   ```

3. **🌐 Open Browser**
   - Navigate to `http://localhost:3000`

4. **💬 Start Chatting**
   - Type your questions in Bengali or Banglish
   - Select preferred search method
   - View conversation history

### 📝 Sample Questions

#### 🇧🇩 Bengali Questions:
- **অনুপমের বয়স কত?** (What is Anupam's age?)
- **কল্যাণীর চরিত্র কেমন?** (What is Kalyani's character like?)
- **গল্পের মূল বিষয় কি?** (What is the main theme of the story?)
- **বিয়ের অনুষ্ঠানে কি ঘটেছিল?** (What happened at the wedding?)
- **অনুপম কেন বিয়ে করেনি?** (Why didn't Anupam get married?)

#### 🔤 Banglish Questions:
- **anupamer boyosh koto?**
- **kalyani kemon meyer chilo?**
- **golper main theme ki?**
- **biye te ki ghotechilo?**
- **anupam keno biye kore ni?**

## � API Reference

### Endpoints Overview

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/` | Health check | System status |
| `POST` | `/api/query` | Submit question | AI response |
| `GET` | `/api/search-methods` | Available search methods | Method list |
| `GET` | `/api/sample-questions` | Example questions | Question list |
| `GET` | `/api/stats` | System statistics | Usage stats |

### 📊 Detailed API Documentation

#### 🔍 Query Endpoint
```http
POST /api/query
Content-Type: application/json

{
  "question": "অনুপমের বয়স কত?",
  "search_method": "hybrid",
  "context_limit": 5
}
```

**Response:**
```json
{
  "answer": "AI generated response",
  "confidence": 0.95,
  "sources": ["source1", "source2"],
  "search_method": "hybrid",
  "processing_time": 1.23
}
```

#### 📈 Statistics Endpoint
```http
GET /api/stats
```

**Response:**
```json
{
  "total_queries": 150,
  "avg_response_time": 1.2,
  "popular_search_method": "hybrid",
  "uptime": "2h 45m"
}
```

## 🎨 Frontend Components

### 🧩 Component Architecture

#### **Main App Component** (`App.tsx`)
- **State Management**: React hooks for conversation and UI state
- **API Integration**: Axios-based HTTP client
- **Real-time Updates**: Live status monitoring
- **Error Handling**: User-friendly error messages

#### **Key Features**
- **📱 Responsive Layout**: Flexbox-based responsive design
- **🎭 Dynamic Theming**: CSS custom properties for theming
- **⚡ Performance**: Optimized rendering with React best practices
- **🔄 State Persistence**: Session-based conversation history

### 🎨 Styling Features

#### **CSS Architecture**
```css
/* Modern gradient backgrounds */
.chat-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Smooth animations */
.message {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Bengali font support */
.bengali-text {
  font-family: 'Kalpurush', 'Noto Sans Bengali', sans-serif;
}
```

## 🔧 Configuration

### 🌍 Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# API Configuration
API_HOST=localhost
API_PORT=8000
DEBUG_MODE=true

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TITLE=অপরিচিতা RAG Chatbot
```

**🔑 Get your OpenAI API key**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### ⚙️ Backend Configuration

Edit `api.py` to customize:

```python
# CORS settings
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your production URLs
]

# Server configuration
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True  # Set to False in production
    )
```

### 🎨 Frontend Configuration

Customize `frontend/src/App.tsx`:

```typescript
// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// UI text customization
const UI_TEXT = {
  title: 'অপরিচিতা RAG Chatbot',
  subtitle: 'Ask questions about Rabindranath Tagore\'s story',
  placeholder: 'আপনার প্রশ্ন লিখুন...'
};
```

## � Development Workflow

### 🐍 Backend Development

```bash
# Start development server with auto-reload
python api.py

# Alternative: Use uvicorn directly for more control
uvicorn api:app --reload --host 127.0.0.1 --port 8000

# Test API endpoints
curl http://localhost:8000/
curl -X GET http://localhost:8000/api/search-methods
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question":"অনুপমের বয়স কত?","search_method":"hybrid"}'
```

### ⚛️ Frontend Development

```bash
cd frontend

# Development server (auto-reload on changes)
npm start

# Type checking
npm run type-check

# Build for production
npm run build

# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Lint code
npm run lint
```

### 🧪 Testing Strategy

#### **Backend Testing**
```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run backend tests
pytest tests/ -v

# Test with coverage
pytest --cov=api tests/
```

#### **Frontend Testing**
```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests (if configured)
npm run test:e2e
```

## 🚀 Deployment Guide

### 🌐 Production Deployment

#### **Backend Deployment (Ubuntu/Linux)**
```bash
# Install production dependencies
pip install gunicorn

# Start production server
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile access.log \
  --error-logfile error.log

# Using systemd service (recommended)
sudo nano /etc/systemd/system/rag-api.service
```

**systemd service configuration:**
```ini
[Unit]
Description=RAG Chatbot API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/PROJECT
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### **Frontend Deployment**
```bash
cd frontend

# Build production bundle
npm run build

# Serve with nginx (recommended)
sudo cp -r build/* /var/www/html/

# Or serve with simple HTTP server
npx serve -s build -l 3000
```

#### **Docker Deployment** 🐳
```dockerfile
# Dockerfile.backend
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile.frontend
FROM node:18-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

### ☁️ Cloud Deployment Options

#### **🔥 Firebase Hosting (Frontend)**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

#### **🚀 Vercel (Frontend)**
```bash
npm install -g vercel
vercel --prod
```

#### **🌊 Railway (Backend)**
```bash
# Add railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api:app --host 0.0.0.0 --port $PORT"
  }
}
```

#### **☁️ AWS EC2 (Full Stack)**
```bash
# User data script for EC2 instance
#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip nodejs npm nginx
git clone https://github.com/AnitPaul112/PROJECT
cd PROJECT
pip3 install -r requirements.txt
cd frontend && npm install && npm run build
# Configure nginx and systemd services
```

## 🐛 Troubleshooting

### ❗ Common Issues & Solutions

#### **1. 🔌 API Connection Errors**

**Problem:** Frontend can't connect to backend
```
Error: Network Error
Failed to fetch from http://localhost:8000
```

**Solutions:**
```bash
# Check if backend is running
curl http://localhost:8000/

# Verify port availability
netstat -an | findstr :8000

# Check CORS configuration in api.py
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
```

#### **2. ⚛️ React Build Errors**

**Problem:** TypeScript compilation errors
```
error TS2345: Argument of type 'string' is not assignable to parameter of type 'never'
```

**Solutions:**
```bash
# Clear cache and reinstall
rmdir /s node_modules
del package-lock.json
npm install

# Update TypeScript
npm install --save-dev @types/react @types/node typescript

# Check tsconfig.json configuration
```

#### **3. 🤖 RAG System Issues**

**Problem:** "processed_data.json not found"
```bash
# Verify file exists
dir processed_data.json

# Regenerate if missing
python text_processor.py
```

**Problem:** OpenAI API errors
```bash
# Check API key
echo %OPENAI_API_KEY%

# Test API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### **4. 📱 Performance Issues**

**Problem:** Slow response times

**Backend Optimization:**
```python
# Increase worker processes
uvicorn api:app --workers 4

# Enable response compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Cache embeddings
import functools
@functools.lru_cache(maxsize=128)
def get_embeddings(text):
    # Embedding logic
```

**Frontend Optimization:**
```typescript
// React.memo for preventing unnecessary re-renders
const ChatMessage = React.memo(({ message }) => {
  return <div>{message}</div>;
});

// Debounce user input
const debouncedSearch = useCallback(
  debounce((query) => searchAPI(query), 300),
  []
);
```

### 🔍 Debug Mode

#### **Backend Debug Configuration**
```bash
# Enable debug logging
python -m uvicorn api:app --reload --log-level debug

# Add debug endpoints
@app.get("/debug/health")
async def debug_health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "memory_usage": psutil.virtual_memory().percent
    }
```

#### **Frontend Debug Tools**
```typescript
// Add console debugging
console.log('API Response:', response.data);

// React Developer Tools
// Chrome Extension: React Developer Tools

// Performance monitoring
import { Profiler } from 'react';

<Profiler id="ChatComponent" onRender={onRenderCallback}>
  <ChatComponent />
</Profiler>
```

### 📊 Monitoring & Logging

#### **Application Metrics**
```python
# Add request timing middleware
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### **Error Tracking**
```bash
# Install Sentry for error tracking
pip install sentry-sdk[fastapi]

# Add to api.py
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")
```

## 📚 Technology Stack

### 🎨 Frontend Technologies
- **⚛️ React 18**: Modern React with hooks and functional components
- **📘 TypeScript**: Type-safe JavaScript for better development experience
- **🎨 CSS3**: Modern styling with flexbox, grid, and animations
- **📡 Axios**: Promise-based HTTP client for API requests
- **🔄 React Hooks**: useState, useEffect, useCallback for state management
- **📱 Responsive Design**: Mobile-first approach with media queries

### 🐍 Backend Technologies
- **⚡ FastAPI**: Modern, fast Python web framework
- **🤖 OpenAI GPT**: Advanced language model for text generation
- **🧠 Sentence Transformers**: Pre-trained models for semantic embeddings
- **🔍 FAISS**: Efficient similarity search and clustering
- **📊 NumPy**: Numerical computing library
- **🐼 Pandas**: Data manipulation and analysis
- **🔧 Uvicorn**: ASGI server implementation

### 🗄️ Data & Storage
- **📄 JSON**: Structured data storage for processed content
- **🥒 Pickle**: Python object serialization for embeddings
- **📚 Vector Database**: In-memory vector storage for semantic search
- **💾 Session Storage**: Browser-based conversation history

### 🛠️ Development Tools
- **📦 npm**: Node.js package manager
- **🐍 pip**: Python package installer
- **🔄 Git**: Version control system
- **🐳 Docker**: Containerization platform
- **🧪 Jest**: JavaScript testing framework
- **🧪 Pytest**: Python testing framework

## 📈 Performance Optimization

### ⚡ Frontend Performance
```typescript
// Code splitting with React.lazy
const ChatComponent = React.lazy(() => import('./ChatComponent'));

// Memoization for expensive calculations
const processedData = useMemo(() => {
  return expensiveDataProcessing(rawData);
}, [rawData]);

// Virtual scrolling for large chat histories
import { FixedSizeList as List } from 'react-window';
```

### 🚀 Backend Performance
```python
# Async/await for non-blocking operations
async def process_query(query: str):
    embeddings = await get_embeddings_async(query)
    results = await search_database_async(embeddings)
    return results

# Connection pooling for database operations
from asyncpg import create_pool
pool = await create_pool(DATABASE_URL)

# Caching frequently accessed data
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_cached_embedding(text: str):
    return generate_embedding(text)
```

## 🔐 Security Best Practices

### 🛡️ API Security
```python
# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/query")
@limiter.limit("30/minute")
async def query_endpoint(request: Request):
    # API logic
```

### 🔒 Environment Security
```bash
# Secure environment variables
OPENAI_API_KEY=sk-...  # Never commit this!
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,localhost
```

### 🌐 CORS Configuration
```python
# Secure CORS setup
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains in production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🧪 Testing Strategy

### 🔬 Backend Testing
```python
# test_api.py
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_query_endpoint():
    response = client.post(
        "/api/query",
        json={"question": "test question", "search_method": "hybrid"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()

@pytest.mark.asyncio
async def test_rag_system():
    from basic_rag import RAGSystem
    rag = RAGSystem()
    result = await rag.query("test question")
    assert result is not None
```

### ⚛️ Frontend Testing
```typescript
// App.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

test('renders chat interface', () => {
  render(<App />);
  const titleElement = screen.getByText(/অপরিচিতা RAG Chatbot/i);
  expect(titleElement).toBeInTheDocument();
});

test('sends message when form is submitted', async () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/আপনার প্রশ্ন লিখুন/i);
  const button = screen.getByRole('button', { name: /send/i });
  
  fireEvent.change(input, { target: { value: 'test question' } });
  fireEvent.click(button);
  
  await waitFor(() => {
    expect(screen.getByText(/test question/i)).toBeInTheDocument();
  });
});
```

## 📊 Analytics & Monitoring

### 📈 Usage Analytics
```python
# Track API usage
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = datetime.now() - start_time
    
    logger.info(f"Request: {request.method} {request.url} - "
                f"Status: {response.status_code} - "
                f"Duration: {duration.total_seconds():.3f}s")
    return response
```

### 📊 Performance Metrics
```typescript
// Performance monitoring in React
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);

// Custom performance tracking
const trackUserAction = (action: string, data?: any) => {
  if (process.env.NODE_ENV === 'production') {
    // Send to analytics service
    analytics.track(action, data);
  }
};
```

## 🌍 Internationalization (i18n)

### 🌐 Multi-language Support
```typescript
// i18n configuration
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      "welcome": "Welcome to Oporichita RAG Chatbot",
      "askQuestion": "Ask your question..."
    }
  },
  bn: {
    translation: {
      "welcome": "অপরিচিতা RAG চ্যাটবটে স্বাগতম",
      "askQuestion": "আপনার প্রশ্ন লিখুন..."
    }
  }
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'bn',
  fallbackLng: 'en'
});
```

## 🤝 Contributing Guidelines

### � Git Workflow
```bash
# Fork and clone
git clone https://github.com/YourUsername/PROJECT.git
cd PROJECT

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git add .
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

### 📝 Code Standards
```typescript
// TypeScript/React standards
interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
}

const ChatComponent: React.FC<Props> = ({ title, onSubmit }) => {
  const [message, setMessage] = useState<string>('');
  
  return (
    <div className="chat-component">
      <h2>{title}</h2>
      {/* Component content */}
    </div>
  );
};
```

```python
# Python standards (PEP 8)
from typing import List, Dict, Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    search_method: str = "hybrid"
    context_limit: Optional[int] = 5

async def process_query(request: QueryRequest) -> Dict[str, any]:
    """
    Process user query and return AI response.
    
    Args:
        request: Query request object
        
    Returns:
        Dictionary containing response data
    """
    # Implementation
    pass
```

### 🧪 Testing Requirements
- **Frontend**: Minimum 80% test coverage
- **Backend**: All API endpoints must have tests
- **Integration**: End-to-end tests for critical user flows
- **Performance**: Load testing for API endpoints

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### � MIT License Summary
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## �🙏 Acknowledgments

### 📚 Literature & Content
- **রবীন্দ্রনাথ ঠাকুর** - Author of "অপরিচিতা" (Oporichita)
- **বাংলা সাহিত্য** - Rich Bengali literary tradition
- **Open Source Community** - For countless contributions

### 🤖 AI & Technology
- **OpenAI** - GPT models and API services
- **Hugging Face** - Transformer models and tokenizers
- **Meta AI** - FAISS vector similarity search
- **Sentence Transformers** - Semantic embedding models

### 🌐 Web Technologies
- **React Team** - Modern frontend framework
- **FastAPI Team** - High-performance Python web framework
- **TypeScript Team** - Type-safe JavaScript
- **Node.js Community** - JavaScript runtime and ecosystem

### 🎨 Design & UX
- **CSS Working Group** - Modern CSS features
- **Google Fonts** - Bengali typography support
- **Material Design** - Design principles and guidelines
- **Accessibility Community** - Web accessibility standards

### 🛠️ Development Tools
- **GitHub** - Version control and collaboration
- **VS Code Team** - Development environment
- **npm Community** - Package management
- **Python Software Foundation** - Python ecosystem

---

## 🎯 Quick Links

| Resource | Link | Description |
|----------|------|-------------|
| 🚀 **Live Demo** | [View Demo](https://your-demo-url.com) | Try the chatbot online |
| 📖 **Documentation** | [API Docs](http://localhost:8000/docs) | Interactive API documentation |
| 🐛 **Report Issues** | [GitHub Issues](https://github.com/AnitPaul112/PROJECT/issues) | Bug reports and feature requests |
| 💬 **Discussions** | [GitHub Discussions](https://github.com/AnitPaul112/PROJECT/discussions) | Community discussions |
| 📧 **Contact** | [Email](mailto:your-email@example.com) | Direct contact |

---

**Happy Coding! 🚀 কোড করুন আনন্দে! 💻**

*Made with ❤️ for Bengali literature enthusiasts and AI developers*
