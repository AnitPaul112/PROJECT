import re
import os
from typing import List, Dict
import json

class BanglaTextProcessor:
    def __init__(self, txt_file_path: str):
        self.txt_file_path = txt_file_path
        self.cleaned_text = ""
        self.chunks = []
        
    def clean_text(self) -> str:
        """Clean and preprocess the Bengali text"""
        with open(self.txt_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Remove page markers
        text = re.sub(r'--- Page \d+ ---', '', text)
        
        # Remove phone numbers and unnecessary numbers
        text = re.sub(r'₹\d+', '', text)
        text = re.sub(r'\d{7,}', '', text)
        
        # Remove extra whitespaces and newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Clean up common OCR errors
        text = re.sub(r'[|।]{2,}', '।', text)
        text = re.sub(r'[।\.]{2,}', '।', text)
        
        # Remove isolated numbers and symbols
        text = re.sub(r'\b\d+\b(?!\s*[।\.]\s*)', '', text)
        
        self.cleaned_text = text.strip()
        return self.cleaned_text
    
    def create_chunks(self, chunk_size: int = 300, overlap: int = 50) -> List[Dict]:
        """Create text chunks for better retrieval"""
        if not self.cleaned_text:
            self.clean_text()
        
        # Split by different delimiters to get better chunks
        text_parts = []
        
        # First, split by major sections
        major_sections = re.split(r'(?=শব্দার্থ ও টীকা|মূল গল্প)', self.cleaned_text)
        
        for section in major_sections:
            if not section.strip():
                continue
                
            # Split each section by sentences and questions
            sentences = re.split(r'[।\.\?]\s*', section)
            
            # Also split by question patterns
            questions = []
            for sentence in sentences:
                if sentence.strip():
                    # Split by multiple choice questions
                    q_parts = re.split(r'(?=[১২৩৪৫৬৭৮৯০]\.)', sentence)
                    questions.extend([q.strip() for q in q_parts if q.strip()])
            
            text_parts.extend(questions)
        
        # Now create chunks from these parts
        chunks = []
        current_chunk = ""
        chunk_id = 0
        
        for part in text_parts:
            part = part.strip()
            if len(part) < 10:  # Skip very short parts
                continue
                
            # If adding this part would exceed chunk size, save current chunk
            if len(current_chunk) + len(part) > chunk_size and current_chunk:
                chunks.append({
                    'id': chunk_id,
                    'text': current_chunk.strip(),
                    'type': self._identify_content_type(current_chunk)
                })
                chunk_id += 1
                
                # Keep some overlap
                words = current_chunk.split()
                if len(words) > 10:
                    current_chunk = " ".join(words[-10:]) + " "
                else:
                    current_chunk = ""
            
            current_chunk += part + " "
            
            # If this part itself is long enough, make it a separate chunk
            if len(part) > chunk_size:
                chunks.append({
                    'id': chunk_id,
                    'text': part.strip(),
                    'type': self._identify_content_type(part)
                })
                chunk_id += 1
                current_chunk = ""
        
        # Add the last chunk if it has content
        if current_chunk.strip():
            chunks.append({
                'id': chunk_id,
                'text': current_chunk.strip(),
                'type': self._identify_content_type(current_chunk)
            })
        
        self.chunks = chunks
        return chunks
    
    def _identify_content_type(self, text: str) -> str:
        """Identify the type of content (question, explanation, vocabulary, etc.)"""
        if '?' in text or 'প্রশ্ন' in text or any(q in text for q in ['ক)', 'খ)', 'গ)', 'ঘ)']):
            return 'question'
        elif 'শব্দার্থ' in text or 'টীকা' in text:
            return 'vocabulary'
        elif 'অনুচ্ছেদ' in text:
            return 'passage'
        elif any(char in text for char in ['১।', '২।', '৩।', '৪।', '৫।']):
            return 'numbered_content'
        else:
            return 'explanation'
    
    def save_processed_data(self, output_file: str = 'processed_data.json'):
        """Save processed chunks to JSON file"""
        if not self.chunks:
            self.create_chunks()
        
        data = {
            'total_chunks': len(self.chunks),
            'chunks': self.chunks,
            'metadata': {
                'source_file': self.txt_file_path,
                'total_text_length': len(self.cleaned_text)
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Processed data saved to {output_file}")
        print(f"📊 Total chunks created: {len(self.chunks)}")
        return output_file

if __name__ == "__main__":
    # Process the Bangla text
    processor = BanglaTextProcessor('bangla_output.txt')
    processor.clean_text()
    processor.create_chunks()
    processor.save_processed_data()
    
    # Print some sample chunks
    print("\n📝 Sample chunks:")
    for i, chunk in enumerate(processor.chunks[:3]):
        print(f"\nChunk {i+1} ({chunk['type']}):")
        print(chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'])
