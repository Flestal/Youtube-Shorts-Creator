import re
import os
import time
from moviepy.editor import *
from PIL import Image, ImageDraw,ImageFont
import moviepy.editor

from GenerateContent import generate_script
from GenerateTTS import generate_TTS

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
                           "]+", flags=re.UNICODE) # AI 생성 결과물에서 이모지 지우기

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
font = ImageFont.truetype("Jersey10-Regular.ttf", 60)
image_width, image_height = bg_image.size
position = ((image_width) / 2, (image_height) / 4)

draw.text((position[0]-1,position[1]-1), title, (0, 0, 0), font=font, anchor='mm')
draw.text((position[0]-1,position[1]+1), title, (0, 0, 0), font=font, anchor='mm')
draw.text((position[0]+1,position[1]+1), title, (0, 0, 0), font=font, anchor='mm')
draw.text((position[0]+1,position[1]-1), title, (0, 0, 0), font=font, anchor='mm')

draw.text(position, title, (255, 255, 255), font=font, anchor='mm')

bg_image.save("modified_background.png")

background_clip = ImageClip("modified_background.png").set_duration(AudioFileClip(tts_audio_path).duration)

tts_audio = AudioFileClip(tts_audio_path)
background_music = AudioFileClip(bg_music_path).volumex(0.25)

if background_music.duration > tts_audio.duration:
    background_music = background_music.subclip(0, tts_audio.duration)
else:
    background_music = background_music.fx(vfx.loop, duration=tts_audio.duration)

combined_audio = CompositeAudioClip([tts_audio, background_music])

final_video = background_clip.set_audio(combined_audio)

final_video.write_videofile(output_video_path, codec='libx264', fps=24)
