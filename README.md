# tree-md

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#licencia)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Requires: pathspec](https://img.shields.io/badge/requires-pathspec-orange.svg)](#uso)

Un script sencillo en **Python** para generar un árbol de directorios en formato Markdown.

Este proyecto se realizó **con fines educativos**. Sé que ya existen herramientas similares (como el comando `tree` en Unix), pero el objetivo fue practicar y aprender Python creando mi propia versión.

---

## ✨ Características

- Genera árboles de directorios con conectores Unicode (`├──`, `└──`, `│`).
- Exporta salida en formato Markdown lista para documentación.
- Soporta reglas de `.gitignore` (usando [pathspec](https://pypi.org/project/pathspec/)).
- Bandera opcional para ocultar archivos y carpetas ocultas (`-I` o `--ignore-hidden`).
- Configurable hasta una profundidad máxima (`--max-depth`).
- Permite omitir carpetas específicas con `--skip-dirs`.
- Manejo seguro de errores de permisos y entornos virtuales.
- Funciona como:
  - **Herramienta CLI**
  - **Módulo Python importable**

---

## 🚀 Uso

### CLI

```bash
# Uso básico
python tree_md.py --path . --max-depth 3

# Ignorar archivos/carpetas ocultas
python tree_md.py --path . -I

# Aplicar reglas de .gitignore
python tree_md.py --path . --gitignore

# Omitir directorios específicos
python tree_md.py --path . --skip-dirs venv __pycache__
```

El resultado se guarda en un archivo Markdown (por defecto: `estructura_folderv3.md`).

### Ejemplo de salida

```
proyecto/
├── src/
│   ├── main.py
│   └── utils.py
├── .gitignore
├── README.md
└── tree_md.py
```

### Como módulo Python

```python
from tree_md import tree_md

output = tree_md(path=".", skip_dirs=["venv"], max_depth=2)
print(output)
```

---

## 📚 Fines educativos

Este script fue construido como un **ejercicio de aprendizaje**:

- Practicar Python (`argparse`, `pathlib`, recursión).
- Explorar cómo manejar `.gitignore` desde código.
- Aprender a estructurar un script como herramienta CLI.

No busca reemplazar otras herramientas existentes, sino ser un recurso de práctica y aprendizaje.

---

## 📜 Licencia

MIT License. Libre para usar, modificar y compartir.
