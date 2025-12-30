"""Formulas tab for viewing all scent formulas"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.scent_models import ScentFormula

class FormulasTab:
    def __init__(self, parent, user_data):
        self.user_data = user_data
        self.frame = ttk.Frame(parent)
        
        self.create_widgets()
        self.load_formulas()
    
    def create_widgets(self):
        """Create formulas tab widgets"""
        # Top controls
        controls_frame = ttk.Frame(self.frame, padding=10)
        controls_frame.pack(fill='x', side='top')
        
        ttk.Label(controls_frame, text="All Scent Formulas", font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame,
            text="Refresh",
            command=self.load_formulas,
            width=10
        ).pack(side='left', padx=5)
        
        # Formulas list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Formula ID', 'User', 'Base Note', 'Middle Note', 'Top Note', 'Created')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=18)
        
        self.tree.heading('Formula ID', text='ID')
        self.tree.heading('User', text='User')
        self.tree.heading('Base Note', text='Base Note')
        self.tree.heading('Middle Note', text='Middle Note')
        self.tree.heading('Top Note', text='Top Note')
        self.tree.heading('Created', text='Created At')
        
        self.tree.column('Formula ID', width=80)
        self.tree.column('User', width=150)
        self.tree.column('Base Note', width=150)
        self.tree.column('Middle Note', width=150)
        self.tree.column('Top Note', width=150)
        self.tree.column('Created', width=180)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def load_formulas(self):
        """Load all formulas"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            formulas = ScentFormula.get_all_formulas()
            
            if formulas:
                for formula in formulas:
                    # Safely access fields
                    formula_id = formula[0] if len(formula) > 0 else 'N/A'
                    created_at = str(formula[4])[:19] if len(formula) > 4 else 'N/A'
                    user_name = formula[5] if len(formula) > 5 else 'Unknown'
                    base_note = formula[6] if len(formula) > 6 else 'N/A'
                    middle_note = formula[7] if len(formula) > 7 else 'N/A'
                    top_note = formula[8] if len(formula) > 8 else 'N/A'
                    
                    self.tree.insert('', 'end', values=(
                        formula_id,
                        user_name,
                        base_note,
                        middle_note,
                        top_note,
                        created_at
                    ))
        except Exception as e:
            print(f"Error loading formulas: {e}")
