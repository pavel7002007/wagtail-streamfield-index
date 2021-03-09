import json

import pytest
from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.models import Page

from streamfieldindex import indexer
from streamfieldindex.models import IndexEntry

from .testapp.models import HomePage

# Define a mark for all tests in this file
pytestmark = pytest.mark.django_db


def create_page(stream_data):
    """Create a valid page by saving data to a real page model and getting it back out of the database"""
    root_page = Page.objects.get(slug="root", depth=1)
    stream_block = HomePage.body.field.stream_block
    test_page = HomePage(
        body=StreamValue(stream_block, [], is_lazy=True, raw_text=json.dumps(stream_data)),
        title="Home Page",
        slug="homepage",
    )
    root_page.add_child(instance=test_page)
    test_page.refresh_from_db()
    return test_page


def test_basic_blocks():
    page = create_page(
        [
            {"type": "heading", "value": "This is a test char block"},
            {"type": "description", "value": "This is a test text block"},
            {"type": "email", "value": "nye.bevan@nhs.net"},
            {"type": "number", "value": 123},
        ]
    )
    indexer.index_page(page)

    assert IndexEntry.objects.count() == 4
    assert IndexEntry.objects.get(block_name="heading").block_value == "This is a test char block"
    assert IndexEntry.objects.get(block_name="description").block_value == "This is a test text block"
    assert IndexEntry.objects.get(block_name="email").block_value == "nye.bevan@nhs.net"
    assert IndexEntry.objects.get(block_name="number").block_value == "123"


def test_richtext_block():
    page = create_page([{"type": "paragraph", "value": "<p>This is a test <em>richtext</em> block</p>"}])
    indexer.index_page(page)

    assert IndexEntry.objects.count() == 1
    assert (
        IndexEntry.objects.get(block_name="paragraph").block_value == "<p>This is a test <em>richtext</em> block</p>"
    )


def test_list_block():
    page = create_page([{"type": "numbers", "value": [1, 2, 3]}])
    indexer.index_page(page)

    # There should be 4 entries, 1 for the list block and 3 for the items inside the list
    assert IndexEntry.objects.count() == 4

    # Indexes for list blocks have no value
    assert IndexEntry.objects.get(block_name="numbers").block_value == ""

    # The values are stored individually as separate items
    assert list(IndexEntry.objects.filter(block_name="numbers:item").values_list("block_value", flat=True)) == [
        "1",
        "2",
        "3",
    ]


def test_complex_list_block():
    """Ensure list blocks also work when they have complex structural blocks as the child block"""
    complex_list_block_data = {
        "type": "people",
        "value": [
            {
                "name": "Kofoworola Abeni Pratt",
                "bio": "<p>The first black nurse to work in the NHS</p>",
                "body": [
                    {"type": "heading", "value": "Career"},
                    {
                        "type": "paragraph",
                        "value": "<p>She became vice-president of the International Council of Nurses and the first black Chief Nursing Officer of Nigeria, working in the Federal Ministry of Health.</p>",
                    },
                ],
            },
            {
                "name": "Benjamin Moore",
                "bio": "<p>Credited with the first use of the words National Health Service.</p>",
                "body": [
                    {"type": "heading", "value": "Career"},
                    {
                        "type": "paragraph",
                        "value": "<p>He held the first chair of biochemistry in the UK, and founded the Biochemical Journal, one of the earliest academic journals in the subject.</p>",
                    },
                ],
            },
        ],
    }
    page = create_page([complex_list_block_data])
    indexer.index_page(page)

    # 1 - The list block
    # 2 - Items inside the list
    # 2x3 - Sub blocks of the PersonBlock struct
    # 2x2 - Sub blocks if the PersonBlock.body streamblock
    # = 13 blocks in total
    assert IndexEntry.objects.count() == 13

    assert list(IndexEntry.objects.filter(block_name="name").values_list("block_value", flat=True)) == [
        "Kofoworola Abeni Pratt",
        "Benjamin Moore",
    ]
    assert list(IndexEntry.objects.filter(block_name="heading").values_list("block_value", flat=True)) == [
        "Career",
        "Career",
    ]

    # list blocks do not have values themselves
    assert IndexEntry.objects.get(block_name="people").block_value == ""

    # There are two items inside the list
    assert IndexEntry.objects.filter(block_name="people:item").count() == 2


def test_struct_block():
    struct_block_data = {
        "type": "person",
        "value": {
            "name": "Aneurin Bevan",
            "bio": "<p>Founder of the NHS</p>",
            "body": [],
        },
    }
    page = create_page([struct_block_data])
    indexer.index_page(page)

    assert IndexEntry.objects.count() == 4

    # struct blocks do not have value themselves
    assert IndexEntry.objects.get(block_name="person").block_value == ""

    # the struct block children have values instead
    assert IndexEntry.objects.get(block_name="name").block_value == "Aneurin Bevan"
    assert IndexEntry.objects.get(block_name="bio").block_value == "<p>Founder of the NHS</p>"


def test_stream_block():
    stream_block_data = {
        "type": "stream",
        "value": [
            {
                "type": "heading",
                "value": "This is a test heading block",
            },
            {
                "type": "paragraph",
                "value": "<p>This is a test paragraph block</p>",
            },
        ],
    }
    page = create_page([stream_block_data])
    indexer.index_page(page)

    # stream blocks do not have value themselves
    assert IndexEntry.objects.get(block_name="stream").block_value == ""

    # the stream block children have values instead
    assert IndexEntry.objects.get(block_name="heading").block_value == "This is a test heading block"
    assert IndexEntry.objects.get(block_name="paragraph").block_value == "<p>This is a test paragraph block</p>"


def test_image_block(image):
    page = create_page([{"type": "image", "value": image.id}])
    indexer.index_page(page)

    assert IndexEntry.objects.get(block_name="image").block_value == str(image.id)
