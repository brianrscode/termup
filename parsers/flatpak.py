from commands import run_command
from models import PackageItem

from .parser import Parser


class FlatpakParser(Parser):
    async def parse(self) -> list[PackageItem]:
        paquetes = await run_command(
            "flatpak remote-ls --updates --app --columns=application,version"
        )
        pkgs_list: list[PackageItem] = []
        for paquete in paquetes:
            if not paquete.strip():
                continue
            datos = paquete.split()
            if len(datos) >= 1:
                pkgs_list.append(
                    PackageItem(name=datos[0], new_version=datos[1], origin="flatpak")
                )
        return pkgs_list
