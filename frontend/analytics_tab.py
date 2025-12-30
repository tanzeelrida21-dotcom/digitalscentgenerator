"""Analytics tab for viewing quiz analytics"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.scent_models import Analytics

class AnalyticsTab:
    def __init__(self, parent, user_data):
        self.user_data = user_data
        self.frame = ttk.Frame(parent)
        
        self.create_widgets()
        self.load_analytics()
    
    def create_widgets(self):
        """Create analytics tab widgets"""
        # Top controls
        controls_frame = ttk.Frame(self.frame, padding=10)
        controls_frame.pack(fill='x', side='top')
        
        ttk.Label(controls_frame, text="Quiz Analytics", font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame,
            text="Refresh",
            command=self.load_analytics,
            width=10
        ).pack(side='left', padx=5)
        
        # Analytics list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('ID', 'User', 'Session', 'Questions', 'Time (sec)', 'Popular Scent', 'Date')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=18)
        
        self.tree.heading('ID', text='Analytics ID')
        self.tree.heading('User', text='User')
        self.tree.heading('Session', text='Session ID')
        self.tree.heading('Questions', text='Total Questions')
        self.tree.heading('Time (sec)', text='Completion Time')
        self.tree.heading('Popular Scent', text='Most Popular Scent')
        self.tree.heading('Date', text='Date')
        
        self.tree.column('ID', width=100)
        self.tree.column('User', width=150)
        self.tree.column('Session', width=100)
        self.tree.column('Questions', width=120)
        self.tree.column('Time (sec)', width=140)
        self.tree.column('Popular Scent', width=150)
        self.tree.column('Date', width=180)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def load_analytics(self):
        """Load analytics data"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        analytics = Analytics.get_all()
        
        if analytics:
            for analytic in analytics:
                self.tree.insert('', 'end', values=(
                    analytic[0],  # analytics_id
                    analytic[7],  # user_name
                    analytic[2],  # session_id
                    analytic[3],  # total_questions
                    analytic[4],  # completion_time
                    analytic[8] if len(analytic) > 8 else 'N/A',  # popular_scent
                    str(analytic[6])[:19]  # created_at
                ))
