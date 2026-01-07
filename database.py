import pyodbc

class DatabaseSession:
    def __init__(self):
        # Update with your DESKTOP-C3S4GC0\SQLEXPRESS details
        self.conn_str = (
            r"Driver={SQL Server};"
            r"Server=DESKTOP-C3S4GC0\SQLEXPRESS;"
            r"Database=ScentGeneratorDB;"
            r"Trusted_Connection=yes;"
        )

    def execute_query(self, query, params=None):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_non_query(self, query, params=None):
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
