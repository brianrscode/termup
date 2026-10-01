from models import PackageItem
from commands import run_command
from .parser import Parser


class AURParser(Parser):
    async def parse(self) -> list[PackageItem]:
        paquetes = await run_command("paru -Qua")
        pkgs_list: list[PackageItem] = []
        for paquete in paquetes:
            if not paquete.strip():
                continue
            datos = paquete.split()
            if len(datos) >= 1:
                pkgs_list.append(
                    PackageItem(name=datos[0], old_version=datos[1], new_version=datos[3], origin="aur")
                )
        return pkgs_list
        