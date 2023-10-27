class Logger:
    _logging = False
    _permer_off = False

    @property
    def permer_off(cls):
        pass

    @classmethod
    def on(cls):
        if not Logger.permer_off:
            Logger._logging = True

    @classmethod
    def off(cls):
        if not Logger.permer_off:
            Logger._logging = False

    @classmethod
    def info(cls, msg: str):
        print(f"[Info] {msg}")

    @classmethod
    def debug(cls, msg: str):
        if Logger._logging:
            print(f"[Debug] {msg}")

    @classmethod
    def warn(cls, msg: str):
        print(f"[Warn] {msg}")
