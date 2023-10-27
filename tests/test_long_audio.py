import unittest
from source.engine.transcriber import Transcriber
from source.engine.tools import TimebasedAudioSplitter, SilenceAudioSplitter


class TestEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.filename = "./tests/samples/mp3/sample01.mp3"
        self.t = Transcriber()
        return super().setUp()

    def test_timebased_translation_works(self):
        """
        Test that the time based translation returns any input
        """
        timebased_split = TimebasedAudioSplitter(self.filename, 5)
        v = self.t.transcribe(timebased_split)
        self.assertNotEqual(v, "" or None)

    def test_silence_based_translation_works(self):
        """
        Test that the silence based translation works
        """
        silencebased_split = SilenceAudioSplitter(self.filename)
        v = self.t.transcribe(silencebased_split)
        self.assertNotEqual(v, "" or None)


if __name__ == "__main__":
    unittest.main()
