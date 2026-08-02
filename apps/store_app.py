import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Sample product catalog
PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Noise-Canceling Headphones",
        "price": 299.99,
        "category": "Electronics",
        "badge": "BESTSELLER",
        "icon": "🎧"
    },
    {
        "id": 2,
        "name": "Ultra-Wide Gaming Monitor 34\"",
        "price": 649.00,
        "category": "Electronics",
        "badge": "SALE",
        "icon": "🖥️"
    },
    {
        "id": 3,
        "name": "Ergonomic Mechanical Keyboard",
        "price": 149.50,
        "category": "Accessories",
        "badge": "POPULAR",
        "icon": "⌨️"
    },
    {
        "id": 4,
        "name": "Smart Fitness Watch Series 9",
        "price": 399.00,
        "category": "Wearables",
        "badge": "NEW",
        "icon": "⌚"
    }
]

class FlipkartStoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Flipkart E-Commerce Store")
        self.geometry("780x600")
        self.resizable(False, False)

        self.logged_in_user = None
        self.cart = []

        self._build_ui()

    def _build_ui(self):
        # Header / Navigation Bar
        nav = ctk.CTkFrame(self, fg_color="#1C1C1E", height=60, corner_radius=0)
        nav.pack(fill="x")

        logo = ctk.CTkLabel(
            nav,
            text="🛍️ Flipkart Store",
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#FF9F0A"
        )
        logo.pack(side="left", padx=20, pady=15)

        self.user_btn = ctk.CTkButton(
            nav,
            text="👤 Sign In / Register",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3A3A3C",
            hover_color="#48484A",
            corner_radius=10,
            command=self.open_auth_modal
        )
        self.user_btn.pack(side="right", padx=(10, 20), pady=12)

        self.cart_btn = ctk.CTkButton(
            nav,
            text="🛒 Cart (0)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0A84FF",
            hover_color="#0066CC",
            corner_radius=10,
            command=self.open_cart_modal
        )
        self.cart_btn.pack(side="right", padx=5, pady=12)

        # Products Grid View
        self.content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        title_lbl = ctk.CTkLabel(
            self.content,
            text="Featured Products Catalog",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        title_lbl.pack(anchor="w", pady=(0, 15))

        for prod in PRODUCTS:
            self._render_product_card(prod)

    def _render_product_card(self, item):
        card = ctk.CTkFrame(self.content, fg_color="#2C2C2E", corner_radius=14)
        card.pack(fill="x", pady=8, padx=5)

        icon_lbl = ctk.CTkLabel(card, text=item["icon"], font=ctk.CTkFont(size=36))
        icon_lbl.pack(side="left", padx=20, pady=15)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=10)

        name_lbl = ctk.CTkLabel(
            info_frame,
            text=item["name"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        )
        name_lbl.pack(fill="x")

        price_lbl = ctk.CTkLabel(
            info_frame,
            text=f"${item['price']:.2f}  |  {item['badge']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#30D158",
            anchor="w"
        )
        price_lbl.pack(fill="x", pady=(4, 0))

        add_btn = ctk.CTkButton(
            card,
            text="+ Add to Cart",
            width=120,
            fg_color="#0A84FF",
            hover_color="#0066CC",
            corner_radius=10,
            command=lambda p=item: self.add_to_cart(p)
        )
        add_btn.pack(side="right", padx=20)

    def add_to_cart(self, product):
        self.cart.append(product)
        self.cart_btn.configure(text=f"🛒 Cart ({len(self.cart)})")
        messagebox.showinfo("Cart Updated", f"Added '{product['name']}' to your cart!")

    def open_auth_modal(self):
        auth_win = ctk.CTkToplevel(self)
        auth_win.title("Account Login / Registration")
        auth_win.geometry("380x360")

        lbl = ctk.CTkLabel(auth_win, text="Sign In to Flipkart", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=20)

        email_entry = ctk.CTkEntry(auth_win, placeholder_text="Email address", width=280)
        email_entry.pack(pady=10)

        pass_entry = ctk.CTkEntry(auth_win, placeholder_text="Password", show="•", width=280)
        pass_entry.pack(pady=10)

        def login_action():
            email = email_entry.get()
            if email:
                self.logged_in_user = email
                self.user_btn.configure(text=f"👤 {email.split('@')[0]}")
                messagebox.showinfo("Welcome", f"Logged in successfully as {email}!")
                auth_win.destroy()

        login_btn = ctk.CTkButton(auth_win, text="Login", width=280, fg_color="#30D158", command=login_action)
        login_btn.pack(pady=15)

    def open_cart_modal(self):
        cart_win = ctk.CTkToplevel(self)
        cart_win.title("Your Shopping Cart")
        cart_win.geometry("450x450")

        lbl = ctk.CTkLabel(cart_win, text="🛒 Shopping Cart Items", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=15)

        textbox = ctk.CTkTextbox(cart_win, font=ctk.CTkFont(size=13))
        textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        total = sum(p["price"] for p in self.cart)
        if not self.cart:
            textbox.insert("1.0", "Your cart is currently empty.")
        else:
            lines = [f"• {p['name']} - ${p['price']:.2f}" for p in self.cart]
            lines.append(f"\n───────────────────────────\nTotal Amount: ${total:,.2f}")
            textbox.insert("1.0", "\n".join(lines))

        def checkout():
            if not self.cart:
                messagebox.showwarning("Cart Empty", "Please add items to your cart before checkout.")
                return
            messagebox.showinfo("Checkout Complete", f"Order placed successfully! Total: ${total:,.2f}")
            self.cart = []
            self.cart_btn.configure(text="🛒 Cart (0)")
            cart_win.destroy()

        chk_btn = ctk.CTkButton(cart_win, text="Proceed to Checkout 💳", fg_color="#FF9F0A", command=checkout)
        chk_btn.pack(pady=(0, 15))


if __name__ == "__main__":
    app = FlipkartStoreApp()
    app.mainloop()
