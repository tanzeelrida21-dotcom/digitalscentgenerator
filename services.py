import random


class ScentService:
    def __init__(self, db):
        self.db = db

    def generate_formula(self):
        all_notes = self.db.execute_query("SELECT NoteName, Category FROM ScentNotes")

        top = random.choice([n[0] for n in all_notes if n[1] == 'Top'])
        mid = random.choice([n[0] for n in all_notes if n[1] == 'Middle'])
        base = random.choice([n[0] for n in all_notes if n[1] == 'Base'])

        recipe = f"{top} + {mid} + {base}"
        self.db.execute_non_query(
            "INSERT INTO GeneratedFormulas (FormulaName, Recipe) VALUES (?, ?)",
            ("Custom Blend", recipe)
        )
        return recipe