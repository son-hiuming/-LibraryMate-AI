# LibraryMate simulated catalog (150 entries)

- Entries 1–15: existing example catalog from Milestone 2, kept unchanged.
- Entries 16–150: synthetic educational titles generated for demo, NOT verified published books.
- Synthetic author: `Nhóm biên soạn LibraryMate (giả lập)`.
- All counts, availability and shelf codes are fictional; do not claim live library inventory.
- `books.csv` is the source of truth; rerun `python -m scripts.init_db` to refresh SQLite.
- Search is simple token matching, not semantic retrieval of the catalog; synonym support is limited.
