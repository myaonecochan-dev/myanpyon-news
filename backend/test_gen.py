import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def test():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    topic = "今日の天気"
    prompt = f"""
    Act as a news commentary duo for a popular Japanese summary blog.
    Topic: "{topic}"
    Characters: Myan (Cat), Pyon (Bunny).
    Format: Return ONLY valid JSON with keys: "title", "content", "description", "tweet_text", "reactions", "poll".
    "reactions": [{"name": "名無しさん", "text": "...", "color": "green/blue/red"}]
    "poll": {"question": "...", "option_a": "...", "option_b": "..."}
    """
    
    print("Sending prompt to Gemini...")
    try:
        response = model.generate_content(prompt)
        text = response.text
        print(f"Raw Response:\n{text}\n")
        
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            print("Successfully parsed JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("No JSON found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
