@echo off
REM 동영상 다운로더 GUI 실행 배치 파일

cd /d "%~dp0"

REM Python 버전 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되어 있지 않습니다.
    echo Python 3.7 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 필수 패키지 확인 및 설치
echo 필수 패키지를 확인 중입니다...
pip show yt-dlp >nul 2>&1
if errorlevel 1 (
    echo yt-dlp를 설치 중입니다...
    pip install yt-dlp
)

REM 아이콘 생성 (존재하지 않는 경우)
if not exist "icon.ico" (
    echo 아이콘을 생성 중입니다...
    python create_icon.py
)

REM 프로그램 실행
echo 프로그램을 시작 중입니다...
python downloader.py

pause
