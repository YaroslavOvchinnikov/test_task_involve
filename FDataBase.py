import sqlite3

class FDataBase:
    def __init__(self, db='test_database.db'):
        self._db = db
        with sqlite3.connect(self._db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments(
                id integer PRIMARY KEY AUTOINCREMENT,
                currency text NOT NULL,
                amount float NOT NULL,
                time date NOT NULL,
                description text
                );""")
            conn.commit()

    def add_payment_info(self, sum, curr, desc, date):

        with sqlite3.connect(self._db) as conn:

            cursor = conn.cursor()
            cursor.execute("""
                            INSERT INTO payments (currency, amount, time, description)
                            VALUES (?, ?, ?, ?)""", (curr, sum, date, desc))

            conn.commit()
            return cursor.lastrowid

    # def get_shop_order_id(self, date):
    #     with sqlite3.connect(self._db) as conn:
    #         cursor = conn.cursor()
    #         id = cursor.execute(f"""
    #                 SELECT id FROM payments WHERE time = ?
    #         """, (date,)).fetchone()[0]
    #         conn.commit()
    #     return id

    def get_description(self, id):
        with sqlite3.connect(self._db) as conn:
            cursor = conn.cursor()
            desc = cursor.execute(f"""
                    SELECT description FROM payments WHERE id = ?
            """, (id,)).fetchone()[0]
            conn.commit()
        return desc