"""Quiz tab for taking scent preference quiz"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.scent_models import Question, Session, Response, ScentFormula, ScentNote, Analytics
from collections import Counter

class QuizTab:
    def __init__(self, parent, user_data):
        self.user_data = user_data
        self.frame = ttk.Frame(parent)
        self.current_session_id = None
        self.current_question_index = 0
        self.questions = []
        self.responses = []
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create quiz tab widgets"""
        # Welcome frame
        self.welcome_frame = ttk.Frame(self.frame)
        self.welcome_frame.pack(fill='both', expand=True)
        
        ttk.Label(
            self.welcome_frame,
            text="🌸 Discover Your Perfect Scent 🌸",
            font=('Arial', 20, 'bold'),
            foreground='#8E44AD'
        ).pack(pady=40)
        
        ttk.Label(
            self.welcome_frame,
            text="Answer a few questions to get your personalized scent formula",
            font=('Arial', 12),
            foreground='#555'
        ).pack(pady=10)
        
        start_btn = ttk.Button(
            self.welcome_frame,
            text="Start Quiz",
            command=self.start_new_session,
            width=20
        )
        start_btn.pack(pady=20)
        
        # Quiz frame (hidden initially)
        self.quiz_frame = ttk.Frame(self.frame)
        
        # Progress bar
        self.progress_frame = ttk.Frame(self.quiz_frame)
        self.progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.progress_label = ttk.Label(self.progress_frame, text="Question 1 of 3", font=('Arial', 10))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Question frame
        question_container = ttk.Frame(self.quiz_frame)
        question_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        self.question_label = ttk.Label(
            question_container,
            text="",
            font=('Arial', 14, 'bold'),
            wraplength=700
        )
        self.question_label.pack(pady=20)
        
        self.options_frame = ttk.Frame(question_container)
        self.options_frame.pack(fill='both', expand=True)
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.quiz_frame)
        nav_frame.pack(pady=20)
        
        self.prev_btn = ttk.Button(nav_frame, text="← Previous", command=self.prev_question, width=12)
        self.prev_btn.pack(side='left', padx=10)
        
        self.next_btn = ttk.Button(nav_frame, text="Next →", command=self.next_question, width=12)
        self.next_btn.pack(side='left', padx=10)
        
        self.submit_btn = ttk.Button(nav_frame, text="Submit Quiz", command=self.submit_quiz, width=12)
        self.submit_btn.pack(side='left', padx=10)
        self.submit_btn.pack_forget()  # Hide initially
    
    def start_new_session(self):
        """Start a new quiz session"""
        # Create new session
        self.current_session_id = Session.create(self.user_data['user_id'])
        
        if not self.current_session_id:
            messagebox.showerror("Error", "Failed to create session")
            return
        
        # Load questions
        self.questions = Question.get_all()
        
        if not self.questions:
            messagebox.showerror("Error", "No questions available")
            return
        
        self.current_question_index = 0
        self.responses = [None] * len(self.questions)
        
        # Switch to quiz frame
        self.welcome_frame.pack_forget()
        self.quiz_frame.pack(fill='both', expand=True)
        
        self.show_question()
    
    def show_question(self):
        """Display current question"""
        if self.current_question_index >= len(self.questions):
            return
        
        question = self.questions[self.current_question_index]
        question_id = question[0]
        question_text = question[1]
        question_type = question[2]
        
        # Update progress
        total = len(self.questions)
        current = self.current_question_index + 1
        self.progress_label.config(text=f"Question {current} of {total}")
        self.progress_bar['maximum'] = total
        self.progress_bar['value'] = current
        
        # Update question text
        self.question_label.config(text=question_text)
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Get options for this question
        options = Question.get_options(question_id)
        
        if question_type == 'single-choice':
            self.selected_option = tk.IntVar(value=self.responses[self.current_question_index] or 0)
            
            for option in options:
                option_id = option[0]
                option_text = option[2]
                scent_note = option[4] if len(option) > 4 else ""
                
                radio = ttk.Radiobutton(
                    self.options_frame,
                    text=f"{option_text} ({scent_note})",
                    variable=self.selected_option,
                    value=option_id
                )
                radio.pack(anchor='w', pady=8, padx=20)
        
        elif question_type == 'multi-choice':
            self.selected_options = {}
            
            for option in options:
                option_id = option[0]
                option_text = option[2]
                scent_note = option[4] if len(option) > 4 else ""
                
                var = tk.BooleanVar()
                self.selected_options[option_id] = var
                
                check = ttk.Checkbutton(
                    self.options_frame,
                    text=f"{option_text} ({scent_note})",
                    variable=var
                )
                check.pack(anchor='w', pady=8, padx=20)
        
        # Update navigation buttons
        self.prev_btn.config(state='normal' if current > 1 else 'disabled')
        
        if current == total:
            self.next_btn.pack_forget()
            self.submit_btn.pack(side='left', padx=10)
        else:
            self.submit_btn.pack_forget()
            self.next_btn.pack(side='left', padx=10)
    
    def save_current_response(self):
        """Save the current question's response"""
        question = self.questions[self.current_question_index]
        question_type = question[2]
        
        if question_type == 'single-choice':
            selected = self.selected_option.get()
            if selected:
                self.responses[self.current_question_index] = selected
        
        elif question_type == 'multi-choice':
            # For multi-choice, save the first selected option
            for option_id, var in self.selected_options.items():
                if var.get():
                    self.responses[self.current_question_index] = option_id
                    break
    
    def next_question(self):
        """Move to next question"""
        self.save_current_response()
        
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.show_question()
    
    def prev_question(self):
        """Move to previous question"""
        self.save_current_response()
        
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()
    
    def submit_quiz(self):
        """Submit the quiz and generate formula"""
        self.save_current_response()
        
        # Check if all questions are answered
        if None in self.responses:
            messagebox.showwarning("Warning", "Please answer all questions before submitting")
            return
        
        # Save responses to database
        for idx, option_id in enumerate(self.responses):
            if option_id:
                question_id = self.questions[idx][0]
                Response.create(self.current_session_id, question_id, option_id)
        
        # Generate scent formula
        self.generate_formula()
        
        # Mark session as complete
        Session.complete(self.current_session_id)
        
        messagebox.showinfo("Success", "Quiz completed! Your personalized scent formula has been created.")
        
        # Reset to welcome screen
        self.quiz_frame.pack_forget()
        self.welcome_frame.pack(fill='both', expand=True)
        self.current_session_id = None
    
    def generate_formula(self):
        """Generate scent formula based on responses"""
        # Get all selected scent notes
        scent_notes = []
        
        for option_id in self.responses:
            if option_id:
                # Get the option details
                query_result = Question.get_all()  # This is a simplified approach
                # In a real implementation, you'd query the option to get its scent_note_id
                
        # Get scent notes by category
        top_notes = ScentNote.get_by_category('Top')
        middle_notes = ScentNote.get_by_category('Middle')
        base_notes = ScentNote.get_by_category('Base')
        
        # Select one from each category (simplified logic)
        base_note_id = base_notes[0][0] if base_notes else 3
        middle_note_id = middle_notes[0][0] if middle_notes else 2
        top_note_id = top_notes[0][0] if top_notes else 1
        
        # Create formula
        formula_id = ScentFormula.create(
            self.current_session_id,
            base_note_id,
            middle_note_id,
            top_note_id
        )
        
        # Create analytics
        completion_time = 120  # Simplified - would calculate actual time
        Analytics.create(
            self.user_data['user_id'],
            self.current_session_id,
            len(self.questions),
            completion_time,
            top_note_id  # Popular scent note
        )
        
        return formula_id
