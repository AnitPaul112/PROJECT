import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv('OPENAI_API_KEY')
print(f"Loaded API Key: {api_key[:4]}...{api_key[-4:] if api_key else 'None'}")
from basic_rag import BasicBanglaRAG
from datetime import datetime

# Page config minimal
st.set_page_config(page_title="অপরিচিতা", layout="centered")

st.title("আলোচ্য বিষয় 'অপরিচিতা' গল্প")

# Remove API Key input and related logic

# Initialize session state for conversation memory (Short-term memory)
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'related_topics' not in st.session_state:
    st.session_state.related_topics = set()

# Initialize or reuse RAG system (Long-term memory)
if 'rag_system' not in st.session_state:
    try:
        with st.spinner("Loading Long-term Memory (Vector Database)..."):
            st.session_state.rag_system = BasicBanglaRAG()
        st.success("Memory system loaded!")
    except Exception as e:
        st.error(f"RAG initialization failed: {e}")
        st.stop()

# Memory status sidebar
with st.sidebar:
    st.header("Memory Status")
    
    # Short-term memory
    st.subheader("Short-term Memory")
    st.metric("Conversation History", len(st.session_state.conversation_history))
    st.metric("Related Topics", len(st.session_state.related_topics))
    
    # Long-term memory
    st.subheader("Long-term Memory")
    if st.session_state.rag_system:
        st.metric("Vector Database", f"{len(st.session_state.rag_system.chunks)} chunks")
        st.info("Knowledge base loaded")
    
    # Show recent topics
    if st.session_state.related_topics:
        st.subheader("Discussed Topics")
        for topic in list(st.session_state.related_topics)[-5:]:
            st.write(f"{topic}")
    
    # Clear memory button
    if st.button("Clear Short-term Memory"):
        st.session_state.conversation_history = []
        st.session_state.related_topics = set()
        st.success("Memory cleared!")

# Input box for question
question = st.text_input(
    "আপনার প্রশ্ন লিখুন", 
    placeholder="যেমন: anupamer boyosh koto? অথবা অনুপমের বয়স কত?"
)

# Search method selection
search_method = st.selectbox(
    "সার্চ পদ্ধতি নির্বাচন করুন:",
    ["hybrid", "vector", "keyword"],
    format_func=lambda x: {
        "hybrid": "হাইব্রিড (সেরা ফলাফল - ভেক্টর + কীওয়ার্ড)",
        "vector": "সিমান্টিক সার্চ (অর্থ বুঝে খোঁজে)",
        "keyword": "কীওয়ার্ড সার্চ (শব্দ মিল)"
    }[x]
)

if st.button("জিজ্ঞাসা করুন") and question.strip():
    with st.spinner("উত্তর খুঁজছে (Short-term + Long-term Memory)..."):
        # Pass conversation history for context-aware responses
        result = st.session_state.rag_system.query(
            question, 
            search_method=search_method,
            conversation_history=st.session_state.conversation_history
        )
    
    st.markdown("উত্তর:")
    st.write(result['answer'])
    
    # Add to conversation history (Short-term memory)
    st.session_state.conversation_history.append({
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'question': question,
        'answer': result['answer'],
        'search_method': search_method
    })
    
    # Extract and add topics to related topics
    question_lower = question.lower()
    topics = []
    if 'anupam' in question_lower or 'অনুপম' in question_lower:
        topics.append('অনুপম')
    if 'kalyani' in question_lower or 'কল্যাণী' in question_lower:
        topics.append('কল্যাণী')
    if 'mama' in question_lower or 'মামা' in question_lower:
        topics.append('মামা')
    if 'biye' in question_lower or 'বিয়ে' in question_lower or 'marriage' in question_lower:
        topics.append('বিবাহ')
    if 'shikkha' in question_lower or 'শিক্ষা' in question_lower or 'education' in question_lower:
        topics.append('শিক্ষা')
    
    for topic in topics:
        st.session_state.related_topics.add(topic)
    
    # Show search method used and memory status
    method_names = {
        "hybrid": "হাইব্রিড সার্চ",
        "vector": "সিমান্টিক সার্চ", 
        "keyword": "কীওয়ার্ড সার্চ"
    }
    
    memory_status = "Short-term + Long-term Memory" if result.get('used_conversation_memory') else "📚 Long-term Memory only"
    
    st.info(f"ব্যবহৃত পদ্ধতি: {method_names.get(result.get('search_method', 'hybrid'), 'হাইব্রিড')} | {memory_status}")
    
    if result.get('relevant_chunks'):
        st.markdown("প্রাসঙ্গিক তথ্যসূত্র:")
        for idx, chunk in enumerate(result['relevant_chunks']):
            # Show similarity score if available
            metadata = chunk.get('metadata', {})
            similarity_info = ""
            if 'similarity_score' in metadata:
                similarity_info = f" (সিমিলারিটি: {metadata['similarity_score']:.2f})"
            
            st.write(f"{idx+1}. {chunk['text'][:300]}{'...' if len(chunk['text']) > 300 else ''}{similarity_info}")

else:
    st.info("প্রশ্ন লিখে 'জিজ্ঞাসা করুন' বাটনে ক্লিক করুন।")
    
    # Sample questions
    st.markdown("নমুনা প্রশ্ন:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**বাংলায়:**")
        st.markdown("• অনুপমের বয়স কত?")
        st.markdown("• কল্যাণীর চরিত্র কেমন?")
        st.markdown("• গল্পের মূল বিষয় কি?")
    
    with col2:
        st.markdown("**ব্যাংলিশে:**")
        st.markdown("• anupamer boyosh koto?")
        st.markdown("• kalyani kemon meyer chilo?")
        st.markdown("• golper main theme ki?")

# Show conversation history (Short-term memory)
if st.session_state.conversation_history:
    st.markdown("---")
    st.markdown("কথোপকথনের ইতিহাস (Short-term Memory)")
    
    # Show last 3 conversations
    recent_conversations = st.session_state.conversation_history[-3:]
    
    for i, conv in enumerate(reversed(recent_conversations), 1):
        with st.expander(f"🕐 {conv['timestamp']} - {conv['question'][:50]}{'...' if len(conv['question']) > 50 else ''}"):
            st.markdown(f"**প্রশ্ন:** {conv['question']}")
            st.markdown(f"**উত্তর:** {conv['answer'][:200]}{'...' if len(conv['answer']) > 200 else ''}")
            st.caption(f"পদ্ধতি: {conv['search_method']}")

# Memory explanation

