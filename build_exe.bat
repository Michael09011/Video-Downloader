@echo off
REM EXE 파일 빌드 배치 파일

cd /d "%~dp0"

echo.
echo ========================================
echo Video Downloader EXE 빌드 시작
echo ========================================
echo.

REM Python 버전 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되어 있지 않습니다.
    echo Python 3.7 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 아이콘 생성 (존재하지 않는 경우)
if not exist "icon.ico" (
    echo 아이콘을 생성 중입니다...
    python create_icon.py
    echo.
)

REM PyInstaller 설치 확인
echo PyInstaller를 확인 중입니다...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller를 설치 중입니다...
    pip install pyinstaller
    echo.
)

REM yt-dlp 설치 확인
echo yt-dlp를 확인 중입니다...
pip show yt-dlp >nul 2>&1
if errorlevel 1 (
    echo yt-dlp를 설치 중입니다...
    pip install yt-dlp
    echo.
)

REM EXE 빌드
echo EXE 파일을 빌드 중입니다...
python build_exe.py

if errorlevel 1 (
    echo.
    echo EXE 빌드 실패
    pause
    exit /b 1
)

echo.
echo ========================================
echo 빌드 완료!
echo EXE 파일: dist\VideoDownloader.exe
echo ========================================
echo.
pause
