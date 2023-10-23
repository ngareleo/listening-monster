from pydub import AudioSegment
from pydub.silence import split_on_silence


class AudioSplitter:
    DEFAULT_OFFSET = 10
    DEFAULT_MIN_SILENCE_LEN = 1000

    def __init__(self, file: str) -> None:
        self.file = file
        self.audio = AudioSegment.from_mp3(self.file)

    def _load_chunks(
        self,
        min_silence_len: int,
        silence_thresh: int,
        keep_silence=200,
        verbose=False,
    ) -> list:
        audio_chunks = split_on_silence(
            audio_segment=self.audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            keep_silence=keep_silence,
        )
        if verbose:
            print(
                f"Audio splitting into chunks complete! Number of chunks: {len(audio_chunks)}"
            )
        return audio_chunks

    def load_chunks(
        self, offset=DEFAULT_OFFSET, min_silence_len=DEFAULT_MIN_SILENCE_LEN
    ) -> list:
        """
        Splits mp3 files into chunks

        Parameters:
        offset (int): Increment for finding the best configuration
        min_silence_len (int): Minumum length of silence

        Returns:
        list[AudioSegment]
        """

        # TODO: Spin up multiple threads since self.audio is immutable

        opt_silence_thresh = 0
        highest_chunk_count = 0

        for i in range(1, 100, offset):
            silence_thresh = -(i + offset)
            chunks = self._load_chunks(min_silence_len, (i + offset))
            if len(chunks) > highest_chunk_count:
                highest_chunk_count = len(chunks)
                opt_silence_thresh = silence_thresh

        return self._load_chunks(min_silence_len, opt_silence_thresh, verbose=True)
