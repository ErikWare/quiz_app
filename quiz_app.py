import json
import os
import tkinter as tk
from tkinter import messagebox

# Constants for GUI dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# Styling configurations
BG_COLOR = 'white'
FRAME_BG_COLOR = 'lightgrey'
LABEL_FONT = ('Arial', 12)
LABEL_FONT_BOLD = ('Arial', 12, 'bold')
TITLE_FONT = ('Arial', 16, 'bold')
BUTTON_FONT = ('Arial', 12)
BUTTON_WIDTH = 15
BUTTON_HEIGHT = 2
BUTTON_BG_COLOR = '#4CAF50'       # Green
BUTTON_FG_COLOR = 'white'
SUBMIT_BUTTON_BG = '#f0ad4e'      # Orange
SUBMIT_BUTTON_FG = 'black'
FINISH_BUTTON_BG = '#5cb85c'      # Light Green
FINISH_BUTTON_FG = 'white'
PRACTICE_BUTTON_BG = '#2196F3'    # Blue
PRACTICE_BUTTON_FG = 'white'
EXIT_BUTTON_BG = '#d9534f'        # Red
EXIT_BUTTON_FG = 'white'

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Professional Test Platform")
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.master.configure(bg=BG_COLOR)

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
        self.create_start_screen()

    def get_test_files(self):
        # Get list of *.json files in the /tests folder
        test_folder = 'tests'
        try:
            files = os.listdir(test_folder)
            test_files = [f for f in files if f.endswith('.json')]
            if not test_files:
                messagebox.showerror("Error", "No test files found in the /tests folder.")
            return test_files
        except FileNotFoundError:
            messagebox.showerror("Error", "Tests folder not found. Please create a 'tests' folder and add test files.")
            return []

    def create_start_screen(self):
        self.clear_screen()

        title_label = tk.Label(
            self.master,
            text="Welcome to the Professional Test Platform",
            font=TITLE_FONT,
            bg=BG_COLOR,
            fg='white'
        )
        title_label.pack(pady=20)

        # Test selection dropdown
        if self.test_files:
            selection_frame = tk.Frame(self.master, bg=BG_COLOR)
            selection_frame.pack(pady=10)
            tk.Label(
                selection_frame,
                text="Select a test:",
                font=LABEL_FONT,
                bg=BG_COLOR,
                fg='white'
            ).pack(side='left')
            test_dropdown = tk.OptionMenu(selection_frame, self.selected_test_file, *self.test_files)
            test_dropdown.config(font=LABEL_FONT)
            test_dropdown.pack(side='left')

            # Start Test Button
            start_button = tk.Button(
                self.master,
                text="Start Test",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=BUTTON_BG_COLOR,
                fg=BUTTON_FG_COLOR,
                command=self.start_test
            )
            start_button.pack(pady=10)

            # Practice Test Button
            practice_button = tk.Button(
                self.master,
                text="Practice Test",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=PRACTICE_BUTTON_BG,
                fg=PRACTICE_BUTTON_FG,
                command=self.start_practice_test
            )
            practice_button.pack(pady=10)

            # Exit Button
            exit_button = tk.Button(
                self.master,
                text="Exit",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=EXIT_BUTTON_BG,
                fg=EXIT_BUTTON_FG,
                command=self.master.destroy
            )
            exit_button.pack(pady=10)
        else:
            # No test files available
            error_label = tk.Label(
                self.master,
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
            self.show_question()

    def start_practice_test(self):
        self.practice_mode = True
        self.load_questions()
        if self.questions:
            self.current_question = 0
            self.show_question()

    def show_question(self):
        self.clear_screen()
        if not (0 <= self.current_question < len(self.questions)):
            messagebox.showerror("Error", "Invalid question index.")
            self.main_menu()
            return

        question_data = self.questions[self.current_question]
        question_type = question_data['type']
        question_text = question_data['question']
        options = question_data['options']

        # Top Frame for question and options
        top_frame = tk.Frame(self.master, bg=FRAME_BG_COLOR)
        top_frame.pack(side='top', fill='both', expand=True, padx=20, pady=10)

        # Bottom Frame for rationale or status
        self.bottom_frame = tk.Frame(self.master, bg=FRAME_BG_COLOR)
        self.bottom_frame.pack(side='bottom', fill='both', expand=True, padx=20, pady=10)

        # Display question counter
        counter_label = tk.Label(
            top_frame,
            text=f"Question {self.current_question + 1} of {len(self.questions)}",
            font=LABEL_FONT_BOLD,
            bg=FRAME_BG_COLOR
        )
        counter_label.pack()

        # Display question text
        question_label = tk.Label(
            top_frame,
            text=question_text,
            wraplength=WINDOW_WIDTH - 60,
            justify="left",
            font=LABEL_FONT,
            bg=FRAME_BG_COLOR
        )
        question_label.pack(pady=10)

        # Display answer options
        self.answer_vars = []
        if question_type == 'single':
            selected_value = self.user_answers[self.current_question]['answer'] if self.user_answers[self.current_question] else ""
            self.selected_var = tk.StringVar(value=selected_value)
            for option in options:
                rb = tk.Radiobutton(
                    top_frame,
                    text=option,
                    variable=self.selected_var,
                    value=option,
                    font=LABEL_FONT,
                    bg=FRAME_BG_COLOR,
                    anchor='w',
                    width=50
                )
                rb.pack(anchor='w')
        elif question_type == 'multiple':
            if self.user_answers[self.current_question]:
                previous_selections = self.user_answers[self.current_question]
            else:
                previous_selections = {option: False for option in options}
            for option in options:
                var = tk.BooleanVar(value=previous_selections.get(option, False))
                cb = tk.Checkbutton(
                    top_frame,
                    text=option,
                    variable=var,
                    font=LABEL_FONT,
                    bg=FRAME_BG_COLOR,
                    anchor='w',
                    width=50
                )
                cb.pack(anchor='w')
                self.answer_vars.append((option, var))

        # Navigation buttons
        nav_frame = tk.Frame(top_frame, bg=FRAME_BG_COLOR)
        nav_frame.pack(pady=10)

        if self.current_question > 0:
            prev_button = tk.Button(
                nav_frame,
                text="Previous",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=BUTTON_BG_COLOR,
                fg=BUTTON_FG_COLOR,
                command=self.prev_question
            )
            prev_button.pack(side='left', padx=5)

        # Submit button
        self.submit_button = tk.Button(
            nav_frame,
            text="Submit",
            font=BUTTON_FONT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            bg=SUBMIT_BUTTON_BG,
            fg=SUBMIT_BUTTON_FG,
            command=self.submit_answer
        )
        self.submit_button.pack(side='left', padx=5)

        if self.current_question < len(self.questions) - 1:
            next_button = tk.Button(
                nav_frame,
                text="Next",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=BUTTON_BG_COLOR,
                fg=BUTTON_FG_COLOR,
                command=self.next_question
            )
            next_button.pack(side='left', padx=5)
        else:
            finish_button = tk.Button(
                nav_frame,
                text="Finish Test",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=FINISH_BUTTON_BG,
                fg=FINISH_BUTTON_FG,
                command=self.finish_test
            )
            finish_button.pack(side='left', padx=5)

        # Disable Submit button if already submitted
        if self.current_question in self.submitted_questions and not self.practice_mode:
            self.submit_button.config(state='disabled')
            status_label = tk.Label(
                self.bottom_frame,
                text="Answer Submitted",
                font=LABEL_FONT,
                fg="green",
                bg=FRAME_BG_COLOR
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
            font=LABEL_FONT,
            fg="green",
            bg=FRAME_BG_COLOR
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
            bg=FRAME_BG_COLOR
        )
        result_label.pack(pady=5)

        rationale_text = question_data.get('rationale', 'No rationale provided.')
        rationale_label = tk.Label(
            self.bottom_frame,
            text=f"Rationale:\n{rationale_text}",
            wraplength=WINDOW_WIDTH - 60,
            justify="left",
            font=LABEL_FONT,
            bg=FRAME_BG_COLOR
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
            fg='white'
        )
        summary_label.pack(pady=20)

        # Frame for summary content
        summary_frame = tk.Frame(self.master, bg=BG_COLOR)
        summary_frame.pack(pady=10)

        # Display list of questions with correct/incorrect/incomplete status
        for i, question in enumerate(self.questions):
            if incomplete_questions and i in incomplete_questions:
                status = "Incomplete"
                status_color = "orange"
            elif self.check_answer(i):
                status = "Correct"
                status_color = "green"
                correct_count += 1
            else:
                status = "Incorrect"
                status_color = "red"

            question_summary = tk.Label(
                summary_frame,
                text=f"Question {i+1}: {status}",
                fg=status_color,
                font=LABEL_FONT,
                bg=BG_COLOR
            )
            question_summary.pack(anchor='w')

        result_text = f"You answered {correct_count} out of {total_questions} questions correctly."
        result_label = tk.Label(
            self.master,
            text=result_text,
            font=('Arial', 14),
            bg=BG_COLOR,
            fg='white'
        )
        result_label.pack(pady=10)

        # Navigation buttons
        nav_frame = tk.Frame(self.master, bg=BG_COLOR)
        nav_frame.pack(pady=10)

        if incomplete_questions:
            message_label = tk.Label(
                self.master,
                text="Please complete all questions before finishing the test.",
                fg="orange",
                font=LABEL_FONT,
                bg=BG_COLOR
            )
            message_label.pack()

            back_button = tk.Button(
                nav_frame,
                text="Go Back",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=BUTTON_BG_COLOR,
                fg=BUTTON_FG_COLOR,
                command=self.go_to_incomplete_question
            )
            back_button.pack(side='left', padx=5)
        else:
            # Change Exit button to return to the main menu
            return_button = tk.Button(
                nav_frame,
                text="Return to Home",
                font=BUTTON_FONT,
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                bg=BUTTON_BG_COLOR,
                fg=BUTTON_FG_COLOR,
                command=self.main_menu
            )
            return_button.pack(side='left', padx=5)

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
        for widget in self.master.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()