import asyncio
from textual.containers import HorizontalGroup
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button
from textual import on


class CategoryModal(ModalScreen):
    
    def __init__(self, category: str) -> None:
        super().__init__()
        self.category = category
    
    def compose(self) -> ComposeResult:
        with Vertical(id="modal_dialog"):
            yield Static(f"Category selected for updating:\n\n[bold cyan]{self.category}[/bold cyan]")
            yield HorizontalGroup(
                Button("Update", variant="primary", id="upgrade_btn"),
                Button("Cancel", variant="primary", id="close_btn")
            )

    @on(Button.Pressed, "#upgrade_btn")
    async def upgrade_package(self) -> None:

        if "pacman" in self.category:
            await asyncio.create_subprocess_exec(
                "kitty",
                "sudo",
                "pacman",
                "-S",
                "; read -rp 'Press Enter to close...'",
            )
            self.dismiss()
        elif "aur" in self.category:
            await asyncio.create_subprocess_exec(
                "kitty",
                "sudo",
                "paru",
                "-S",
                "; read -rp 'Press Enter to close...'",
            )
            self.dismiss()
        elif "flatpak" in self.category:
            await asyncio.create_subprocess_exec(
                "kitty",
                "flatpak",
                "update; read -rp 'Press Enter to close...'",
            )
            self.dismiss()

    @on(Button.Pressed, "#close_btn")
    def close_modal(self) -> None:
        self.dismiss()