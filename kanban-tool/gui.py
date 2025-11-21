"""
CWT Thread Verification System - GUI Module
Tkinter-based graphical user interface for Kanban card management
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
from typing import Callable, Optional

from config import (
    APP_TITLE, APP_VERSION, APP_WIDTH, APP_HEIGHT,
    COLOR_SUCCESS, COLOR_ERROR, COLOR_WARNING, COLOR_INFO, COLOR_BG
)


class KanbanGUI:
    """Main GUI window for Kanban card tool"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - APP_WIDTH) // 2
        y = (screen_height - APP_HEIGHT) // 2
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
        
        # Callbacks to be set by main application
        self.on_write_kanban: Optional[Callable] = None
        self.on_read_kanban: Optional[Callable] = None
        self.on_write_bypass: Optional[Callable] = None
        self.on_clear_card: Optional[Callable] = None
        self.on_write_multiple: Optional[Callable] = None
        self.on_read_multiple: Optional[Callable] = None
        self.on_clear_multiple: Optional[Callable] = None  # NEW
        
        # Status variables
        self.reader_status = tk.StringVar(value="Not Connected")
        self.card_status = tk.StringVar(value="No Card")
        self.uid_var = tk.StringVar(value="-")
        
        # Thread input variables
        self.thread1_var = tk.StringVar()
        self.thread2_var = tk.StringVar()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Create sections
        self._create_header(main_frame)
        self._create_status_section(main_frame)
        self._create_input_section(main_frame)
        self._create_button_section(main_frame)
        self._create_log_section(main_frame)
    
    def _create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(
            header_frame,
            text="Thread Verification",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Kanban Card Management Tool",
            font=('Arial', 10)
        )
        subtitle_label.grid(row=1, column=0)
        
        version_label = ttk.Label(
            header_frame,
            text=f"Version {APP_VERSION}",
            font=('Arial', 8),
            foreground='gray'
        )
        version_label.grid(row=2, column=0)
    
    def _create_status_section(self, parent):
        """Create status indicators section"""
        status_frame = ttk.LabelFrame(parent, text="Status", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # Reader status
        ttk.Label(status_frame, text="Reader:").grid(row=0, column=0, sticky=tk.W)
        reader_label = ttk.Label(
            status_frame,
            textvariable=self.reader_status,
            font=('Arial', 10, 'bold')
        )
        reader_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Card status
        ttk.Label(status_frame, text="Card:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        card_label = ttk.Label(
            status_frame,
            textvariable=self.card_status,
            font=('Arial', 10, 'bold')
        )
        card_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Card UID
        ttk.Label(status_frame, text="Card UID:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        uid_label = ttk.Label(
            status_frame,
            textvariable=self.uid_var,
            font=('Consolas', 9)
        )
        uid_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
    
    def _create_input_section(self, parent):
        """Create thread input section"""
        input_frame = ttk.LabelFrame(parent, text="Thread Codes", padding="10")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Thread 1 input
        ttk.Label(input_frame, text="Thread 1:").grid(row=0, column=0, sticky=tk.W)
        thread1_entry = ttk.Entry(
            input_frame,
            textvariable=self.thread1_var,
            font=('Arial', 11),
            width=30
        )
        thread1_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Thread 1 length indicator
        thread1_length = ttk.Label(input_frame, text="0/16", foreground='gray')
        thread1_length.grid(row=0, column=2, padx=(5, 0))
        
        # Update length indicator
        def update_thread1_length(*args):
            length = len(self.thread1_var.get())
            thread1_length.config(
                text=f"{length}/16",
                foreground='red' if length > 16 else 'gray'
            )
        self.thread1_var.trace('w', update_thread1_length)
        
        # Thread 2 input
        ttk.Label(input_frame, text="Thread 2:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        thread2_entry = ttk.Entry(
            input_frame,
            textvariable=self.thread2_var,
            font=('Arial', 11),
            width=30
        )
        thread2_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # Thread 2 length indicator
        thread2_length = ttk.Label(input_frame, text="0/16", foreground='gray')
        thread2_length.grid(row=1, column=2, padx=(5, 0), pady=(10, 0))
        
        # Update length indicator
        def update_thread2_length(*args):
            length = len(self.thread2_var.get())
            thread2_length.config(
                text=f"{length}/16",
                foreground='red' if length > 16 else 'gray'
            )
        self.thread2_var.trace('w', update_thread2_length)
        
        # Example text
        example_label = ttk.Label(
            input_frame,
            text="Example: TH-001, TH-RED-100, etc. (Max 16 characters)",
            font=('Arial', 8),
            foreground='gray'
        )
        example_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
    
    def _create_button_section(self, parent):
        """Create action buttons section"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configure columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Style for larger buttons
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 11), padding=10)
        
        # Row 1: Write, Write Multiple, Write Bypass
        write_btn = ttk.Button(
            button_frame,
            text="📝 Write Kanban",
            command=self._handle_write_kanban,
            style='Large.TButton'
        )
        write_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5), ipady=5)
        
        write_multi_btn = ttk.Button(
            button_frame,
            text="📝📝 Write Multiple",
            command=self._handle_write_multiple,
            style='Large.TButton'
        )
        write_multi_btn.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5), ipady=5)
        
        bypass_btn = ttk.Button(
            button_frame,
            text="⚡ Write Bypass",
            command=self._handle_write_bypass,
            style='Large.TButton'
        )
        bypass_btn.grid(row=0, column=2, sticky=(tk.W, tk.E), ipady=5)
        
        # Row 2: Read, Read Multiple, Clear
        read_btn = ttk.Button(
            button_frame,
            text="📖 Read Kanban",
            command=self._handle_read_kanban,
            style='Large.TButton'
        )
        read_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(8, 0), ipady=5)
        
        read_multi_btn = ttk.Button(
            button_frame,
            text="📖📖 Read Multiple",
            command=self._handle_read_multiple,
            style='Large.TButton'
        )
        read_multi_btn.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(8, 0), ipady=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Card",
            command=self._handle_clear_card,
            style='Large.TButton'
        )
        clear_btn.grid(row=1, column=2, sticky=(tk.W, tk.E), pady=(8, 0), ipady=5)
        
        # Row 3: Clear Multiple
        clear_multi_btn = ttk.Button(
            button_frame,
            text="🗑️🗑️ Clear Multiple",
            command=self._handle_clear_multiple,
            style='Large.TButton'
        )
        clear_multi_btn.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 5), pady=(8, 0), ipady=5)
    
    def _create_log_section(self, parent):
        """Create log display section"""
        log_frame = ttk.LabelFrame(parent, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure parent to expand log section
        parent.rowconfigure(4, weight=1)
        
        # Scrolled text widget for log
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=('Consolas', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colored output
        self.log_text.tag_config('success', foreground=COLOR_SUCCESS)
        self.log_text.tag_config('error', foreground=COLOR_ERROR)
        self.log_text.tag_config('warning', foreground=COLOR_WARNING)
        self.log_text.tag_config('info', foreground=COLOR_INFO)
    
    def _handle_write_kanban(self):
        """Handle Write Kanban button click"""
        if self.on_write_kanban:
            thread1 = self.thread1_var.get().strip()
            thread2 = self.thread2_var.get().strip()
            
            if not thread1 or not thread2:
                messagebox.showwarning(
                    "Invalid Input",
                    "Please enter both Thread 1 and Thread 2 codes."
                )
                return
            
            if len(thread1) > 16 or len(thread2) > 16:
                messagebox.showerror(
                    "Invalid Input",
                    "Thread codes must be 16 characters or less."
                )
                return
            
            self.on_write_kanban(thread1, thread2)
    
    def _handle_write_multiple(self):
        """Handle Write Multiple button click"""
        if self.on_write_multiple:
            thread1 = self.thread1_var.get().strip()
            thread2 = self.thread2_var.get().strip()
            
            if not thread1 or not thread2:
                messagebox.showwarning(
                    "Invalid Input",
                    "Please enter both Thread 1 and Thread 2 codes."
                )
                return
            
            if len(thread1) > 16 or len(thread2) > 16:
                messagebox.showerror(
                    "Invalid Input",
                    "Thread codes must be 16 characters or less."
                )
                return
            
            # Ask for quantity
            quantity = self._ask_quantity()
            if quantity > 0:
                self.on_write_multiple(thread1, thread2, quantity)
    
    def _ask_quantity(self) -> int:
        """Ask user for number of cards to write"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Write Multiple Cards")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        result = [0]  # Use list to store result from inner function
        
        # Label
        ttk.Label(
            dialog,
            text="How many cards do you want to write?",
            font=('Arial', 10)
        ).pack(pady=(20, 10))
        
        # Spinbox for quantity
        quantity_var = tk.IntVar(value=1)
        spinbox = ttk.Spinbox(
            dialog,
            from_=1,
            to=100,
            textvariable=quantity_var,
            width=10,
            font=('Arial', 12)
        )
        spinbox.pack(pady=10)
        spinbox.focus()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def on_ok():
            result[0] = quantity_var.get()
            dialog.destroy()
        
        def on_cancel():
            result[0] = 0
            dialog.destroy()
        
        ttk.Button(button_frame, text="OK", command=on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        dialog.wait_window()
        return result[0]
    
    def _handle_read_kanban(self):
        """Handle Read Kanban button click"""
        if self.on_read_kanban:
            self.on_read_kanban()
    
    def _handle_read_multiple(self):
        """Handle Read Multiple button click"""
        if self.on_read_multiple:
            self.on_read_multiple()
    
    def _ask_quantity_read(self) -> int:
        """Ask user for number of cards to read"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Read Multiple Cards")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        result = [0]
        
        # Label
        ttk.Label(
            dialog,
            text="How many cards do you want to read?",
            font=('Arial', 10)
        ).pack(pady=(20, 10))
        
        # Spinbox for quantity
        quantity_var = tk.IntVar(value=1)
        spinbox = ttk.Spinbox(
            dialog,
            from_=1,
            to=100,
            textvariable=quantity_var,
            width=10,
            font=('Arial', 12)
        )
        spinbox.pack(pady=10)
        spinbox.focus()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def on_ok():
            result[0] = quantity_var.get()
            dialog.destroy()
        
        def on_cancel():
            result[0] = 0
            dialog.destroy()
        
        ttk.Button(button_frame, text="OK", command=on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        dialog.wait_window()
        return result[0]
    
    def _handle_write_bypass(self):
        """Handle Write Bypass button click"""
        if self.on_write_bypass:
            result = messagebox.askyesno(
                "Confirm Bypass",
                "This will write a bypass card that skips verification.\n\n"
                "Are you sure you want to continue?"
            )
            if result:
                self.on_write_bypass()
    
    def _handle_clear_card(self):
        """Handle Clear Card button click"""
        if self.on_clear_card:
            result = messagebox.askyesno(
                "Confirm Clear",
                "This will erase all data from the card.\n\n"
                "Are you sure you want to continue?"
            )
            if result:
                self.on_clear_card()
    
    def _handle_clear_multiple(self):
        """Handle Clear Multiple button click"""
        if self.on_clear_multiple:
            result = messagebox.askyesno(
                "Confirm Clear Multiple",
                "This will erase all data from multiple cards.\n\n"
                "You can stop anytime by clicking 'Stop' button.\n\n"
                "Are you sure you want to continue?"
            )
            if result:
                self.on_clear_multiple()
    
    def _ask_quantity_clear(self) -> int:
        """Ask user for number of cards to clear"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Clear Multiple Cards")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        result = [0]
        
        # Label
        ttk.Label(
            dialog,
            text="How many cards do you want to clear?",
            font=('Arial', 10)
        ).pack(pady=(20, 10))
        
        # Spinbox for quantity
        quantity_var = tk.IntVar(value=1)
        spinbox = ttk.Spinbox(
            dialog,
            from_=1,
            to=100,
            textvariable=quantity_var,
            width=10,
            font=('Arial', 12)
        )
        spinbox.pack(pady=10)
        spinbox.focus()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def on_ok():
            result[0] = quantity_var.get()
            dialog.destroy()
        
        def on_cancel():
            result[0] = 0
            dialog.destroy()
        
        ttk.Button(button_frame, text="OK", command=on_ok, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())
        
        dialog.wait_window()
        return result[0]
    
    def log(self, message: str, level: str = 'info'):
        """
        Add message to log display
        
        Args:
            message: Message to log
            level: Log level ('info', 'success', 'warning', 'error')
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, full_message, level)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def set_reader_status(self, status: str, connected: bool = False):
        """Update reader status indicator"""
        self.reader_status.set(status)
    
    def set_card_status(self, status: str, present: bool = False):
        """Update card status indicator"""
        self.card_status.set(status)
    
    def set_card_uid(self, uid: str):
        """Update card UID display"""
        self.uid_var.set(uid if uid else "-")
    
    def set_thread_values(self, thread1: str, thread2: str):
        """Set thread input values"""
        self.thread1_var.set(thread1)
        self.thread2_var.set(thread2)
    
    def clear_inputs(self):
        """Clear thread input fields"""
        self.thread1_var.set("")
        self.thread2_var.set("")
    
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def show_success(self, title: str, message: str):
        """Show success dialog"""
        messagebox.showinfo(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show warning dialog"""
        messagebox.showwarning(title, message)
