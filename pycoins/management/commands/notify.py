from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from pycoins.notifier.notifier import Notifier
        notifier = Notifier()
        notifier.notify()
