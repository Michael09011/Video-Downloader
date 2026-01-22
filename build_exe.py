import os
import subprocess
import sys

def build_exe():
    """PyInstaller를 사용하여 EXE 파일 생성"""
    
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    
    # PyInstaller 명령어
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "VideoDownloader",
        "--distpath", "./dist",
        "--workpath", "./build",
        "--specpath", "./",
        f"--icon={icon_path}",
        "--add-data", f"{icon_path}:.",
        "downloader.py"
    ]
    
    print("EXE 파일을 빌드 중입니다...")
    print(f"명령어: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    
    if result.returncode == 0:
        print("-" * 50)
        print("✓ EXE 파일 생성 완료!")
        print(f"위치: {os.path.join(os.path.dirname(__file__), 'dist', 'VideoDownloader.exe')}")
    else:
        print("✗ 빌드 실패")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
