from ninja import Schema

class ImageResponse(Schema):
    profileID: int
    image_url: str
