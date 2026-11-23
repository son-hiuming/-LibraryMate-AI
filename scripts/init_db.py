from pathlib import Path
import csv
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "books.csv"
DB = ROOT / "data" / "library.db"

def init_database(db_path=DB, csv_path=CSV):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL,
            category TEXT NOT NULL, description TEXT NOT NULL,
            total_copies INTEGER NOT NULL CHECK(total_copies >= 0),
            available_copies INTEGER NOT NULL CHECK(available_copies >= 0 AND available_copies <= total_copies),
            shelf_location TEXT NOT NULL
        )""")
        with open(csv_path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        con.execute("DELETE FROM books")
        con.executemany("""INSERT INTO books VALUES
            (:book_id,:title,:author,:category,:description,:total_copies,:available_copies,:shelf_location)""", rows)
    return len(rows)

if __name__ == '__main__':
    n = init_database()
    print(f"Initialized {n} fictional books in {DB}")
