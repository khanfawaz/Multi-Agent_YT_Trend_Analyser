import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_comments_with_llm(comments: list[str], model="llama-3.3-70b-versatile") -> str:
    # Chunk and condense long comment lists
    if len(comments) > 100:
        comments = comments[:100]

    prompt = (
        "Summarize the following YouTube comments into a single paragraph that captures the main themes, "
        "overall sentiment, and noteworthy reactions. Be neutral and insightful.\n\n"
        + "\n".join([f"- {c}" for c in comments])
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in summarizing user opinions from online discussions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
