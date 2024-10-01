import random
import base64
from PIL import Image, ImageDraw, ImageFont
from typing import NamedTuple
from io import BytesIO

font = ImageFont.truetype('vulnsite/static/Teko-Regular.ttf', size=40)


class CaptchaData(NamedTuple):
    captcha: str
    value: str


def generate_captcha() -> CaptchaData:
    """
    :return: encoded_captcha, value
    :rtype: CaptchaData
    """
    value = str(random.randint(100000000000, 999999999999))
    captcha = Image.new('RGB', (200, 100), color=(255, 255, 255))

    draw = ImageDraw.Draw(captcha)
    draw.text((20, 22), value, font=font, fill=(0, 0, 0))

    buffered = BytesIO()
    captcha.save(buffered, "JPEG")
    encoded_captcha = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return CaptchaData(captcha=encoded_captcha, value=value)


if __name__ == "__main__":
    captcha = generate_captcha()
    print(captcha)
