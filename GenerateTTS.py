import re
import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to(device)

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE) # AI 생성 결과물에서 이모지 지우기

def generate_TTS(text:str):
    text=emoji_pattern.sub(r'',text)
    text=text.replace('’','\'').replace('—',' ').replace('%',' percent ')
    tts.tts_to_file(text=text, file_path="output.wav")