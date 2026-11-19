"""Функції для завантаження даних і збереження графіків."""

from pathlib import Path
import hashlib
import json

import kagglehub
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display


ROOT = Path(__file__).resolve().parent
SEED = 42
AUTHOR = "Георгій Апопій Іванович"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "figure.figsize": (10, 5),
    "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.2, "figure.dpi": 110,
})


def save_figure(fig, assignment, name):
    """Зберегти графік окремим PNG і показати його у ноутбуці."""
    path = ROOT / "images" / f"assignment-{assignment}" / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170, bbox_inches="tight")
    display(fig)
    plt.close(fig)
    return path.relative_to(ROOT).as_posix()


def save_json(value, assignment, name):
    path = ROOT / "results" / f"assignment-{assignment}" / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_table(frame, assignment, name):
    path = ROOT / "results" / f"assignment-{assignment}" / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, encoding="utf-8")
    return path


def load_dataset(handle, csv_file):
    """Завантажити CSV з Kaggle та зберегти посилання на набір."""
    dataset_dir = Path(kagglehub.dataset_download(handle))
    path = dataset_dir / csv_file
    if not path.is_file():
        dataset_dir = Path(kagglehub.dataset_download(handle, force_download=True))
        path = dataset_dir / csv_file
    if not path.is_file():
        raise FileNotFoundError(f'Файл {csv_file} відсутній у наборі {handle}')
    frame = pd.read_csv(path)
    manifest_path = ROOT / "results" / "data_sources.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    key = f"{handle}/{csv_file}"
    manifest[key] = {
        "source": f"https://www.kaggle.com/datasets/{handle.split('/versions/')[0]}",
        "file": csv_file, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size, "rows": len(frame),
        "columns": list(frame.columns),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return frame
