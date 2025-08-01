"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 30/12/2024

Module to Create the GUI of Spell Checking System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as scrolledtext

from Class.dictionary_builder import DictionaryBuilder
from Class.spell_check_model import SpellCheckModel
from Class.tokens_cleaning import TokenCleaner

class SpellCheckerGUI(tk.Tk):
    
    def __init__(self):

        # Initialise Tkinter
        super().__init__()
        print("Starting...")
        
        # Title of the GUI
        self.title("Spelling Correction System for Psychology")
        # Size of the window
        self.geometry("900x700")
        # Background colour
        self.configure(bg="#f5f5f5")


        # Build and Obtain the dictionary
        self.dictionary_builder = DictionaryBuilder()
        self.dict = self.dictionary_builder.get_sorted_dict()
        self.psy_dict = self.dictionary_builder.get_psy_dict()


        # Build the model
        self.error_detection_model = SpellCheckModel(
            self.dict, self.psy_dict, bi_weight = 0.3, bi_right_weight = 0.15,
            tri_weight = 0.55, threshold = -12
        )


        # Initialize the GUI layout
        self.create_layout()
        print("\n Ready \n")


    # Setup the layout for the Tkinter interface
    def create_layout(self):
        
        # Title label
        self.create_title_label()
        
        # Main content frame
        main_frame = tk.Frame(self, bg = "#f5f5f5")
        main_frame.pack(expand=True, fill = "both", padx = 20, pady = 20)
        
        # Create Left and Right Panels
        self.create_left_panel(main_frame)
        self.create_right_panel(main_frame)


    # Title of the system
    def create_title_label(self):
        title = tk.Label(
            self, text = "Spelling Correction System - Psychology",
            bg="#7aa6c7", fg="white", font = ("Helvetica", 20, "bold"),
            pady=10
        )

        title.pack(fill = "x")

    # Left Panel : Instructions & Dictionary
    def create_left_panel(self, main_frame):
        
        # Initialising left panel
        left_panel = tk.Frame(main_frame, bg = "#e9f2f9", bd = 2, relief = "ridge", padx = 10, pady = 10)
        left_panel.pack(side = "left", fill = "both", expand = True, padx = 10)
        
        # Add instructions and dictionary
        self.create_instructions_section(left_panel)
        self.create_dictionary_section(left_panel)


    # Building Instruction Section
    def create_instructions_section(self, parent):

        # Instruction Label
        tk.Label(
            parent, text = "Instructions", bg = "#e9f2f9", fg = "black",
            font = ("Helvetica", 14, "bold"), pady = 5
        ).pack(anchor = "w")

        # Instructions to use the system
        instructions = [
            "1. Input text.",
            "2. Click the CHECK button.",
            "3. Double-click to select a spelling error.",
            "4. Right-click to view the suggestion of correction.",
            "5. Double-click a suggestion to replace the error.", 
            "----------------------- OR -------------------------",
            "             add a non-word to dictionary."
        ]

        for instruction in instructions:

            tk.Label(
                parent, text=instruction, bg = "#e9f2f9", fg = "black",
                font = ("Helvetica", 10), anchor = "w"

            ).pack(anchor="w", pady=2)


    # Building the Dictionary Section
    def create_dictionary_section(self, parent):

        # Dictionary Label
        tk.Label(

            parent, text = "Dictionary", bg = "#e9f2f9", fg = "black",
            font = ("Helvetica", 14, "bold"), pady = 10

        ).pack(anchor="w")

        # List all the words from dictionary.txt
        self.dic_list = tk.Listbox(parent, bg = "white", fg = "black", font = ("Helvetica", 10))
        for word in self.dict:
            self.dic_list.insert(tk.END, word)


        # Adding a Scroll Bar for Dictionary
        dic_scroll = tk.Scrollbar(self.dic_list, orient = tk.VERTICAL)
        dic_scroll.config(command = self.dic_list.yview)
        dic_scroll.pack(side = "right", fill = "y")
        self.dic_list.config(yscrollcommand = dic_scroll.set)
        self.dic_list.pack(expand = True, fill = "both", padx = 10)

        self.create_dictionary_search(parent)

    # Function to search for words in dictionary.txt
    def create_dictionary_search(self, parent):
        search_frame = tk.Frame(parent, bg = "#e9f2f9")
        search_frame.pack(fill = "x", pady = 10)
        self.user_search = tk.StringVar()
        tk.Entry(search_frame, textvariable = self.user_search, font = ("Helvetica", 10)).pack(side = "left", expand = True, 
                                                                                               fill = "x", padx = 5)
        ttk.Button(search_frame, text = "Search", command = self.search_dictionary).pack(side = "left", padx = 5)


    # Right Panel : Input field, Original Text Field, Result & Buttons
    def create_right_panel(self, main_frame):

        # Initialising right panel
        right_panel = tk.Frame(main_frame, bg = "#f5f5f5", padx = 10, pady = 10)
        right_panel.pack(side = "right", fill = "both", expand = True, padx = 10)
        
        # Add input field, buttons, and result sections
        self.create_input_section(right_panel)
        self.create_buttons_section(right_panel)
        self.create_result_label(right_panel)
        self.create_original_text_section(right_panel)


    # Building Input field Section
    def create_input_section(self, parent):
        tk.Label(parent, text = "Enter Text", bg = "#f5f5f5", font = ("Helvetica", 12, "bold")).pack(anchor = "w")
        self.txt_input = scrolledtext.ScrolledText(parent, wrap = tk.WORD, font = ("Helvetica", 10))
        self.txt_input.pack(fill = "both", expand = True, pady = 5)
        self.txt_input.focus()
        
        # Enable popup for user suggestion
        self.txt_input.tag_bind("sel", '<Button-3>', self.popup)


    # Building Action Buttons
    def create_buttons_section(self, parent):
        btn_frame = tk.Frame(parent, bg = "#f5f5f5")
        btn_frame.pack(fill = "x", pady = 5)
        ttk.Button(btn_frame, text = "CHECK", command = self.check_spelling).pack(side = "left", padx = 10)
        ttk.Button(btn_frame, text = "CLEAR", command = self.clear_input).pack(side = "left", padx = 10)
        ttk.Button(btn_frame, text = "REVERT", command = self.revert_text).pack(side = "left", padx = 10)


    # Building Error Detection Label
    def create_result_label(self, parent):

        self.lbl_result = tk.Label(
            parent, text="---", bg = "#f5f5f5", fg = "black",
            font = ("Helvetica", 12, "italic"), pady = 10
        )
        self.lbl_result.pack(fill = "x")


    # Building Original Text Field 
    def create_original_text_section(self, parent):
        tk.Label(parent, text = "Original Text", bg = "#f5f5f5", font = ("Helvetica", 12, "bold")).pack(anchor = "w")
        self.txt_original = scrolledtext.ScrolledText(parent, wrap = tk.WORD, font = ("Helvetica", 10))
        self.txt_original.pack(fill = "both", expand = True, pady = 5)


    # Function to clears the input fields.
    def clear_input(self):

        # Delete text from input field
        self.txt_input.delete("1.0", tk.END)

        # Delete text from original text field
        self.txt_original.configure(state = 'normal')
        self.txt_original.delete("1.0", tk.END)
        self.txt_original.configure(state = 'disabled')

        # Reset result label
        self.lbl_result.config(text = "---")


    # Function to revert changes
    def revert_text(self):
        self.txt_input.delete("1.0", tk.END)
        self.txt_input.insert("1.0", self.txt_original.get("1.0", tk.END))
    

    # Select Text
    def text_selected(self):

        if len(self.non_word_errors) != 0 or len(self.real_word_errors) != 0:
            self.selection_ind = self.txt_input.tag_ranges(tk.SEL)
            
            if self.selection_ind:

                # Get the start and end indices of the selection
                start_index, end_index = self.selection_ind[0], self.selection_ind[1]

                # Get the tag names applied to the selected text
                tag_names = self.txt_input.tag_names(start_index)
                if len(tag_names) > 1:  # Ensure there is a second tag
                    self.selected_tag = tag_names[1]
                else:
                    self.selected_tag = None

                # Return True to indicate text is selected
                return True
            else:
                return False
        else:
            return False
    

    # Get Correction Candidates
    def get_candidate_for_selection(self):

        for err in self.non_word_errors:
            if err["id"] == self.selected_tag:
                return err["candidates"]
        
        for err in self.real_word_errors:
            if err["id"] == self.selected_tag:
                return err["candidates"]
            
        return []
    

    # Get Error Token
    def get_non_word_error_token(self):

        for err in self.non_word_errors:
            if err["id"] == self.selected_tag:
                return err["error_token"]
            
        return None
    

    # Replace Word
    def replace_word(self, selected_word):

        if self.txt_input.tag_ranges(tk.SEL):
            start, end = self.txt_input.tag_ranges(tk.SEL)

            word_to_delete = self.txt_input.get(start, end)
            self.txt_input.delete(start, end)

            self.txt_input.insert(start, selected_word)


    # Pop up candidate for selection
    def popup(self, event):

        # Check if a word in the input field is selected
        if self.text_selected():
            candidates = self.get_candidate_for_selection()

            if not candidates:
                messagebox.showinfo(title = "No Suggestions", message = "No Suggestions Available for the Selected Word.")
                return

            # Create a new top-level window for the popup
            suggestion_window = tk.Toplevel(self)
            suggestion_window.title("Suggestions")
            suggestion_window.geometry("+{0}+{1}".format(event.x_root + 10, event.y_root + 10))
            suggestion_window.grab_set()  # Make the popup modal

            # Create a Listbox for displaying suggestions
            suggestions_listbox = tk.Listbox(suggestion_window, selectmode = tk.SINGLE, height = len(candidates))
            suggestions_listbox.pack(padx = 10, pady = 10, fill = tk.BOTH, expand = True)

            # Populate the Listbox with suggestions
            for candidate in candidates:
                suggestions_listbox.insert(tk.END, candidate)

            # Function to handle double-click on a suggestion
            def select_suggestion(event):
                selected_index = suggestions_listbox.curselection()
                if selected_index:
                    selected_suggestion = suggestions_listbox.get(selected_index[0])
                    self.replace_word(selected_suggestion)
                suggestion_window.destroy()

            # Bind double-click event to selection
            suggestions_listbox.bind("<Double-Button-1>", select_suggestion)

            # Button to add the selected error word to the dictionary
            def add_to_dictionary():

                error_word = self.get_non_word_error_token()

                if error_word:

                    self.add_to_dict(error_word)
                    suggestion_window.destroy()

                else:
                    messagebox.showwarning(title="Failed", message="Can only add a non-word to dictionary.")

            # Add button to add non-word error to the dictionary
            btn_add_to_dict = tk.Button(suggestion_window, text = "Add to Dictionary", command = add_to_dictionary)
            btn_add_to_dict.pack(pady=10)

            # Handle window closing
            def on_close():
                suggestion_window.destroy()

            suggestion_window.protocol("WM_DELETE_WINDOW", on_close)
        else:
            messagebox.showinfo(title="No Selection", message="Please select a word to see suggestions.")


    # Function to convert a character index to a Tkinter text widget index.
    def char_index_to_tk_index(self, char_index, text):

        # Preserve line endings to account for accurate indexing
        lines = text.splitlines(keepends = True)
        current_index = 0

        for line_num, line in enumerate(lines, start = 1):

            # Calculate the end index of the current line
            line_length = len(line)

            # If the character index falls within the current line, calculate the column
            if current_index <= char_index < current_index + line_length:
                column = char_index - current_index
                return f"{line_num}.{column}"
            current_index += line_length

        # Fallback to the end of the text
        return f"{len(lines)}.{len(lines[-1]) if lines else 0}"
    

    # Function to checks the spelling in the input text
    def check_spelling(self):
        
        self.non_word_errors = []
        self.real_word_errors = []

        self.txt_original.configure(state = 'normal')
        self.txt_original.delete('1.0', tk.END)

        user_input = self.txt_input.get('1.0', 'end-1c')

        # Check for errors
        self.non_word_errors, self.real_word_errors = self.error_detection_model.error_detection(user_input)

        # Reset tags and add tags for errors
        self.txt_input.tag_delete(*self.txt_input.tag_names())


        # Highlight non-word errors
        for err in self.non_word_errors:
            start, end = err["position"]
            print(f"Error: {err}, Substring: {user_input[start:end]}")

            # Validate indices to ensure correct substring extraction
            if start < 0 or end > len(user_input):
                print(f"Invalid indices for error: {err}")
                continue

            error_substring = user_input[start:end]

            if not error_substring.strip():
                print(f"Empty substring for error: {err}")
                continue
            
            # Convert to Tkinter indices
            start_index = self.char_index_to_tk_index(start, user_input)
            end_index = self.char_index_to_tk_index(end, user_input)

            # Log for debugging
            # print(f"Highlighting: {user_input[start:end]} from {start_index} to {end_index}")r

            # Apply tag
            tag_id = f"error_{start}_{end}"  # Ensure a unique tag ID
            self.txt_input.tag_config(err["id"], foreground = "red")
            self.txt_input.tag_add(err["id"], start_index, end_index)

        for err in self.real_word_errors:
            start, end = err["position"]

            # Validate indices to ensure correct substring extraction
            if start < 0 or end > len(user_input):
                print(f"Invalid indices for real-word error: {err}")
                continue
            
            error_substring = user_input[start:end]
            if not error_substring.strip():
                print(f"Empty substring for real-word error: {err}")
                continue
            
            # Convert to Tkinter indices
            start_index = self.char_index_to_tk_index(start, user_input)
            end_index = self.char_index_to_tk_index(end, user_input)

            # Apply tag
            self.txt_input.tag_config(err["id"], foreground = "blue")
            self.txt_input.tag_add(err["id"], start_index, end_index)

        # Update the original text field
        self.txt_original.insert(tk.INSERT, user_input)
        self.txt_original.configure(state = 'disabled')

        # Update result label
        if not self.non_word_errors and not self.real_word_errors:
            self.lbl_result.config(text = "No errors found.")
        else:
            self.lbl_result.config(text = "Errors found.")

        return None


    # Function to search for a word in the dictionary
    def search_dictionary(self):
        
        search_term = self.user_search.get()

        if search_term in self.dict:

            index = self.dict.index(search_term)
            self.dic_list.selection_set(index)
            self.dic_list.see(index)

        else:

            messagebox.showinfo(title="Not Found", message=f"{search_term} not found in dictionary.")


    # Function to add new words to dictionary
    def add_to_dict(self, word):
        
        if word.isalpha():

            self.dictionary_builder.add_word_to_dict(word)
            messagebox.showinfo(title = "Word Added", message = f"{word} added to dictionary.")

        else:

            messagebox.showwarning(title = "Invalid Word", message = "Only alphabetic words can be added.")