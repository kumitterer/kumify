from django import template

from io import BytesIO

import holoviews as hv

import base64

register = template.Library()

@register.simple_tag
def pildata(image):
    data = BytesIO()
    image.save(data, "JPEG")
    content = base64.b64encode(data.getvalue()).decode("UTF-8")
    return f"data:img/jpeg;base64,{content}"

@register.simple_tag
def hvhtml(hvobject):
    renderer = hv.renderer('bokeh')
    html = renderer.html(hvobject, resources="inline")

    html = html.replace("http://localhost:5006/static/extensions/panel/css", "/static/frontend/vendor/panel")

    return html
    
@register.simple_tag
def hvdata(hvobject):
    html = hvhtml(hvobject)
    return f"data:text/html;charset=utf-8,{html}"