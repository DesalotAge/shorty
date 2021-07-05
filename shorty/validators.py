from pydantic import BaseModel, Extra, StrictStr
from typing import Optional
from enum import Enum


class Provider(str, Enum):
    """
        Contains possible values for 'provider' field
    """
    bitly = 'bit.ly'
    tinyurl = 'tinyurl.com'


class ShortifyRequest(BaseModel):
    """
        Object which validate shortify view request data
    """
    url: StrictStr
    provider: Optional[Provider]

    class Config:
        extra = Extra.forbid

