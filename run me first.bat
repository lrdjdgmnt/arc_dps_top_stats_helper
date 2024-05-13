@echo off
:: This Script will install the requirements for the WvW Log parser
:: It will also install all the requirements for logs.py
:: It will then move all the required files to C:/wvw_dps_report
:: this ensures that there are no path issues with the script or sub script / processes
:: If your installation of ARC DPS does not save logs to the default location you will
:: need to revert to the default location or edit logs.py to reflect your save location

Echo Installing parser requirements
pip install -r requirements.txt

Echo Checking to see if C:\wvw_dps_report exists and deleting if it does
:: Check if C:\wvw_dps_report exists
if exist "C:\wvw_dps_report" (
    echo Folder C:\wvw_dps_report exists. Deleting it...
    rd /s /q "C:\wvw_dps_report"
    if exist "C:\wvw_dps_report" (
        echo Error: Unable to delete C:\wvw_dps_report.
        exit /B
    )
) else (
    echo Folder C:\wvw_dps_report does not exist.
)

:: Move the folder and its contents to C:\wvw_dps_report
Echo Moving script and required parser to C:\wvw_dps_report
move "wvw_dps_report" "C:\wvw_dps_report"
if %errorlevel% EQU 0 (
    echo Folder moved successfully.
) else (
    echo Error: Unable to move folder.
)

:: Ask the user if they want to set the TiddlyHost password
set /p UserInput=Do you want to set the TiddlyHost password? (yes/no): 
if /i "%UserInput%"=="yes" (
    set /p TIDDLYHOST_PASSWORD=Enter your TiddlyHost password: 
    setx TIDDLYHOST_PASSWORD "%TIDDLYHOST_PASSWORD%" /M
    echo TiddlyHost password set successfully.
) else (
    echo Reminder: Without the password set, the script will fail.
)

:: pausing script for user to read any errors
Pause
