import pydantic
from typing import Optional


class CreateAnnouncement(pydantic.BaseModel):
    """
    This class checks that the data type is correct when creating an announcement.
    """
    owner: str
    title: str
    description: str


class UpdateAnnouncement(pydantic.BaseModel):
    """
    This class checks that the data type is correct when updating an announcement
    """
    owner: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
