from typing import List
from pydantic import BaseModel

class NewsletterThemeOutput(BaseModel):
    theme: str
    sub_themes: List[str]