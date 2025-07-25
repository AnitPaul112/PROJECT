import json
import os
from dotenv import load_dotenv
import openai
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load environment variables
load_dotenv()

class BasicBanglaRAG:
    def __init__(self, processed_data_file='processed_data.json', embeddings_file='embeddings.pkl'):
        """Basic RAG system for Bangla PDF chatbot with vector search"""
        
        # Initialize OpenAI
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Load processed data
        with open(processed_data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.chunks = self.data['chunks']
        self.embeddings_file = embeddings_file
        
        # Initialize sentence transformer for multilingual support
        print("🤖 Loading multilingual sentence transformer...")
        self.encoder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Load or create embeddings
        self.embeddings = self._load_or_create_embeddings()
        
        # Banglish to Bangla transliteration mapping
        self.banglish_mapping = {
            # Characters and names
            'anupam': 'অনুপম',
            'kalyani': 'কল্যাণী',
            'mama': 'মামা',
            'aparichita': 'অপরিচিতা',
            'rabindranath': 'রবীন্দ্রনাথ',
            'tagore': 'ঠাকুর',
            
            # Common words
            'golpo': 'গল্প',
            'charitra': 'চরিত্র',
            'biyer': 'বিয়ের',
            'biye': 'বিয়ে',
            'shikkha': 'শিক্ষা',
            'nari': 'নারী',
            'meye': 'মেয়ে',
            'chele': 'ছেলে',
            'baba': 'বাবা',
            'ma': 'মা',
            'maa': 'মা',
            'ghor': 'ঘর',
            'bashay': 'বাসায়',
            'basha': 'বাসা',
            'school': 'স্কুল',
            'college': 'কলেজ',
            'english': 'ইংরেজি',
            'bangla': 'বাংলা',
            'question': 'প্রশ্ন',
            'proshno': 'প্রশ্ন',
            'uttor': 'উত্তর',
            'answer': 'উত্তর',
            'ki': 'কি',
            'kemon': 'কেমন',
            'keno': 'কেন',
            'kothai': 'কোথায়',
            'kokhon': 'কখন',
            'kar': 'কার',
            'koto': 'কত',
            'kotogulo': 'কতগুলো',
            'amra': 'আমরা',
            'tumi': 'তুমি',
            'tomar': 'তোমার',
            'amar': 'আমার',
            'tar': 'তার',
            'oder': 'ওদের',
            'oder': 'তাদের',
            'kore': 'করে',
            'korte': 'করতে',
            'korchi': 'করছি',
            'korbo': 'করবো',
            'hobe': 'হবে',
            'hoye': 'হয়ে',
            'hoyeche': 'হয়েছে',
            'ache': 'আছে',
            'chilo': 'ছিল',
            'chile': 'ছিলে',
            'chole': 'চলে',
            'gele': 'গেলে',
            'gelo': 'গেলো',
            'elo': 'এলো',
            'esho': 'এসো',
            'dekho': 'দেখো',
            'dekhi': 'দেখি',
            'bolo': 'বলো',
            'boli': 'বলি',
            'bole': 'বলে',
            'boleche': 'বলেছে',
            'shono': 'শোনো',
            'shuni': 'শুনি',
            'age': 'আগে',
            'pore': 'পরে',
            'ekhon': 'এখন',
            'kal': 'কাল',
            'aj': 'আজ',
            'ajke': 'আজকে',
            'valo': 'ভালো',
            'valobashe': 'ভালোবাসে',
            'kharap': 'খারাপ',
            'sundor': 'সুন্দর',
            'bhalo': 'ভালো',
            'kalo': 'কালো',
            'shada': 'সাদা',
            'lal': 'লাল',
            'nil': 'নীল',
            'holud': 'হলুদ',
            'sobuj': 'সবুজ',
            'boro': 'বড়ো',
            'choto': 'ছোটো',
            'meyer': 'মেয়ের',
            'cheler': 'ছেলের',
            'babar': 'বাবার',
            'mayer': 'মায়ের',
            'family': 'পরিবার',
            'poribar': 'পরিবার',
            'shathe': 'সাথে',
            'shomoye': 'সময়ে',
            'shomoy': 'সময়',
            'jaygay': 'জায়গায়',
            'jayga': 'জায়গা',
            'theme': 'বিষয়',
            'bishoy': 'বিষয়',
            'ghotona': 'ঘটনা',
            'ghote': 'ঘটে',
            'hoy': 'হয়',
            'na': 'না',
            'nai': 'নাই',
            'nei': 'নেই',
            'eto': 'এতো',
            'oi': 'ওই',
            'ei': 'এই',
            'shei': 'সেই',
            'je': 'যে',
            'jar': 'যার',
            'jeta': 'যেটা',
            'jegulo': 'যেগুলো',
            'analysis': 'বিশ্লেষণ',
            'bishleshan': 'বিশ্লেষণ',
            'character': 'চরিত্র',
            'importance': 'গুরুত্ব',
            'gurutto': 'গুরুত্ব',
            'love': 'ভালোবাসা',
            'valobasha': 'ভালোবাসা',
            'marriage': 'বিবাহ',
            'bibaho': 'বিবাহ',
            'society': 'সমাজ',
            'shomaj': 'সমাজ',
            'social': 'সামাজিক',
            'shamajik': 'সামাজিক',
            'education': 'শিক্ষা',
            'woman': 'নারী',
            'women': 'নারী',
            'girl': 'মেয়ে',
            'boy': 'ছেলে',
            'man': 'পুরুষ',
            'purush': 'পুরুষ',
            'lok': 'লোক',
            'manush': 'মানুষ',
            'jonnyo': 'জন্য',
            'jonno': 'জন্য',
            'main': 'মূল',
            'mul': 'মূল',
            'story': 'গল্প',
            'kotha': 'কথা',
            'kobitay': 'কবিতায়',
            'kobita': 'কবিতা',
            'lekhok': 'লেখক',
            'lekha': 'লেখা',
            'likhe': 'লিখে',
            'likhte': 'লিখতে',
            'lekhen': 'লেখেন',
            'lekheni': 'লেখেনি',
            'boi': 'বই',
            'book': 'বই',
            'page': 'পাতা',
            'pata': 'পাতা',
            'number': 'নম্বর',
            'nombor': 'নম্বর',
            'details': 'বিস্তারিত',
            'bistari': 'বিস্তারিত',
            'bishesh': 'বিশেষ',
            'special': 'বিশেষ',
            'important': 'গুরুত্বপূর্ণ',
            'guruttopurno': 'গুরুত্বপূর্ণ',
            'interesting': 'মজার',
            'mojar': 'মজার',
            'shundor': 'সুন্দর',
            'cute': 'সুন্দর',
            'smart': 'চালাক',
            'chalak': 'চালাক',
            'wise': 'জ্ঞানী',
            'gyani': 'জ্ঞানী',
            'foolish': 'বোকা',
            'boka': 'বোকা',
            'stupid': 'বোকা',
        }
        
        print(f"✅ Vector-based RAG system ready with {len(self.chunks)} chunks")
        print(f"🔤 Banglish support enabled with {len(self.banglish_mapping)} word mappings")
        print(f"🧠 Using multilingual sentence transformer for semantic search")
    
    def _load_or_create_embeddings(self):
        """Load embeddings from file or create new ones"""
        if os.path.exists(self.embeddings_file):
            print("📁 Loading existing embeddings...")
            with open(self.embeddings_file, 'rb') as f:
                embeddings = pickle.load(f)
            print(f"✅ Loaded {len(embeddings)} embeddings from cache")
            return embeddings
        else:
            print("🔄 Creating new embeddings... (this may take a moment)")
            texts = [chunk['text'] for chunk in self.chunks]
            embeddings = self.encoder.encode(texts, show_progress_bar=True)
            
            # Save embeddings for future use
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(embeddings, f)
            print(f"💾 Saved {len(embeddings)} embeddings to cache")
            return embeddings
    
    def convert_banglish_to_bangla(self, text):
        """Convert banglish text to bangla for better matching"""
        # Convert to lowercase for matching
        lower_text = text.lower()
        
        # Replace banglish words with bangla equivalents
        for banglish_word, bangla_word in self.banglish_mapping.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(banglish_word) + r'\b'
            lower_text = re.sub(pattern, bangla_word, lower_text)
        
        return lower_text
    
    def find_relevant_chunks_vector(self, query, top_k=5):
        """Find relevant chunks using semantic similarity (vector search)"""
        # Convert banglish to bangla for better matching
        bangla_query = self.convert_banglish_to_bangla(query)
        
        # Use both original and converted query
        combined_query = f"{query} {bangla_query}"
        
        # Encode the query
        query_embedding = self.encoder.encode([combined_query])
        
        # Calculate cosine similarity with all chunk embeddings
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top_k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return chunks with similarity scores
        relevant_chunks = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                relevant_chunks.append({
                    **self.chunks[idx],
                    'similarity_score': float(similarities[idx])
                })
        
        return relevant_chunks
    
    def find_relevant_chunks_basic(self, query, top_k=5):
        """Find relevant chunks using simple keyword matching with banglish support"""
        # Convert banglish to bangla for better matching
        bangla_query = self.convert_banglish_to_bangla(query)
        
        # Use both original and converted query for matching
        query_words = query.lower().split() + bangla_query.split()
        
        scored_chunks = []
        for chunk in self.chunks:
            text = chunk['text'].lower()
            score = 0
            
            # Simple keyword matching
            for word in query_words:
                if len(word) > 2:  # Only consider words longer than 2 characters
                    score += text.count(word)
            
            # Bonus points for exact phrase matches
            if bangla_query.strip() in text:
                score += 5
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score
                })
        
        # Sort by score and return top_k
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        return [item['chunk'] for item in scored_chunks[:top_k]]
    
    def find_relevant_chunks_hybrid(self, query, top_k=5):
        """Hybrid search combining vector similarity and keyword matching"""
        # Get results from both methods
        vector_chunks = self.find_relevant_chunks_vector(query, top_k=top_k*2)
        keyword_chunks = self.find_relevant_chunks_basic(query, top_k=top_k*2)
        
        # Combine and score
        combined_chunks = {}
        
        # Add vector results with similarity scores
        for i, chunk in enumerate(vector_chunks):
            chunk_id = chunk['id']
            score = chunk.get('similarity_score', 0) * 100  # Scale up similarity
            combined_chunks[chunk_id] = {
                'chunk': chunk,
                'vector_score': score,
                'keyword_score': 0,
                'rank_bonus_vector': (len(vector_chunks) - i) * 2,
                'rank_bonus_keyword': 0
            }
        
        # Add keyword results
        for i, chunk in enumerate(keyword_chunks):
            chunk_id = chunk['id']
            if chunk_id in combined_chunks:
                # Update existing entry
                combined_chunks[chunk_id]['keyword_score'] = max(1, 10 - i)
                combined_chunks[chunk_id]['rank_bonus_keyword'] = (len(keyword_chunks) - i)
            else:
                # New entry
                combined_chunks[chunk_id] = {
                    'chunk': chunk,
                    'vector_score': 0,
                    'keyword_score': max(1, 10 - i),
                    'rank_bonus_vector': 0,
                    'rank_bonus_keyword': (len(keyword_chunks) - i)
                }
        
        # Calculate final scores
        final_chunks = []
        for chunk_data in combined_chunks.values():
            total_score = (
                chunk_data['vector_score'] * 0.6 +  # 60% weight to semantic similarity
                chunk_data['keyword_score'] * 0.3 +  # 30% weight to keyword matching
                chunk_data['rank_bonus_vector'] * 0.05 +  # 5% rank bonus from vector
                chunk_data['rank_bonus_keyword'] * 0.05   # 5% rank bonus from keyword
            )
            
            final_chunks.append({
                'chunk': chunk_data['chunk'],
                'final_score': total_score
            })
        
        # Sort by final score and return top_k
        final_chunks.sort(key=lambda x: x['final_score'], reverse=True)
        return [item['chunk'] for item in final_chunks[:top_k]]
    
    def generate_answer(self, query, relevant_chunks, conversation_history=None):
        """Generate answer using OpenAI with relevant context, banglish support, and conversation memory"""
        
        # Detect if query is banglish (mixed English-Bengali romanized)
        is_banglish = self.is_banglish_query(query)
        bangla_query = self.convert_banglish_to_bangla(query)
        
        # Prepare context from relevant chunks (Long-term memory)
        context = "\n\n".join([chunk['text'] for chunk in relevant_chunks[:3]])
        
        # Prepare conversation context (Short-term memory)
        conversation_context = ""
        if conversation_history and len(conversation_history) > 0:
            recent_conversations = conversation_history[-3:]  # Last 3 exchanges
            conversation_context = "\n\nRecent conversation context:\n"
            for i, conv in enumerate(recent_conversations, 1):
                conversation_context += f"Previous Q{i}: {conv['question']}\n"
                conversation_context += f"Previous A{i}: {conv['answer'][:100]}...\n"
        
        # Create prompt based on query type
        if is_banglish:
            prompt = f"""You are a helpful assistant for Bangla literature educational content about "অপরিচিতা" (Aparichita) by Rabindranath Tagore.

The user asked in Banglish (romanized Bengali): {query}
Which translates to: {bangla_query}

LONG-TERM MEMORY (Knowledge Base):
{context}

SHORT-TERM MEMORY (Recent Conversation):
{conversation_context}

Instructions:
- The user asked in Banglish, so respond in a mix of Bangla and simple English that's easy to understand
- You can use both Bangla script and romanized Bengali (banglish) in your answer
- Consider the conversation history to provide contextual answers
- If this question relates to previous questions, mention the connection
- Be accurate and refer to the provided context
- If you cannot find the answer in the context, say so politely
- Keep answers concise but informative
- Examples: "Anupamer boyosh chilo..." or "অনুপমের বয়স ছিল..."

Answer:"""
        else:
            prompt = f"""You are a helpful assistant for Bangla literature educational content about "অপরিচিতা" (Aparichita) by Rabindranath Tagore.

LONG-TERM MEMORY (Knowledge Base):
{context}

SHORT-TERM MEMORY (Recent Conversation):
{conversation_context}

Question: {query}

Instructions:
- Answer in the same language as the question (if Bangla question, answer in Bangla; if English question, answer in English)
- Consider the conversation history to provide contextual and connected answers
- If this question relates to previous questions, mention the connection
- Be accurate and refer to the provided context
- If you cannot find the answer in the context, say so politely
- For multiple choice questions, explain the reasoning
- Keep answers concise but informative

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Bangla literature education with support for Banglish (romanized Bengali) and conversation memory."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"
    
    def is_banglish_query(self, text):
        """Detect if the query is written in banglish (romanized Bengali)"""
        # Check if text contains romanized Bengali words
        banglish_indicators = ['anupam', 'kalyani', 'mama', 'golpo', 'charitra', 'ki', 'kemon', 'keno', 
                              'tar', 'tomar', 'amar', 'ache', 'chilo', 'hoy', 'kore', 'bole', 'dekho',
                              'valo', 'bhalo', 'meyer', 'cheler', 'age', 'pore', 'ekhon']
        
        text_lower = text.lower()
        banglish_count = sum(1 for word in banglish_indicators if word in text_lower)
        
        # If more than 1 banglish word detected, consider it banglish
        return banglish_count > 0
    
    def query(self, question, search_method='hybrid', conversation_history=None):
        """Main query method with vector-based, hybrid search, and conversation memory support"""
        print(f"🔍 Processing query: {question}")
        
        # Check if it's banglish and show converted query
        if self.is_banglish_query(question):
            bangla_equivalent = self.convert_banglish_to_bangla(question)
            print(f"🔤 Banglish detected, converted to: {bangla_equivalent}")
        
        # Show memory status
        if conversation_history:
            print(f"🧠 Using conversation memory: {len(conversation_history)} previous exchanges")
        
        # Find relevant chunks using specified method (Long-term memory)
        if search_method == 'vector':
            print("🧠 Using vector-based semantic search...")
            relevant_chunks = self.find_relevant_chunks_vector(question, top_k=5)
        elif search_method == 'keyword':
            print("🔍 Using keyword-based search...")
            relevant_chunks = self.find_relevant_chunks_basic(question, top_k=5)
        else:  # hybrid (default)
            print("⚡ Using hybrid search (vector + keyword)...")
            relevant_chunks = self.find_relevant_chunks_hybrid(question, top_k=5)
        
        if not relevant_chunks:
            return {
                'answer': "দুঃখিত, এই প্রশ্নের উত্তর খুঁজে পাওয়া যায়নি। অন্য প্রশ্ন করার চেষ্টা করুন।\n\nSorry, answer not found for this question. Try asking differently.",
                'relevant_chunks': [],
                'success': False,
                'search_method': search_method,
                'used_conversation_memory': bool(conversation_history)
            }
        
        print(f"📚 Found {len(relevant_chunks)} relevant chunks")
        
        # Generate answer with conversation memory (Short-term + Long-term)
        answer = self.generate_answer(question, relevant_chunks, conversation_history)
        
        return {
            'answer': answer,
            'relevant_chunks': [{'text': chunk['text'], 'metadata': chunk} for chunk in relevant_chunks[:3]],
            'success': True,
            'search_method': search_method,
            'total_chunks_found': len(relevant_chunks),
            'used_conversation_memory': bool(conversation_history)
        }


