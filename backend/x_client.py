import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# X API Keys
API_KEY = os.environ.get("X_API_KEY")
API_SECRET = os.environ.get("X_API_SECRET")
ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET")

def post_tweet(text):
    """
    Posts a tweet to X.
    If keys are missing, performs a Dry Run (prints to console).
    """
    print(f"--- X Posting Service ---")
    
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("!! Credentials missing. Switching to DRY RUN mode. !!")
        print(f"[Dry Run Tweet]: {text}")
        return True

    try:
        # Authenticate
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        # Post
        response = client.create_tweet(text=text)
        print(f"Successfully posted to X! ID: {response.data['id']}")
        return True

    except Exception as e:
        print(f"Error posting to X: {e}")
        return False

# Test run if executed directly
if __name__ == "__main__":
    post_tweet("Test tweet from MyanPyon Bot (Warm-up Mode)")
