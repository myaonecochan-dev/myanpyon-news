
import requests

def check():
    url = "https://image.pollinations.ai/prompt/brothers%20family%20happy%20anime?width=1200&height=630&nologo=true&seed=384"
    print(f"Checking: {url}")
    try:
        resp = requests.head(url, timeout=10)
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")
        print(f"Content-Length: {resp.headers.get('content-length')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
