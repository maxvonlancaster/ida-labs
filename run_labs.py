"""Запуск лабораторних по черзі."""

from pathlib import Path
from tempfile import TemporaryDirectory
import argparse
import asyncio
import json
import os
import sys

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager


def main():
    parser = argparse.ArgumentParser(description='Виконати лабораторні роботи 1-3')
    parser.add_argument('numbers', nargs='*', type=int, choices=[1, 2, 3])
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    os.environ['PYTHONHASHSEED'] = '42'
    os.environ['OMP_NUM_THREADS'] = '2'
    os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with TemporaryDirectory(prefix='ida-labs-kernel-') as temporary:
        kernels = Path(temporary)
        kernel_dir = kernels / 'ida-labs'
        kernel_dir.mkdir()
        (kernel_dir / 'kernel.json').write_text(json.dumps({
            'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name': 'Python 3', 'language': 'python',
        }), encoding='utf-8')

        for number in args.numbers or [1, 2, 3]:
            path = root / f'assignement-{number}.ipynb'
            notebook = nbformat.read(path, as_version=4)
            manager = KernelManager(kernel_name='ida-labs', kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernels)]))

            def progress(cell, cell_index, **kwargs):
                if cell.cell_type == 'code':
                    print(f'ЛР{number}: клітинка {cell_index}', flush=True)

            client = NotebookClient(notebook, km=manager, timeout=600, allow_errors=False,
                                    record_timing=False, store_widget_state=False,
                                    resources={'metadata': {'path': str(root)}}, on_cell_start=progress)
            try:
                client.execute()
            finally:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
            notebook.metadata.kernelspec = {'display_name': 'Python 3', 'name': 'python3', 'language': 'python'}
            nbformat.write(notebook, path)
            print(f'ЛР{number}: виконано без помилок', flush=True)


if __name__ == '__main__':
    main()
