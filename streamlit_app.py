import streamlit as st

from youtube_transcript_api import (
    TranscriptsDisabled, 
    YouTubeTranscriptApi,
    InvalidVideoId,
    NoTranscriptFound
)

st.title("Check Proxy!")

proxy = st.text_input('Type proxy')
video_id = st.text_input('Type URL')

texts = []

if st.button('Check availability'):
    try:
        if video_id is None:
            st.write('Invalid URL')
            exit()

        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": proxy})
        for lang in ['en', 'pt', 'es', 'it', 'fr']:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": proxy})
            text = '\n'.join([t['text'] for t in transcript])
            result = {'text': text, 'language': lang}
            texts.append(result)
    except:
        pass

    if transcript is None:
        st.write('No transcript found for this video in Portuguese, English, Spanish, Italian or French.')

    st.write(len(texts))
