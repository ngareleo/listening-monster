import speech_recognition as sr

from utils import AudioSplitter


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    fn = "./samples/mp3/sample01.mp3"

    splitter = AudioSplitter(fn)
    chunks = splitter.load_chunks()

    for i, audio_chunk in enumerate(chunks):
        print(f"Chunk {i}: {audio_chunk}")
        audio_chunk.export("temp", format="wav")
        with sr.AudioFile("temp") as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print("Chunk : {}".format(text))

            except Exception as ex:
                print("Error occured")
                print(ex)
