from src.Transcriber.transcriber import Transcriber
from src.Tools import Logger, TimebasedAudioSplitter

if __name__ == "__main__":
    fn = "./samples/mp3/sample01.mp3"
    logger = Logger()
    timebased_split = TimebasedAudioSplitter(fn, 5)
    t = Transcriber()
    t.transcribe(timebased_split)
