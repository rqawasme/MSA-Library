"""
Convert a Libib CSV export to a Django fixture for library.Book.
Usage: python scripts/csv_to_fixture.py path/to/books.csv > library/fixtures/books_fixture.json
"""
import csv
import json
import sys


def csv_to_fixture(csv_path):
    books = []
    pk = 1

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        # Normalize headers
        reader.fieldnames = [h.strip().lower().replace(' ', '_') for h in reader.fieldnames]

        for row in reader:
            if row.get('item_type', '').strip().lower() != 'book':
                continue

            title = row.get('title', '').strip()
            if not title:
                continue

            creators = row.get('creators', '').strip()
            description = row.get('description', '').strip()
            publisher = row.get('publisher', '').strip()
            publish_date = row.get('publish_date', '').strip()

            copies_raw = row.get('copies', '1').strip() or '1'
            try:
                copies = int(float(copies_raw))
            except ValueError:
                copies = 1

            books.append({
                "model": "library.book",
                "pk": pk,
                "fields": {
                    "title": title,
                    "creators": creators,
                    "description": description,
                    "publisher": publisher,
                    "publish_date": publish_date,
                    "total_copies": copies,
                    "available_copies": copies,
                    "unique_number": pk,
                }
            })
            pk += 1

    return books


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/csv_to_fixture.py <csv_path>", file=sys.stderr)
        sys.exit(1)

    fixture = csv_to_fixture(sys.argv[1])
    print(json.dumps(fixture, indent=4, ensure_ascii=False))
