"""Main window for Scent Quiz System"""

import tkinter as tk
from tkinter import ttk, messagebox
from frontend.quiz_tab import QuizTab
from frontend.results_tab import ResultsTab
from frontend.formulas_tab import FormulasTab
from frontend.analytics_tab import AnalyticsTab
from frontend.users_management_tab import UsersTab

class ScentMainWindow:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        
        self.root.title(f"Scent Quiz System - {user_data['name']}")
        self.root.geometry("1000x650")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"1000x650+{x}+{y}")
        
        self.create_widgets()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create main window widgets"""
        # Top bar with user info
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill='x', side='top')
        
        # User info
        user_label = ttk.Label(
            top_frame,
            text=f"Welcome, {self.user_data['name']} ({self.user_data['email']})",
            font=('Arial', 11, 'bold')
        )
        user_label.pack(side='left')
        
        # New Session button
        new_session_btn = ttk.Button(
            top_frame,
            text="New Quiz Session",
            command=self.new_session,
            width=15
        )
        new_session_btn.pack(side='right', padx=5)
        
        # Exit button
        exit_btn = ttk.Button(
            top_frame,
            text="Exit",
            command=self.on_closing,
            width=10
        )
        exit_btn.pack(side='right')
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x')
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.quiz_tab = QuizTab(self.notebook, self.user_data)
        self.notebook.add(self.quiz_tab.frame, text="📋 Take Quiz")
        
        self.results_tab = ResultsTab(self.notebook, self.user_data)
        self.notebook.add(self.results_tab.frame, text="📊 My Sessions")
        
        self.formulas_tab = FormulasTab(self.notebook, self.user_data)
        self.notebook.add(self.formulas_tab.frame, text="🧪 Scent Formulas")
        
        self.analytics_tab = AnalyticsTab(self.notebook, self.user_data)
        self.notebook.add(self.analytics_tab.frame, text="📈 Analytics")
        
        self.users_tab = UsersTab(self.notebook, self.user_data)
        self.notebook.add(self.users_tab.frame, text="👥 Users")
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready to start your scent journey!",
            relief='sunken',
            anchor='w'
        )
        self.status_bar.pack(fill='x', side='bottom')
    
    def new_session(self):
        """Start a new quiz session"""
        self.notebook.select(0)  # Switch to quiz tab
        self.quiz_tab.start_new_session()
    
    def on_closing(self):
        """Handle window close event"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
