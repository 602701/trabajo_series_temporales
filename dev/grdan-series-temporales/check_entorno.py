import importlib
import platform
import subprocess
import sys
from datetime import datetime

LIBRERIAS = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "statsmodels",
    "sklearn",
    "statsforecast",
    "utilsforecast",
    "jupyter_core",
    "ipykernel",
]


def version_de(nombre: str) -> str:
    try:
        modulo = importlib.import_module(nombre)
    except ImportError:
        return "FALTA <- instálala con: uv add " + nombre.replace(
            "sklearn", "scikit-learn"
        )
    return getattr(modulo, "__version__", "instalada")


def remoto_git() -> str:
    try:
        salida = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        return salida.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "sin remoto configurado (todavía no has hecho el paso de GitHub)"


print("=" * 60)
print(" Series Temporales · GRDAN 2627 · comprobación del entorno")
print("=" * 60)
print(f"Fecha : {datetime.now():%Y-%m-%d %H:%M}")
print(f"Sistema : {platform.system()} {platform.release()} ({platform.machine()})")
print(f"Python : {sys.version.split()[0]}")
print(f"Ejecutable : {sys.executable}")
print(f"Remoto git : {remoto_git()}")
print("-" * 60)

fallos = 0

for lib in LIBRERIAS:
    v = version_de(lib)
    if v.startswith("FALTA"):
        fallos += 1
    print(f"{lib:<16}: {v}")

print("-" * 60)

en_venv = ".venv" in sys.executable

if not en_venv:
    print(
        "AVISO: Python no se está ejecutando desde .venv. "
        "Usa `uv run python check_entorno.py`."
    )

if fallos == 0 and en_venv:
    print("TODO OK. Entorno listo para la asignatura.")
else:
    print(
        f"Faltan {fallos} librerías o no estás en el entorno del proyecto. "
        "Revisa el paso 5 de la práctica."
    )