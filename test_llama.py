import pandas as pd
import requests
import json
url = "http://localhost:11434/api/generate"
prompt = {
    "model": "llama3.1",
    "prompt": "Please provide information that is simple and interesting enough to fit into a one-minute YouTube Shorts video, so that when creating a video with TTS, it would be around one minute in length. give one topic script thhat have only title and paragraph."
}
data=[]

def Run():
    headers = {'Content-Type':'application/json'}
    response = requests.post(url,json=prompt,headers=headers)
    if response.status_code!=200:
        print('Error')
        return
    json_objects = response.content.decode().strip().split('\n')
    data_=[json.loads(obj) for obj in json_objects]
    res_text = ''
    for item in data_:
        # print(item)
        res_text+=item['response']
    # print(res_text)
    data.append(res_text)
    return


if __name__=='__main__':
    for _ in range(50):
        Run()
    df = pd.DataFrame(data)
    df.to_csv('output.csv',index=False,encoding='utf-8')