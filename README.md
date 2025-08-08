# Bangla RAG Chatbot - অপরিচিতা

A semantic search and question-answering system for Bangla text documents using Retrieval Augmented Generation (RAG).

## Overview

This project converts PDF documents to text, processes them into chunks, and provides an intelligent Q&A interface using vector embeddings and OpenAI's API. Built specifically for Bangla text with support for both Bangla and Banglish queries.

## Tech Stack

**Backend:**
- FastAPI for REST API
- Sentence Transformers for multilingual embeddings
- OpenAI GPT for answer generation
- Scikit-learn for similarity calculations
- PDF2Image + Tesseract for OCR

**Frontend:**
- React with TypeScript
- Modern chat interface with conversation history

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AnitPaul112/PROJECT
   cd PROJECT
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   You can get an openai_api key from https://platform.openai.com/api-keys
   ```

4. **Install Tesseract OCR:**
   - Download and install Tesseract OCR
   - Update the path in `txt_convert.py` if needed

## How to Run

1. **Process PDF to text chunks:**
   ```bash
   python txt_convert.py
   python text_processor.py
   ```

2. **Start the backend API:**
   ```bash
   python api.py
   ```

3. **Start the frontend:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Or use the batch file:**
   ```bash
   run_react_app.bat
   ```

## Implementation Details

### Text Extraction Method
**Library Used:** PDF2Image + Tesseract OCR  
**Why:** Since the PDF contained scanned images rather than selectable text, OCR was necessary. Tesseract with Bengali language support (`lang="ben"`) provides reliable text extraction for Bangla documents.

**Challenges Faced:** OCR accuracy issues with complex Bangla fonts, extra spacing, and page markers. Solved through extensive text cleaning and preprocessing.

### Chunking Strategy
**Method:** Hybrid approach combining content-aware and size-based chunking  
**Details:**
- Primary split by content sections (শব্দার্থ ও টীকা, মূল গল্প)
- Secondary split by sentence boundaries using Bangla punctuation (।)
- Fallback to character-based splitting (300 chars with 50 char overlap)

**Why This Works:** Maintains semantic coherence while ensuring chunks are appropriately sized for retrieval. Content-aware splitting preserves context better than simple character-based methods.

### Embedding Model
**Model:** `paraphrase-multilingual-MiniLM-L12-v2`  
**Why Chosen:**
- Supports 50+ languages including Bangla
- Optimized for semantic similarity tasks
- Good balance between performance and accuracy
- Works well with both Bangla and Banglish text

**How It Captures Meaning:** Uses transformer architecture to create dense vector representations that capture semantic relationships beyond simple keyword matching.

### Similarity Comparison & Storage
**Method:** Cosine similarity with vector embeddings  
**Storage:** Pickle files for embeddings, JSON for processed chunks  
**Why This Approach:**
- Cosine similarity measures semantic closeness effectively
- Vector embeddings capture context better than TF-IDF
- In-memory storage provides fast retrieval for this dataset size

### Query Processing & Meaningful Comparison
**Techniques Used:**
- Banglish-to-Bangla transliteration mapping
- Combined query approach (original + converted)
- Minimum similarity threshold (0.1)
- Multiple search methods (vector, keyword, hybrid)

**Handling Vague Queries:** The system uses conversation history and combines multiple similarity signals. For missing context, it provides the most relevant available information while indicating uncertainty.

### Results Quality & Improvements

**Current Performance:** Results are generally relevant for specific queries about characters, plot points, and themes.

**Potential Improvements:**
1. **Better Chunking:** Implement paragraph-level chunking for longer coherent sections
2. **Enhanced Embedding:** Fine-tune embedding model on Bangla literature corpus
3. **Larger Context:** Include more related documents for comprehensive knowledge base
4. **Query Expansion:** Implement automatic query expansion using synonyms and related terms
5. **Re-ranking:** Add a re-ranking layer to improve result ordering

## API Endpoints

- `GET /health` - System health check
- `POST /ask` - Submit questions (supports Bangla/Banglish)
- `GET /chunks` - View processed text chunks
- `POST /search` - Direct similarity search

## Features

- **Multilingual Support:** Handles both Bangla and Banglish queries
- **Conversation Memory:** Maintains context across questions
- **Multiple Search Methods:** Vector, keyword, and hybrid search
- **Real-time Processing:** Fast similarity-based retrieval
- **Clean UI:** Modern chat interface with search method selection

## Project Structure

```
├── txt_convert.py          # PDF to text conversion using OCR
├── text_processor.py       # Text cleaning and chunking
├── basic_rag.py           # Core RAG implementation
├── api.py                 # FastAPI backend
├── requirements.txt       # Python dependencies
├── run_react_app.bat      # One-click launcher batch file
└── frontend/              # React TypeScript app
    ├── src/
    │   ├── App.tsx        # Main chat interface
    │   └── App.css        # Styling
    └── package.json       # Node dependencies
```

## Quick Start with Batch File

For the easiest setup, simply double-click the `run_react_app.bat` file. This batch file will automatically:

1. **Install Python dependencies** from `requirements.txt`
2. **Navigate to frontend directory** and install npm packages
3. **Start the React development server** 
4. **Open the application** in your default browser

**Requirements:** Make sure you have Python and Node.js installed on your system before running the batch file.

Just double-click `run_react_app.bat` and the entire application will be set up and running automatically!

## License

MIT License
