import logging
import whisper


class Models():
    def get_tiny_model(self) -> whisper.Whisper:
        """gather model `tiny.en`"""
        tiny_model = whisper.load_model("tiny.en")
        logging.info("tiny_model mounted")
        return tiny_model

    def get_small_model(self) -> whisper.Whisper:
        """gather model `small.en`"""
        small_model = whisper.load_model("small.en")
        logging.info("small_model mounted")
        return small_model

    def get_medium_model(self) -> whisper.Whisper:
        """gather model `medium.en`"""
        medium_model = whisper.load_model("medium.en")
        logging.info("medium_model mounted")
        return medium_model
