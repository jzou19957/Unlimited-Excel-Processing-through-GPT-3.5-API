@echo off
setlocal EnableDelayedExpansion

:: The name of your Python script
set "PYTHON_SCRIPT=gpt35.py"

:: Loop indefinitely until all rows are processed
:loop
echo Running the Python script...
python %PYTHON_SCRIPT%

:: Optional: Check condition to exit loop here if necessary
:: For example, check for a flag file or specific output from your Python script

echo Script ended, restarting...
goto loop

:end
echo All rows have been processed. Exiting.
