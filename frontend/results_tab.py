"""Results tab for viewing quiz sessions"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.scent_models import Session, Response, ScentFormula

class ResultsTab:
    def __init__(self, parent, user_data):
        self.user_data = user_data
        self.frame = ttk.Frame(parent)
        self.selected_session_id = None
        
        self.create_widgets()
        self.load_sessions()
    
    def create_widgets(self):
        """Create results tab widgets"""
        # Top controls
        controls_frame = ttk.Frame(self.frame, padding=10)
        controls_frame.pack(fill='x', side='top')
        
        ttk.Label(controls_frame, text="My Quiz Sessions", font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame,
            text="Refresh",
            command=self.load_sessions,
            width=10
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame,
            text="View Details",
            command=self.view_session_details,
            width=12
        ).pack(side='right', padx=5)
        
        ttk.Button(
            controls_frame,
            text="View Formula",
            command=self.view_formula,
            width=12
        ).pack(side='right', padx=5)
        
        # Sessions list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Session ID', 'Started', 'Completed', 'Status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('Session ID', text='Session ID')
        self.tree.heading('Started', text='Started At')
        self.tree.heading('Completed', text='Completed At')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('Session ID', width=100)
        self.tree.column('Started', width=200)
        self.tree.column('Completed', width=200)
        self.tree.column('Status', width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-Button-1>', lambda e: self.view_session_details())
    
    def load_sessions(self):
        """Load user's sessions"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sessions = Session.get_by_user(self.user_data['user_id'])
        
        if sessions:
            for session in sessions:
                status = 'Completed' if session[3] else 'In Progress'
                completed_str = str(session[3])[:19] if session[3] else 'N/A'
                
                self.tree.insert('', 'end', values=(
                    session[0],  # session_id
                    str(session[2])[:19],  # started_at
                    completed_str,  # completed_at
                    status
                ))
    
    def on_select(self, event):
        """Handle session selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_session_id = item['values'][0]
    
    def view_session_details(self):
        """View session responses"""
        if not self.selected_session_id:
            messagebox.showwarning("Warning", "Please select a session")
            return
        
        responses = Response.get_by_session(self.selected_session_id)
        
        if responses:
            details = f"Session #{self.selected_session_id} - Responses:\n\n"
            
            for response in responses:
                question_text = response[4]
                option_text = response[5]
                scent_note = response[6] if len(response) > 6 else 'N/A'
                
                details += f"Q: {question_text}\n"
                details += f"A: {option_text} ({scent_note})\n\n"
            
            # Show in a new window
            self.show_details_window(details)
        else:
            messagebox.showinfo("Info", "No responses found for this session")
    
    def show_details_window(self, details):
        """Show details in a new window"""
        details_window = tk.Toplevel(self.frame)
        details_window.title(f"Session Details - #{self.selected_session_id}")
        details_window.geometry("600x500")
        
        text_widget = tk.Text(details_window, wrap='word', font=('Arial', 10), padx=10, pady=10)
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', details)
        text_widget.config(state='disabled')
        
        ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
    
    def view_formula(self):
        """View scent formula for session"""
        if not self.selected_session_id:
            messagebox.showwarning("Warning", "Please select a session")
            return
        
        formula = ScentFormula.get_by_session(self.selected_session_id)
        
        if formula and len(formula) > 0:
            f = formula[0]
            
            formula_text = f"""
🧪 Your Personalized Scent Formula 🧪

Base Note: {f[5]} (Foundation of the scent)
Middle Note: {f[6]} (Heart of the fragrance)
Top Note: {f[7]} (First impression)

Created: {str(f[4])[:19]}

This unique combination has been crafted based on your 
preferences to create a perfectly balanced fragrance just for you!
            """
            
            messagebox.showinfo("Your Scent Formula", formula_text)
        else:
            messagebox.showinfo("Info", "No formula found for this session")
