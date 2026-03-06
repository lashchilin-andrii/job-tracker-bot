from src.exceptions import InvalidCallbackData


class ButtonBase:
    def __init__(self, text: str, callback_prefix: str | None = None) -> None:
        self.text: str = text
        self.callback_prefix: str = callback_prefix or text.replace(" ", "_").lower()

    def set_text(self, value):
        self.text = value
        return self.text

    def get_data_from_callback_without_prefix(self, callback: str) -> str:
        if not callback:
            raise InvalidCallbackData("Callback data is empty")
        if callback.startswith(self.callback_prefix):
            return callback[len(self.callback_prefix) :]
        return callback
