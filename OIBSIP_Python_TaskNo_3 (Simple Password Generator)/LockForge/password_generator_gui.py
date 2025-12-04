#!/usr/bin/env python3
"""
Random Password Generator - GUI Version
An advanced graphical password generator with security rules and clipboard integration.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import pyperclip
import re

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 LockForge - Advanced Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # Configure style
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10, 'bold'))
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TCheckbutton', font=('Arial', 9))

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="🔐 Advanced Password Generator",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Password Length
        ttk.Label(main_frame, text="Password Length:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=12)
        length_frame = ttk.Frame(main_frame)
        length_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.length_spin = ttk.Spinbox(length_frame, from_=4, to=128, textvariable=self.length_var, width=10)
        self.length_spin.grid(row=0, column=0)
        ttk.Label(length_frame, text="(4-128 characters)").grid(row=0, column=1, padx=(10, 0))

        # Character Types
        ttk.Label(main_frame, text="Character Types:", font=('Arial', 11, 'bold')).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digit_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(main_frame, text="Uppercase Letters (A-Z)", variable=self.upper_var).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(main_frame, text="Lowercase Letters (a-z)", variable=self.lower_var).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(main_frame, text="Digits (0-9)", variable=self.digit_var).grid(
            row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Checkbutton(main_frame, text="Symbols (!@#$%^&*)", variable=self.symbol_var).grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Exclude Characters
        ttk.Label(main_frame, text="Exclude Characters:").grid(row=7, column=0, sticky=tk.W, pady=(20, 5))
        self.exclude_var = tk.StringVar()
        exclude_entry = ttk.Entry(main_frame, textvariable=self.exclude_var, width=30)
        exclude_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=(20, 5))
        ttk.Label(main_frame, text="(Enter characters to exclude, e.g., 0O1lI)",
                 font=('Arial', 8)).grid(row=8, column=1, sticky=tk.W)

        # Security Rules
        ttk.Label(main_frame, text="Security Rules:", font=('Arial', 11, 'bold')).grid(
            row=9, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        self.strong_password_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Enforce Strong Password Rules", variable=self.strong_password_var).grid(
            row=10, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Generate Button
        generate_btn = ttk.Button(main_frame, text="🔄 Generate Password",
                                 command=self.generate_password)
        generate_btn.grid(row=11, column=0, columnspan=2, pady=(20, 10))

        # Password Display
        ttk.Label(main_frame, text="Generated Password:", font=('Arial', 11, 'bold')).grid(
            row=12, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.password_var = tk.StringVar()
        password_frame = ttk.Frame(main_frame)
        password_frame.grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var,
                                       font=('Courier', 12, 'bold'), state='readonly')
        self.password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))

        copy_btn = ttk.Button(password_frame, text="📋 Copy", command=self.copy_to_clipboard, width=8)
        copy_btn.grid(row=0, column=1, padx=(10, 0))

        # Password Strength Indicator
        ttk.Label(main_frame, text="Password Strength:", font=('Arial', 11, 'bold')).grid(
            row=14, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))

        self.strength_var = tk.StringVar(value="Not Generated")
        strength_label = ttk.Label(main_frame, textvariable=self.strength_var,
                                  font=('Arial', 10, 'bold'))
        strength_label.grid(row=15, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Password History
        ttk.Label(main_frame, text="Password History:", font=('Arial', 11, 'bold')).grid(
            row=16, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))

        self.history_text = scrolledtext.ScrolledText(main_frame, height=8, width=50,
                                                     font=('Courier', 9))
        self.history_text.grid(row=17, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Clear History Button
        clear_btn = ttk.Button(main_frame, text="🗑️ Clear History", command=self.clear_history)
        clear_btn.grid(row=18, column=0, columnspan=2, pady=(5, 20))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def generate_password(self):
        try:
            length = self.length_var.get()
            use_upper = self.upper_var.get()
            use_lower = self.lower_var.get()
            use_digits = self.digit_var.get()
            use_symbols = self.symbol_var.get()
            exclude_chars = self.exclude_var.get()
            enforce_strong = self.strong_password_var.get()

            # Validate inputs
            if length < 4:
                messagebox.showerror("Error", "Password length must be at least 4 characters!")
                return

            if not any([use_upper, use_lower, use_digits, use_symbols]):
                messagebox.showerror("Error", "At least one character type must be selected!")
                return

            # Generate password with security rules if enabled
            if enforce_strong:
                password = self.generate_strong_password(length, use_upper, use_lower,
                                                       use_digits, use_symbols, exclude_chars)
            else:
                password = self.generate_basic_password(length, use_upper, use_lower,
                                                      use_digits, use_symbols, exclude_chars)

            if password:
                self.password_var.set(password)
                self.update_strength_indicator(password)
                self.add_to_history(password)
            else:
                messagebox.showerror("Error", "Could not generate password with current settings!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_basic_password(self, length, use_upper, use_lower, use_digits, use_symbols, exclude_chars):
        """Generate a basic random password."""
        charset = ""
        if use_upper:
            charset += string.ascii_uppercase
        if use_lower:
            charset += string.ascii_lowercase
        if use_digits:
            charset += string.digits
        if use_symbols:
            charset += string.punctuation

        # Remove excluded characters
        if exclude_chars:
            charset = ''.join(c for c in charset if c not in exclude_chars)

        if not charset:
            return None

        return ''.join(random.choice(charset) for _ in range(length))

    def generate_strong_password(self, length, use_upper, use_lower, use_digits, use_symbols, exclude_chars):
        """Generate a strong password that meets security requirements."""
        # Ensure minimum requirements for strong password
        if length < 8:
            length = 8
            self.length_var.set(8)

        # Build required character sets
        required_sets = []
        charset = ""

        if use_upper:
            charset += string.ascii_uppercase
            required_sets.append(string.ascii_uppercase)
        if use_lower:
            charset += string.ascii_lowercase
            required_sets.append(string.ascii_lowercase)
        if use_digits:
            charset += string.digits
            required_sets.append(string.digits)
        if use_symbols:
            charset += string.punctuation
            required_sets.append(string.punctuation)

        # Remove excluded characters
        if exclude_chars:
            charset = ''.join(c for c in charset if c not in exclude_chars)
            # Update required sets to exclude characters
            required_sets = [''.join(c for c in s if c not in exclude_chars) for s in required_sets]

        if not charset or not all(required_sets):
            return None

        # Generate password ensuring at least one character from each required set
        password = []

        # Add at least one from each required set
        for char_set in required_sets:
            if char_set:  # Only if set is not empty after exclusions
                password.append(random.choice(char_set))

        # Fill the rest randomly
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(random.choice(charset) for _ in range(remaining_length))

        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        return ''.join(password)

    def update_strength_indicator(self, password):
        """Update the password strength indicator."""
        strength = self.validate_password_strength(password)

        if strength['is_strong']:
            self.strength_var.set("🟢 Strong - Meets all security requirements")
        elif strength['score'] >= 3:
            self.strength_var.set("🟡 Medium - Good but could be stronger")
        else:
            self.strength_var.set("🔴 Weak - Consider adding more character types or length")

    def validate_password_strength(self, password):
        """Validate password strength and return detailed results."""
        result = {
            'length_ok': len(password) >= 8,
            'has_upper': any(c.isupper() for c in password),
            'has_lower': any(c.islower() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_symbol': any(c in string.punctuation for c in password),
            'no_repeats': len(password) == len(set(password)),  # No repeated characters
            'not_sequential': not self.has_sequential_chars(password)
        }

        # Calculate strength score
        score = sum(result.values())
        result['score'] = score
        result['is_strong'] = score >= 5  # Require most criteria

        return result

    def has_sequential_chars(self, password):
        """Check if password contains sequential characters."""
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and
                ord(password[i+2]) == ord(password[i+1]) + 1):
                return True
        return False

    def copy_to_clipboard(self):
        """Copy the generated password to clipboard."""
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    def add_to_history(self, password):
        """Add password to history."""
        current_time = tk.StringVar().get()  # Get current timestamp
        # Since we don't have datetime import, just add the password
        self.history_text.insert(tk.END, f"{password}\n")
        self.history_text.see(tk.END)  # Scroll to bottom

    def clear_history(self):
        """Clear the password history."""
        self.history_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()