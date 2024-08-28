import re 

def get_youtube_video_id(url: str) -> str | bool:
    regexp = re.compile(r'(?:youtube(?:-nocookie)?\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/\s]{11})', re.IGNORECASE)
    matches = regexp.search(url)
    
    return matches.group(1) if matches else False