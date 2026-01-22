# 🎬 Video Downloader
<img width="749" height="710" alt="스크린샷 2026-01-22 135851" src="https://github.com/user-attachments/assets/9136598d-560a-440c-a329-3bc5b51de3cc" />


> URL을 입력하면 동영상을 다운받을 수 있는 GUI 기반 프로그램

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](#)

## ✨ 주요 기능

### 🎯 핵심 기능
- ✅ **간편한 URL 입력**: 다운로드할 동영상 URL 입력
- ✅ **1000개 이상 사이트 지원**: YouTube, Vimeo, Instagram, TikTok 등
- ✅ **품질 선택**: best, 720p, 480p, 360p, audio (MP3)
- ✅ **저장 경로 설정**: 원하는 폴더 선택

### 📊 진행 상황 표시
- ✅ **실시간 진행률**: 0% → 5.2% → ... → 100%
- ✅ **동적 진행바**: 시각적 진행 상황 표시
- ✅ **백분율 표시**: 진행바 옆에 정확한 % 표시
- ✅ **상세 로그**: 다운로드 상태를 실시간으로 확인

### 🎮 다운로드 제어
- ✅ **⏸ 일시 중지**: 다운로드 일시 중단
- ✅ **▶ 재개**: 일시 중지된 다운로드 계속 진행
- ✅ **✕ 취소**: 다운로드 강제 중단

### 🎨 사용자 인터페이스
- ✅ **직관적 GUI**: tkinter 기반 깔끔한 인터페이스
- ✅ **아이콘 적용**: 프로그램 윈도우에 아이콘 표시
- ✅ **반응형 UI**: 백그라운드 스레드로 UI 반응성 유지

### 📦 배포 형식
- ✅ **독립 실행형 EXE**: Python 설치 없이 직접 실행
- ✅ **단일 파일**: 11MB 크기의 모든 것이 포함된 EXE

---

## 🚀 빠른 시작

### 방법 1: EXE 파일로 즉시 실행 (권장)

```bash
# dist 폴더의 VideoDownloader.exe 더블클릭
dist\VideoDownloader.exe
```

### 방법 2: 배치 파일로 실행

```bash
# 자동으로 필요한 패키지 설치 후 실행
run.bat
```

### 방법 3: Python 스크립트로 실행

```bash
python downloader.py
```

---

## 📖 사용 방법

### 1단계: URL 입력
```
URL 필드에 다운로드할 동영상 URL 입력
예: https://www.youtube.com/watch?v=...
```

### 2단계: 저장 경로 설정
```
[찾아보기] 버튼으로 저장 폴더 선택
(기본값: 사용자 다운로드 폴더)
```

### 3단계: 품질 선택
```
- best    : 최고 품질 (기본값)
- 720p    : HD 품질
- 480p    : 중간 품질 (빠른 다운로드)
- 360p    : 저 품질 (최소 용량)
- audio   : MP3로 음성만 추출
```

### 4단계: 다운로드 시작
```
[다운로드 시작] 버튼 클릭
→ 진행률이 실시간으로 표시됨
→ 필요시 [⏸ 일시 중지] 또는 [✕ 취소] 가능
```

---

## 🔧 설치 및 설정

### 시스템 요구사항

**최종 사용자 (EXE 실행)**
- Windows 10 이상
- 약 11MB 디스크 공간
- 인터넷 연결

**개발자 (소스 코드)**
- Python 3.7 이상
- tkinter (Python 기본 포함)
- yt-dlp (자동 설치)
- PyInstaller (빌드용)

### 의존성 설치

```bash
# 필수 패키지 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install yt-dlp>=2024.1.1
pip install Pillow>=10.0.0
pip install pyinstaller>=6.0.0
```

### 아이콘 생성 (선택사항)

```bash
python create_icon.py
```

---

## 🏗️ 프로젝트 구조

```
Downloader/
├── dist/
│   └── VideoDownloader.exe          # ⭐ 최종 실행 파일 (11MB)
├── 
├── downloader.py                    # 메인 GUI 프로그램
├── create_icon.py                   # 아이콘 생성 스크립트
├── build_exe.py                     # EXE 빌드 스크립트
├── 
├── icon.ico                         # 프로그램 아이콘
├── icon.png                         # PNG 아이콘
├── 
├── requirements.txt                 # Python 의존성
├── run.bat                          # 프로그램 실행 배치
├── build_exe.bat                    # EXE 빌드 배치
├── 
├── README.md                        # 이 파일
├── setup_guide.md                   # 설정 상세 가이드
├── 사용설명서.md                    # 한글 사용 설명서
├── 업데이트_가이드.md               # 신기능 설명
└── 최종_완성_보고서.md              # 프로젝트 완성 현황
```

---

## 🛠️ 빌드 방법

### Python 스크립트로 빌드

```bash
python build_exe.py
```

### 배치 파일로 빌드

```bash
build_exe.bat
```

### PyInstaller로 직접 빌드

```bash
pyinstaller --onefile --windowed --name VideoDownloader --icon=icon.ico downloader.py
```

빌드 완료 후: `dist/VideoDownloader.exe` 생성

---

## 💡 사용 예제

### YouTube 동영상 다운로드

```
1. URL: https://www.youtube.com/watch?v=ABC123
2. 품질: best
3. 저장 경로: C:\Users\YourName\Downloads
4. [다운로드 시작] 클릭
```

### 유튜브 음악 추출

```
1. URL: YouTube 음악 영상 URL
2. 품질: audio
3. [다운로드 시작] 클릭
→ 자동으로 MP3 파일 생성
```

### 일시 중지 후 재개

```
1. 다운로드 중 [⏸ 일시 중지] 클릭
2. 잠시 후 [▶ 재개] 클릭
→ 다운로드 계속 진행
```

### 다운로드 취소

```
[✕ 취소] 클릭
→ 다운로드 중단 및 상태 초기화
```

---

## ⚙️ 고급 설정

### 품질별 다운로드 크기 비교

| 품질 | 설명 | 예상 크기 | 소요 시간 |
|------|------|----------|---------|
| best | 최고 품질 (4K/1080p) | 1000-2000MB | 5-10분 |
| 720p | HD 품질 | 500-800MB | 3-5분 |
| 480p | 중간 품질 | 300-500MB | 2-3분 |
| 360p | 저 품질 | 150-300MB | 1-2분 |
| audio | MP3 음성만 | 5-20MB | 30초-1분 |

### 지원 사이트

yt-dlp는 1000개 이상의 웹사이트를 지원합니다:

- **동영상**: YouTube, Vimeo, Dailymotion, Facebook
- **소셜**: Instagram, TikTok, Twitter, Twitch
- **방송**: Dailymotion, Niconico, 텔레그램
- **그 외**: Spotify, SoundCloud, Bandcamp 등

더 많은 사이트 확인: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

---

## 🔧 문제 해결

### "yt-dlp를 찾을 수 없습니다" 오류

```bash
# yt-dlp 설치
pip install yt-dlp --upgrade

# 또는 업데이트
yt-dlp -U
```

### EXE 파일이 실행되지 않음

1. Windows Defender 또는 방화벽 확인
2. 관리자 권한으로 실행
3. 다시 빌드:
   ```bash
   python build_exe.py
   ```

### 다운로드가 느림

- 품질을 낮게 설정 (360p, 480p)
- 인터넷 연결 확인
- 다른 애플리케이션 종료
- 와이파이 신호 확인

### 특정 사이트에서 다운로드 실패

```bash
# yt-dlp 최신 버전으로 업데이트
pip install yt-dlp --upgrade
yt-dlp -U
```

### 진행률이 표시되지 않음

- URL이 올바른지 확인
- 사이트가 yt-dlp로 지원되는지 확인
- 콘솔 창에서 에러 메시지 확인

---

## 📊 기술 스택

| 항목 | 기술 |
|------|------|
| **언어** | Python 3.13 |
| **GUI** | tkinter |
| **다운로드** | yt-dlp (YouTube-DL 개선판) |
| **패키징** | PyInstaller |
| **아이콘** | PIL/Pillow |
| **스레드** | threading |
| **정규식** | re (진행률 파싱) |

---

## 📈 업데이트 이력

### v1.1 (2026-01-22)
- ✅ 진행바 백분율 실시간 표시
- ✅ 일시 중지/재개/취소 버튼 추가
- ✅ 콘솔 자동 표시
- ✅ 진행률 파싱 개선
- ✅ 로그 필터링 (NA 제거)

### v1.0 (2026-01-22)
- ✅ 기본 동영상 다운로더 완성
- ✅ GUI 인터페이스
- ✅ 품질 선택 기능
- ✅ EXE 파일 생성

---

## 🤝 기여

이 프로젝트는 개인 프로젝트이며, 자유롭게 사용, 수정, 배포할 수 있습니다.

버그 보고나 기능 제안은 이슈로 등록해 주세요.

---

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

### 관련 링크
- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **Python**: https://www.python.org/
- **tkinter**: https://docs.python.org/3/library/tkinter.html
- **PyInstaller**: https://pyinstaller.readthedocs.io/

---

## 🎉 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트를 사용합니다:
- **yt-dlp**: YouTube 및 다른 사이트에서 동영상 다운로드
- **Python**: 프로그래밍 언어
- **tkinter**: GUI 라이브러리

---

**마지막 업데이트**: 2026년 1월 22일  
**현재 버전**: v1.1  
**상태**: ✅ 완성 및 배포 준비 완료
