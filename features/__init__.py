import os
import sys

# Получить абсолютный путь к текущему пакету
package_dir = os.path.dirname(os.path.abspath(__file__))

# Добавить путь к пакету в переменную окружения PYTHONPATH
sys.path.append(package_dir)

# Автоматический импорт всех файлов в директории
for filename in os.listdir(package_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        __import__(module_name)

# Экспортировать все импортированные модули
__all__ = [module_name for module_name in globals() if not module_name.startswith('_')]