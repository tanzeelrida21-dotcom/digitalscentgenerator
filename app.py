import pyodbc

class DBManager:
    def __init__(self):
        # We use raw strings (r"") to prevent escape sequence errors with \SQLEXPRESS
        self.conn_str = (
            r"Driver={SQL Server};"
            r"Server=DESKTOP-C3S4GC0\SQLEXPRESS;" 
            r"Database=ScentGeneratorDB;"
            r"Trusted_Connection=yes;"
        )

    def get_notes(self):
        """Encapsulated data retrieval for the Scent Notes."""
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT NoteName, Category FROM ScentNotes")
                return cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Database connection error: {e}")
            return []

    def save_result(self, name, recipe):
        """Persists the generated formula to the SQL Server."""
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO GeneratedFormulas (FormulaName, Recipe) VALUES (?, ?)",
                    (name, recipe)
                )
                conn.commit()
        except pyodbc.Error as e:
            print(f"Error saving formula: {e}")