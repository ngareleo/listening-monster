import os
from pydub import AudioSegment


# TODO: Support most audio formats
def get_audio_file_length_in_ms(loc: str) -> int:
    """Get length of mp3 files"""

    if not os.path.exists(loc):
        raise ValueError("File doesn't exist")

    audio = AudioSegment.from_mp3(str)
    return len(audio)
