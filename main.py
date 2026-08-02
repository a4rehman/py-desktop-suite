import subprocess
import sys
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def launch_app(script_path):
    subprocess.Popen([sys.executable, script_path])


class AppLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Desktop Suite — Launcher")
        self.geometry("560x620")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # Gradient-style header panel
        header = ctk.CTkFrame(self, fg_color="#1C1C1E", corner_radius=0)
        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="🚀 Python Desktop Suite",
            font=ctk.CTkFont(family="Inter", size=26, weight="bold"),
            text_color="#FFFFFF"
        )
        title.pack(pady=(25, 5))

        subtitle = ctk.CTkLabel(
            header,
            text="Select an app to launch",
            font=ctk.CTkFont(size=14),
            text_color="#8E8E93"
        )
        subtitle.pack(pady=(0, 20))

        # App cards
        apps_frame = ctk.CTkFrame(self, fg_color="transparent")
        apps_frame.pack(fill="both", expand=True, padx=30, pady=25)

        apps = [
            {
                "name": "Pro Calculator",
                "desc": "Scientific calculator with history & keyboard support",
                "icon": "🧮",
                "color": "#FF9F0A",
                "hover": "#D98200",
                "script": "apps/calculator.py"
            },
            {
                "name": "Global News Hub",
                "desc": "Live news feed with category filters & article previews",
                "icon": "📰",
                "color": "#0A84FF",
                "hover": "#0066CC",
                "script": "apps/news_app.py"
            },
            {
                "name": "Nexus ATM Terminal",
                "desc": "Interactive ATM simulator with PIN security & receipts",
                "icon": "🏧",
                "color": "#30D158",
                "hover": "#24A143",
                "script": "apps/atm_system.py"
            },
            {
                "name": "Flipkart Store",
                "desc": "E-commerce product catalog with cart & checkout",
                "icon": "🛍️",
                "color": "#FF453A",
                "hover": "#D1342B",
                "script": "apps/store_app.py"
            },
        ]

        for app_data in apps:
            self._build_app_card(apps_frame, app_data)

        # Footer
        footer = ctk.CTkLabel(
            self,
            text="Built with Python & CustomTkinter",
            font=ctk.CTkFont(size=12),
            text_color="#3A3A3C"
        )
        footer.pack(pady=(0, 18))

    def _build_app_card(self, parent, data):
        card = ctk.CTkFrame(parent, fg_color="#2C2C2E", corner_radius=16)
        card.pack(fill="x", pady=8)

        icon_lbl = ctk.CTkLabel(
            card,
            text=data["icon"],
            font=ctk.CTkFont(size=34)
        )
        icon_lbl.pack(side="left", padx=20, pady=18)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=12)

        ctk.CTkLabel(
            info,
            text=data["name"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF",
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info,
            text=data["desc"],
            font=ctk.CTkFont(size=12),
            text_color="#8E8E93",
            anchor="w",
            wraplength=280
        ).pack(fill="x", pady=(3, 0))

        script = data["script"]
        ctk.CTkButton(
            card,
            text="Launch ▶",
            width=100,
            fg_color=data["color"],
            hover_color=data["hover"],
            corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda s=script: launch_app(s)
        ).pack(side="right", padx=20)


if __name__ == "__main__":
    app = AppLauncher()
    app.mainloop()
