import speech_recognition as sr
from .utils import AudioSplitter


class Transcriber:
    def __init__(self):
        self.r = sr.Recognizer()

    def transcribe(self, audio_file_loc: str):
        splitter = AudioSplitter(audio_file_loc)
        chunks = splitter.load_chunks()
        res = ""
        e = ""

        for i, audio_chunk in enumerate(chunks):
            audio_chunk.export("temp", format="wav")
            with sr.AudioFile("temp") as source:
                audio = self.r.listen(source)
                try:
                    text = self.r.recognize_google(audio)
                    res += f" [{i}] {text} "

                except Exception as ex:
                    res += f"<<[e{i}>>"
                    e += f"{ex.with_traceback}\n"

        if res != "":
            print(f"{res}")

        if e != "":
            print(f"[Errors] {e}")
