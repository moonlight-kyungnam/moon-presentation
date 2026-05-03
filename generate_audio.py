import os
import re
import asyncio
import edge_tts

# 음성 설정 (Microsoft Edge TTS 한국어 고품질 음성)
# 남성: InJoon (신뢰감 있고 전문적인 톤)
# 여성: SunHi (차분하고 또렷한 아나운서 톤)
VOICE_MALE = "ko-KR-InJoonNeural"
VOICE_FEMALE = "ko-KR-SunHiNeural"

# 남성과 여성 목소리의 피치(Pitch)나 속도(Rate)를 미세 조정하려면 아래 파라미터를 활용할 수 있습니다.
# 여기서는 기본값을 사용합니다. (예: RATE="+0%", PITCH="+0Hz")

INPUT_FILE = "script_full_podcast.txt"
OUTPUT_DIR = "audio"

async def generate_audio_for_slide(slide_num, lines):
    temp_files = []
    
    for i, (speaker, text) in enumerate(lines):
        voice = VOICE_MALE if speaker == 'M' else VOICE_FEMALE
        
        # 텍스트가 비어있으면 건너뜀
        if not text:
            continue
            
        print(f"[Slide {slide_num}] {'남성' if speaker == 'M' else '여성'} 음성 생성 중... ({i+1}/{len(lines)})")
        
        # edge-tts를 사용하여 음성 생성
        communicate = edge_tts.Communicate(text, voice)
        temp_file = os.path.join(OUTPUT_DIR, f"temp_{slide_num}_{i}.mp3")
        await communicate.save(temp_file)
        temp_files.append(temp_file)
    
    if not temp_files:
        return

    # 임시 파일들을 하나로 병합 (MP3 바이너리 이어붙이기)
    output_file = os.path.join(OUTPUT_DIR, f"slide_{slide_num}.mp3")
    with open(output_file, "wb") as f_out:
        for temp_file in temp_files:
            with open(temp_file, "rb") as f_in:
                f_out.write(f_in.read())
            # 임시 파일 삭제
            os.remove(temp_file)
            
    print(f"완성: {output_file}\n")

async def main():
    print("팟캐스트 오디오 생성을 시작합니다...")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"오류: {INPUT_FILE} 파일을 찾을 수 없습니다.")
        return
        
    # 슬라이드별 텍스트 파싱
    # [Slide 숫자 : 제목] 패턴을 기준으로 텍스트 분리
    slide_blocks = re.split(r'\[Slide \d+ :.*?\]', content)
    slide_headers = re.findall(r'\[Slide (\d+) :.*?\]', content)
    
    # 첫 번째 블록은 슬라이드 시작 전의 공백이므로 제거
    slide_blocks = slide_blocks[1:]
    
    for slide_num, slide_text in zip(slide_headers, slide_blocks):
        lines = []
        for line in slide_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('👨남성'):
                text = line.split(':', 1)[1].strip()
                lines.append(('M', text))
            elif line.startswith('👩여성'):
                text = line.split(':', 1)[1].strip()
                lines.append(('F', text))
            else:
                # 발화자 표시가 없는 일반 텍스트는 이전 발화자의 대사에 이어붙임
                if lines:
                    lines[-1] = (lines[-1][0], lines[-1][1] + " " + line)
                    
        if lines:
            await generate_audio_for_slide(slide_num, lines)
            
    print("모든 오디오 파일 생성이 완료되었습니다!")

if __name__ == "__main__":
    asyncio.run(main())
