from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import IntegrityError, ProgrammingError, transaction, DatabaseError

CATEGORY_FIXTURES_PATH = settings.BASE_DIR.joinpath('categories.json')
PRODUCT_FIXTURES_PATH = settings.BASE_DIR.joinpath('products.json')


class Command(BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                call_command('loaddata', CATEGORY_FIXTURES_PATH)
                call_command('loaddata', PRODUCT_FIXTURES_PATH)
        except ProgrammingError:
            pass
        except IntegrityError as e:
            self.stdout.write(f'Invalid fixtures: {e}', self.style.NOTICE)
        except DatabaseError as e:
            self.stdout.write(f'Something went wrong: {e}', self.style.ERROR)
        else:
            self.stdout.write(
                'Command have been completed successfully',
                self.style.SUCCESS
            )
