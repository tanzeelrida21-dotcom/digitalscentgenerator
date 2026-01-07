import tkinter as tk
from tkinter import ttk
from .formula_view import FormulaView
from .analytics_view import AnalyticsView


class MainWindow(tk.Frame):
    def __init__(self, parent, scent_service, analytics_service):
        super().__init__(parent)
        notebook = ttk.Notebook(self)

        self.formula_tab = FormulaView(notebook, scent_service)
        self.analytics_tab = AnalyticsView(notebook, analytics_service)

        notebook.add(self.formula_tab, text="Generator")
        notebook.add(self.analytics_tab, text="Analytics")
        notebook.pack(expand=True, fill="both")