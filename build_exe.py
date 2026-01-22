import os
import subprocess
import sys

def build_exe():
    """PyInstaller를 사용하여 EXE 파일 생성 (PyQt6 버전)"""
    
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
        "downloader_qt.py"
    ]
    
    print("EXE 파일을 빌드 중입니다...")
    print(f"명령어: {' '.join(cmd)}")
    print("-" * 50)
    
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    
    if result.returncode == 0:
        print("-" * 50)
        print("[OK] EXE 파일 생성 완료!")
        exe_path = os.path.join(os.path.dirname(__file__), 'dist', 'VideoDownloader.exe')
        print(f"위치: {exe_path}")
    else:
        print("[ERROR] 빌드 실패")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
