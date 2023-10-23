from src.transcriber import Transcriber

if __name__ == "__main__":
    fn = "./samples/mp3/sample01.mp3"
    t = Transcriber()
    t.transcribe(fn)
