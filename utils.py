from sys import getsizeof
from re import T
from pydub import AudioSegment
from pydub.silence import split_on_silence
import concurrent.futures


MAX_WORKERS = 5


class AudioSplitter:
    DEFAULT_OFFSET = 10
    DEFAULT_MIN_SILENCE_LEN = 2000
    DEFAULT_MAX_N_OF_CHUNKS = 10

    def __init__(self, file: str) -> None:
        self.file = file
        self.audio = AudioSegment.from_mp3(self.file)

    def _load_chunks(
        self,
        min_silence_len: int,
        silence_thresh: int,
        keep_silence=200,
    ) -> list:
        return split_on_silence(
            audio_segment=self.audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh,
            keep_silence=keep_silence,
        )

    def _get_average_chunk_size(self, chunks: list):
        if len(chunks) == 0:
            return None
        return sum([getsizeof(obj) for obj in chunks]) / len(chunks)

    def load_chunks(
        self, min_silence_len=DEFAULT_MIN_SILENCE_LEN, verbose=True
    ) -> list:
        """
        Splits mp3 files into chunks

        Parameters:
        offset (int): Increment for finding the best configuration
        min_silence_len (int): Minumum length of silence

        Returns:
        list[AudioSegment]
        """

        if verbose:
            print("[Info] Converting audio into chunks")

        opt_chunks = []
        highest_chunk_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_offset = {
                executor.submit(
                    self._load_chunks,
                    min_silence_len,
                    -offset,
                )
                for offset in range(1, 100, self.DEFAULT_OFFSET)
            }
            for i, future in enumerate(
                concurrent.futures.as_completed(future_to_offset)
            ):
                chunks = future.result()
                try:
                    size = len(chunks)
                    if verbose:
                        print(
                            f"[Info] Phase_{i+1}\nNumber of chunks: {size}.\nAverage chunk size: {self._get_average_chunk_size(chunks)}bytes.\n\n"
                        )

                    if (
                        size > highest_chunk_count
                        and size <= self.DEFAULT_MAX_N_OF_CHUNKS
                    ):
                        highest_chunk_count = size
                        opt_chunks = chunks

                except Exception as exc:
                    print(
                        f"[Error] Something went wrong while splitting chunks. See error msg: {exc}"
                    )

        if verbose:
            print(
                f"[Info] Audio splitting into chunks complete! Number of chunks: {len(opt_chunks)}"
            )
        return opt_chunks
