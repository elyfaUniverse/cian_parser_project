"""Установка зависимостей проекта в выбранное окружение Python."""

from pathlib import Path
import subprocess
import sys


def install_dependencies():
    requirements = Path(__file__).with_name("requirements.txt")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
        check=True,
    )
    print("Зависимости проекта установлены.")


if __name__ == "__main__":
    install_dependencies()
