from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from basic_rag import BasicBanglaRAG
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="অপরিচিতা RAG API", description="API for Bangla RAG chatbot")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
try:
    rag_system = BasicBanglaRAG()
    print("✅ RAG system initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize RAG system: {e}")
    rag_system = None

# Pydantic models for request/response
class QuestionRequest(BaseModel):
    question: str
    search_method: str = "hybrid"  # hybrid, vector, keyword
    conversation_history: Optional[List[Dict[str, Any]]] = []

class QuestionResponse(BaseModel):
    answer: str
    search_method: str
    relevant_chunks: List[Dict[str, Any]]
    used_conversation_memory: bool
    timestamp: str
    question: str
    success: bool = True
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    rag_system_loaded: bool
    chunks_count: int
    message: str

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        rag_system_loaded=rag_system is not None,
        chunks_count=len(rag_system.chunks) if rag_system else 0,
        message="অপরিচিতা RAG API is running"
    )

@app.post("/api/query", response_model=QuestionResponse)
async def query_question(request: QuestionRequest):
    """Query the RAG system with a question"""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="প্রশ্ন ফাঁকা রাখা যাবে না!")
    try:
        # Process the query
        result = rag_system.query(
            question=request.question,
            search_method=request.search_method,
            conversation_history=request.conversation_history
        )
        return QuestionResponse(
            success=True,
            error=None,
            answer=result['answer'],
            search_method=result.get('search_method', request.search_method),
            relevant_chunks=result.get('relevant_chunks', []),
            used_conversation_memory=result.get('used_conversation_memory', False),
            timestamp=datetime.now().isoformat(),
            question=request.question
        )
    except Exception as e:
        return QuestionResponse(
            success=False,
            error=f"Error processing query: {str(e)}",
            answer="",
            search_method=request.search_method,
            relevant_chunks=[],
            used_conversation_memory=False,
            timestamp=datetime.now().isoformat(),
            question=request.question
        )

@app.get("/api/search-methods")
async def get_search_methods():
    """Get available search methods"""
    return {
        "methods": [
            {
                "id": "hybrid",
                "name": "হাইব্রিড (সেরা ফলাফল - ভেক্টর + কীওয়ার্ড)",
                "description": "Combines vector and keyword search for best results"
            },
            {
                "id": "vector",
                "name": "সিমান্টিক সার্চ (অর্থ বুঝে খোঁজে)",
                "description": "Semantic search that understands meaning"
            },
            {
                "id": "keyword",
                "name": "কীওয়ার্ড সার্চ (শব্দ মিল)",
                "description": "Traditional keyword matching"
            }
        ]
    }

@app.get("/api/sample-questions")
async def get_sample_questions():
    """Get sample questions for the user"""
    return {
        "questions": [
            {
                "bangla": "অনুপমের বয়স কত?",
                "banglish": "anupamer boyosh koto?"
            },
            {
                "bangla": "কল্যাণীর চরিত্র কেমন?",
                "banglish": "kalyani kemon meyer chilo?"
            },
            {
                "bangla": "গল্পের মূল বিষয় কি?",
                "banglish": "golper main theme ki?"
            },
            {
                "bangla": "মামার ভূমিকা কি ছিল?",
                "banglish": "mamar bhumika ki chilo?"
            },
            {
                "bangla": "অপরিচিতা গল্পের লেখক কে?",
                "banglish": "aparichita golper lekhok ke?"
            }
        ]
    }

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    if not rag_system:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    return {
        "total_chunks": len(rag_system.chunks),
        "embedding_dimensions": len(rag_system.embeddings[0]) if rag_system.embeddings else 0,
        "model_name": "paraphrase-multilingual-MiniLM-L12-v2",
        "api_status": "active"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 