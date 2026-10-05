import asyncio

from parsers.aur import AURParser
from parsers.flatpak import FlatpakParser
from parsers.pacman import PacmanParser


async def main():
    pacman_parser = PacmanParser()
    aur_parser = AURParser()
    flatpak_parser = FlatpakParser()

    # Se inician y ejecutan los 3 parsers al mismo tiempo en paralelo/concurrencia
    pacman_packages, aur_packages, flatpak_packages = await asyncio.gather(
        pacman_parser.parse(), aur_parser.parse(), flatpak_parser.parse()
    )

    # Una vez que los 3 terminan, imprimes los resultados
    print("Pacman updates:".center(50, "-"))
    for pkg in pacman_packages:
        print(
            f"Nombre: {pkg.name}\nVersion anterior: {pkg.old_version}\nVersión nueva: {pkg.new_version}\n"
        )
    print(f"Total de actualizaciones: {len(pacman_packages)}")

    print("AUR updates:".center(50, "-"))
    for pkg_aur in aur_packages:
        print(
            f"Nombre: {pkg_aur.name}\nVersion anterior: {pkg_aur.old_version}\nVersión nueva: {pkg_aur.new_version}\n"
        )
    print(f"Total de actualizaciones: {len(aur_packages)}")

    print("Flatpak updates".center(50, "-"))
    for pkg_flatpak in flatpak_packages:
        print(f"Nombre: {pkg_flatpak.name}\nVersión nueva: {pkg_flatpak.new_version}\n")
    print(f"Total de actualizaciones: {len(flatpak_packages)}")

    print(
        "Total de actualizaciones disponibles: ",
        len(pacman_packages) + len(aur_packages) + len(flatpak_packages),
    )


if __name__ == "__main__":
    asyncio.run(main())
