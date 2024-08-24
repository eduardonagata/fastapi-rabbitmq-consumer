import os
import importlib
from .base import Base

# Caminho da pasta atual
models_dir = os.path.dirname(__file__)

# Itera sobre todos os arquivos Python na pasta
for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"app.models.{filename[:-3]}"  # remove a extensão .py
        importlib.import_module(module_name)
