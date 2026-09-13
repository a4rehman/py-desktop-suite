import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from atm_core import AtmAccount

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ATMSystemApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nexus Bank - Interactive ATM Terminal")
        self.geometry("640x580")
        self.resizable(False, False)

        self.account = AtmAccount()

        self._build_ui()

    def _build_ui(self):
        # Header / Bank Logo
        header = ctk.CTkFrame(self, fg_color="#1C1C1E", height=60, corner_radius=0)
        header.pack(fill="x")

        logo_lbl = ctk.CTkLabel(
            header,
            text="🏦 NEXUS DIGITAL BANK ATM",
            font=ctk.CTkFont(family="Inter", size=20, weight="bold"),
            text_color="#30D158"
        )
        logo_lbl.pack(side="left", padx=20, pady=15)

        # Virtual Credit/Debit Card Frame
        self.card_frame = ctk.CTkFrame(self, fg_color="#0A84FF", corner_radius=18, height=150)
        self.card_frame.pack(fill="x", padx=25, pady=20)

        card_title = ctk.CTkLabel(
            self.card_frame,
            text="PREMIUM PLATINUM DEBIT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#E0E0E0"
        )
        card_title.pack(anchor="w", padx=20, pady=(15, 5))

        self.card_num = ctk.CTkLabel(
            self.card_frame,
            text="•••• •••• •••• 8842",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFFFFF"
        )
        self.card_num.pack(anchor="w", padx=20, pady=5)

        self.bal_display = ctk.CTkLabel(
            self.card_frame,
            text=f"Available Balance: ${self.account.balance:,.2f}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        self.bal_display.pack(anchor="e", padx=20, pady=(0, 15))

        # ATM Action Grid Buttons
        actions_grid = ctk.CTkFrame(self, fg_color="transparent")
        actions_grid.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        for i in range(2):
            actions_grid.grid_rowconfigure(i, weight=1)
            actions_grid.grid_columnconfigure(i, weight=1)

        btn_pin = ctk.CTkButton(
            actions_grid,
            text="🔒 Set / Change PIN",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2C2C2E",
            hover_color="#3A3A3C",
            corner_radius=14,
            command=self.change_pin
        )
        btn_pin.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        btn_deposit = ctk.CTkButton(
            actions_grid,
            text="💵 Deposit Cash",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#30D158",
            hover_color="#24A143",
            corner_radius=14,
            command=self.deposit_cash
        )
        btn_deposit.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        btn_withdraw = ctk.CTkButton(
            actions_grid,
            text="💳 Withdraw Cash",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#FF9F0A",
            hover_color="#D98200",
            corner_radius=14,
            command=self.withdraw_cash
        )
        btn_withdraw.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        btn_history = ctk.CTkButton(
            actions_grid,
            text="📋 View Receipt Log",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#0A84FF",
            hover_color="#0066CC",
            corner_radius=14,
            command=self.view_history
        )
        btn_history.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    def _verify_pin(self):
        dialog = ctk.CTkInputDialog(text="Enter your 4-digit Security PIN:", title="PIN Security Check")
        entered_pin = dialog.get_input()
        if entered_pin is not None and self.account.verify_pin(entered_pin):
            return True
        messagebox.showerror("Access Denied", "Incorrect Security PIN entered!")
        return False

    def change_pin(self):
        if not self._verify_pin():
            return
        dialog = ctk.CTkInputDialog(text="Enter New 4-digit Security PIN:", title="Update PIN")
        new_pin = dialog.get_input()
        if new_pin is None:
            return
        success, message = self.account.change_pin(new_pin)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def deposit_cash(self):
        if not self._verify_pin():
            return
        dialog = ctk.CTkInputDialog(text="Enter Cash Deposit Amount ($):", title="Deposit Cash")
        raw = dialog.get_input()
        if raw is None:
            return
        success, message = self.account.deposit(raw)
        if success:
            self._update_card()
            messagebox.showinfo("Transaction Complete", message)
        else:
            messagebox.showerror("Error", message)

    def withdraw_cash(self):
        if not self._verify_pin():
            return
        dialog = ctk.CTkInputDialog(text="Enter Withdrawal Amount ($):", title="Withdraw Cash")
        raw = dialog.get_input()
        if raw is None:
            return
        success, message = self.account.withdraw(raw)
        if success:
            self._update_card()
            messagebox.showinfo("Transaction Complete", message)
        else:
            messagebox.showerror("Error", message)

    def view_history(self):
        if not self._verify_pin():
            return
        log_window = ctk.CTkToplevel(self)
        log_window.title("Digital Receipt & Activity Log")
        log_window.geometry("400x400")

        lbl = ctk.CTkLabel(log_window, text="🧾 ATM Receipt History", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=15)

        textbox = ctk.CTkTextbox(log_window, font=ctk.CTkFont(size=13))
        textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        if not self.account.transactions:
            textbox.insert("1.0", "No recent transactions found.")
        else:
            content = "\n".join([f"• {t}" for t in self.account.transactions])
            textbox.insert("1.0", f"Account: •••• 8842\nTotal Balance: ${self.account.balance:,.2f}\n\nRecent Activity:\n" + content)
        textbox.configure(state="disabled")

    def _update_card(self):
        self.bal_display.configure(text=f"Available Balance: ${self.account.balance:,.2f}")


if __name__ == "__main__":
    app = ATMSystemApp()
    app.mainloop()
