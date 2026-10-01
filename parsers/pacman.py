from models import PackageItem
from commands import run_command
from .parser import Parser

class PacmanParser(Parser):
    async def parse(self) -> list[PackageItem]:
        paquetes = await run_command("checkupdates")
        pkgs_list: list[PackageItem] = []
        for paquete in paquetes:
            if not paquete.strip():
                continue
            datos = paquete.split()
            if len(datos) >= 4:
                pkgs_list.append(
                    PackageItem(name=datos[0], old_version=datos[1], new_version=datos[3], origin="Pacman")
                )
        return pkgs_list