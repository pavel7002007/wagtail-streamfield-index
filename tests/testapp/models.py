from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from . import blocks


class HomePage(Page):

    body = StreamField(blocks.BodyBlock, use_json_field=True)
    content_panels = Page.content_panels + [FieldPanel("body")]
