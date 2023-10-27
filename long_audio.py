from src.transcriber import Transcriber
from src.tools.logger import Logger

if __name__ == "__main__":
    fn = "./samples/mp3/sample01.mp3"
    logger = Logger()
    t = Transcriber()
    t.transcribe(fn)
