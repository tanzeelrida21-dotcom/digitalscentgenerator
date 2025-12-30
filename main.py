"""Main application entry point with GUI"""

import tkinter as tk
from tkinter import ttk, messagebox
import traceback
import sys

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scent Quiz System")
        # Don't withdraw initially - keep it visible
        
        # Initialize database connection pool
        try:
            from database.db_config import initialize_pool
            from frontend.user_entry_window import UserEntryWindow
            
            initialize_pool()
            print("Database connection initialized successfully")
            
            # Show user entry window
            self.user_entry_window = UserEntryWindow(self.root, self.on_user_entry_success)
            print("User entry window created successfully")
            
            # Now hide the main root window after entry window is created
            self.root.withdraw()
            
        except Exception as e:
            error_msg = f"Failed to start application.\n\nError: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Application Error", error_msg)
            self.root.destroy()
            sys.exit(1)
    
    def on_user_entry_success(self, user_data):
        """Callback when user enters successfully"""
        try:
            # Import here to avoid circular imports
            from frontend.scent_main_window import ScentMainWindow
            self.main_window = ScentMainWindow(self.root, user_data)
            self.root.deiconify()  # Show main window
        except Exception as e:
            error_msg = f"Failed to open main window.\n\nError: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Application Error", error_msg)
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            error_msg = f"Application error.\n\nError: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            messagebox.showerror("Application Error", error_msg)

if __name__ == '__main__':
    try:
        print("Starting SCD Application...")
        print("Python version:", sys.version)
        app = MainApp()
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        print(traceback.format_exc())
        input("Press Enter to exit...")
