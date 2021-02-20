from django import template

from io import BytesIO

import base64

register = template.Library()

@register.simple_tag
def pildata(image):
    data = BytesIO()
    image.save(data, "JPEG")
    content = base64.b64encode(data.getvalue()).decode("UTF-8")
    return f"data:img/jpeg;base64,{content}"