import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional

DATABASE_PATH = Path(__file__).parent.parent / "receipts.db"


async def init_db():
    """Initialiseer de database met de benodigde tabellen."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL,
                store_name TEXT,
                date DATE,
                total_amount REAL,
                btw_amount REAL,
                payment_method TEXT,
                category TEXT,
                raw_text TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS receipt_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                description TEXT,
                quantity REAL DEFAULT 1,
                unit_price REAL,
                total_price REAL,
                btw_percentage REAL,
                FOREIGN KEY (receipt_id) REFERENCES receipts(id)
            )
        """)

        await db.commit()


async def save_receipt(
    telegram_user_id: int,
    store_name: Optional[str] = None,
    date: Optional[str] = None,
    total_amount: Optional[float] = None,
    btw_amount: Optional[float] = None,
    payment_method: Optional[str] = None,
    category: Optional[str] = None,
    raw_text: Optional[str] = None,
    image_path: Optional[str] = None
) -> int:
    """Sla een bonnetje op en retourneer het ID."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO receipts (
                telegram_user_id, store_name, date, total_amount,
                btw_amount, payment_method, category, raw_text, image_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            telegram_user_id, store_name, date, total_amount,
            btw_amount, payment_method, category, raw_text, image_path
        ))
        await db.commit()
        return cursor.lastrowid


async def save_receipt_items(receipt_id: int, items: list[dict]):
    """Sla de items van een bonnetje op."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        for item in items:
            await db.execute("""
                INSERT INTO receipt_items (
                    receipt_id, description, quantity, unit_price,
                    total_price, btw_percentage
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                receipt_id,
                item.get('description'),
                item.get('quantity', 1),
                item.get('unit_price'),
                item.get('total_price'),
                item.get('btw_percentage')
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
    """Bereken een samenvatting voor een maand."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT
                COUNT(*) as total_receipts,
                SUM(total_amount) as total_spent,
                SUM(btw_amount) as total_btw,
                SUM(CASE WHEN payment_method = 'pin' THEN total_amount ELSE 0 END) as total_pin,
                SUM(CASE WHEN payment_method = 'cash' THEN total_amount ELSE 0 END) as total_cash,
                SUM(CASE WHEN payment_method = 'onbekend' OR payment_method IS NULL THEN total_amount ELSE 0 END) as total_unknown
            FROM receipts
            WHERE telegram_user_id = ?
            AND strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
        """, (telegram_user_id, str(year), f"{month:02d}"))

        row = await cursor.fetchone()
        return dict(row) if row else {}


async def delete_receipt(receipt_id: int, telegram_user_id: int) -> bool:
    """Verwijder een bonnetje (alleen als het van de gebruiker is)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("""
            DELETE FROM receipts
            WHERE id = ? AND telegram_user_id = ?
        """, (receipt_id, telegram_user_id))
        await db.commit()
        return cursor.rowcount > 0
