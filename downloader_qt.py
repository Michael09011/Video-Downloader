import sys
import os
import subprocess
import threading
import re
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QProgressBar,
    QFileDialog, QMessageBox, QTabWidget, QFrame, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject, QSize
from PyQt6.QtGui import QFont, QColor, QIcon


class DownloadThread(QThread):
    progress_update = pyqtSignal(float)
    log_update = pyqtSignal(str)
    status_update = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, url, quality, save_path, cookies_file):
        super().__init__()
        self.url = url
        self.quality = quality
        self.save_path = save_path
        self.cookies_file = cookies_file
        self.is_running = True
    
    def run(self):
        try:
            self.status_update.emit("다운로드 중...")
            self.log_update.emit(f"URL: {self.url}")
            self.log_update.emit(f"저장 경로: {self.save_path}")
            self.log_update.emit(f"품질: {self.quality}")
            self.log_update.emit("-" * 50)
            
            os.makedirs(self.save_path, exist_ok=True)
            
            quality_map = {
                "best": "bestvideo+bestaudio/best",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]/best",
                "audio": "bestaudio/best"
            }
            
            format_str = quality_map.get(self.quality, "best")
            
            cmd = [
                "yt-dlp",
                "-f", format_str,
                "-o", os.path.join(self.save_path, "%(title)s.%(ext)s"),
                "--progress-template", "[download] %(progress)s",
                "--no-warnings",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            ]
            
            if os.path.exists(self.cookies_file):
                cmd.extend(["--cookies", self.cookies_file])
            
            cmd.append(self.url)
            
            self.log_update.emit(f"명령어: yt-dlp -f {format_str} [옵션] {self.url[:50]}...")
            self.log_update.emit("다운로드를 시작합니다...\n")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            progress_pattern = re.compile(r'(\d+\.?\d*)%')
            
            for line in process.stdout:
                if not self.is_running:
                    process.terminate()
                    break
                
                line_stripped = line.rstrip()
                
                if "[download]" in line_stripped and "%" in line_stripped:
                    match = progress_pattern.search(line_stripped)
                    if match:
                        try:
                            progress = float(match.group(1))
                            progress = min(progress, 99)
                            self.progress_update.emit(progress)
                        except:
                            pass
                    if "%" in line_stripped:
                        try:
                            percent_match = progress_pattern.search(line_stripped)
                            if percent_match:
                                pct = percent_match.group(1)
                                self.log_update.emit(f"다운로드 진행 중: {pct}%")
                        except:
                            pass
                else:
                    if line_stripped and not "[download]" in line_stripped:
                        self.log_update.emit(line_stripped)
            
            return_code = process.wait()
            
            if return_code == 0:
                self.log_update.emit("-" * 50)
                self.log_update.emit("✓ 다운로드 완료!")
                self.progress_update.emit(100)
                self.finished.emit(True, "다운로드가 완료되었습니다.")
            else:
                self.log_update.emit("-" * 50)
                self.log_update.emit("✗ 다운로드 실패!")
                self.finished.emit(False, "다운로드 중 오류가 발생했습니다.")
        
        except FileNotFoundError:
            self.log_update.emit("✗ yt-dlp를 찾을 수 없습니다.")
            self.log_update.emit("설치하려면 명령 프롬프트에서 다음을 실행하세요:")
            self.log_update.emit("pip install yt-dlp")
            self.finished.emit(False, "yt-dlp가 설치되어 있지 않습니다.\npip install yt-dlp 를 실행하세요.")
        
        except Exception as e:
            self.log_update.emit(f"✗ 오류 발생: {str(e)}")
            self.finished.emit(False, f"오류가 발생했습니다:\n{str(e)}")


class ModernVideoDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Video Downloader")
        self.setGeometry(100, 100, 900, 750)
        
        # 아이콘 설정
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.setWindowIcon(QIcon(icon_path))
            except:
                pass
        
        self.cookies_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
        self.download_thread = None
        
        # 스타일 설정
        self.set_style()
        
        # UI 설정
        self.setup_ui()
    
    def set_style(self):
        """다크 테마 스타일 설정"""
        style = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        QLineEdit, QComboBox, QSpinBox {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 5px;
            font-size: 10pt;
        }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
            border: 1px solid #0d47a1;
        }
        QPushButton {
            background-color: #0d47a1;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 10pt;
        }
        QPushButton:hover {
            background-color: #1565c0;
        }
        QPushButton:pressed {
            background-color: #0a3d91;
        }
        QPushButton:disabled {
            background-color: #555555;
            color: #aaaaaa;
        }
        QTextEdit {
            background-color: #252525;
            color: #00ff00;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            font-family: 'Courier New';
            font-size: 9pt;
        }
        QProgressBar {
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            background-color: #2d2d2d;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #0d47a1;
            border-radius: 3px;
        }
        QLabel {
            color: #ffffff;
        }
        QTabWidget::pane {
            border: 1px solid #3d3d3d;
        }
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #aaaaaa;
            padding: 8px 20px;
            border: 1px solid #3d3d3d;
        }
        QTabBar::tab:selected {
            background-color: #0d47a1;
            color: #ffffff;
        }
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        """
        self.setStyleSheet(style)
    
    def setup_ui(self):
        """UI 레이아웃 구성"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # 제목
        title_font = QFont("Arial", 16, QFont.Weight.Bold)
        title = QLabel("🎬 Video Downloader")
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # 탭 위젯
        tabs = QTabWidget()
        
        # 다운로드 탭
        download_tab = self.create_download_tab()
        tabs.addTab(download_tab, "📥 다운로드")
        
        # 설정 탭
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "⚙️ 설정")
        
        main_layout.addWidget(tabs)
        
        central_widget.setLayout(main_layout)
    
    def create_download_tab(self):
        """다운로드 탭 생성"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # URL 입력
        url_label = QLabel("🔗 URL 입력:")
        url_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(url_label)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=... 또는 https://tver.jp/...")
        self.url_input.setMinimumHeight(35)
        layout.addWidget(self.url_input)
        
        # 옵션 행
        options_layout = QHBoxLayout()
        options_layout.setSpacing(15)
        
        # 품질 선택
        quality_label = QLabel("품질:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["best", "720p", "480p", "360p", "audio"])
        self.quality_combo.setMinimumWidth(120)
        options_layout.addWidget(quality_label)
        options_layout.addWidget(self.quality_combo)
        
        # 저장 경로
        path_label = QLabel("저장 경로:")
        self.path_input = QLineEdit()
        self.path_input.setText(str(Path.home() / "Downloads"))
        self.path_input.setReadOnly(True)
        options_layout.addWidget(path_label)
        options_layout.addWidget(self.path_input)
        
        # 찾아보기 버튼
        browse_btn = QPushButton("📂 찾아보기")
        browse_btn.setMaximumWidth(120)
        browse_btn.clicked.connect(self.browse_folder)
        options_layout.addWidget(browse_btn)
        
        layout.addLayout(options_layout)
        
        # 제어 버튼
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.download_btn = QPushButton("▶ 다운로드 시작")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.download_btn.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_btn)
        
        self.pause_btn = QPushButton("⏸ 일시 중지")
        self.pause_btn.setMinimumHeight(40)
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.pause_download)
        button_layout.addWidget(self.pause_btn)
        
        self.cancel_btn = QPushButton("✕ 취소")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_download)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        # 진행바
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # 상태 표시
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)
        
        self.status_label = QLabel("준비 완료")
        self.status_label.setFont(QFont("Arial", 9))
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # 로그 출력
        log_label = QLabel("📋 로그:")
        log_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(300)
        layout.addWidget(self.log_text)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """설정 탭 생성"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 정보 섹션
        info_label = QLabel("ℹ️ 정보")
        info_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(info_label)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        info_text.setText("""
Video Downloader v1.2

🎯 주요 기능:
• YouTube, Tver, TikTok 등 1000개 이상 사이트 지원
• 품질 선택 (best, 720p, 480p, 360p, audio)
• 실시간 진행률 표시
• 일시 중지/재개/취소 기능

🔗 지원 사이트:
• YouTube, Vimeo, Instagram, TikTok
• Tver (일본 온라인 서비스)
• Niconico, Dailymotion 등 수백 개 사이트

⚙️ 기술:
• 다운로드: yt-dlp
• GUI: PyQt6
• Python 3.7+

📝 주의사항:
• 저작권 보호 콘텐츠 다운로드는 개인 목적으로만 사용
• Tver는 일본 VPN 환경에서만 접근 가능
• cookies.txt 파일로 로그인 계정 관리 가능
        """)
        layout.addWidget(info_text)
        
        # 빠른 설정
        settings_label = QLabel("🔧 빠른 설정")
        settings_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(settings_label)
        
        # 다운로드 후 폴더 열기
        self.open_folder_check = QCheckBox("다운로드 완료 후 폴더 자동 열기")
        layout.addWidget(self.open_folder_check)
        
        # 동시 다운로드 수
        concurrent_layout = QHBoxLayout()
        concurrent_label = QLabel("동시 다운로드 수:")
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setValue(1)
        self.concurrent_spin.setMinimum(1)
        self.concurrent_spin.setMaximum(5)
        concurrent_layout.addWidget(concurrent_label)
        concurrent_layout.addWidget(self.concurrent_spin)
        concurrent_layout.addStretch()
        layout.addLayout(concurrent_layout)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def browse_folder(self):
        """폴더 선택"""
        try:
            folder = QFileDialog.getExistingDirectory(self, "저장 폴더 선택")
            if folder:
                self.path_input.setText(folder)
        except Exception as e:
            QMessageBox.warning(self, "오류", f"폴더 선택 중 오류: {str(e)}")
    
    def log(self, message):
        """로그 출력"""
        try:
            self.log_text.append(message)
            scrollbar = self.log_text.verticalScrollBar()
            if scrollbar:
                scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            print(f"로그 출력 오류: {e}")
    
    def start_download(self):
        """다운로드 시작"""
        url = self.url_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "경고", "URL을 입력해주세요.")
            return
        
        if not url.startswith(("http://", "https://")):
            QMessageBox.warning(self, "경고", "유효한 URL을 입력해주세요.")
            return
        
        if self.download_thread is not None and self.download_thread.is_running:
            QMessageBox.warning(self, "경고", "이미 다운로드 중입니다.")
            return
        
        # UI 업데이트
        self.download_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        # 다운로드 스레드 시작
        self.download_thread = DownloadThread(
            url,
            self.quality_combo.currentText(),
            self.path_input.text(),
            self.cookies_file
        )
        
        self.download_thread.progress_update.connect(self.update_progress)
        self.download_thread.log_update.connect(self.log)
        self.download_thread.status_update.connect(self.update_status)
        self.download_thread.finished.connect(self.download_finished)
        
        self.download_thread.start()
    
    def update_progress(self, value):
        """진행률 업데이트"""
        self.progress_bar.setValue(int(value))
    
    def update_status(self, status):
        """상태 업데이트"""
        self.status_label.setText(status)
    
    def download_finished(self, success, message):
        """다운로드 완료"""
        try:
            self.download_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)
            
            if success:
                self.progress_bar.setValue(100)
                self.status_label.setText("다운로드 완료")
                QMessageBox.information(self, "완료", message)
                
                if self.open_folder_check.isChecked():
                    try:
                        os.startfile(self.path_input.text())
                    except:
                        pass
            else:
                self.status_label.setText("다운로드 실패")
                QMessageBox.critical(self, "오류", message)
        except Exception as e:
            print(f"다운로드 완료 처리 오류: {e}")
    
    def pause_download(self):
        """다운로드 일시 중지"""
        if self.download_thread:
            self.download_thread.is_running = False
            self.status_label.setText("일시 중지됨")
            self.pause_btn.setEnabled(False)
            self.log("⏸ 다운로드가 일시 중지되었습니다.")
    
    def cancel_download(self):
        """다운로드 취소"""
        if self.download_thread:
            self.download_thread.is_running = False
            self.download_thread.wait()
            self.status_label.setText("취소됨")
            self.progress_bar.setValue(0)
            self.log("-" * 50)
            self.log("✕ 다운로드가 취소되었습니다.")
            self.download_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = ModernVideoDownloader()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
