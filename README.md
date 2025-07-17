# 🎥 Multi-Agent YouTube Trend Analyzer

This is a multi-agent LLM-powered system that analyzes trending YouTube videos by fetching, filtering, and evaluating public sentiment based on comments. It uses Google’s YouTube Data API and Groq-hosted LLaMA 3.3 for real-time summarization and insights.

---

## 🚀 Key Features

- **Trending Video Fetcher**: Retrieves top trending YouTube videos by region and time window (1, 3, 7 days).
- **Human-in-the-Loop Selection**: Choose which video to analyze from the trending list.
- **Sentiment Analysis Agent**: Classifies YouTube comments into Positive, Neutral, and Negative.
- **LLM-Based Summarization Agent**: Uses Groq + LLaMA 3.3 to generate concise summaries of viewer sentiment.
- **Streamlit Frontend**: Intuitive and interactive UI with real-time insights.

---

## 🧠 Tech Stack

- `LangChain + LangGraph`: Agent orchestration
- `Streamlit`: Web UI for interaction
- `Google YouTube Data API`: Fetch trending video data and comments
- `NLTK`: Sentiment analysis using VADER
- `Groq SDK + LLaMA 3.3`: Comment summarization
- `dotenv`: Secure environment variable management

---
