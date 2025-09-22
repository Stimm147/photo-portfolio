import reflex as rx
import os

api_url = os.getenv("API_URL", "http://127.0.0.1:8000")

config = rx.Config(
    app_name="main_page",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    api_url=api_url,
)
