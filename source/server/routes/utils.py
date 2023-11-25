from dataclasses import dataclass
from source.server.models import User


@dataclass
class AudioDiagnosticsFile:
    uid: str


class AudioUploadException(Exception):
    def __init__(self, user: User, *args) -> None:
        super().__init__(*args)


class ConfirmedAudioFileExists(AudioUploadException):
    def __init__(self, user: User, file_details: AudioDiagnosticsFile) -> None:
        # Log the information
        super().__init__(user)
