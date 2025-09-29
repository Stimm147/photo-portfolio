import reflex as rx
import os
import gc

api_url = os.getenv(
    "API_URL", "http://reflex-example-backend-production.up.railway.app"
)

config = rx.Config(
    app_name="reflex_example",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    api_url=api_url,
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://frontend-copy-production-f2a9.up.railway.app",
    ],
    compile=True,
    telemetry_enabled=False,
)
