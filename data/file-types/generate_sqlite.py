#!/usr/bin/env python3
"""Write the synthetic SQLite 3 samples of this folder.

Run from this folder: python3 generate_sqlite.py
All names, addresses and values are invented. The byte content depends on the
SQLite library version, so the SHA-256 in README.md is for the committed copy.
"""
import os
import sqlite3

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlite")

FIRST = ["Ana", "Ben", "Cora", "Dan", "Eli", "Fay", "Gus", "Hana", "Ivo", "Jun"]
LAST = ["Abel", "Brook", "Cole", "Dale", "Eden", "Frost", "Gale", "Hale", "Isle", "Jory"]


def fresh(name):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        os.remove(path)
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode = DELETE")
    db.execute("PRAGMA page_size = 4096")
    return path, db


def contacts_orders():
    """Two tables, a BLOB column, a NULL, a view, an index and a trigger."""
    path, db = fresh("contacts-orders.sqlite3")
    db.executescript("""
        CREATE TABLE contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            joined DATE,
            photo BLOB
        );
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            contact_id INTEGER REFERENCES contacts(id),
            item TEXT,
            quantity INTEGER,
            price REAL,
            paid BOOLEAN,
            placed_at TIMESTAMP
        );
        CREATE INDEX orders_contact ON orders(contact_id);
        CREATE VIEW order_totals AS
            SELECT c.name AS name, count(o.id) AS orders, sum(o.quantity * o.price) AS total
            FROM contacts c LEFT JOIN orders o ON o.contact_id = c.id
            GROUP BY c.id;
        CREATE TRIGGER orders_audit AFTER INSERT ON orders BEGIN SELECT 1; END;
    """)
    # A small PNG-like header followed by filler, so a reader that prints BLOBs as
    # text would show binary bytes.
    blob = b"\x89PNG\r\n\x1a\n" + bytes(range(256)) * 4
    for i in range(10):
        db.execute(
            "INSERT INTO contacts VALUES (?, ?, ?, ?, ?, ?)",
            (i + 1, f"{FIRST[i]} {LAST[i]}", f"{FIRST[i].lower()}@example.org",
             None if i == 3 else f"+1 555 01{i:02d}", f"2024-0{1 + i % 9}-1{i}",
             blob if i % 3 == 0 else None))
    items = ["paper", "toner", "stapler", "binder", "pen"]
    for i in range(25):
        db.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)",
            (i + 1, 1 + i % 10, items[i % 5], 1 + i % 4, 2.5 + i, i % 2,
             f"2024-05-{1 + i % 28:02d} 10:{i:02d}:00"))
    db.commit()
    db.close()


def many_rows():
    """One table of 6,000 rows, for a row cap test."""
    path, db = fresh("many-rows.sqlite3")
    db.execute("CREATE TABLE readings (id INTEGER PRIMARY KEY, station TEXT, "
               "taken_at TEXT, value REAL, note TEXT)")
    db.executemany(
        "INSERT INTO readings VALUES (?, ?, ?, ?, ?)",
        ((i + 1, f"station-{i % 17}", f"2024-01-01T00:{i % 60:02d}:00",
          (i * 37 % 1000) / 10.0, "" if i % 5 else "check")
         for i in range(6000)))
    db.commit()
    db.close()


def no_extension():
    """A database without a name extension, as a mail attachment or a phone dump has."""
    path, db = fresh("app-data")
    db.executescript("""
        CREATE TABLE messages (id INTEGER PRIMARY KEY, sender TEXT, body TEXT, sent INTEGER);
        CREATE TABLE "odd name; with quotes" ("col one" TEXT, "col""two" INTEGER);
        CREATE TABLE empty_table (a TEXT);
        CREATE TABLE wide AS SELECT 1 AS c1;
    """)
    db.executemany("INSERT INTO messages VALUES (?, ?, ?, ?)",
                   [(1, "ana", "Meeting at 10", 1714550400),
                    (2, "ben", "Moved to 11", 1714554000),
                    (3, "cora", "Bring the report", 1714557600)])
    db.execute('INSERT INTO "odd name; with quotes" VALUES (?, ?)', ("x", 1))
    db.commit()
    db.close()


if __name__ == "__main__":
    os.makedirs(HERE, exist_ok=True)
    contacts_orders()
    many_rows()
    no_extension()
