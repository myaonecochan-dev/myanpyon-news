import time
import subprocess
import datetime
import sys
import random

def run_collector():
    print(f"\n[Scheduler] Starting job at {datetime.datetime.now()}")
    try:
        # Run collector.py
        subprocess.run([sys.executable, "backend/collector.py"], check=True)
        
        # Run sitemap generator to update sitemap with new post
        print("[Scheduler] Updating Sitemap...")
        subprocess.run([sys.executable, "backend/generate_sitemap.py"], check=True)
        
        print("[Scheduler] Job finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[Scheduler] Error running job: {e}")
    except Exception as e:
        print(f"[Scheduler] Unexpected error: {e}")

def main():
    print("=== MyanPyon Auto-Scheduler Started ===")
    print("Interval: Approx. 1 hour")
    print("Press Ctrl+C to stop.\n")

    # Run once immediately on start?
    # run_collector() 
    # Let's wait first or ask user. Assuming we want to start loop.

    while True:
        run_collector()
        
        # Wait for 1 hour (3600 seconds)
        # Add a little fuzziness (+- 5 mins) so it doesn't look too bot-like to APIs
        sleep_time = 3600 + random.randint(-300, 300)
        
        next_run = datetime.datetime.now() + datetime.timedelta(seconds=sleep_time)
        print(f"[Scheduler] Sleeping for {sleep_time/60:.1f} minutes.")
        print(f"[Scheduler] Next run at: {next_run.strftime('%H:%M:%S')}")
        
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
