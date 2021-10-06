from wagtail.core import hooks
from wagtail.core.signals import page_published

from .indexer import index_page


@hooks.register("after_create_page")
def index_after_create_page(request, page):
    index_page(page)


@hooks.register("after_edit_page")
def index_after_edit_page(request, page):
    index_page(page)


def post_publish(sender, instance, **kwargs):
    index_page(instance)


page_published.connect(post_publish)
