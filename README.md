# অপরিচিতা RAG Chatbot - React Frontend

এই প্রজেক্টটি একটি বাংলা RAG (Retrieval-Augmented Generation) চ্যাটবট যা React frontend এবং FastAPI backend ব্যবহার করে তৈরি করা হয়েছে।

## 🚀 Features

- **Modern React Frontend**: TypeScript দিয়ে তৈরি, responsive design
- **FastAPI Backend**: RESTful API endpoints
- **Multilingual Support**: বাংলা এবং বাংলিশ উভয় ভাষায় প্রশ্ন করা যায়
- **Multiple Search Methods**: 
  - হাইব্রিড সার্চ (ভেক্টর + কীওয়ার্ড)
  - সিমান্টিক সার্চ (অর্থ বুঝে খোঁজে)
  - কীওয়ার্ড সার্চ (শব্দ মিল)
- **Conversation History**: কথোপকথনের ইতিহাস সংরক্ষণ
- **Real-time Status**: API সংযোগের অবস্থা দেখানো

## 📁 Project Structure

```
PROJECT/
├── api.py                 # FastAPI backend
├── basic_rag.py          # RAG system implementation
├── app.py                # Original Streamlit app
├── frontend/             # React frontend
│   ├── src/
│   │   ├── App.tsx       # Main React component
│   │   └── App.css       # Styling
│   ├── package.json
│   └── ...
├── requirements.txt      # Python dependencies
└── README.md
```

## 🛠️ Installation & Setup

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt
pip install fastapi uvicorn

# Start the FastAPI backend
python api.py
```

Backend will run on: `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

Frontend will run on: `http://localhost:3000`

## 🎯 How to Use

1. **Backend চালু করুন**: `python api.py`
2. **Frontend চালু করুন**: `cd frontend && npm start`
3. **Browser এ যান**: `http://localhost:3000`
4. **প্রশ্ন করুন**: বাংলা বা বাংলিশে প্রশ্ন লিখুন

### Sample Questions

**বাংলায়:**
- অনুপমের বয়স কত?
- কল্যাণীর চরিত্র কেমন?
- গল্পের মূল বিষয় কি?

**বাংলিশে:**
- anupamer boyosh koto?
- kalyani kemon meyer chilo?
- golper main theme ki?

## 🔧 API Endpoints

- `GET /` - Health check
- `POST /api/query` - প্রশ্ন জিজ্ঞাসা
- `GET /api/search-methods` - সার্চ পদ্ধতি সমূহ
- `GET /api/sample-questions` - নমুনা প্রশ্ন
- `GET /api/stats` - সিস্টেম পরিসংখ্যান

## 🎨 Frontend Features

### Modern UI Components
- **Responsive Design**: Mobile এবং Desktop উভয় ডিভাইসে কাজ করে
- **Real-time Status**: API সংযোগের অবস্থা দেখানো
- **Conversation History**: কথোপকথনের ইতিহাস
- **Sample Questions**: ক্লিক করে প্রশ্ন নির্বাচন
- **Search Method Selection**: বিভিন্ন সার্চ পদ্ধতি নির্বাচন

### Styling
- **Gradient Backgrounds**: সুন্দর gradient effects
- **Smooth Animations**: Hover effects এবং transitions
- **Modern Typography**: বাংলা ফন্ট support
- **Card-based Layout**: Clean এবং organized interface

## 🔄 Development Workflow

### Backend Development
```bash
# API development
python api.py

# Test API endpoints
curl http://localhost:8000/
curl http://localhost:8000/api/search-methods
```

### Frontend Development
```bash
cd frontend
npm start          # Development server
npm run build      # Production build
npm test           # Run tests
```

## 🚀 Deployment

### Backend Deployment
```bash
# Production server
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy build/ folder to your hosting service
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### API Configuration
Edit `api.py` to change:
- CORS origins
- Port number
- RAG system parameters

### Frontend Configuration
Edit `frontend/src/App.tsx` to change:
- API base URL
- UI text
- Styling preferences

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Check if backend is running on port 8000
   - Verify CORS settings in `api.py`

2. **React Build Errors**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check TypeScript errors

3. **RAG System Not Loading**
   - Verify `processed_data.json` exists
   - Check OpenAI API key in `.env`

### Debug Mode
```bash
# Backend debug
python -m uvicorn api:app --reload --log-level debug

# Frontend debug
cd frontend && npm start
```

## 📚 Technologies Used

- **Frontend**: React 18, TypeScript, CSS3
- **Backend**: FastAPI, Python 3.12
- **AI/ML**: OpenAI GPT, Sentence Transformers
- **Styling**: Modern CSS with gradients and animations
- **HTTP Client**: Axios for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- রবীন্দ্রনাথ ঠাকুরের "অপরিচিতা" গল্প
- OpenAI API for language processing
- React and FastAPI communities
- Bengali language support libraries

---

**Happy Coding! 🚀**
