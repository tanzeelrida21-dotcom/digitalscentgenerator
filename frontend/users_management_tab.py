"""Users management tab for viewing and deleting users"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.scent_models import User
import psycopg2

class UsersTab:
    def __init__(self, parent, user_data):
        self.user_data = user_data
        self.frame = ttk.Frame(parent)
        self.selected_user_id = None
        
        self.create_widgets()
        self.load_users()
    
    def create_widgets(self):
        """Create users management widgets"""
        # Top controls
        controls_frame = ttk.Frame(self.frame, padding=10)
        controls_frame.pack(fill='x', side='top')
        
        ttk.Label(controls_frame, text="Users Management", font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame,
            text="Refresh",
            command=self.load_users,
            width=10
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame,
            text="Delete Selected User",
            command=self.delete_user,
            width=18
        ).pack(side='right', padx=5)
        
        ttk.Button(
            controls_frame,
            text="Delete All Data",
            command=self.delete_user_data,
            width=15
        ).pack(side='right', padx=5)
        
        # Users list
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('ID', 'Name', 'Email', 'Age', 'Gender', 'Created', 'Sessions')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=18)
        
        self.tree.heading('ID', text='User ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Created', text='Created At')
        self.tree.heading('Sessions', text='Sessions')
        
        self.tree.column('ID', width=80)
        self.tree.column('Name', width=150)
        self.tree.column('Email', width=200)
        self.tree.column('Age', width=80)
        self.tree.column('Gender', width=100)
        self.tree.column('Created', width=180)
        self.tree.column('Sessions', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Info label
        info_label = ttk.Label(
            self.frame,
            text="⚠️ Warning: Deleting a user will also delete all their sessions, responses, formulas, and analytics",
            foreground='red',
            font=('Arial', 9)
        )
        info_label.pack(pady=10)
    
    def load_users(self):
        """Load all users with session count"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='0000',
                database='scentdb'
            )
            cursor = conn.cursor()
            
            # Get users with session count
            cursor.execute("""
                SELECT u.user_id, u.name, u.email, u.age, u.gender, u.created_at,
                       COUNT(s.session_id) as session_count
                FROM Users u
                LEFT JOIN Sessions s ON u.user_id = s.user_id
                GROUP BY u.user_id, u.name, u.email, u.age, u.gender, u.created_at
                ORDER BY u.created_at DESC
            """)
            
            users = cursor.fetchall()
            
            if users:
                for user in users:
                    self.tree.insert('', 'end', values=(
                        user[0],  # user_id
                        user[1],  # name
                        user[2],  # email
                        user[3],  # age
                        user[4],  # gender
                        str(user[5])[:19],  # created_at
                        user[6]  # session_count
                    ))
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
    
    def on_select(self, event):
        """Handle user selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_user_id = item['values'][0]
    
    def delete_user_data(self):
        """Delete all data for selected user"""
        if not self.selected_user_id:
            messagebox.showwarning("Warning", "Please select a user")
            return
        
        # Get user info
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        user_name = item['values'][1]
        user_email = item['values'][2]
        
        if messagebox.askyesno(
            "Confirm Delete All Data",
            f"Are you sure you want to delete ALL DATA for:\n\n{user_name} ({user_email})\n\nThis will delete:\n• All sessions\n• All responses\n• All scent formulas\n• All analytics\n\nBut keep the user account."
        ):
            self.delete_user_related_data(self.selected_user_id, keep_user=True)
    
    def delete_user(self):
        """Delete selected user and all related data"""
        if not self.selected_user_id:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        # Prevent deleting current user
        if self.selected_user_id == self.user_data.get('user_id'):
            messagebox.showerror("Error", "You cannot delete your own account while logged in")
            return
        
        # Get user info
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        user_name = item['values'][1]
        user_email = item['values'][2]
        session_count = item['values'][6]
        
        if messagebox.askyesno(
            "Confirm Delete User",
            f"Are you sure you want to permanently delete:\n\n{user_name} ({user_email})\n\nThis will delete:\n• The user account\n• {session_count} session(s)\n• All responses\n• All scent formulas\n• All analytics\n\nThis action cannot be undone!"
        ):
            self.delete_user_related_data(self.selected_user_id, keep_user=False)
    
    def delete_user_related_data(self, user_id, keep_user=False):
        """Delete user and all related data"""
        try:
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user='postgres',
                password='0000',
                database='scentdb'
            )
            cursor = conn.cursor()
            
            # Delete in correct order due to foreign key constraints
            
            # 1. Delete Analytics
            cursor.execute("DELETE FROM Analytics WHERE user_id = %s", (user_id,))
            analytics_count = cursor.rowcount
            
            # 2. Delete ScentFormula (via session_id)
            cursor.execute("""
                DELETE FROM ScentFormula 
                WHERE session_id IN (SELECT session_id FROM Sessions WHERE user_id = %s)
            """, (user_id,))
            formula_count = cursor.rowcount
            
            # 3. Delete Responses (via session_id)
            cursor.execute("""
                DELETE FROM Responses 
                WHERE session_id IN (SELECT session_id FROM Sessions WHERE user_id = %s)
            """, (user_id,))
            response_count = cursor.rowcount
            
            # 4. Delete Sessions
            cursor.execute("DELETE FROM Sessions WHERE user_id = %s", (user_id,))
            session_count = cursor.rowcount
            
            # 5. Delete User (if not keeping)
            if not keep_user:
                cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            
            conn.commit()
            
            cursor.close()
            conn.close()
            
            action = "User data deleted" if keep_user else "User deleted"
            messagebox.showinfo(
                "Success",
                f"{action} successfully!\n\n"
                f"• {session_count} session(s)\n"
                f"• {response_count} response(s)\n"
                f"• {formula_count} formula(s)\n"
                f"• {analytics_count} analytics record(s)"
            )
            
            self.selected_user_id = None
            self.load_users()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")
            import traceback
            traceback.print_exc()
