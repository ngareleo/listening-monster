import os
from pydub import AudioSegment


# TODO: Support most audio formats
def get_audio_file_length_in_secs(loc: str) -> int:
    """Get length of mp3 files in sec"""

    if not os.path.exists(loc):
        raise FileExistsError()

    audio: AudioSegment = AudioSegment.from_mp3(loc)
    return int(audio.duration_seconds)
