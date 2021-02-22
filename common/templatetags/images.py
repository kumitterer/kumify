from django import template

from io import BytesIO

import holoviews as hv

from bokeh.embed import file_html
from bokeh.resources import INLINE
from bokeh.models.tools import PanTool, WheelZoomTool

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
    bokeh = hv.render(hvobject)

    pan_tool = bokeh.select(dict(type=PanTool))
    pan_tool.dimensions = "width"

    zoom_tool = bokeh.select(dict(type=WheelZoomTool))
    zoom_tool.dimensions = "width"

    html = file_html(bokeh, INLINE)
    html = html.replace("http://localhost:5006/static/extensions/panel/css", "/static/frontend/vendor/panel")

    return html
    
@register.simple_tag
def hvdata(hvobject):
    html = hvhtml(hvobject)
    return f"data:text/html;charset=utf-8,{html}"