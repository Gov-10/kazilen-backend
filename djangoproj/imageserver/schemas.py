from uuid import UUID
from ninja import Schema

class ImageResponse(Schema):
    profileID: UUID
    image_url: str
