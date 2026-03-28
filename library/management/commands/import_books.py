import csv
from django.core.management.base import BaseCommand, CommandError
from library.models import Book


class Command(BaseCommand):
    help = 'Import books from a CSV file. Columns: unique_number, title, author, description'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument(
            '--skip-duplicates',
            action='store_true',
            help='Skip books whose unique_number already exists instead of erroring',
        )

    def handle(self, *args, **options):
        path = options['csv_file']
        skip_dupes = options['skip_duplicates']
        created = 0
        skipped = 0

        try:
            with open(path, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                # Normalise header names to lowercase with no spaces
                reader.fieldnames = [h.strip().lower().replace(' ', '_') for h in reader.fieldnames]

                for i, row in enumerate(reader, start=2):  # start=2 accounts for header row
                    unique_number = row.get('unique_number', '').strip()
                    title = row.get('title', '').strip()
                    author = row.get('author', '').strip()
                    description = row.get('description', '').strip()

                    if not unique_number or not title:
                        self.stdout.write(self.style.WARNING(f'Row {i}: missing unique_number or title — skipped'))
                        skipped += 1
                        continue

                    try:
                        unique_number = int(unique_number)
                    except ValueError:
                        self.stdout.write(self.style.WARNING(f'Row {i}: unique_number "{unique_number}" is not an integer — skipped'))
                        skipped += 1
                        continue

                    if Book.objects.filter(unique_number=unique_number).exists():
                        if skip_dupes:
                            self.stdout.write(self.style.WARNING(f'Row {i}: book #{unique_number} already exists — skipped'))
                            skipped += 1
                            continue
                        else:
                            raise CommandError(f'Row {i}: book with unique_number {unique_number} already exists. Use --skip-duplicates to ignore.')

                    Book.objects.create(
                        unique_number=unique_number,
                        title=title,
                        author=author,
                        description=description,
                        available=True,
                    )
                    created += 1

        except FileNotFoundError:
            raise CommandError(f'File not found: {path}')

        self.stdout.write(self.style.SUCCESS(f'Done — {created} books imported, {skipped} skipped'))
