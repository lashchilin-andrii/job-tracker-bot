from pydantic import BaseModel

from src.exceptions import InvalidCallbackData


class ButtonBase(BaseModel):
    text: str
    callback_prefix: str = "noop"

    def get_data_from_callback_without_prefix(self, callback: str | None) -> str:
        if not callback:
            raise InvalidCallbackData
        if callback.startswith(self.callback_prefix):
            return callback[len(self.callback_prefix) :]
        return callback
