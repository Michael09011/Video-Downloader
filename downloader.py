import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import subprocess
import sys
import re
import signal
from pathlib import Path

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("750x680")
        self.root.resizable(True, True)
        
        # 아이콘 설정
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass
        
        # 현재 디렉토리에서 쿠키 파일 경로 설정 (Tver 등 인증이 필요한 사이트용)
        self.cookies_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
        
        # 스타일 설정
        self.root.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.theme_use('clam')
        
        # 다운로드 프로세스 관련 변수
        self.download_process = None
        self.is_paused = False
        
        # 메인 프레임
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # 제목
        title_label = ttk.Label(main_frame, text="🎬 Video Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky=tk.W)
        
        # URL 입력 영역
        url_label = ttk.Label(main_frame, text="URL:", font=("Arial", 10))
        url_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.url_entry = ttk.Entry(main_frame, width=70, font=("Arial", 10))
        self.url_entry.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=(50, 0))
        
        # 저장 경로 설정
        path_label = ttk.Label(main_frame, text="저장 경로:", font=("Arial", 10))
        path_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.path_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=50, font=("Arial", 10))
        path_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(80, 0))
        
        browse_btn = ttk.Button(main_frame, text="찾아보기", command=self.browse_folder)
        browse_btn.grid(row=2, column=2, padx=5)
        
        # 다운로드 품질 선택
        quality_label = ttk.Label(main_frame, text="품질:", font=("Arial", 10))
        quality_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                     values=["best", "720p", "480p", "360p", "audio"], 
                                     state="readonly", width=20)
        quality_combo.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(60, 0))
        
        # 다운로드 버튼
        download_btn = ttk.Button(main_frame, text="다운로드 시작", command=self.start_download)
        download_btn.grid(row=3, column=2, padx=5)
        
        # 제어 버튼 프레임
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.pause_btn = ttk.Button(control_frame, text="⏸ 일시 중지", command=self.pause_download, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.resume_btn = ttk.Button(control_frame, text="▶ 재개", command=self.resume_download, state=tk.DISABLED)
        self.resume_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(control_frame, text="✕ 취소", command=self.cancel_download, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # 로그 출력 영역
        log_label = ttk.Label(main_frame, text="로그:", font=("Arial", 10, "bold"))
        log_label.grid(row=5, column=0, sticky=tk.W, pady=(15, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, 
                                                  font=("Courier", 9), bg="white", fg="black")
        self.log_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        # 상태 바
        self.status_var = tk.StringVar(value="준비 완료")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, font=("Arial", 9))
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 진행률
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.progress_label = ttk.Label(progress_frame, text="0%", font=("Arial", 10, "bold"), width=5)
        self.progress_label.pack(side=tk.LEFT)
        
        self.is_downloading = False
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory(title="저장 폴더 선택")
        if folder_path:
            self.path_var.set(folder_path)
    
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def start_download(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("오류", "URL을 입력해주세요.")
            return
        
        if not url.startswith(("http://", "https://")):
            messagebox.showerror("오류", "유효한 URL을 입력해주세요. (http:// 또는 https://로 시작)")
            return
        
        if self.download_process is not None and self.download_process.poll() is None:
            messagebox.showwarning("경고", "이미 다운로드 중입니다.")
            return
        
        self.is_paused = False
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 버튼 상태 변경
        self.pause_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL)
        self.resume_btn.config(state=tk.DISABLED)
        
        # 스레드에서 다운로드 실행
        download_thread = threading.Thread(target=self.download_video, args=(url,), daemon=True)
        download_thread.start()
    
    def pause_download(self):
        if self.download_process and self.download_process.poll() is None:
            try:
                # Windows에서 프로세스 일시 중지
                import subprocess as sp
                sp.run(f"pause {self.download_process.pid}", shell=True, capture_output=True)
                self.is_paused = True
                self.pause_btn.config(state=tk.DISABLED)
                self.resume_btn.config(state=tk.NORMAL)
                self.status_var.set("일시 중지됨")
                self.log("⏸ 다운로드가 일시 중지되었습니다.")
            except:
                self.log("일시 중지 실패")
    
    def resume_download(self):
        if self.download_process and self.download_process.poll() is None:
            try:
                # Windows에서 프로세스 재개
                import subprocess as sp
                sp.run(f"pres {self.download_process.pid}", shell=True, capture_output=True)
                self.is_paused = False
                self.pause_btn.config(state=tk.NORMAL)
                self.resume_btn.config(state=tk.DISABLED)
                self.status_var.set("다운로드 중...")
                self.log("▶ 다운로드가 재개되었습니다.")
            except:
                self.log("재개 실패")
    
    def cancel_download(self):
        if self.download_process and self.download_process.poll() is None:
            try:
                # 프로세스 강제 종료
                self.download_process.terminate()
                # 2초 대기 후에도 종료되지 않으면 kill
                try:
                    self.download_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.download_process.kill()
                    self.download_process.wait()
                
                self.log("-" * 50)
                self.log("✕ 다운로드가 취소되었습니다.")
                self.status_var.set("취소됨")
                self.progress_var.set(0)
                self.progress_label.config(text="0%")
                
                # 버튼 상태 초기화
                self.pause_btn.config(state=tk.DISABLED)
                self.resume_btn.config(state=tk.DISABLED)
                self.cancel_btn.config(state=tk.DISABLED)
            except Exception as e:
                self.log(f"취소 중 오류: {str(e)}")
    
    def download_video(self, url):
        try:
            self.status_var.set("다운로드 중...")
            self.log(f"URL: {url}")
            self.log(f"저장 경로: {self.path_var.get()}")
            self.log(f"품질: {self.quality_var.get()}")
            self.log("-" * 50)
            
            download_path = self.path_var.get()
            os.makedirs(download_path, exist_ok=True)
            
            quality_map = {
                "best": "bestvideo+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]/best",
                "audio": "bestaudio/best"
            }
            
            format_str = quality_map.get(self.quality_var.get(), "best")
            
            # yt-dlp 명령어 구성
            cmd = [
                "yt-dlp",
                "-f", format_str,
                "-o", os.path.join(download_path, "%(title)s.%(ext)s"),
                "--progress-template", "[download] %(progress)s",
                "--no-warnings",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            ]
            
            # Tver 및 기타 인증이 필요한 사이트용 쿠키 파일 추가
            if os.path.exists(self.cookies_file):
                cmd.extend(["--cookies", self.cookies_file])
            
            # URL 추가
            cmd.append(url)
            
            self.log(f"명령어: yt-dlp -f {format_str} [옵션] {url[:50]}...")
            self.log("다운로드를 시작합니다...\n")
            
            # 프로세스 실행 (콘솔도 표시)
            startupinfo = None
            if sys.platform == 'win32':
                # Windows에서 콘솔 창 표시
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            self.download_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
                startupinfo=startupinfo
            )
            
            # 진행률 추출 패턴 (개선된 정규식)
            # [download] 5.5% 또는 [download] 5% 또는 [download] 0% of 100MiB 모두 매칭
            progress_pattern = re.compile(r'(\d+\.?\d*)%')
            
            for line in self.download_process.stdout:
                if self.download_process is None:
                    break
                    
                line_stripped = line.rstrip()
                
                # [download] 라인에서만 진행률 추출
                if "[download]" in line_stripped and "%" in line_stripped:
                    match = progress_pattern.search(line_stripped)
                    if match:
                        try:
                            progress = float(match.group(1))
                            progress = min(progress, 99)
                            self.progress_var.set(progress)
                            self.progress_label.config(text=f"{progress:.1f}%")
                            self.root.update()
                        except:
                            pass
                    # [download]로 시작하는 진행 상황 라인은 로그에 간단히 표시
                    if "%" in line_stripped:
                        # 진행률 라인만 짧게 표시
                        try:
                            percent_match = progress_pattern.search(line_stripped)
                            if percent_match:
                                pct = percent_match.group(1)
                                self.log(f"다운로드 진행 중: {pct}%")
                        except:
                            pass
                else:
                    # [download]이 없는 다른 정보들만 로그에 표시
                    if line_stripped and not "[download]" in line_stripped:
                        self.log(line_stripped)
            
            return_code = self.download_process.wait()
            self.download_process = None
            
            # 표준 오류 출력
            for line in self.download_process.stderr if self.download_process else []:
                self.log(f"[오류] {line.rstrip()}")
            
            if return_code == 0:
                self.log("-" * 50)
                self.log("✓ 다운로드 완료!")
                self.status_var.set("다운로드 완료")
                self.progress_var.set(100)
                self.progress_label.config(text="100%")
                messagebox.showinfo("성공", "동영상 다운로드가 완료되었습니다.")
            else:
                self.log("-" * 50)
                self.log("✗ 다운로드 실패!")
                self.status_var.set("다운로드 실패")
        
        except FileNotFoundError:
            self.log("✗ yt-dlp를 찾을 수 없습니다.")
            self.log("설치하려면 명령 프롬프트에서 다음을 실행하세요:")
            self.log("pip install yt-dlp")
            self.status_var.set("오류: yt-dlp 없음")
            messagebox.showerror("오류", "yt-dlp가 설치되어 있지 않습니다.\n명령 프롬프트에서 다음을 실행하세요:\npip install yt-dlp")
        
        except Exception as e:
            self.log(f"✗ 오류 발생: {str(e)}")
            self.status_var.set("오류 발생")
            messagebox.showerror("오류", f"오류가 발생했습니다:\n{str(e)}")
        
        finally:
            # 버튼 상태 초기화
            self.pause_btn.config(state=tk.DISABLED)
            self.resume_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.DISABLED)
            if self.status_var.get() not in ["다운로드 완료", "취소됨"]:
                self.status_var.set("준비 완료")

def main():
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
