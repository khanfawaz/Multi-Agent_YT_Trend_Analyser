import os
import nltk
from dotenv import load_dotenv
from googleapiclient.discovery import build
from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()
nltk.download('vader_lexicon')
API_KEY = os.getenv("YT_API_KEY")

sia = SentimentIntensityAnalyzer()

def fetch_and_analyze_comments(video_id, max_comments=500):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    comments = []  
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(text)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    # Sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}

    for comment in comments:
        score = sia.polarity_scores(comment)["compound"]
        if score > 0.05:
            sentiments["positive"] += 1
        elif score < -0.05:
            sentiments["negative"] += 1
        else:
            sentiments["neutral"] += 1

    return sentiments, comments