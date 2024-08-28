import requests
import streamlit as st

from src.app.utils.yt import get_youtube_video_id

st.title("Check Proxy!")

video_url = st.text_input('Type URL')

video_id = get_youtube_video_id(video_url)
print(video_id)

if st.button('Check availability'):
    # access the API
    url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
    headers = {
        'x-rapidapi-host': "youtube-media-downloader.p.rapidapi.com",
        'x-rapidapi-key': "076266eb35msh8e4d582226372b0p195f86jsn3007f30df660"
    }
    # send a get request to the API 
    qs_video_id = {"videoId": video_id}
    response = requests.request("GET", url, headers=headers, params=qs_video_id)
    # conver the response to json format
    json_response = response.json()
    # obtain the subtitle url (in XML format)
    subtitleURL = json_response['subtitles']['items'][0]['url']

    url_subtitle = "https://youtube-media-downloader.p.rapidapi.com/v2/video/subtitles"
    # send a get subtitle text request to the API 
    qs_subtitle = {"subtitleUrl": subtitleURL}
    response = requests.request("GET", url_subtitle, headers=headers, params=qs_subtitle)
    # return the text response
    txt = response.text
    print(txt)
    
    st.text_area(txt)
