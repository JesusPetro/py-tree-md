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
- Bandera opcional para **ocultar archivos y carpetas cuyo nombre comience con `.`** (`-I` o `--ignore-hidden`).
- Configurable hasta una profundidad máxima (`--max-depth`).
- Permite **no expandir el contenido** de las carpetas especificadas con `--skip-dirs`.
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
- 
Se sabe que ya existen otras herramientas (y mucho más completas). Este proyecto solo busca ser un recurso de práctica y aprendizaje.

---

## 📜 Licencia

MIT License. Libre para usar, modificar y compartir.
