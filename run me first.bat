:: This Script will install the requirments for the WvW Log parser
:: It will also install all the requirments for logs.exe
:: It will then move all the required files to C:/wvw_dps_report 
:: this ensures that there are no path issues with the script or sub script / processes
:: If your installation of ARC DPS does not save logs to the default location you will
:: need to revert to the default location

@echo off
:: Install packages listed in requirements.txt

Echo Installing parser requirements 
pip install -r requirements.txt

Echo Checking to see if C:\wvw_dps_report exists and deletign if it does
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

:: pausing script for user to read any errors
Pause
