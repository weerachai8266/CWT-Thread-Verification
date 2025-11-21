"""
CWT Thread Verification System - Kanban Tool
Main application for writing and reading Kanban cards using ACR122U RFID reader

Author: CWT Team
Version: 1.0.0
License: MIT
"""

import tkinter as tk
import logging
import sys
from typing import Optional

from gui import KanbanGUI
from rfid_manager import RFIDManager
from config import APP_TITLE, BYPASS_KEYWORD


class KanbanToolApp:
    """Main application controller"""
    
    def __init__(self):
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Create main window
        self.root = tk.Tk()
        self.gui = KanbanGUI(self.root)
        
        # Create RFID manager
        self.rfid = RFIDManager()
        
        # Connect GUI callbacks
        self.gui.on_write_kanban = self.write_kanban
        self.gui.on_read_kanban = self.read_kanban
        self.gui.on_write_bypass = self.write_bypass
        self.gui.on_clear_card = self.clear_card
        self.gui.on_write_multiple = self.write_multiple
        self.gui.on_read_multiple = self.read_multiple
        self.gui.on_clear_multiple = self.clear_multiple  # NEW
        
        # Card detection state
        self.card_present = False
        self.is_busy = False  # Flag to prevent checking during operations
        self.stop_multiple_operation = False  # Flag to stop continuous operations
        
        # Initialize reader
        self.initialize_reader()
        
        # Start card detection polling
        self.start_card_detection()
    
    def initialize_reader(self):
        """Initialize RFID reader connection"""
        self.gui.log("Initializing RFID reader...", 'info')
        
        success, msg = self.rfid.connect_reader()
        
        if success:
            self.gui.log(msg, 'success')
            self.gui.set_reader_status("Connected", True)
        else:
            self.gui.log(msg, 'error')
            self.gui.set_reader_status("Not Connected", False)
            self.gui.show_warning(
                "Reader Not Found",
                "ACR122U reader not detected.\n\n"
                "Please connect the reader and restart the application.\n\n"
                "You can still use the interface, but card operations will fail."
            )
    
    def wait_for_card(self) -> bool:
        """
        Wait for card to be placed on reader
        
        Returns:
            bool: True if card detected, False otherwise
        """
        self.gui.log("Waiting for card... Please place card on reader.", 'info')
        self.gui.set_card_status("Waiting...", False)
        
        # Allow GUI to update
        self.root.update()
        
        success, msg = self.rfid.wait_for_card(timeout=10)
        
        if success:
            self.gui.log(msg, 'success')
            self.gui.set_card_status("Card Detected", True)
            return True
        else:
            self.gui.log(msg, 'warning')
            self.gui.set_card_status("No Card", False)
            return False
    
    def write_kanban(self, thread1: str, thread2: str):
        """
        Write thread codes to Kanban card
        
        Args:
            thread1: Thread 1 code
            thread2: Thread 2 code
        """
        self.is_busy = True  # Disable card detection during operation
        self.gui.log(f"Writing Kanban: Thread1='{thread1}', Thread2='{thread2}'", 'info')
        
        # Wait for card
        if not self.wait_for_card():
            self.gui.show_error(
                "No Card Detected",
                "Please place a card on the reader and try again."
            )
            self.is_busy = False
            return
        
        # Write data
        success, msg = self.rfid.write_kanban(thread1, thread2)
        
        if success:
            self.gui.log(msg, 'success')
            self.gui.show_success(
                "Success",
                f"Kanban card written successfully!\n\n"
                f"Thread 1: {thread1}\n"
                f"Thread 2: {thread2}"
            )
        else:
            self.gui.log(f"Failed to write Kanban: {msg}", 'error')
            self.gui.show_error(
                "Write Failed",
                f"Failed to write Kanban card.\n\n{msg}"
            )
        
        # Disconnect from card
        self.rfid.disconnect()
        self.is_busy = False  # Re-enable card detection
        
        # Force immediate card status check
        self.root.after(100, self.update_card_status_now)
    
    def write_multiple(self, thread1: str, thread2: str, quantity: int):
        """
        Write the same thread codes to multiple Kanban cards
        
        Args:
            thread1: Thread 1 code
            thread2: Thread 2 code
            quantity: Number of cards to write
        """
        self.is_busy = True  # Disable card detection during operation
        self.gui.log(f"=== Writing {quantity} cards ===", 'info')
        self.gui.log(f"Thread1='{thread1}', Thread2='{thread2}'", 'info')
        
        success_count = 0
        failed_count = 0
        
        for i in range(1, quantity + 1):
            self.gui.log(f"\n[Card {i}/{quantity}] Waiting for card...", 'warning')
            
            # Wait for card
            if not self.wait_for_card():
                self.gui.log(f"[Card {i}/{quantity}] No card detected - Skipping", 'error')
                failed_count += 1
                continue
            
            # Write data
            self.gui.log(f"[Card {i}/{quantity}] Writing data...", 'info')
            success, msg = self.rfid.write_kanban(thread1, thread2)
            
            if success:
                success_count += 1
                self.gui.log(f"[Card {i}/{quantity}] ✓ Success!", 'success')
                
                # Disconnect and wait for card removal
                self.rfid.disconnect()
                
                if i < quantity:  # Not the last card
                    self.gui.log(f"[Card {i}/{quantity}] Please remove card and place next card", 'warning')
                    
                    # Wait for card to be removed
                    removed = False
                    for _ in range(50):  # Wait up to 5 seconds
                        self.root.update()
                        if not self.rfid.check_card_present():
                            removed = True
                            break
                        import time
                        time.sleep(0.1)
                    
                    if not removed:
                        self.gui.log(f"[Card {i}/{quantity}] Warning: Card not removed yet", 'warning')
            else:
                failed_count += 1
                self.gui.log(f"[Card {i}/{quantity}] ✗ Failed: {msg}", 'error')
                self.rfid.disconnect()
        
        # Summary
        self.gui.log(f"\n=== Write Multiple Complete ===", 'info')
        self.gui.log(f"Success: {success_count}/{quantity}", 'success')
        if failed_count > 0:
            self.gui.log(f"Failed: {failed_count}/{quantity}", 'error')
        
        # Show summary dialog
        if failed_count == 0:
            self.gui.show_success(
                "All Cards Written",
                f"Successfully wrote all {quantity} cards!\n\n"
                f"Thread 1: {thread1}\n"
                f"Thread 2: {thread2}"
            )
        else:
            self.gui.show_warning(
                "Write Complete with Errors",
                f"Success: {success_count}/{quantity}\n"
                f"Failed: {failed_count}/{quantity}\n\n"
                f"Please check the log for details."
            )
        
        self.is_busy = False  # Re-enable card detection
        
        # Force immediate card status check
        self.root.after(100, self.update_card_status_now)
    
    def read_kanban(self):
        """Read and display thread codes from Kanban card"""
        self.is_busy = True  # Disable card detection during operation
        self.gui.log("Reading Kanban card...", 'info')
        
        # Wait for card
        if not self.wait_for_card():
            self.gui.show_error(
                "No Card Detected",
                "Please place a card on the reader and try again."
            )
            self.is_busy = False
            return
        
        # Read data
        success, thread1, thread2, msg = self.rfid.read_kanban()
        
        if success:
            self.gui.log(msg, 'success')
            self.gui.log(f"Thread 1: {thread1}", 'info')
            self.gui.log(f"Thread 2: {thread2}", 'info')
            
            # Update GUI inputs
            self.gui.set_thread_values(thread1, thread2)
            
            # Show results
            if thread1.lower() == BYPASS_KEYWORD.lower():
                self.gui.show_warning(
                    "Bypass Card",
                    "This is a BYPASS card.\n\n"
                    "Machine will operate without verification."
                )
            else:
                self.gui.show_success(
                    "Card Read Successfully",
                    f"Thread 1: {thread1}\n"
                    f"Thread 2: {thread2}"
                )
        else:
            self.gui.log(f"Failed to read Kanban: {msg}", 'error')
            self.gui.show_error(
                "Read Failed",
                f"Failed to read Kanban card.\n\n{msg}"
            )
        
        # Disconnect from card
        self.rfid.disconnect()
        self.is_busy = False  # Re-enable card detection
        
        # Force immediate card status check
        self.root.after(100, self.update_card_status_now)
    
    def read_multiple(self):
        """
        Read multiple Kanban cards continuously until stopped
        """
        self.is_busy = True
        self.stop_multiple_operation = False
        self.gui.log(f"=== Reading Multiple Cards (Continuous Mode) ===", 'info')
        self.gui.log("Click 'Stop' button to finish reading.", 'warning')
        
        # Create stop button window
        stop_window = self._create_stop_window("Reading Cards")
        
        success_count = 0
        failed_count = 0
        cards_data = []
        card_number = 1
        
        while not self.stop_multiple_operation:
            self.gui.log(f"\n[Card {card_number}] Waiting for card...", 'warning')
            self.root.update()
            
            # Wait for card with shorter timeout for better responsiveness
            if not self._wait_for_card_continuous(timeout=10):
                if self.stop_multiple_operation:
                    break
                self.gui.log(f"[Card {card_number}] No card detected - Skipping", 'error')
                failed_count += 1
                card_number += 1
                continue
            
            if self.stop_multiple_operation:
                self.rfid.disconnect()
                break
            
            # Read data
            self.gui.log(f"[Card {card_number}] Reading data...", 'info')
            success, thread1, thread2, msg = self.rfid.read_kanban()
            
            if success:
                success_count += 1
                
                # Store card data
                cards_data.append({
                    'number': card_number,
                    'thread1': thread1,
                    'thread2': thread2,
                    'is_bypass': thread1.lower() == BYPASS_KEYWORD.lower()
                })
                
                # Log the data
                if thread1.lower() == BYPASS_KEYWORD.lower():
                    self.gui.log(f"[Card {card_number}] ⚠️ BYPASS CARD", 'warning')
                else:
                    self.gui.log(f"[Card {card_number}] Thread 1: {thread1}", 'success')
                    self.gui.log(f"[Card {card_number}] Thread 2: {thread2}", 'success')
                
                # Disconnect and wait for card removal
                self.rfid.disconnect()
                
                if not self.stop_multiple_operation:
                    self.gui.log(f"[Card {card_number}] Please remove card and place next card", 'warning')
                    
                    # Wait for card to be removed
                    removed = False
                    for _ in range(50):
                        self.root.update()
                        if self.stop_multiple_operation:
                            break
                        if not self.rfid.check_card_present():
                            removed = True
                            break
                        import time
                        time.sleep(0.1)
                    
                    if not removed and not self.stop_multiple_operation:
                        self.gui.log(f"[Card {card_number}] Warning: Card not removed yet", 'warning')
            else:
                failed_count += 1
                self.gui.log(f"[Card {card_number}] ✗ Failed: {msg}", 'error')
                self.rfid.disconnect()
            
            card_number += 1
            self.root.update()
        
        # Close stop window
        stop_window.destroy()
        
        # Summary
        total_cards = card_number - 1
        self.gui.log(f"\n=== Read Multiple Complete ===", 'info')
        self.gui.log(f"Total cards processed: {total_cards}", 'info')
        self.gui.log(f"Success: {success_count}", 'success')
        if failed_count > 0:
            self.gui.log(f"Failed: {failed_count}", 'error')
        
        # Show detailed summary
        if cards_data:
            self.gui.log(f"\n--- Cards Summary ---", 'info')
            for card in cards_data:
                if card['is_bypass']:
                    self.gui.log(f"Card {card['number']}: BYPASS CARD", 'warning')
                else:
                    self.gui.log(f"Card {card['number']}: {card['thread1']} / {card['thread2']}", 'info')
        
        # Show summary dialog
        if total_cards > 0:
            if failed_count == 0:
                summary_text = f"Successfully read {success_count} cards!\n\n"
                if cards_data:
                    summary_text += "Cards:\n"
                    for card in cards_data[:10]:
                        if card['is_bypass']:
                            summary_text += f"{card['number']}. BYPASS CARD\n"
                        else:
                            summary_text += f"{card['number']}. {card['thread1']} / {card['thread2']}\n"
                    if len(cards_data) > 10:
                        summary_text += f"... and {len(cards_data) - 10} more\n"
                
                self.gui.show_success("Cards Read", summary_text)
            else:
                self.gui.show_warning(
                    "Read Complete",
                    f"Total: {total_cards}\n"
                    f"Success: {success_count}\n"
                    f"Failed: {failed_count}\n\n"
                    f"Please check the log for details."
                )
        
        self.is_busy = False
        self.root.after(100, self.update_card_status_now)
    
    def write_bypass(self):
        """Write bypass mode to card"""
        self.is_busy = True  # Disable card detection during operation
        self.gui.log("Writing BYPASS card...", 'warning')
        
        # Wait for card
        if not self.wait_for_card():
            self.gui.show_error(
                "No Card Detected",
                "Please place a card on the reader and try again."
            )
            self.is_busy = False
            return
        
        # Write bypass
        success, msg = self.rfid.write_bypass()
        
        if success:
            self.gui.log("BYPASS card written successfully", 'success')
            self.gui.show_success(
                "Success",
                "BYPASS card written successfully!\n\n"
                "⚠️ WARNING: This card will bypass all verification.\n"
                "Use only for maintenance or special operations."
            )
        else:
            self.gui.log(f"Failed to write BYPASS: {msg}", 'error')
            self.gui.show_error(
                "Write Failed",
                f"Failed to write BYPASS card.\n\n{msg}"
            )
        
        # Disconnect from card
        self.rfid.disconnect()
        self.is_busy = False  # Re-enable card detection
        
        # Force immediate card status check
        self.root.after(100, self.update_card_status_now)
    
    def clear_card(self):
        """Clear all data from card"""
        self.is_busy = True  # Disable card detection during operation
        self.gui.log("Clearing card...", 'info')
        
        # Wait for card
        if not self.wait_for_card():
            self.gui.show_error(
                "No Card Detected",
                "Please place a card on the reader and try again."
            )
            self.is_busy = False
            return
        
        # Clear data
        success, msg = self.rfid.clear_card()
        
        if success:
            self.gui.log(msg, 'success')
            self.gui.show_success(
                "Success",
                "Card cleared successfully!"
            )
        else:
            self.gui.log(f"Failed to clear card: {msg}", 'error')
            self.gui.show_error(
                "Clear Failed",
                f"Failed to clear card.\n\n{msg}"
            )
        
        # Disconnect from card
        self.rfid.disconnect()
        self.is_busy = False  # Re-enable card detection
        
        # Force immediate card status check
        self.root.after(100, self.update_card_status_now)
    
    def clear_multiple(self):
        """
        Clear multiple Kanban cards continuously until stopped
        """
        self.is_busy = True
        self.stop_multiple_operation = False
        self.gui.log(f"=== Clearing Multiple Cards (Continuous Mode) ===", 'info')
        self.gui.log("Click 'Stop' button to finish clearing.", 'warning')
        
        # Create stop button window
        stop_window = self._create_stop_window("Clearing Cards")
        
        success_count = 0
        failed_count = 0
        card_number = 1
        
        while not self.stop_multiple_operation:
            self.gui.log(f"\n[Card {card_number}] Waiting for card...", 'warning')
            self.root.update()
            
            # Wait for card with shorter timeout
            if not self._wait_for_card_continuous(timeout=10):
                if self.stop_multiple_operation:
                    break
                self.gui.log(f"[Card {card_number}] No card detected - Skipping", 'error')
                failed_count += 1
                card_number += 1
                continue
            
            if self.stop_multiple_operation:
                self.rfid.disconnect()
                break
            
            # Clear data
            self.gui.log(f"[Card {card_number}] Clearing data...", 'info')
            success, msg = self.rfid.clear_card()
            
            if success:
                success_count += 1
                self.gui.log(f"[Card {card_number}] ✓ Cleared!", 'success')
                
                # Disconnect and wait for card removal
                self.rfid.disconnect()
                
                if not self.stop_multiple_operation:
                    self.gui.log(f"[Card {card_number}] Please remove card and place next card", 'warning')
                    
                    # Wait for card to be removed
                    removed = False
                    for _ in range(50):
                        self.root.update()
                        if self.stop_multiple_operation:
                            break
                        if not self.rfid.check_card_present():
                            removed = True
                            break
                        import time
                        time.sleep(0.1)
                    
                    if not removed and not self.stop_multiple_operation:
                        self.gui.log(f"[Card {card_number}] Warning: Card not removed yet", 'warning')
            else:
                failed_count += 1
                self.gui.log(f"[Card {card_number}] ✗ Failed: {msg}", 'error')
                self.rfid.disconnect()
            
            card_number += 1
            self.root.update()
        
        # Close stop window
        stop_window.destroy()
        
        # Summary
        total_cards = card_number - 1
        self.gui.log(f"\n=== Clear Multiple Complete ===", 'info')
        self.gui.log(f"Total cards processed: {total_cards}", 'info')
        self.gui.log(f"Success: {success_count}", 'success')
        if failed_count > 0:
            self.gui.log(f"Failed: {failed_count}", 'error')
        
        # Show summary dialog
        if total_cards > 0:
            if failed_count == 0:
                self.gui.show_success(
                    "All Cards Cleared",
                    f"Successfully cleared {success_count} cards!"
                )
            else:
                self.gui.show_warning(
                    "Clear Complete",
                    f"Total: {total_cards}\n"
                    f"Success: {success_count}\n"
                    f"Failed: {failed_count}\n\n"
                    f"Please check the log for details."
                )
        
        self.is_busy = False
        self.root.after(100, self.update_card_status_now)
    
    def start_card_detection(self):
        """Start automatic card detection polling"""
        if self.rfid.reader is None:
            # No reader, try again later
            self.root.after(2000, self.start_card_detection)
            return
        
        self.check_card_status()
    
    def check_card_status(self):
        """Check if card is present and update GUI"""
        if not self.is_busy and self.rfid.reader is not None:
            card_now = self.rfid.check_card_present()
            
            # Update GUI only if status changed
            if card_now != self.card_present:
                self.card_present = card_now
                if card_now:
                    self.gui.set_card_status("Card Detected", True)
                    # Try to get and display UID
                    uid = self._get_card_uid_safe()
                    if uid:
                        self.gui.set_card_uid(uid)
                        self.gui.log(f"Card detected - UID: {uid}", 'success')
                    else:
                        self.gui.set_card_uid("-")
                        self.gui.log("Card detected on reader", 'success')
                else:
                    self.gui.set_card_status("No Card", False)
                    self.gui.set_card_uid("-")
                    self.gui.log("Card removed from reader", 'info')
        
        # Schedule next check (every 500ms)
        self.root.after(500, self.check_card_status)
    
    def update_card_status_now(self):
        """Force immediate card status update (called after operations)"""
        if self.rfid.reader is not None:
            card_now = self.rfid.check_card_present()
            self.card_present = card_now
            
            if card_now:
                self.gui.set_card_status("Card Detected", True)
                uid = self._get_card_uid_safe()
                self.gui.set_card_uid(uid if uid else "-")
            else:
                self.gui.set_card_status("No Card", False)
                self.gui.set_card_uid("-")
    
    def _get_card_uid_safe(self) -> Optional[str]:
        """Safely get card UID without interfering with operations"""
        try:
            # Create temporary connection to get UID
            if self.rfid.reader is None:
                return None
            
            temp_conn = self.rfid.reader.createConnection()
            temp_conn.connect()
            
            # Get UID
            from smartcard.util import toHexString
            get_uid_cmd = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            data, sw1, sw2 = temp_conn.transmit(get_uid_cmd)
            
            temp_conn.disconnect()
            
            if sw1 == 0x90 and sw2 == 0x00:
                return toHexString(data)
            return None
        except:
            return None
    
    def _create_stop_window(self, title: str):
        """Create a window with Stop button for continuous operations"""
        stop_win = tk.Toplevel(self.root)
        stop_win.title(title)
        stop_win.geometry("500x250")
        stop_win.resizable(False, False)
        stop_win.transient(self.root)
        
        # Center on main window
        stop_win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 250) // 2
        stop_win.geometry(f"500x250+{x}+{y}")
        
        # Prevent closing with X button
        stop_win.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Main frame with padding
        main_frame = tk.Frame(stop_win, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Title label
        tk.Label(
            main_frame,
            text=f"🔄 {title}",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=(15, 20))
        
        # Status message
        tk.Label(
            main_frame,
            text="Operation in progress...",
            font=('Arial', 12),
            bg='white',
            fg='#34495e'
        ).pack(pady=8)
        
        # Instruction
        tk.Label(
            main_frame,
            text="Place next card or click Stop to finish",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=8)
        
        # Stop button - MUCH LARGER
        def stop_operation():
            self.stop_multiple_operation = True
        
        stop_btn = tk.Button(
            main_frame,
            text="⏹  STOP",
            command=stop_operation,
            font=('Arial', 24, 'bold'),
            bg='#dc3545',
            fg='white',
            padx=50,
            pady=60,
            relief=tk.RAISED,
            bd=5,
            cursor='hand2',
            activebackground='#c82333',
            activeforeground='white'
        )
        stop_btn.pack(pady=10, ipadx=20, ipady=50)
        
        stop_win.update()
        return stop_win
    
    def _wait_for_card_continuous(self, timeout: int = 10) -> bool:
        """
        Wait for card with continuous operation support (can be interrupted)
        
        Returns:
            bool: True if card detected, False otherwise
        """
        self.gui.set_card_status("Waiting...", False)
        self.root.update()
        
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.stop_multiple_operation:
                return False
            
            # Try to detect card
            if self.rfid.reader is None:
                return False
            
            # Close any existing connection first
            if self.rfid.connection is not None:
                try:
                    self.rfid.connection.disconnect()
                except:
                    pass
                self.rfid.connection = None
            
            try:
                from smartcard.Exceptions import NoCardException, CardConnectionException
                
                # Create new connection
                self.rfid.connection = self.rfid.reader.createConnection()
                self.rfid.connection.connect()
                
                # Get card ATR
                atr = self.rfid.connection.getATR()
                self.gui.set_card_status("Card Detected", True)
                return True
                
            except NoCardException:
                # No card, keep waiting
                self.root.update()
                time.sleep(0.3)
                continue
            except CardConnectionException:
                # Connection error, retry
                if self.rfid.connection is not None:
                    try:
                        self.rfid.connection.disconnect()
                    except:
                        pass
                    self.rfid.connection = None
                self.root.update()
                time.sleep(0.3)
                continue
            except Exception as e:
                self.logger.debug(f"Error waiting for card: {e}")
                self.root.update()
                time.sleep(0.3)
                continue
        
        self.gui.set_card_status("No Card", False)
        return False
    
    def run(self):
        """Start the application"""
        self.gui.log("=== Thread Verification - Kanban Tool ===", 'info')
        self.gui.log("Ready to use. Please ensure ACR122U reader is connected.", 'info')
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = KanbanToolApp()
        app.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
