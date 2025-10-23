#!/usr/bin/env python3
"""CLI wrapper para ejecutar los scripts del proyecto sin modificarlos.

Ejemplos:
  python cli.py createpng 3
  python cli.py findfile ruta/al/archivo.txt termino
  python cli.py show ruta/al/archivo.txt
  python cli.py scrape
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from typing import List

ROOT = os.path.dirname(__file__)

SCRIPTS = {
    'createpng': os.path.join(ROOT, 'createpng', 'createpng.py'),
    'createpng2': os.path.join(ROOT, 'CreatePNG2.0', 'CreatePNG.py'),
    'findfile': os.path.join(ROOT, 'Find_File', 'Find_File.py'),
    'show': os.path.join(ROOT, 'main', 'main.py'),
    'scrape': os.path.join(ROOT, 'Scraping', 'Scraping.py'),
}


def run_script(script_path: str, args: List[str]) -> int:
    if not os.path.exists(script_path):
        print(f"Error: script no encontrado: {script_path}", file=sys.stderr)
        return 2

    cmd = [sys.executable, script_path] + args
    # Mostrar el comando que se va a ejecutar
    print('Ejecutando:', ' '.join(f'"{p}"' if ' ' in p else p for p in cmd))

    try:
        proc = subprocess.run(cmd)
        return proc.returncode
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"Error al ejecutar el script: {e}", file=sys.stderr)
        return 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Wrapper CLI para scripts del proyecto')
    sub = p.add_subparsers(dest='command', help='subcomando')

    # createpng: forwardea todos los argumentos al script original
    sc = sub.add_parser('createpng', help='Crear PNGs (forwardea args a createpng/createpng.py)')
    sc.add_argument('args', nargs=argparse.REMAINDER, help='Argumentos para createpng.py')

    sc2 = sub.add_parser('createpng2', help='Crear PNGs (CreatePNG2.0)')
    sc2.add_argument('args', nargs=argparse.REMAINDER, help='Argumentos para CreatePNG.py')

    sf = sub.add_parser('findfile', help='Buscar término en archivo')
    sf.add_argument('args', nargs=argparse.REMAINDER, help='Argumentos para Find_File.py (ruta termino)')

    ss = sub.add_parser('show', help='Mostrar archivo (invoca main/main.py)')
    ss.add_argument('args', nargs=argparse.REMAINDER, help='Argumentos para main.py (ruta)')

    scc = sub.add_parser('scrape', help='Ejecutar scraping (Scraping/Scraping.py)')
    scc.add_argument('args', nargs=argparse.REMAINDER, help='Argumentos opcionales para Scraping.py')

    return p


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    ns = parser.parse_args(argv)

    if ns.command is None:
        parser.print_help()
        return 0

    args = getattr(ns, 'args', []) or []

    if ns.command not in SCRIPTS:
        print(f"Comando desconocido: {ns.command}", file=sys.stderr)
        return 2

    script_path = SCRIPTS[ns.command]
    return run_script(script_path, args)


if __name__ == '__main__':
    raise SystemExit(main())
