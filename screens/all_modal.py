import asyncio

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class AllModal(ModalScreen):
    def compose(self) -> ComposeResult:
        with Vertical(id="modal_dialog"):
            yield Static("Do you want to update all packages?")
            yield HorizontalGroup(
                Button("Update", variant="primary", id="upgrade_btn"),
                Button("Cancel", variant="primary", id="close_btn"),
            )

    @on(Button.Pressed, "#close_btn")
    def close_modal(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#upgrade_btn")
    async def upgrade_package(self) -> None:

        await asyncio.create_subprocess_exec(
            "kitty",
            "bash",
            "-lc",
            "paru -Syu && flatpak update; read -rp 'Press Enter to close...'",
        )
        self.dismiss()
