import asyncio
import subprocess
from textual import on
from textual.widgets import Button
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import DataTable, Footer, Header, Static, RadioButton, RadioSet
from textual.containers import VerticalGroup, VerticalScroll, HorizontalGroup, Container

from parsers.pacman import PacmanParser
from parsers.aur import AURParser
from parsers.flatpak import FlatpakParser

from screens.package_modal import PackageModal
from screens.category_modal import CategoryModal
from screens.all_modal import AllModal


class Categories(VerticalGroup):
    pacman_count: reactive[int] = reactive(0)
    aur_count: reactive[int] = reactive(0)
    flatpak_count: reactive[int] = reactive(0)
    all_count: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        self.border_title = "CATEGORIES"
        with RadioSet(id="radio_set"):
            yield RadioButton(f"All ({self.all_count})", id="all_rbtn", value=True)
            yield RadioButton(f"Pacman ({self.pacman_count})", id="pacman_rbtn")
            yield RadioButton(f"AUR ({self.aur_count})", id="aur_rbtn")
            yield RadioButton(f"Flatpak ({self.flatpak_count})", id="flatpak_rbtn")

    def watch_pacman_count(self, new_count: int) -> None:
        try:
            self.query_one("#pacman_rbtn", RadioButton).label = f"Pacman ({new_count})"
        except Exception:
            pass

    def watch_aur_count(self, new_count: int) -> None:
        try:
            self.query_one("#aur_rbtn", RadioButton).label = f"AUR ({new_count})"
        except Exception:
            pass

    def watch_flatpak_count(self, new_count: int) -> None:
        try:
            self.query_one("#flatpak_rbtn", RadioButton).label = f"Flatpak ({new_count})"
        except Exception:
            pass

    def watch_all_count(self, new_count: int) -> None:
        try:
            self.query_one("#all_rbtn", RadioButton).label = f"All ({new_count})"
        except Exception:
            pass


class Actions(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "ACTIONS"
        yield Button(f"[U] Upgrade All", id="upgrade_all_btn")  # , compact=True
        yield Button(f"[C] Upgrade Selected Category", id="upgrade_selected_btn")  # , compact=True
        yield Button(f"[S] Upgrade Selected Package", id="upgrade_package_btn")  # , compact=True
        # yield Button(f"[D] Delete Selected Package", id="delete_package_btn")  # , compact=True


class Details(Container):
    def compose(self) -> ComposeResult:
        yield Static(subprocess.run(["checkupdates", "-d"], capture_output=True, text=True).stdout, id="details") # Static("", id="details")


class AppHeader(Static):
    def __init__(self) -> None:
        super().__init__(
            """
░▀█▀░█▀▀░█▀▄░█▄█░█░█░█▀█
░░█░░█▀▀░█▀▄░█░█░█░█░█▀▀
░░▀░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░░
            """,
            id="app-header",
        )


class TermUp(App):
    """An update manager for Arch Linux."""
    CSS_PATH = "styles/main.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("u", "upgrade_all", "Upgrade all"),
        Binding("c", "upgrade_selected", "Upgrade selected category"),
        Binding("s", "upgrade_package", "upgrade selected package"),
        # Binding("d", "", "delete package")
    ]

    # App packages
    pacman_packages = []
    aur_packages = []
    flatpak_packages = []
    all_packages = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield HorizontalGroup(
            VerticalGroup(
                AppHeader(),
                Categories(),
                Actions(),
                id="left-side"
            ),
            VerticalScroll(
                DataTable(),
                id="right-side"
            )
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.theme = "tokyo-night"
        self.query_one(RadioSet).focus()  # Starts with focus on the first radio button

        table = self.query_one(DataTable)
        table.border_title="PACKAGES TO UPDATE"
        table.cursor_type = "row"
        table.add_columns("Package", "Old version", "New version", "Origin")

        pacman_parser = PacmanParser()
        aur_parser = AURParser()
        flatpak_parser = FlatpakParser()

        # Save data in instance attributes (self)
        self.pacman_packages, self.aur_packages, self.flatpak_packages = await asyncio.gather(
            pacman_parser.parse(),
            aur_parser.parse(),
            flatpak_parser.parse()
        )
        self.all_packages = self.pacman_packages + self.aur_packages + self.flatpak_packages

        # Update counter panel
        categories = self.query_one(Categories)
        categories.pacman_count = len(self.pacman_packages)
        categories.aur_count = len(self.aur_packages)
        categories.flatpak_count = len(self.flatpak_packages)
        categories.all_count = len(self.all_packages)

        # Load the initial data (All updates by default)
        self.populate_table(self.all_packages)

    @on(RadioSet.Changed)
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        button_id = event.pressed.id

        if button_id == "pacman_rbtn":
            self.populate_table(self.pacman_packages)
        elif button_id == "aur_rbtn":
            self.populate_table(self.aur_packages)
        elif button_id == "flatpak_rbtn":
            self.populate_table(self.flatpak_packages)
        elif button_id == "all_rbtn":
            self.populate_table(self.all_packages)

    def populate_table(self, packages) -> None:
        """Limpia y repuebla la tabla con la lista de paquetes dada."""
        table = self.query_one(DataTable)
        table.clear()
        for pkg in packages:
            table.add_row(pkg.name, pkg.old_version, pkg.new_version, pkg.origin)

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "upgrade_all_btn":
            self.action_upgrade_all()
        elif event.button.id == "upgrade_selected_btn":
            self.action_upgrade_selected()
        elif event.button.id == "upgrade_package_btn":
            self.action_upgrade_package()
        # elif event.button.id == "delete_package_btn":
        #     self.action_delete_package()

    @on(Button.Pressed, "#upgrade_all_btn")
    def action_upgrade_all(self):
        self.push_screen(AllModal())
        

    @on(Button.Pressed, "#upgrade_selected_btn")
    def action_upgrade_selected(self):
        category = self.query_one(RadioSet)
        
        # Get the currently selected button
        selected_button = category.pressed_button

        self.push_screen(CategoryModal(selected_button.label))

    
    @on(Button.Pressed, "#upgrade_package_btn")
    def action_upgrade_package(self) -> None:
        table = self.query_one(DataTable)
        
        if table.cursor_row is None:
            self.notify("No hay ningún paquete seleccionado en la tabla", severity="warning")
        else:
            row_data = table.get_row_at(table.cursor_row)
            package_name = row_data[0]
            
            self.push_screen(PackageModal(package_name))

    async def action_refresh(self):
        self.query_one(DataTable).clear()
        await self.on_mount()

if __name__ == "__main__":
    app = TermUp()
    app.run()