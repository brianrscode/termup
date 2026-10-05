import asyncio

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class PackageModal(ModalScreen):
    def __init__(self, package_name: str, package_origin: str) -> None:
        super().__init__()
        self.package_name = package_name
        self.package_origin = package_origin

    def compose(self) -> ComposeResult:
        with Vertical(id="modal_dialog"):
            yield Static(
                f"Package selected for update:\n\n[bold cyan]{self.package_name}[/bold cyan]"
            )
            yield HorizontalGroup(
                Button("Actualizar", variant="primary", id="upgrade_btn"),
                Button("Cancelar", variant="primary", id="close_btn"),
            )

    @on(Button.Pressed, "#close_btn")
    def close_modal(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#upgrade_btn")
    async def upgrade_package(self) -> None:

        if self.package_origin == "pacman":
            await asyncio.create_subprocess_exec(
                "kitty",
                "sudo",
                "pacman",
                "-S",
                f"{self.package_name}; read -rp 'Press Enter to close...'",
            )
            self.dismiss()
        elif self.package_origin == "aur":
            await asyncio.create_subprocess_exec(
                "kitty",
                "sudo",
                "paru",
                "-S",
                f"{self.package_name}; read -rp 'Press Enter to close...'",
            )
            self.dismiss()
        elif self.package_origin == "flatpak":
            await asyncio.create_subprocess_exec(
                "kitty",
                "flatpak",
                "update",
                f"{self.package_name}; read -rp 'Press Enter to close...'",
            )
            self.dismiss()
