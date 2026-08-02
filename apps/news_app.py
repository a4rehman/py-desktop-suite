import requests
import webbrowser
from io import BytesIO
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Fallback featured news articles when API key is offline or rate-limited
SAMPLE_NEWS = [
    {
        "title": "Quantum Computing Reaches Breakthrough in Error Correction",
        "description": "Researchers have demonstrated a fault-tolerant quantum architecture that reduces computational noise by 90%, opening new doors for cryptography and materials science.",
        "url": "https://news.google.com",
        "urlToImage": "https://picsum.photos/600/300?random=1",
        "source": {"name": "Tech Daily"}
    },
    {
        "title": "Global Clean Energy Investments Hit Record $1.8 Trillion",
        "description": "Solar and wind energy projects dominated capital flows worldwide, outpacing traditional fossil fuel infrastructure investments for the third consecutive year.",
        "url": "https://news.google.com",
        "urlToImage": "https://picsum.photos/600/300?random=2",
        "source": {"name": "World Finance"}
    },
    {
        "title": "Next-Generation Space Telescope Captures Deepest View of Universe",
        "description": "Astronomers reveal stellar nurseries and primordial galaxies formed just 300 million years after the Big Bang, providing fresh insight into early cosmic evolution.",
        "url": "https://news.google.com",
        "urlToImage": "https://picsum.photos/600/300?random=3",
        "source": {"name": "Astro Science"}
    },
    {
        "title": "AI-Driven Healthcare Diagnostic Tool Approved for Clinical Use",
        "description": "Medical regulators have granted clearance to a deep-learning algorithm capable of detecting early-stage cardiovascular anomalies with 98.4% accuracy.",
        "url": "https://news.google.com",
        "urlToImage": "https://picsum.photos/600/300?random=4",
        "source": {"name": "Health Pulse"}
    }
]

class NewsApp(ctk.CTk):
    def __init__(self, api_key=None):
        super().__init__()

        self.title("Global News Desk")
        self.geometry("700x620")
        self.resizable(False, False)

        self.api_key = api_key
        self.articles = []
        self.current_index = 0

        self._build_ui()
        self.load_category("general")

    def _build_ui(self):
        # Header Navigation Frame
        header = ctk.CTkFrame(self, fg_color="#1C1C1E", corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)

        title_lbl = ctk.CTkLabel(
            header,
            text="📰 Global News Hub",
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#FFFFFF"
        )
        title_lbl.pack(side="left", padx=20, pady=15)

        # Categories Buttons
        cat_frame = ctk.CTkFrame(header, fg_color="transparent")
        cat_frame.pack(side="right", padx=20, pady=10)

        categories = [("General", "general"), ("Tech", "technology"), ("Business", "business"), ("Sports", "sports")]
        for label, cat in categories:
            btn = ctk.CTkButton(
                cat_frame,
                text=label,
                width=75,
                height=30,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#2C2C2E",
                hover_color="#0A84FF",
                corner_radius=8,
                command=lambda c=cat: self.load_category(c)
            )
            btn.pack(side="left", padx=4)

        # Content Card Container
        self.card = ctk.CTkFrame(self, fg_color="#2C2C2E", corner_radius=16)
        self.card.pack(fill="both", expand=True, padx=20, pady=20)

        # Article Image Placeholder Label
        self.image_label = ctk.CTkLabel(self.card, text="", corner_radius=12)
        self.image_label.pack(fill="x", padx=15, pady=(15, 10))

        # Source Badge & Title
        self.source_label = ctk.CTkLabel(
            self.card,
            text="CATEGORY / SOURCE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#0A84FF",
            anchor="w"
        )
        self.source_label.pack(fill="x", padx=20, pady=(5, 0))

        self.news_title = ctk.CTkLabel(
            self.card,
            text="Loading news headlines...",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#FFFFFF",
            wraplength=620,
            justify="left",
            anchor="w"
        )
        self.news_title.pack(fill="x", padx=20, pady=(5, 10))

        # Description
        self.news_desc = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#EBEBF5",
            wraplength=620,
            justify="left",
            anchor="w"
        )
        self.news_desc.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Bottom Actions Bar (Prev, Read More, Next)
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.btn_prev = ctk.CTkButton(
            actions_frame,
            text="◀ Previous",
            width=120,
            fg_color="#3A3A3C",
            hover_color="#48484A",
            corner_radius=10,
            command=self.prev_news
        )
        self.btn_prev.pack(side="left")

        self.btn_read_more = ctk.CTkButton(
            actions_frame,
            text="Read Full Story 🔗",
            width=160,
            fg_color="#0A84FF",
            hover_color="#0066CC",
            corner_radius=10,
            command=self.open_link
        )
        self.btn_read_more.pack(side="left", expand=True)

        self.btn_next = ctk.CTkButton(
            actions_frame,
            text="Next ▶",
            width=120,
            fg_color="#3A3A3C",
            hover_color="#48484A",
            corner_radius=10,
            command=self.next_news
        )
        self.btn_next.pack(side="right")

    def load_category(self, category):
        self.articles = []
        if self.api_key and self.api_key != "YOUR_API_KEY":
            try:
                url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={self.api_key}"
                res = requests.get(url, timeout=5).json()
                if "articles" in res and res["articles"]:
                    self.articles = res["articles"]
            except Exception:
                pass

        if not self.articles:
            self.articles = SAMPLE_NEWS

        self.current_index = 0
        self.render_article()

    def render_article(self):
        if not self.articles:
            return

        article = self.articles[self.current_index]
        source_name = article.get("source", {}).get("name", "Headlines")
        self.source_label.configure(text=f"SOURCE: {source_name.upper()}")
        self.news_title.configure(text=article.get("title", "No Title"))
        self.news_desc.configure(text=article.get("description") or "No description provided for this story.")

        # Render Image preview
        img_url = article.get("urlToImage")
        if img_url:
            try:
                resp = requests.get(img_url, timeout=4)
                img_data = Image.open(BytesIO(resp.content))
                img_data = img_data.resize((620, 240), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(620, 240))
                self.image_label.configure(image=photo, text="")
            except Exception:
                self.image_label.configure(image=None, text="[ Image Preview Unavailable ]")
        else:
            self.image_label.configure(image=None, text="[ No Image ]")

    def next_news(self):
        if self.current_index < len(self.articles) - 1:
            self.current_index += 1
            self.render_article()

    def prev_news(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.render_article()

    def open_link(self):
        if self.articles:
            url = self.articles[self.current_index].get("url")
            if url:
                webbrowser.open(url)

if __name__ == "__main__":
    app = NewsApp()
    app.mainloop()
