@echo off
echo 🎓========================================🎓
echo � অপরিচিতা শিক্ষা কেন্দ্র চালু হচ্ছে...
echo 📚 Starting Aparichita Learning Center...
echo �========================================�

echo.
echo 📦 Installing required packages...
"D:/10-minute-project/.venv/Scripts/pip.exe" install streamlit openai python-dotenv plotly

echo.
echo 🔧 Processing educational content...
"D:/10-minute-project/.venv/Scripts/python.exe" text_processor.py

echo.
echo � Starting educational web platform...
echo 🌐 Open your browser and go to: http://localhost:8501
echo 📚 AI-Powered Interactive Learning Experience
echo.

"D:/10-minute-project/.venv/Scripts/streamlit.exe" run app.py

pause
