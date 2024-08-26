import os
from groq import Groq
from dotenv import load_dotenv


# Load the Groq API key from environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_chunk(chunk: str):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes text into concise and clear summaries."},
            {"role": "user", "content": f"Summarize the following text:\n\n{chunk}"},
        ]
    )
    return response.choices[0].message.content

def summarize_text(chunks: list[str]):
    summaries = [summarize_chunk(chunk) for chunk in chunks]
    combined_summary = " ".join(summaries)
    # Optionally, summarize the combined summary if it's still too long
    final_summary = summarize_chunk(combined_summary) if len(combined_summary) > 4000 else combined_summary    
    return final_summary