import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YT_API_KEY")

def fetch_trending_videos(region="IN", max_results=10):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region,
        maxResults=max_results
    )
    
    response = request.execute()
    videos = []
    for item in response["items"]:
        stats = item["statistics"]
        engagement_score = (
            int(stats.get("likeCount", 0)) +
            int(stats.get("commentCount", 0)) * 2
        ) / max(1, int(stats.get("viewCount", 1)))
        
        videos.append({
            "videoId": item["id"],
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
            "channelTitle": item["snippet"]["channelTitle"],
            "viewCount": stats.get("viewCount", "0"),
            "likeCount": stats.get("likeCount", "0"),
            "commentCount": stats.get("commentCount", "0"),
            "score": round(engagement_score, 4),
            "publishedAt": item["snippet"]["publishedAt"]
        })

    return sorted(videos, key=lambda v: v["score"], reverse=True)

