"""User entry window for Scent Quiz System"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.scent_models import User
import re

class UserEntryWindow:
    def __init__(self, parent, on_success_callback):
        self.on_success = on_success_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Scent Quiz - User Entry")
        self.window.geometry("450x400")
        self.window.resizable(False, False)
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"450x400+{x}+{y}")
        
        self.create_widgets()
        
        # Force window to front
        self.window.lift()
        self.window.focus_force()
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))
        
        self.window.transient(parent)
        self.window.grab_set()
    
    def create_widgets(self):
        """Create user entry form widgets"""
        # Title
        title_label = tk.Label(
            self.window, 
            text="Welcome to Scent Quiz", 
            font=('Arial', 18, 'bold'),
            fg='#2C3E50'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.window,
            text="Discover your perfect scent formula",
            font=('Arial', 10),
            fg='#7F8C8D'
        )
        subtitle_label.pack(pady=5)
        
        # Frame for form
        form_frame = ttk.Frame(self.window, padding=20)
        form_frame.pack(expand=True)
        
        # Name
        ttk.Label(form_frame, text="Name:", font=('Arial', 10)).grid(
            row=0, column=0, sticky='w', pady=8
        )
        self.name_entry = ttk.Entry(form_frame, width=30, font=('Arial', 10))
        self.name_entry.grid(row=0, column=1, pady=8, padx=10)
        self.name_entry.focus()
        
        # Email
        ttk.Label(form_frame, text="Email:", font=('Arial', 10)).grid(
            row=1, column=0, sticky='w', pady=8
        )
        self.email_entry = ttk.Entry(form_frame, width=30, font=('Arial', 10))
        self.email_entry.grid(row=1, column=1, pady=8, padx=10)
        
        # Age
        ttk.Label(form_frame, text="Age:", font=('Arial', 10)).grid(
            row=2, column=0, sticky='w', pady=8
        )
        self.age_spinbox = ttk.Spinbox(form_frame, from_=13, to=100, width=28, font=('Arial', 10))
        self.age_spinbox.set(25)
        self.age_spinbox.grid(row=2, column=1, pady=8, padx=10)
        
        # Gender
        ttk.Label(form_frame, text="Gender:", font=('Arial', 10)).grid(
            row=3, column=0, sticky='w', pady=8
        )
        self.gender_var = tk.StringVar(value='Female')
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=3, column=1, pady=8, sticky='w', padx=10)
        
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value='Female').pack(side='left', padx=5)
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value='Male').pack(side='left', padx=5)
        ttk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value='Other').pack(side='left', padx=5)
        
        # Buttons frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Start Quiz button
        start_btn = ttk.Button(
            button_frame, 
            text="Start Quiz", 
            command=self.start_quiz,
            width=15
        )
        start_btn.pack(side='left', padx=5)
        
        # Existing User button
        existing_btn = ttk.Button(
            button_frame, 
            text="Existing User", 
            command=self.show_existing_users,
            width=15
        )
        existing_btn.pack(side='left', padx=5)
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def start_quiz(self):
        """Handle start quiz"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        age = self.age_spinbox.get()
        gender = self.gender_var.get()
        
        # Validation
        if not name or not email:
            messagebox.showerror("Error", "Please enter your name and email")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        try:
            age = int(age)
            if age < 13 or age > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age (13-100)")
            return
        
        # Check if user exists
        existing_user = User.get_by_email(email)
        
        if existing_user and len(existing_user) > 0:
            user_data = {
                'user_id': existing_user[0][0],
                'name': existing_user[0][1],
                'email': existing_user[0][2],
                'age': existing_user[0][3],
                'gender': existing_user[0][4]
            }
        else:
            # Create new user
            user_id = User.create(name, email, age, gender)
            
            if not user_id:
                messagebox.showerror("Error", "Failed to create user. Please try again.")
                return
            
            user_data = {
                'user_id': user_id,
                'name': name,
                'email': email,
                'age': age,
                'gender': gender
            }
        
        self.window.destroy()
        self.on_success(user_data)
    
    def show_existing_users(self):
        """Show list of existing users"""
        ExistingUsersWindow(self.window, self.select_existing_user)
    
    def select_existing_user(self, user_data):
        """Callback when existing user is selected"""
        self.window.destroy()
        self.on_success(user_data)
    
    def destroy(self):
        """Close the window"""
        self.window.destroy()

class ExistingUsersWindow:
    def __init__(self, parent, on_select_callback):
        self.on_select = on_select_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Select Existing User")
        self.window.geometry("600x400")
        
        # Center window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"600x400+{x}+{y}")
        
        self.create_widgets()
        self.load_users()
        
        self.window.transient(parent)
        self.window.grab_set()
    
    def create_widgets(self):
        """Create widgets"""
        ttk.Label(
            self.window,
            text="Select Your Profile",
            font=('Arial', 14, 'bold')
        ).pack(pady=10)
        
        # Users list
        list_frame = ttk.Frame(self.window)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Name', 'Email', 'Age', 'Gender')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Gender', text='Gender')
        
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=150)
        self.tree.column('Email', width=200)
        self.tree.column('Age', width=80)
        self.tree.column('Gender', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<Double-Button-1>', lambda e: self.select_user())
        
        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Select", command=self.select_user, width=12).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy, width=12).pack(side='left', padx=5)
    
    def load_users(self):
        """Load all users"""
        users = User.get_all()
        
        if users:
            for user in users:
                self.tree.insert('', 'end', values=(
                    user[0], user[1], user[2], user[3], user[4]
                ))
    
    def select_user(self):
        """Select a user"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        user_data = {
            'user_id': values[0],
            'name': values[1],
            'email': values[2],
            'age': values[3],
            'gender': values[4]
        }
        
        self.window.destroy()
        self.on_select(user_data)
