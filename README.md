Proyecto "python"
===============

Este repositorio contiene varios scripts de utilidad en Python:

- `createpng/createpng.py`: crea archivos PNG vacíos con nombres aleatorios. Ahora soporta argumentos CLI (cantidad, carpeta, tamaño, color).
- `CreatePNG2.0/CreatePNG.py`: versión alternativa que crea archivos vacíos usando Pathlib.
- `Find_File/Find_File.py`: busca cuántas veces aparece una subcadena en un archivo de texto.
- `main/main.py`: muestra el contenido de un archivo por su ruta.
- `Scraping/Scraping.py`: ejemplo de scraping local con requests + BeautifulSoup.

Requisitos
---------
Instala dependencias con:
```powershell
python -m pip install --user -r requirements.txt
```

Uso principal (`createpng`)
--------------------------
Desde PowerShell, sitúate en la carpeta `createpng` y ejecuta:

```powershell
cd "C:\xampp\htdocs\marcos 2 año desarrollo no tocar pls\python\createpng"
python createpng.py 5 -o imagenes -W 200 -H 200 -c white
```

Esto creará 5 imágenes PNG blancas 200x200 en la carpeta `imagenes`.

Siguientes pasos sugeridos
-------------------------
- Añadir tests (pytest) para funciones utilitarias.
- Añadir un pequeño CLI central que invoque los sub-scripts desde un único punto.
- Contenerizar con Docker o preparar un entorno virtual (venv).
- Añadir CI (GitHub Actions) para linting y test.

Entorno virtual (PowerShell)
----------------------------
Se recomienda usar un entorno virtual para mantener las dependencias aisladas.

1. Crear y activar el entorno (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

2. Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Automatización (script)
------------------------
He añadido un script opcional `setup_env.ps1` en la raíz que crea el entorno y instala dependencias. Para ejecutarlo:

```powershell
cd "C:\xampp\htdocs\marcos 2 año desarrollo no tocar pls\python"
.\setup_env.ps1
```

Si prefieres no usar PowerShell, los comandos equivalentes para otros shells están descritos en la documentación oficial de Python.
