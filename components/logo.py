from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def create_logo() -> BytesIO:
    size = 280

    image = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (18, 18, size - 18, size - 18),
        radius=54,
        fill=(7, 31, 69, 255),
        outline=(201, 161, 74, 255),
        width=7,
    )

    draw.rounded_rectangle(
        (31, 31, size - 31, size - 31),
        radius=44,
        outline=(231, 211, 157, 150),
        width=2,
    )

    try:
        font = ImageFont.truetype(
            "arialbd.ttf",
            132,
        )
    except OSError:
        font = ImageFont.load_default()

    text = "N"

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    draw.text(
        (
            (size - text_width) / 2,
            (size - text_height) / 2 - 10,
        ),
        text,
        font=font,
        fill=(231, 211, 157, 255),
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    buffer.seek(0)

    return buffer
