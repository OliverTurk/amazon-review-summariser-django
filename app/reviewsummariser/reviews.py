import requests
from bs4 import BeautifulSoup
import anthropic
import os
from dotenv import load_dotenv

def get_reviews(url):
    headers = {
    "Accept-language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    }
    
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    reviews = soup.find_all("div", {"data-hook": "review"})
    
    text = ""
    
    for review in reviews:
        body = review.find("span", {"data-hook": "review-body"}).text.strip()
        body = body.replace("Read more", "")
        text = text + body
    
    return text

def summarise_text(text):
    if text == "":
        return ""
    load_dotenv()
    MODEL="claude-3-5-sonnet-20240620"
    MAX_TOKENS=1024

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    message = client.messages.create(
        model = MODEL,
        max_tokens = MAX_TOKENS,
        temperature = 0,
        messages=[
            {"role": "user", "content": f"summarise the following set of reviews into a 100-200 word paragraph escribing both the positives and the negatives of the product in english give only the summary: {text}"}
        ]
    )
    
    summary = message.content[0].text
    slide_index = summary.find(":") + 1
    
    return summary[slide_index:]

def summarise_reviews(url):
    text = get_reviews(url)
        
    summary = summarise_text(text)
    
    return summary


