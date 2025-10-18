import tkinter as tk
from tkinter import messagebox
import time
import random


class TypingSpeedTest:
    def __init__(self, window):
        self.window = window
        self.window.title("Typing Speed Test")
        self.window.geometry("850x580")
        self.window.config(bg="#BBDCE5")

        # Sample texts for the typing test
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog. This sentence contains all the letter in the English alphabet.",
            "Programming is the process of creating a set of instructions that tell a computer how to perform a task.",
            "Typing speed is measured in words per minute, which is often abbreviated as WPM in the keyboarding world.",
            "Practice makes perfect. Consistent practice will help you improve your typing speed and accuracy over time.",
            "The best way to learn touch typing is to use all ten fingers and not look at the keyboard while typing."
        ]

        self.current_text = ""
        self.start_time = None
        self.running = False
        self.elapsed_time = 0
        self.correct_chars = 0
        self.total_chars = 0

        self.setup_ui()
        self.new_text()

    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.window, text="Typing Speed Test",
                              font=("Arial", 20, "bold"),
                              fg="#2A4B6A", bg="#BBDCE5")
        title_label.pack(pady=(20, 5))

        # Instruction label
        instruction_label = tk.Label(self.window, text="Start typing the text below:",
                                    font=("Arial", 12), fg="#2A4B6A", bg="#BBDCE5")
        instruction_label.pack(pady=10)

        # Sample text frame with border
        sample_frame = tk.Frame(self.window, relief="solid", borderwidth=2)
        sample_frame.pack(pady=10, padx=20, fill="both")

        self.sample_label = tk.Label(sample_frame, text="", font=("Arial", 14),
                                     wraplength=800, justify="left", fg="#2A4B6A")
        self.sample_label.pack(pady=20, padx=20)

        # Text entry frame with border
        text_frame = tk.Frame(self.window, bg="#F0F0F0", relief="solid", borderwidth=2)
        text_frame.pack(pady=10, padx=20, fill="both")

        self.text_entry = tk.Text(text_frame, height=2, font=("Arial", 14),
                                  wrap="word", relief="flat", borderwidth=2,
                                  fg="#2A4B6A", bg="#F0F0F0", padx=10, pady=10)
        self.text_entry.pack(pady=10, padx=20, fill="both")
        self.text_entry.bind("<KeyPress>", self.start_timer)
        self.text_entry.bind("<KeyRelease>", self.check_typing)

        # Metrics frame for timer and WPM
        metrics_frame = tk.Frame(self.window, bg="#BBDCE5")
        metrics_frame.pack(pady=20)

        # Timer label
        self.timer_label = tk.Label(metrics_frame, text="Time: 0s",
                                    font=("Arial", 14, "bold"),
                                    fg="#2A4B6A", bg="#BBDCE5")
        self.timer_label.pack(side="left", pady=30)

        # WPM label
        self.wpm_label = tk.Label(metrics_frame, text="WPM: 0",
                                  font=("Arial", 14, "bold"),
                                  fg="#2A4B6A", bg="#BBDCE5")
        self.wpm_label.pack(side="left", padx=30, )

        # Reset button
        button_frame = tk.Frame(self.window, bg="#BBDCE5")
        button_frame.pack(fill="x", pady=40)

        self.reset_button = tk.Button(button_frame, text="Reset",
                                      font=("Arial", 14, "bold"),
                                      fg="#2A4B6A", bg="#FFC0CB",
                                      command=self.reset_test)
        self.reset_button.pack(side="right", padx=20)

    def new_text(self):
        self.current_text = random.choice(self.sample_texts)
        self.sample_label.config(text=self.current_text)
        self.text_entry.delete(1.0, tk.END)
        self.correct_chars = 0
        self.total_chars = 0
        self.update_colors()

    def start_timer(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()

    def update_timer(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {int(self.elapsed_time)}s")

            # Calculate WPM (assuming 5 characters per word)
            if self.elapsed_time > 0:
                wpm = (self.correct_chars / 5) / (self.elapsed_time / 60)
                self.wpm_label.config(text=f"WPM: {int(wpm)}")

            self.window.after(100, self.update_timer)

    def check_typing(self, event):
        typed_text = self.text_entry.get(1.0, tk.END).strip()
        self.total_chars = len(typed_text)

        # Count correct characters
        self.correct_chars = 0
        for i, (typed_char, correct_char) in enumerate(zip(typed_text, self.current_text)):
            if typed_char == correct_char:
                self.correct_chars += 1

        # Check if text is completed
        if typed_text == self.current_text:
            self.running = False
            wpm = (self.correct_chars / 5) / (self.elapsed_time / 60)
            messagebox.showinfo("Completed", f"Your typing speed: {int(wpm)} WPM")
            self.reset_test()

        self.update_colors()

    def update_colors(self):
        # Update text colors based on correctness
        typed_text = self.text_entry.get(1.0, tk.END).strip()

        # Configure tag for correct and incorrect text
        self.text_entry.tag_configure("correct", foreground="green")
        self.text_entry.tag_configure("incorrect", foreground="red")

        # Remove previous tags
        self.text_entry.tag_remove("correct", 1.0, tk.END)
        self.text_entry.tag_remove("incorrect", 1.0, tk.END)

        # Apply tags based on correctness
        for i, (typed_char, correct_char) in enumerate(zip(typed_text, self.current_text)):
            if typed_char == correct_char:
                self.text_entry.tag_add("correct", f"1.{i}", f"1.{i + 1}")
            else:
                self.text_entry.tag_add("incorrect", f"1.{i}", f"1.{i + 1}")

    def reset_test(self):
        self.running = False
        self.elapsed_time = 0
        self.timer_label.config(text="Time: 0s")
        self.wpm_label.config(text="WPM: 0")
        self.new_text()


if __name__ == "__main__":
    window = tk.Tk()
    app = TypingSpeedTest(window)
    window.mainloop()
