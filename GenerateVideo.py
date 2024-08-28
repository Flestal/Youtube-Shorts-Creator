import re
import os
import time
from moviepy.editor import *
from PIL import Image, ImageDraw,ImageFont
import moviepy.editor

from GenerateContent import generate_script
from GenerateTTS import generate_TTS

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

bg_img_path = "./background.png"
bg_music_path = "./background_music.mp3"


title, text = generate_script()
title = emoji_pattern.sub(r'',title)
title = title.replace("Title: ",'').replace('*','').replace('\"','').replace('#','').replace(': ',':\n')
print("Title: ",title)
print("Text: ",text)
generate_TTS(text)

tts_audio_path = "./output.wav"
output_video_path = "./"+title+".mp4"

bg_image = Image.open(bg_img_path)
draw = ImageDraw.Draw(bg_image)
font = ImageFont.truetype("Jersey10-Regular.ttf", 60)  # 글꼴과 크기 설정 (컴퓨터에 설치된 적절한 .ttf 파일 필요)
image_width, image_height = bg_image.size
position = ((image_width) / 2, (image_height) / 4)  # 이미지 상단 중앙에 제목 배치

draw.text((position[0]-1,position[1]-1), title, (0, 0, 0), font=font, anchor='mm')
draw.text((position[0]-1,position[1]+1), title, (0, 0, 0), font=font, anchor='mm')
draw.text((position[0]+1,position[1]+1), title, (0, 0, 0), font=font, anchor='mm')
draw.text((position[0]+1,position[1]-1), title, (0, 0, 0), font=font, anchor='mm')

draw.text(position, title, (255, 255, 255), font=font, anchor='mm')

bg_image.save("modified_background.png")

background_clip = ImageClip("modified_background.png").set_duration(AudioFileClip(tts_audio_path).duration)

# TTS 오디오와 배경 음악을 결합
tts_audio = AudioFileClip(tts_audio_path)
background_music = AudioFileClip(bg_music_path).volumex(0.25)  # 배경 음악 볼륨 줄이기

# TTS 길이에 맞춰 배경 음악 길이 조정하기
if background_music.duration > tts_audio.duration:
    # 배경 음악이 TTS 오디오보다 길면 자르기
    background_music = background_music.subclip(0, tts_audio.duration)
else:
    # 배경 음악이 TTS 오디오보다 짧으면 반복
    background_music = background_music.fx(vfx.loop, duration=tts_audio.duration)

# TTS 오디오와 조정된 배경 음악을 결합
combined_audio = CompositeAudioClip([tts_audio, background_music])

# 오디오와 비디오 결합
final_video = background_clip.set_audio(combined_audio)

# 영상 파일로 내보내기
final_video.write_videofile(output_video_path, codec='libx264', fps=24)
