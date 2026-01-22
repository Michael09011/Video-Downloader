@echo off
REM PyQt6 버전 실행

cd /d "%~dp0"

echo.
echo ========================================
echo Video Downloader (PyQt6 Modern UI)
echo ========================================
echo.

REM 필요 패키지 확인 및 설치
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo PyQt6를 설치 중입니다...
    pip install PyQt6 -q
)

python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo yt-dlp를 설치 중입니다...
    pip install yt-dlp -q
)

REM PyQt6 버전 실행
python downloader_qt.py

pause
