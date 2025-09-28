import reflex as rx
import os

api_url = os.getenv("API_URL", "http://127.0.0.1:8000")


config = rx.Config(
    app_name="portfolio",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    api_url=api_url,
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://photo-portfolio-production.up.railway.app",
    ],
    compile=True,
    telemetry_enabled=False,
)
