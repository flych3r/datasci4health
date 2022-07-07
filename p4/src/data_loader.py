from __future__ import annotations

from collections import defaultdict
from itertools import chain
from pathlib import Path

import numpy as np

from scipy import stats
from skimage.feature import greycomatrix, greycoprops, local_binary_pattern
from tqdm.auto import tqdm

from .image import read_img

def calc_histogram_statistics(hist: list[int | float]) -> list[float]:
    return [
        np.std(hist),
        np.var(hist),
        stats.mode(hist, axis=None).mode[0],
        np.median(hist),
        stats.skew(hist),
        stats.kurtosis(hist),
        stats.entropy(hist)
    ]

def features_generator(data: dict[str, list[Path]]) -> dict[str, list[list[float]]]:
    images_patient = [
        [k] * len(v) for k, v in data.items()
    ]
    images_patient = list(chain(*images_patient))
    images_paths = list(chain(*data.values()))

    features = defaultdict(list)
    for p, img in tqdm(zip(images_patient, images_paths), total=len(images_patient)):
        img_array = read_img(img)

        hist, _ = np.histogram(img_array, bins=50)
        hist_stats = calc_histogram_statistics(hist)
        contrast = greycoprops(
            greycomatrix(img_array.copy(), distances=[0], angles=[45, 90, 135], levels=256, symmetric=True, normed=True),
            prop='contrast'
        )[0]
        lbp_histogram, _ = np.histogram(local_binary_pattern(img_array, 8 * 3, 3, 'uniform'), bins=50)
        lbp_hist_stats = calc_histogram_statistics(lbp_histogram)

        feats = list(contrast) + list(hist_stats) + list(lbp_hist_stats)

        features[p].append(feats)

    return features

def generate_x_y(
    ids_patients: list[str],
    features_patients: dict[str, list[list[float]]],
    label_patients: int = None,
    shuffle: bool = True
) -> tuple[np.array, np.array]:
    X_features = list(chain(*[features_patients[i] for i in ids_patients]))
    X_features = np.array(X_features)

    if y_target is not None:
        y_target = [label_patients] * len(X_features)
        y_target = np.array(y_target)
    else:
        y_target = None

    if shuffle:
        idx = np.random.permutation(len(X_features))
        X_features = X_features[idx]
        if y_target is not None:
            y_target = y_target[idx]

    return X_features, y_target
