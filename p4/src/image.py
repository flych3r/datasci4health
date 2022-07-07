from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps


def get_file_paths(dirname: str, exts: str | list[str], dir: Path) -> list:
    if isinstance(exts, str):
        exts = [exts]

    files = []
    for ext in exts:
        files.extend((dir / dirname).glob(f'*.{ext}'))
    return files

def read_img(path: Path, grayscale: bool = True) -> np.array:
    img = Image.open(path)
    if grayscale:
        img = ImageOps.grayscale(img)
    return np.asarray(img)

def split_brain_and_mask(images_paths: list[Path]) -> tuple[list[Path], list[Path]]:
    brains = list(filter(lambda x: 'mask' not in str(x), images_paths))
    masks = list(filter(lambda x: 'mask' in str(x), images_paths))
    return brains, masks

def group_patients(brains: dict[str, Path], masks: dict[str, Path], only_masked: bool = True):
    mask_patients = defaultdict(list)

    for img in masks:
        pct = img.stem.split('_')[0]
        flair = img.stem.split('_')[1]
        mask_patients[pct].append(flair)

    brain_patients = defaultdict(list)

    for img in brains:
        pct = img.stem.split('_')[0]
        flair = img.stem.split('_')[1]
        if not only_masked or flair in mask_patients[pct]:
            brain_patients[pct].append(img)

    return brain_patients, mask_patients

def plot_10_brain_images(images: list[Path], labels: list[str] = None):
    if labels is None:
        labels = [None] * 10
    rows, cols = (2, 5)

    fig, ax = plt.subplots(rows, cols, figsize=(20, 10))

    i = 0
    for j, (img, lbl) in enumerate(zip(images, labels)):
            ax[i][j % 5].imshow(read_img(img), cmap='gray')
            if lbl is not None:
                ax[i][j % 5].set_title(lbl)
            ax[i][j % 5].grid(False)
            ax[i][j % 5].set_xticklabels([])
            ax[i][j % 5].set_yticklabels([])
            if j == 4:
                i += 1

    plt.tight_layout()
    plt.show()
