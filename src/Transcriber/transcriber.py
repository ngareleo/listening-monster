import speech_recognition as sr
from src.Tools.audio_splitter import AudioSplitter
from src.Tools import Logger, AudioSegment

MAX_WORKERS = 5
BLANK = ""


class Transcriber:
    def __init__(self):
        self.r = sr.Recognizer()

    @Logger.log
    def transcribe(self, splitter: AudioSplitter, *args):
        chunks: list[AudioSegment] = splitter.load_chunks()
        res = err = BLANK
        if not chunks:
            Logger.warn("No chunks found")
            return

        for i, audio_chunk in enumerate(chunks):
            audio_chunk.export(
                "temp", format="wav"
            )  # this could be causing a performance bottleneck if its writting to ROM instead of RAM
            with sr.AudioFile("temp") as source:
                audio = self.r.listen(source)
                try:
                    google_txt = self.r.recognize_google(audio)
                    res.join([f" [{i}]{google_txt}"])
                except Exception as ex:
                    res.join([f"<<[e{i}]>>"])
                    err.join([f"{ex}\n"])

        Logger.info(res)
        Logger.warn(err)
