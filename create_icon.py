"""
아이콘 파일 생성 스크립트
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """동영상 다운로더 아이콘 생성"""
    
    # 아이콘 크기
    size = (256, 256)
    
    # 배경 생성
    img = Image.new('RGBA', size, (0, 120, 200, 255))  # 파란색 배경
    draw = ImageDraw.Draw(img)
    
    # 다운로드 화살표 그리기 (간단한 기하학 도형)
    # 화살표 테일
    arrow_x = size[0] // 2 - 20
    arrow_y = size[1] // 2 - 60
    
    # 화살표 바디 (직사각형)
    draw.rectangle(
        [(arrow_x + 15, arrow_y), (arrow_x + 25, arrow_y + 70)],
        fill=(255, 255, 255, 255)
    )
    
    # 화살표 헤드 (삼각형)
    points = [
        (arrow_x, arrow_y + 70),      # 왼쪽
        (arrow_x + 40, arrow_y + 70), # 오른쪽
        (arrow_x + 20, arrow_y + 100) # 아래
    ]
    draw.polygon(points, fill=(255, 255, 255, 255))
    
    # 동영상 플레이 버튼 심볼 추가
    play_x = size[0] // 2
    play_y = size[1] // 2 + 40
    
    # 플레이 버튼 삼각형
    play_points = [
        (play_x - 20, play_y - 20),
        (play_x - 20, play_y + 20),
        (play_x + 20, play_y)
    ]
    draw.polygon(play_points, fill=(255, 200, 0, 255))  # 노란색
    
    # ICO 파일로 저장
    ico_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    img.save(ico_path, format='ICO', sizes=[size])
    print(f"✓ 아이콘 생성 완료: {ico_path}")
    
    # PNG 버전도 생성
    png_path = os.path.join(os.path.dirname(__file__), "icon.png")
    img.save(png_path)
    print(f"✓ PNG 이미지 생성 완료: {png_path}")

if __name__ == "__main__":
    try:
        create_icon()
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        print("Pillow 설치를 확인해주세요: pip install Pillow")
