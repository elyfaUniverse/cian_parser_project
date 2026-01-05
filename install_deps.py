#!/usr/bin/env python3
import subprocess
import sys

def install_dependencies():
    
    packages = [
        'selenium',
        'beautifulsoup4',
        'lxml', 
    ]
    
    print("📦 Установка зависимостей...")
    
    for package in packages:
        print(f"   Устанавливаю {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} установлен")
        except subprocess.CalledProcessError:
            print(f"   ❌ Не удалось установить {package}")
    
    print("\n✅ Все зависимости установлены!")
    print("\nТеперь можно запустить тестовый парсер:")
    print("python test_cian_parser.py")

if __name__ == "__main__":
    install_dependencies()
