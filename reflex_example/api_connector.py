import reflex as rx
import httpx

CLASSIFY_API_URL = "https://flask-api-production-0454.up.railway.app/api/stats"


class ClassifierState(rx.State):

    image_url: str = ""
    result: dict = {}
    is_loading: bool = False
    error_message: str = ""

    def set_image_url(self, url: str):
        self.image_url = url

    async def classify_image(self):
        if not self.image_url.strip():
            self.error_message = "Podaj URL obrazu"
            return

        self.is_loading = True
        self.error_message = ""
        self.result = {}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    CLASSIFY_API_URL, json={"url": self.image_url}, timeout=30.0
                )
                response.raise_for_status()
                self.result = response.json()
        except httpx.HTTPStatusError as e:
            self.error_message = f"Błąd HTTP: {e.response.status_code}"
        except Exception as e:
            self.error_message = f"Wystąpił błąd: {str(e)}"
        finally:
            self.is_loading = False


def classifier_component() -> rx.Component:
    return rx.box(
        rx.heading("Klasyfikator Obrazów AI", size="5"),
        rx.vstack(
            rx.input(
                placeholder="Wklej URL obrazu (np. https://example.com/image.jpg)",
                value=ClassifierState.image_url,
                on_change=ClassifierState.set_image_url,
                width="100%",
            ),
            rx.button(
                "Klasyfikuj obraz",
                on_click=ClassifierState.classify_image,
                is_loading=ClassifierState.is_loading,
                disabled=~ClassifierState.image_url,
                width="100%",
            ),
            spacing="1",
            margin_top="1",
        ),
        rx.cond(
            ClassifierState.is_loading,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Analizuję obraz..."),
                    spacing="1",
                ),
                margin_top="2",
            ),
        ),
        rx.cond(
            ClassifierState.result,
            rx.vstack(
                rx.heading("Wynik:", size="4"),
                rx.card(
                    rx.vstack(
                        rx.text(
                            f"Klasa ID: {ClassifierState.result.get('class_id', 'N/A')}"
                        ),
                        rx.text(
                            f"Pewność: {ClassifierState.result.get('confidence', 'N/A')}%"
                        ),
                        spacing="1",
                    ),
                    padding="1",
                ),
                rx.cond(
                    ClassifierState.image_url,
                    rx.image(
                        src=ClassifierState.image_url,
                        max_width="300px",
                        max_height="300px",
                        border_radius="8px",
                    ),
                ),
                spacing="1",
                margin_top="2",
            ),
        ),
        rx.cond(
            ClassifierState.error_message,
            rx.callout(
                ClassifierState.error_message,
                icon="alert_triangle",
                color_scheme="red",
                role="alert",
                margin_top="1",
            ),
        ),
        padding="2",
        border="1px solid #eaeaea",
        border_radius="10px",
        max_width="600px",
    )
