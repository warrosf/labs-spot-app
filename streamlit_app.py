import streamlit as st

from youtube_transcript_api import (
    TranscriptsDisabled, 
    YouTubeTranscriptApi,
    InvalidVideoId,
    NoTranscriptFound
)

st.title("Check Proxy!")

proxy = st.text_input('Type proxy', value="socks5h://djusbdqr:m3304yzgdib9@45.127.248.127:5128")

video_id = st.text_input('Type URL')

texts = []

if st.button('Check availability'):
    if video_id is None:
        raise InvalidVideoId('Invalid video ID')
        exit()

    for lang in ['en', 'pt', 'es', 'it', 'fr']:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang], proxies={"http": proxy})
            text = '\n'.join([t['text'] for t in transcript])
            result = {'text': text, 'language': lang}
            texts.append(result)
            if transcript:
                break

        except NoTranscriptFound:
            pass
        
        except TranscriptsDisabled as ex:
            raise TranscriptsDisabled('Transcripts are disabled for this video.')
    
    if transcript is None:
        st.write('No transcript found for this video in Portuguese, English, Spanish, Italian or French.')

    st.write(len(texts))
