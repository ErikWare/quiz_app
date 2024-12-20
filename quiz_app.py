import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time  # Added import
import random  # New import

# Constants for GUI dimensions
WINDOW_WIDTH = 600  # Reduced width
WINDOW_HEIGHT = 600  # Kept the same height

# Modern Color Scheme
PRIMARY_COLOR = "#2C3E50"  # Dark blue-gray
SECONDARY_COLOR = "#3498DB"  # Bright blue
ACCENT_COLOR = "#E74C3C"  # Coral red
BG_COLOR = "#ECF0F1"  # Light gray
TEXT_COLOR = "#2C3E50"  # Dark blue-gray
BUTTON_HOVER = "#2980B9"  # Darker blue for hover

# Fonts
TITLE_FONT = ("Helvetica", 28, "bold")  # Increased size
HEADER_FONT = ("Helvetica", 20, "bold")  # Increased size
BUTTON_FONT = ("Helvetica", 14)  # Increased size
TEXT_FONT = ("Helvetica", 15)  # Increased size

QUESTION_FONT = ("Helvetica", 16)  # New global variable for question text size
OPTION_FONT = ("Helvetica", 14)    # New global variable for option text size

# Button Style
BUTTON_STYLE = {
    'fg': 'black',
    'font': BUTTON_FONT,
    'relief': 'flat',
    'padx': 20,
    'pady': 10,
    'borderwidth': 1
}

# Frame Style
FRAME_STYLE = {
    'bg': BG_COLOR,
    'relief': 'solid',
    'padx': 20,
    'pady': 20,
    'borderwidth': 1
}

# Configuration Variables for Results Page
SHOW_CORRECT_ANSWERS = True  # Toggle to show/hide correct answers
SHOW_USER_ANSWERS = True     # Toggle to show/hide user's answers

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SAFe 6.0 PO/PM Practice Test")
        self.master.configure(bg=BG_COLOR)
        self.master.geometry("800x600")  # Set default window size
        
        # Update button style configuration
        style = ttk.Style()
        style.configure('Custom.TButton',
            foreground='black',  # Revert text color to black
            background=BG_COLOR,  # Set button background to match window
            padding=(20, 10),
            font=BUTTON_FONT,
            borderwidth=1,
            relief='raised'  # Simulate rounded borders
        )
        style.map('Custom.TButton',
            foreground=[('active', 'black'), ('pressed', 'black')],  # Keep text black in all states
            background=[('active', BUTTON_HOVER), ('pressed', BUTTON_HOVER)]
        )

        # Initialize variables
        self.current_question = -1  # Start before the first question
        self.user_answers = []
        self.submitted_questions = set()
        self.practice_mode = False  # Flag for practice test mode
        self.test_files = self.get_test_files()
        self.selected_test_file = tk.StringVar()
        if self.test_files:
            self.selected_test_file.set(self.test_files[0])  # Set default selected test
        self.questions = []
        self.after_id = None  # To store the after callback ID
        self.after_id_timer = None  # Initialize after_id_timer
        self.start_time = None  # Ensure start_time is initialized
        self.elapsed_time = "00:00"  # Initialize elapsed time
        self.create_start_screen()

    def get_test_files(self):
        # Get list of *.json files in the /tests folder
        test_folder = os.path.join(os.path.dirname(__file__), 'tests')
        try:
            files = os.listdir(test_folder)
            test_files = sorted([f for f in files if f.endswith('.json')])  # Sort files alphabetically
            if not test_files:
                messagebox.showerror("Error", "No test files found in the /tests folder.")
            return test_files
        except FileNotFoundError:
            messagebox.showerror("Error", "Tests folder not found. Please create a 'tests' folder and add test files.")
            return []

    def create_start_screen(self):
        self.clear_screen()

        # Center content with a main frame
        main_frame = tk.Frame(self.master, **FRAME_STYLE)  # Removed padx=30, pady=30
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Simulate rounded borders
        main_frame.config(relief='groove', borderwidth=2)

        title_label = tk.Label(
            main_frame,
            text="Welcome to SAFe 6.0 Product Owner / \n Product Manager Practice Test",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=(0, 30))

        # Test selection dropdown
        if self.test_files:
            selection_frame = tk.Frame(main_frame, bg=BG_COLOR)
            selection_frame.pack(pady=10)
            tk.Label(
                selection_frame,
                text="Select a test:",
                font=TEXT_FONT,
                bg=BG_COLOR,
                fg=TEXT_COLOR
            ).pack(side='left')
            test_dropdown = tk.OptionMenu(selection_frame, self.selected_test_file, *self.test_files)
            test_dropdown.config(font=TEXT_FONT)
            test_dropdown.pack(side='left')

            # Start Test Button
            start_button = ttk.Button(
                main_frame,
                text="Start Test",
                style='Custom.TButton',
                command=self.start_test
            )
            start_button.pack(pady=10)

            # Practice Test Button
            practice_button = ttk.Button(
                main_frame,
                text="Practice Mode",
                style='Custom.TButton',
                command=self.start_practice_test
            )
            practice_button.pack(pady=10)

            # Exit Button
            exit_button = ttk.Button(
                main_frame,
                text="Exit",
                style='Custom.TButton',
                command=self.master.destroy
            )
            exit_button.pack(pady=10)
        else:
            # No test files available
            error_label = tk.Label(
                main_frame,
                text="No test files available.",
                fg='red',
                bg=BG_COLOR
            )
            error_label.pack(pady=20)

    def load_questions(self):
        test_file_path = os.path.join('tests', self.selected_test_file.get())
        try:
            with open(test_file_path, 'r') as file:
                self.questions = json.load(file)
            random.shuffle(self.questions)  # Shuffle the order of questions
            self.user_answers = [None for _ in self.questions]  # Initialize user answers
            self.submitted_questions = set()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load test file: {e}")
            self.questions = []
            self.user_answers = []
            self.submitted_questions = set()

    def start_test(self):
        self.practice_mode = False
        self.load_questions()
        if self.questions:
            self.current_question = 0
            self.reset_timer()  # Reset the timer for a new test
            self.start_timer()  # Start the timer
            self.show_question()

    def start_practice_test(self):
        # Timer not needed in practice mode
        self.practice_mode = True
        self.load_questions()
        if self.questions:
            self.current_question = 0
            self.show_question()

    def reset_timer(self):
        self.elapsed_time = "00:00"
        if hasattr(self, 'timer_label'):
            self.timer_label.config(text=f"Time: {self.elapsed_time}")
        if self.after_id_timer:
            self.master.after_cancel(self.after_id_timer)
            self.after_id_timer = None

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time:
            elapsed_seconds = int(time.time() - self.start_time)
            minutes = elapsed_seconds // 60
            seconds = elapsed_seconds % 60
            self.elapsed_time = f"{minutes:02d}:{seconds:02d}"
            if hasattr(self, 'timer_label'):
                self.timer_label.config(text=f"Time: {self.elapsed_time}")
            self.after_id_timer = self.master.after(1000, self.update_timer)

    def stop_timer(self):
        self.start_time = None
        if self.after_id_timer:
            self.master.after_cancel(self.after_id_timer)
            self.after_id_timer = None
        if hasattr(self, 'timer_label'):
            self.timer_label.destroy()
            del self.timer_label

    def show_question(self):
        self.clear_screen()
        if not (0 <= self.current_question < len(self.questions)):
            messagebox.showerror("Error", "Invalid question index.")
            self.main_menu()
            return

        # Create and pack the timer label
        if not self.practice_mode:
            if not hasattr(self, 'timer_label'):
                self.timer_label = tk.Label(
                    self.master,
                    text="Time: 00:00",
                    font=TEXT_FONT,
                    bg=BG_COLOR,
                    fg=TEXT_COLOR
                )
                self.timer_label.pack(anchor='ne', padx=10, pady=10)

        question_data = self.questions[self.current_question]
        question_type = question_data['type']
        question_text = question_data['question']
        options = question_data['options']
        random.shuffle(options)  # Shuffle the order of options

        # Top Frame for question and options
        top_frame = tk.Frame(self.master, **FRAME_STYLE)  # Removed padx=20, pady=20
        top_frame.pack(side='top', fill='both', expand=True, padx=30, pady=20)  # Increased padding

        # Bottom Frame for rationale or status
        self.bottom_frame = tk.Frame(self.master, **FRAME_STYLE)  # Removed padx=10, pady=10
        self.bottom_frame.pack(side='bottom', fill='both', expand=True, padx=30, pady=20)  # Increased padding

        # Adjust frame sizes
        top_frame.config(width=int(WINDOW_WIDTH * 2/3), height=200)  # 2/3 of the area
        self.bottom_frame.config(width=int(WINDOW_WIDTH * 1/3), height=100)  # 1/3 of the area

        # Simulate rounded borders by adjusting 'relief' and 'borderwidth'
        top_frame.config(relief='groove', borderwidth=2)
        self.bottom_frame.config(relief='groove', borderwidth=2)

        # Display question counter
        counter_label = tk.Label(
            top_frame,
            text=f"Question {self.current_question + 1} of {len(self.questions)}",
            font=HEADER_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        counter_label.pack()

        # Display question text
        question_label = tk.Label(
            top_frame,
            text=question_text,
            wraplength=WINDOW_WIDTH - 60,  # Increased wraplength for better text wrapping
            justify="left",
            font=QUESTION_FONT,  # Updated font
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        question_label.pack(pady=15, fill='x')  # Ensure label spans the width

        # Label options with letters
        option_labels = ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'h.']

        # Display answer options
        self.answer_vars = []
        if question_type == 'single':
            selected_value = self.user_answers[self.current_question]['answer'] if self.user_answers[self.current_question] else ""
            self.selected_var = tk.StringVar(value=selected_value)
            for idx, option in enumerate(options):
                label = option_labels[idx] if idx < len(option_labels) else f"{idx +1}."
                rb = tk.Radiobutton(
                    top_frame,
                    text=f"{label} {option}",
                    variable=self.selected_var,
                    value=option,
                    font=OPTION_FONT,  # Updated font
                    bg=BG_COLOR,
                    anchor='w',
                    justify='left',  # Ensure text wraps and aligns left
                    wraplength=WINDOW_WIDTH - 100  # Adjust wraplength
                )
                rb.pack(anchor='w', fill='x')  # Ensure radiobutton spans the width
        elif question_type == 'multiple':
            if self.user_answers[self.current_question]:
                previous_selections = self.user_answers[self.current_question]
            else:
                previous_selections = {option: False for option in options}
            for idx, option in enumerate(options):
                label = option_labels[idx] if idx < len(option_labels) else f"{idx +1}."
                var = tk.BooleanVar(value=previous_selections.get(option, False))
                cb = tk.Checkbutton(
                    top_frame,
                    text=f"{label} {option}",
                    variable=var,
                    font=OPTION_FONT,  # Updated font
                    bg=BG_COLOR,
                    anchor='w',
                    justify='left',  # Ensure text wraps and aligns left
                    wraplength=WINDOW_WIDTH - 100  # Adjust wraplength
                )
                cb.pack(anchor='w', fill='x')  # Ensure checkbox spans the width
                self.answer_vars.append((option, var))

        # Navigation buttons positioned at the bottom
        nav_frame = tk.Frame(top_frame, bg=BG_COLOR)
        nav_frame.pack(side='bottom', pady=10)  # Positioned at the bottom

        if self.current_question > 0:
            prev_button = ttk.Button(
                nav_frame,
                text="Previous",
                style='Custom.TButton',
                command=self.prev_question
            )
            prev_button.pack(side='left', padx=5)

        # Submit button
        self.submit_button = ttk.Button(
            nav_frame,
            text="Submit",
            style='Custom.TButton',
            command=self.submit_answer
        )
        self.submit_button.pack(side='left', padx=5)

        if self.current_question < len(self.questions) - 1:
            next_button = ttk.Button(
                nav_frame,
                text="Next",
                style='Custom.TButton',
                command=self.next_question
            )
            next_button.pack(side='left', padx=5)
        else:
            finish_button = ttk.Button(
                nav_frame,
                text="Finish Test",
                style='Custom.TButton',
                command=self.finish_test
            )
            finish_button.pack(side='left', padx=5)

        # Disable Submit button if already submitted
        if self.current_question in self.submitted_questions and not self.practice_mode:
            self.submit_button.config(state='disabled')
            status_label = tk.Label(
                self.bottom_frame,
                text="Answer Submitted",
                font=TEXT_FONT,
                fg="green",
                bg=BG_COLOR
            )
            status_label.pack()

        # If in practice mode and the user has already submitted this question, display the rationale
        if self.practice_mode and self.current_question in self.submitted_questions:
            self.display_rationale()

    def submit_answer(self):
        question_data = self.questions[self.current_question]
        question_type = question_data['type']
        if question_type == 'single':
            selected = self.selected_var.get()
            if selected == '':
                messagebox.showwarning("Warning", "Please select an option before submitting.")
                return
            self.user_answers[self.current_question] = {'answer': selected}
        elif question_type == 'multiple':
            selections = {option: var.get() for option, var in self.answer_vars}
            if not any(selections.values()):
                messagebox.showwarning("Warning", "Please select at least one option before submitting.")
                return
            self.user_answers[self.current_question] = selections

        self.submitted_questions.add(self.current_question)

        # Disable Submit button after submission
        self.submit_button.config(state='disabled')

        if not self.practice_mode:
            # Indicate that the answer has been submitted
            self.display_submission_status()

            # Automatically advance to the next question
            if self.current_question < len(self.questions) - 1:
                self.after_id = self.master.after(1000, self.next_question)  # Wait 1 second before advancing
        else:
            self.display_rationale()

    def display_submission_status(self):
        # Clear the bottom frame
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()

        status_label = tk.Label(
            self.bottom_frame,
            text="Answer Submitted",
            font=TEXT_FONT,
            fg="green",
            bg=BG_COLOR
        )
        status_label.pack()

    def display_rationale(self):
        # Clear the bottom frame
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()

        question_data = self.questions[self.current_question]
        user_correct = self.check_answer(self.current_question)

        if user_correct:
            result_text = "Correct!"
            result_color = "green"
        else:
            result_text = "Incorrect!"
            result_color = "red"

        result_label = tk.Label(
            self.bottom_frame,
            text=result_text,
            fg=result_color,
            font=('Arial', 14, 'bold'),
            bg=BG_COLOR
        )
        result_label.pack(pady=5)

        rationale_text = question_data.get('rationale', 'No rationale provided.')
        rationale_label = tk.Label(
            self.bottom_frame,
            text=f"Rationale:\n{rationale_text}",
            wraplength=WINDOW_WIDTH - 60,
            justify="left",
            font=TEXT_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        rationale_label.pack(pady=5)

    def check_answer(self, index):
        if self.user_answers[index] is None:
            return False  # Question not answered yet
        question = self.questions[index]
        correct_answers = set(question['answer'])
        user_response = self.user_answers[index]

        if question['type'] == 'single':
            return user_response.get('answer') == question['answer'][0]
        elif question['type'] == 'multiple':
            selected_options = {opt for opt, val in user_response.items() if val}
            return selected_options == correct_answers

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            messagebox.showinfo("Info", "You have reached the end of the test.")

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.show_question()

    def finish_test(self):
        # Cancel any pending after callbacks to prevent errors
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.stop_timer()  # Stop and remove the timer
        incomplete_questions = [i for i, ans in enumerate(self.user_answers) if ans is None]
        self.show_summary(incomplete_questions)

    def show_summary(self, incomplete_questions=None):
        self.clear_screen()
        total_questions = len(self.questions)
        correct_count = 0

        summary_label = tk.Label(
            self.master,
            text="Test Summary",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        summary_label.pack(pady=20)

        # Frame for summary statistics
        stats_frame = tk.Frame(self.master, bg=BG_COLOR)
        stats_frame.pack(pady=10)

        # Calculate correct answers
        for i, question in enumerate(self.questions):
            if incomplete_questions and i in incomplete_questions:
                continue
            if self.check_answer(i):
                correct_count += 1

        result_text = f"You answered {correct_count} out of {total_questions} questions correctly."
        percentage = (correct_count / total_questions) * 100
        pass_threshold = 70  # Define passing percentage
        if percentage >= pass_threshold:
            pass_fail_text = f"Score: {percentage:.2f}% - Passed!"
            pass_fail_color = "green"
        else:
            pass_fail_text = f"Score: {percentage:.2f}% - Failed."
            pass_fail_color = "red"

        result_label = tk.Label(
            stats_frame,
            text=result_text,
            font=('Arial', 14),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        result_label.pack(pady=5)

        score_label = tk.Label(
            stats_frame,
            text=pass_fail_text,
            font=('Arial', 16, 'bold'),
            bg=BG_COLOR,
            fg=pass_fail_color
        )
        score_label.pack(pady=5)

        # Display time taken only if not in practice mode
        if not self.practice_mode:
            time_label = tk.Label(
                stats_frame,
                text=f"Time Taken: {self.elapsed_time}",
                font=('Arial', 14),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            )
            time_label.pack(pady=5)

        # Frame for summary content with two panes
        summary_main_frame = tk.Frame(self.master, bg=BG_COLOR)
        summary_main_frame.pack(pady=10, fill='both', expand=True)

        # Left pane: Scrollable list of questions
        list_frame = tk.Frame(summary_main_frame, bg=BG_COLOR, borderwidth=2, relief='groove')  # Darkened borders
        list_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        canvas = tk.Canvas(list_frame, bg=BG_COLOR)
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate the scrollable list with questions
        for i, question in enumerate(self.questions):
            if incomplete_questions and i in incomplete_questions:
                status = "Incomplete"
                status_color = "orange"
            elif self.check_answer(i):
                status = "Correct"
                status_color = "green"
            else:
                status = "Incorrect"
                status_color = "red"

            btn = tk.Button(
                scrollable_frame,
                text=f"Question {i+1}: {status}",
                fg=status_color,
                bg=BG_COLOR,
                font=TEXT_FONT,
                anchor='w',
                relief='flat',
                command=lambda idx=i: self.display_question_detail(idx)
            )
            btn.pack(fill='x', pady=2)

        # Right pane: Detail view for selected question
        detail_frame = tk.Frame(summary_main_frame, bg=BG_COLOR, borderwidth=2, relief='groove')  # Darkened borders
        detail_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.detail_label = tk.Label(
            detail_frame,
            text="Select a question to view details.",
            wraplength=WINDOW_WIDTH - 150,
            justify="left",
            font=TEXT_FONT,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.detail_label.pack(pady=5, fill='both', expand=True)

        # Navigation buttons
        nav_frame = tk.Frame(self.master, bg=BG_COLOR)
        nav_frame.pack(pady=10)

        if incomplete_questions:
            message_label = tk.Label(
                self.master,
                text="Please complete all questions before finishing the test.",
                fg="orange",
                font=TEXT_FONT,
                bg=BG_COLOR
            )
            message_label.pack()

            back_button = ttk.Button(
                nav_frame,
                text="Go Back",
                style='Custom.TButton',
                command=self.go_to_incomplete_question
            )
            back_button.pack(side='left', padx=5)
        else:
            # Change Exit button to return to the main menu
            return_button = ttk.Button(
                nav_frame,
                text="Return to Home",
                style='Custom.TButton',
                command=self.main_menu
            )
            return_button.pack(side='left', padx=5)

    def display_question_detail(self, question_index):
        question = self.questions[question_index]
        rationale = question.get('rationale', 'No rationale provided.')
        question_text = question['question']
        options = question['options']
        correct_answers = question['answer']  # Assuming 'answer' holds correct option(s)

        # Label options with letters
        option_labels = ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.', 'h.']
        labeled_options = []
        for idx, option in enumerate(options):
            label = option_labels[idx] if idx < len(option_labels) else f"{idx +1}."
            labeled_options.append(f"{label} {option}")

        # Determine correct option letters
        correct_labels = []
        for idx, option in enumerate(options):
            if option in correct_answers:
                label = option_labels[idx] if idx < len(option_labels) else f"{idx +1}."
                correct_labels.append(label)

        # Determine user's selected answers
        user_answer = self.user_answers[question_index]
        user_selected = []
        if question['type'] == 'single':
            selected_option = user_answer.get('answer') if user_answer else None
            if selected_option:
                try:
                    idx = options.index(selected_option)
                    label = option_labels[idx] if idx < len(option_labels) else f"{idx +1}."
                    user_selected.append(label)
                except ValueError:
                    pass
        elif question['type'] == 'multiple':
            for option, selected in user_answer.items():
                if selected:
                    try:
                        idx = options.index(option)
                        label = option_labels[idx] if idx < len(option_labels) else f"{idx +1}."
                        user_selected.append(label)
                    except ValueError:
                        pass

        # Build detail text
        detail_text = f"Question {question_index +1}:\n{question_text}\n\nOptions:\n"
        for lbl_option in labeled_options:
            detail_text += f"{lbl_option}\n"
        detail_text += f"\nRationale:\n{rationale}\n\n"

        if SHOW_CORRECT_ANSWERS:
            correct_str = ', '.join(correct_labels)
            detail_text += f"Correct Answer(s): {correct_str}\n"

        if SHOW_USER_ANSWERS and user_selected:
            user_str = ', '.join(user_selected)
            detail_text += f"Your Answer(s): {user_str}\n"

        self.detail_label.config(text=detail_text)

    def go_to_incomplete_question(self):
        # Go back to the first incomplete question
        incomplete_questions = [i for i, ans in enumerate(self.user_answers) if ans is None]
        if incomplete_questions:
            self.current_question = incomplete_questions[0]
            self.show_question()
        else:
            self.finish_test()

    def main_menu(self):
        # Cancel any pending after callbacks to prevent errors
        if self.after_id is not None:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        # Reset variables for new test
        self.current_question = -1
        self.user_answers = []
        self.submitted_questions = set()
        self.practice_mode = False
        self.questions = []
        self.create_start_screen()

    def clear_screen(self):
        # Clear all widgets except the timer_label
        for widget in self.master.winfo_children():
            if widget != getattr(self, 'timer_label', None):
                widget.destroy()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()