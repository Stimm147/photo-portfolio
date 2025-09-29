import reflex as rx
from rxconfig import config
from reflex_example.api_connector import classifier_component


class State(rx.State):
    """The app state."""

    pass


def index() -> rx.Component:
    """The main page of the app."""
    return rx.container(classifier_component())


app = rx.App(
    theme=rx.theme(
        appearance="light",
    )
)
app.add_page(index)
