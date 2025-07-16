from agents.yt_agent import fetch_trending_videos
from agents.selection_agent import select_video
from agents.comment_agent import fetch_and_analyze_comments
from agents.summarizer_agent import summarize_comments_with_llm  # ✅ NEW
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="YT Trend Analyzer", layout="wide")
st.title("📈 YouTube Trend Analyzer")

# Sidebar Filters
region = st.sidebar.selectbox("Select Region", ["IN", "US", "GB", "CA", "AU"])
max_results = st.sidebar.slider("Number of Videos", 5, 10, 10)
days_filter = st.sidebar.selectbox("Show videos uploaded in last...", ["Any", "1 Day", "3 Days", "7 Days"])

# Filter Mapping
now = datetime.utcnow()
cutoff_days = {
    "1 Day": now - timedelta(days=1),
    "3 Days": now - timedelta(days=3),
    "7 Days": now - timedelta(days=7),
    "Any": None
}
upload_cutoff = cutoff_days[days_filter]

# Fetch Videos
if st.sidebar.button("🔍 Fetch Trending Videos"):
    with st.spinner("Fetching..."):
        all_videos = fetch_trending_videos(region=region, max_results=max_results)
        if upload_cutoff:
            filtered = []
            for v in all_videos:
                upload_time = datetime.strptime(v.get("publishedAt")[:10], "%Y-%m-%d")
                if upload_time >= upload_cutoff:
                    filtered.append(v)
            st.session_state.videos = filtered
        else:
            st.session_state.videos = all_videos

# Phase 1: Video Selection
if "videos" in st.session_state:
    videos = st.session_state.videos

    if len(videos) == 0:
        st.warning("No videos match your filter.")
    else:
        st.subheader("Trending Videos")
        selected_index = st.radio(
            "Choose one to analyze:",
            options=range(len(videos)),
            format_func=lambda i: f"{videos[i]['title']} — {videos[i]['channelTitle']}"
        )
        selected_video = select_video(videos, selected_index)

        if selected_video:
            st.markdown(f"### 🎬 {selected_video['title']}")
            st.image(selected_video["thumbnail"])
            st.write(f"**Channel:** {selected_video['channelTitle']}")
            st.write(f"**Views:** {selected_video['viewCount']}")
            st.write(f"**Likes:** {selected_video['likeCount']}")
            st.write(f"**Comments:** {selected_video['commentCount']}")
            st.info("Selected for sentiment analysis.")

            # Phase 2: Sentiment Analysis
            if st.button("🧠 Analyze Comments"):
                with st.spinner("Analyzing sentiment..."):
                    sentiment, comments = fetch_and_analyze_comments(
                        selected_video["videoId"], max_comments=1000
                    )
                    st.success("Analysis Complete")

                    st.markdown("### 🧭 Sentiment Overview")
                    st.write(sentiment)

                    st.markdown("### 🗣 Sample Comments")
                    for comment in comments[:5]:
                        st.write(f"- {comment}")

                    # ✅ Phase 3: LLM Summarizer
                    st.markdown("### 🤖 LLM-Based Summary")
                    with st.spinner("Summarizing using Groq + LLaMA 3.3..."):
                        try:
                            summary = summarize_comments_with_llm(comments)
                            st.success("LLM Summary Complete")
                            st.markdown(f"📋 **Summary:** {summary}")
                        except Exception as e:
                            st.error(f"Error during LLM summarization: {e}")