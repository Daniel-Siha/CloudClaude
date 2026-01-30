import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional

DATABASE_PATH = Path(__file__).parent.parent / "receipts.db"


async def init_db():
    """Initialiseer de database met de benodigde tabellen voor horeca boekhouding."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Hoofdtabel voor bonnetjes/facturen
        await db.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL,
                store_name TEXT,
                supplier_type TEXT,
                date DATE,
                invoice_number TEXT,
                total_amount REAL,
                total_excl_btw REAL,
                btw_amount REAL,
                btw_9_amount REAL,
                btw_21_amount REAL,
                payment_method TEXT,
                category TEXT,
                raw_text TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Items per bonnetje
        await db.execute("""
            CREATE TABLE IF NOT EXISTS receipt_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                description TEXT,
                quantity REAL DEFAULT 1,
                unit_price REAL,
                total_price REAL,
                btw_percentage REAL,
                btw_amount REAL,
                expense_category TEXT,
                FOREIGN KEY (receipt_id) REFERENCES receipts(id)
            )
        """)

        # Migratie: voeg nieuwe kolommen toe als ze niet bestaan
        await migrate_db(db)

        await db.commit()


async def migrate_db(db):
    """Voeg nieuwe kolommen toe voor horeca boekhouding."""
    # Haal bestaande kolommen op
    cursor = await db.execute("PRAGMA table_info(receipts)")
    columns = [row[1] for row in await cursor.fetchall()]

    # Nieuwe kolommen voor receipts
    new_receipt_columns = [
        ("supplier_type", "TEXT"),
        ("invoice_number", "TEXT"),
        ("total_excl_btw", "REAL"),
        ("btw_9_amount", "REAL"),
        ("btw_21_amount", "REAL"),
    ]

    for col_name, col_type in new_receipt_columns:
        if col_name not in columns:
            try:
                await db.execute(f"ALTER TABLE receipts ADD COLUMN {col_name} {col_type}")
            except Exception:
                pass  # Kolom bestaat al

    # Haal bestaande kolommen op voor items
    cursor = await db.execute("PRAGMA table_info(receipt_items)")
    item_columns = [row[1] for row in await cursor.fetchall()]

    # Nieuwe kolommen voor receipt_items
    new_item_columns = [
        ("btw_amount", "REAL"),
        ("expense_category", "TEXT"),
    ]

    for col_name, col_type in new_item_columns:
        if col_name not in item_columns:
            try:
                await db.execute(f"ALTER TABLE receipt_items ADD COLUMN {col_name} {col_type}")
            except Exception:
                pass


async def save_receipt(
    telegram_user_id: int,
    store_name: Optional[str] = None,
    supplier_type: Optional[str] = None,
    date: Optional[str] = None,
    invoice_number: Optional[str] = None,
    total_amount: Optional[float] = None,
    total_excl_btw: Optional[float] = None,
    btw_amount: Optional[float] = None,
    btw_9_amount: Optional[float] = None,
    btw_21_amount: Optional[float] = None,
    payment_method: Optional[str] = None,
    category: Optional[str] = None,
    raw_text: Optional[str] = None,
    image_path: Optional[str] = None
) -> int:
    """Sla een bonnetje/factuur op en retourneer het ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO receipts (
                telegram_user_id, store_name, supplier_type, date, invoice_number,
                total_amount, total_excl_btw, btw_amount, btw_9_amount, btw_21_amount,
                payment_method, category, raw_text, image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            telegram_user_id, store_name, supplier_type, date, invoice_number,
            total_amount, total_excl_btw, btw_amount, btw_9_amount, btw_21_amount,
            payment_method, category, raw_text, image_path
        ))
        await db.commit()
        return cursor.lastrowid


async def save_receipt_items(receipt_id: int, items: list[dict]):
    """Sla de items van een bonnetje op met horeca categorisatie."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        for item in items:
            await db.execute("""
                INSERT INTO receipt_items (
                    receipt_id, description, quantity, unit_price,
                    total_price, btw_percentage, btw_amount, expense_category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                receipt_id,
                item.get('description'),
                item.get('quantity', 1),
                item.get('unit_price'),
                item.get('total_price'),
                item.get('btw_percentage'),
                item.get('btw_amount'),
                item.get('expense_category')
            ))
        await db.commit()


async def get_receipts_by_month(telegram_user_id: int, year: int, month: int) -> list[dict]:
    """Haal alle bonnetjes op voor een specifieke maand."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM receipts
            WHERE telegram_user_id = ?
            AND strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
            ORDER BY date ASC
        """, (telegram_user_id, str(year), f"{month:02d}"))

        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_receipt_items(receipt_id: int) -> list[dict]:
    """Haal alle items op voor een specifiek bonnetje."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM receipt_items WHERE receipt_id = ?
        """, (receipt_id,))

        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_monthly_summary(telegram_user_id: int, year: int, month: int) -> dict:
    """Bereken een samenvatting voor een maand (horeca optimized)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                COUNT(*) as total_receipts,
                SUM(total_amount) as total_spent,
                SUM(total_excl_btw) as total_excl_btw,
                SUM(btw_amount) as total_btw,
                SUM(btw_9_amount) as total_btw_9,
                SUM(btw_21_amount) as total_btw_21,
                SUM(CASE WHEN payment_method = 'pin' THEN total_amount ELSE 0 END) as total_pin,
                SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END) as total_cash,
                SUM(CASE WHEN payment_method = 'factuur' THEN total_amount ELSE 0 END) as total_factuur,
                SUM(CASE WHEN payment_method = 'onbekend' OR payment_method IS NULL THEN total_amount ELSE 0 END) as total_unknown
            FROM receipts
            WHERE telegram_user_id = ?
            AND strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
        """, (telegram_user_id, str(year), f"{month:02d}"))

        row = await cursor.fetchone()
        return dict(row) if row else {}


async def get_expense_summary_by_month(telegram_user_id: int, year: int, month: int) -> dict:
    """Bereken totalen per kostenpost voor een maand."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                ri.expense_category,
                SUM(ri.total_price) as total_amount,
                SUM(ri.btw_amount) as total_btw,
                COUNT(*) as item_count
            FROM receipt_items ri
            JOIN receipts r ON ri.receipt_id = r.id
            WHERE r.telegram_user_id = ?
            AND strftime('%Y', r.date) = ?
            AND strftime('%m', r.date) = ?
            GROUP BY ri.expense_category
        """, (telegram_user_id, str(year), f"{month:02d}"))

        rows = await cursor.fetchall()
        return {row['expense_category']: dict(row) for row in rows}


async def get_supplier_summary_by_month(telegram_user_id: int, year: int, month: int) -> list[dict]:
    """Bereken totalen per leverancier voor een maand."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                store_name,
                supplier_type,
                COUNT(*) as receipt_count,
                SUM(total_amount) as total_amount,
                SUM(btw_amount) as total_btw
            FROM receipts
            WHERE telegram_user_id = ?
            AND strftime('%Y', r.date) = ?
            AND strftime('%m', r.date) = ?
            GROUP BY store_name
            ORDER BY total_amount DESC
        """, (telegram_user_id, str(year), f"{month:02d}"))

        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def update_receipt(receipt_id: int, telegram_user_id: int, **kwargs) -> bool:
    """Update een bonnetje met de gegeven velden."""
    if not kwargs:
        return False

    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Bouw de update query dynamisch
        set_clauses = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [receipt_id, telegram_user_id]

        cursor = await db.execute(f"""
            UPDATE receipts
            SET {set_clauses}
            WHERE id = ? AND telegram_user_id = ?
        """, values)

        await db.commit()
        return cursor.rowcount > 0


async def delete_receipt(receipt_id: int, telegram_user_id: int) -> bool:
    """Verwijder een bonnetje (alleen als het van de gebruiker is)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Verwijder eerst de items
        await db.execute("""
            DELETE FROM receipt_items WHERE receipt_id = ?
        """, (receipt_id,))

        # Verwijder dan het bonnetje
        cursor = await db.execute("""
            DELETE FROM receipts
            WHERE id = ? AND telegram_user_id = ?
        """, (receipt_id, telegram_user_id))
        await db.commit()
        return cursor.rowcount > 0
