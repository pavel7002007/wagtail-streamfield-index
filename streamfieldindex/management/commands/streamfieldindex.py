from django.core.management.base import BaseCommand

from streamfieldindex import indexer


class Command(BaseCommand):
    """"""

    help = ""

    def handle(self, *args, **kwargs):

        indexer.index_all()
