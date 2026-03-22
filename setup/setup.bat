@echo off
REM ThreatLens - Windows Setup Script

echo ================================================
echo   ThreatLens - Quick Setup (Windows)
echo   See threats before they see you
echo ================================================
echo.

REM Check for Java
echo Checking prerequisites...
echo.

java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Java not found
    echo     Download from: https://www.java.com/download/
    pause
    exit /b 1
) else (
    echo [✓] Java is installed
)

echo.
echo ================================================
echo   Step 1: Download Jython Standalone
echo ================================================
echo.

set JYTHON_VERSION=2.7.3
set JYTHON_JAR=jython-standalone-%JYTHON_VERSION%.jar
set JYTHON_URL=https://repo1.maven.org/maven2/org/python/jython-standalone/%JYTHON_VERSION%/%JYTHON_JAR%

if exist "%JYTHON_JAR%" (
    echo [✓] Jython already downloaded: %JYTHON_JAR%
) else (
    echo Downloading Jython %JYTHON_VERSION%...
    echo.
    
    REM Try with PowerShell
    powershell -Command "& {Invoke-WebRequest -Uri '%JYTHON_URL%' -OutFile '%JYTHON_JAR%'}" 2>nul
    
    if exist "%JYTHON_JAR%" (
        echo [✓] Downloaded: %JYTHON_JAR%
    ) else (
        echo [X] Download failed
        echo     Please download manually from:
        echo     %JYTHON_URL%
        pause
        exit /b 1
    )
)

set JYTHON_PATH=%CD%\%JYTHON_JAR%
echo.
echo Jython JAR location: %JYTHON_PATH%

echo.
echo ================================================
echo   Step 2: Verify Extension File
echo ================================================
echo.

if exist "ai_recon_assistant.py" (
    echo [✓] Extension file found: ai_recon_assistant.py
    set EXTENSION_PATH=%CD%\ai_recon_assistant.py
) else (
    echo [X] Extension file not found: ai_recon_assistant.py
    echo     Please ensure the file is in the current directory
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Step 3: Configuration Instructions
echo ================================================
echo.

echo Next steps to complete installation:
echo.
echo 1. Open Burp Suite
echo.
echo 2. Configure Jython:
echo    - Extensions -^> Extension Settings
echo    - Location of Jython standalone JAR file:
echo    - Paste this path: %JYTHON_PATH%
echo.
echo 3. Load the extension:
echo    - Extensions -^> Installed -^> Add
echo    - Extension type: Python
echo    - Extension file: %EXTENSION_PATH%
echo    - Click Next
echo.
echo 4. Configure API key:
echo    - Click 'ThreatLens' tab
echo    - Enter your OpenAI API key
echo    - Click 'Save Configuration'
echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo Quick reference:
echo    Jython JAR: %JYTHON_PATH%
echo    Extension: %EXTENSION_PATH%
echo.
echo See README.md for detailed usage instructions
echo.
echo Happy hunting!
echo.

pause
