import speech_recognition as sr

from tools.logger import Logger
from .utils import AudioSplitter

MAX_WORKERS = 5
BLANK = ""


class Transcriber:
    def __init__(self):
        self.r = sr.Recognizer()

    def transcribe(self, path: str, *args):
        splitter = AudioSplitter(path)
        chunks = splitter.load_chunks()
        res = err = ""

        for i, audio_chunk in enumerate(chunks):
            audio_chunk.export("temp", format="wav")
            with sr.AudioFile("temp") as source:
                audio = self.r.listen(source)
                try:
                    google_txt = self.r.recognize_google(audio)
                    res.join([f" [{i}]{google_txt}"])
                except Exception as ex:
                    res.join([f"<<[e{i}]>>"])
                    err.join([f"{ex}\n"])

        if res is not BLANK:
            Logger.info(res)

        if err is not BLANK:
            Logger.warn(err)
