import io

import pytest
from django.core.files.images import ImageFile
from PIL import Image
from wagtail.core.models import Page
from wagtail.images import get_image_model


@pytest.fixture
def root_page():
    return Page.objects.get(slug="root", depth=1)


@pytest.fixture
def image():
    image = Image.new("RGBA", size=(50, 50), color=(0, 70, 177))
    image_file = io.BytesIO()
    image.save(image_file, "png")  # or whatever format you prefer
    file = ImageFile(image_file, name="testimage.png")
    wagtail_image = get_image_model()(file=file, title="My Test Image")
    wagtail_image.save()
    return wagtail_image
