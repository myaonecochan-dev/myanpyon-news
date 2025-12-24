@echo off
cd /d "c:\AI\myanpyonsokumato\backend"
echo ---------------------------------------------------------------- >> bot_log.txt
echo [%DATE% %TIME%] Starting MyanPyon Bot... >> bot_log.txt
python collector.py >> bot_log.txt 2>&1
echo [%DATE% %TIME%] Finished. >> bot_log.txt
echo ---------------------------------------------------------------- >> bot_log.txt
