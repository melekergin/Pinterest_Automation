@echo off
:: Pinguin Umzüge - Pinterest Automation Runner
:: This script will run your Pinterest bot automatically.

cd /d "c:\Users\Melek\.gemini\antigravity\playground\distant-schrodinger"

:: Run the script
python pinterest_bot.py

:: (Optional) Log the execution
echo [%date% %time%] Pinterest automation ran successfully. >> execution_log.txt
