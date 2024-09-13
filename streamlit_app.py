import requests
import streamlit as st
import yt_dlp
import glob

import json
import requests

#your api key
apiKey = 'f2fb8d9b414113dcc4f38ec9b0ea2d74c757ca30198a58e5ced14e39afc9f4308fb03e5a6e975813f3d792ab551ebc20e36e4f5d2319e3f7737971bbfe1afaf9'

from src.app.utils.yt import get_youtube_video_id

def check_status(d):
    if d['status'] == 'finished':
      filename = d['filename']
      print("The audio: "+filename+' download is done!')

def downloading_audio(video_url, filename, download=True):
    ydl_opts = {
          'format': 'bestaudio/best',
          'outtmpl': filename,
          'noplaylist': True,
          'quiet': True,
          'no_warnings': True,
          'postprocessors': [{
              'key': 'FFmpegExtractAudio',
              'preferredcodec': 'mp3',
              'preferredquality': '192',
          }],
          'progress_hooks': [check_status]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
         return ydl.extract_info(video_url, download=download)
    
def get_transcript(filepath):
    #language spoken in the audio file
    language = 'en-US'

    params = {
    "language" : language,
    "file_name" : filepath.split("/")[-1]
    }

    headers = {
    "Authorization" : f"Bearer {apiKey}",
    }

    url = 'https://api.tor.app/features/transcribe-file'

    #first request to get the presigned url through which we will upload our audio file
    resp = requests.get(url, params=params, headers=headers)

    if resp.status_code != 200:
        raise Exception(resp.text)
    
    decoded_resp = json.loads(resp.content)
    url = decoded_resp['url']
    given_order_id = decoded_resp["fields"]["key"].split("-+-")[0]

    #attach the audio file
    files = {'file': open(filepath, 'rb')}

    #upload the audio file and initiate the transcription
    r = requests.post(url, data= decoded_resp['fields'], files=files)

    print(r.status_code)
    print(given_order_id)
    return given_order_id

def get_content(given_order_id):
    #order id to get content
    parameters = {
        "orderid" : given_order_id
    }

    url = "https://api.transkriptor.com/3/Get-Content"

    #if the order is still in processing phase, send the following request again.
    response = requests.get(url, params = parameters)

    content = json.loads(response.content)

    if "content" in content:
        return content 
    else:
        raise Exception("Still processing the order. Send the last request later again.", given_order_id)

def use_whisper():
    st.title("Transcribe YouTube Videos!")

    video_url = st.text_input('Type URL')

    video_id = get_youtube_video_id(video_url)
    print(video_id)

    if st.button('Transcribe'):
        
        downloading_audio(video_url, '%(title)s')

        files =  glob.glob('*.mp3')
        print("File(s) found: {}".format(len(files)))
        for file in files:
            filename = f'{file[:-4]}.mp3'

        st.text_input(label="File",value=filename)

        try:
            given_order_id = get_transcript(filename) 
            st.session_state['given_order_id'] = given_order_id
            st.text_input(label="Given Order ID",value=st.session_state.given_order_id)
        except Exception as e:
            st.error(e)

    if st.button('Given transcription'):
        try:
            content = get_content(st.session_state.given_order_id)
            st.text_area(label="Content",value=content['content'])
        except Exception as e:
            st.error(e)


pg = st.navigation([st.Page(use_whisper)])
pg.run()


