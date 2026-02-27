from pydantic import BaseModel


class ButtonBase(BaseModel):
    text: str
    callback: str = "noop"
