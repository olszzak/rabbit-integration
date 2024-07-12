from pydantic import BaseModel


class BaseMessageSchema(BaseModel):
    pass


class MessageSchema(BaseMessageSchema):
    key: str
    value: str


class DownloadMessageSchema(BaseMessageSchema):
    key: str
