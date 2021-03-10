import pytest
from wagtail.core.blocks import (
    BoundBlock,
    CharBlock,
    EmailBlock,
    IntegerBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
    TextBlock,
)
from wagtail.core.rich_text import RichText
from wagtail.images.blocks import ImageChooserBlock

from streamfieldindex import indexer
from streamfieldindex.models import IndexEntry

from .testapp.blocks import PersonBlock

# Define a mark for all tests in this file
pytestmark = pytest.mark.django_db


def test_char_block(basic_blocks_page):
    indexer.index_page(basic_blocks_page)
    bound_block = IndexEntry.objects.get(block_name="heading").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == "This is a test char block"
    assert isinstance(bound_block.block, CharBlock)


def test_text_block(basic_blocks_page):
    indexer.index_page(basic_blocks_page)
    bound_block = IndexEntry.objects.get(block_name="description").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == "This is a test text block"
    assert isinstance(bound_block.block, TextBlock)


def test_email_block(basic_blocks_page):
    indexer.index_page(basic_blocks_page)
    bound_block = IndexEntry.objects.get(block_name="email").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == "nye.bevan@nhs.net"
    assert isinstance(bound_block.block, EmailBlock)


def test_number_block(basic_blocks_page):
    indexer.index_page(basic_blocks_page)
    bound_block = IndexEntry.objects.get(block_name="number").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == 123
    assert isinstance(bound_block.block, IntegerBlock)


def test_richtext_block(richtext_block_page):
    indexer.index_page(richtext_block_page)
    bound_block = IndexEntry.objects.get(block_name="paragraph").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert isinstance(bound_block.value, RichText)
    assert str(bound_block.value) == "<p>This is a test <em>richtext</em> block</p>"
    assert isinstance(bound_block.block, RichTextBlock)


def test_list_block(list_block_page):
    indexer.index_page(list_block_page)
    bound_block = IndexEntry.objects.get(block_name="numbers").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == [1, 2, 3]
    assert isinstance(bound_block.block, ListBlock)


def test_list_block_items(list_block_page):
    indexer.index_page(list_block_page)
    bound_block = IndexEntry.objects.filter(block_name="numbers:item").first().get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == 1
    assert isinstance(bound_block.block, IntegerBlock)


def test_complex_list_block(complex_list_block_page):
    indexer.index_page(complex_list_block_page)

    bound_block = IndexEntry.objects.get(block_name="people").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert "Kofoworola Abeni Pratt" in str(bound_block.value)
    assert "Benjamin Moore" in str(bound_block.value)
    assert isinstance(bound_block.block, ListBlock)


def test_complex_list_block_items(complex_list_block_page):
    indexer.index_page(complex_list_block_page)

    bound_block = IndexEntry.objects.filter(block_name="people:item").first().get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert "Kofoworola Abeni Pratt" in str(bound_block.value)
    assert isinstance(bound_block.block, PersonBlock)

    bound_block = IndexEntry.objects.filter(block_name="name").first().get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == "Kofoworola Abeni Pratt"
    assert isinstance(bound_block.block, CharBlock)


def test_struct_block(struct_block_page):
    indexer.index_page(struct_block_page)

    bound_block = IndexEntry.objects.get(block_name="person").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert "Aneurin Bevan" in str(bound_block.value)
    assert isinstance(bound_block.block, PersonBlock)


def test_struct_block_items(struct_block_page):
    indexer.index_page(struct_block_page)

    bound_block = IndexEntry.objects.get(block_name="name").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == "Aneurin Bevan"
    assert isinstance(bound_block.block, CharBlock)


def test_stream_block(stream_block_page):
    indexer.index_page(stream_block_page)

    bound_block = IndexEntry.objects.get(block_name="stream").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert "<p>This is a test paragraph block</p>" in str(bound_block.value)
    assert isinstance(bound_block.block, StreamBlock)


def test_stream_block_items(stream_block_page):
    indexer.index_page(stream_block_page)

    bound_block = IndexEntry.objects.get(block_name="heading").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert str(bound_block.value) == "This is a test heading block"
    assert isinstance(bound_block.block, CharBlock)


def test_image_block(image, image_block_page):
    indexer.index_page(image_block_page)

    bound_block = IndexEntry.objects.get(block_name="image").get_bound_block()

    assert isinstance(bound_block, BoundBlock)
    assert bound_block.value == image
    assert isinstance(bound_block.block, ImageChooserBlock)
