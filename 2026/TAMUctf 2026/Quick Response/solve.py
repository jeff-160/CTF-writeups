#!/usr/bin/env python3
"""
CTF QR Decoder - Checkerboard XOR Unmask
Fixes QR codes that have been XORed with a checkerboard pattern.

Usage:
    python decode_qr.py <image_path>

Requirements:
    pip install opencv-python-headless pyzbar pillow numpy
"""

import sys
import numpy as np
import cv2
from PIL import Image

def decode_checkerboard_qr(image_path: str, save_corrected: bool = True) -> str | None:
    """
    Decodes a QR code that has been XORed with a (row+col)%2 checkerboard mask.

    Args:
        image_path:      Path to the distorted QR image.
        save_corrected:  If True, saves the corrected QR as 'corrected_qr.png'.

    Returns:
        Decoded string, or None if decoding failed.
    """
    # ── 1. Load & binarise ──────────────────────────────────────────────────
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot open image: {image_path}")

    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    h, w = img.shape

    # ── 2. Detect module size from pixel transitions ─────────────────────────
    # Scan along row 0 to find the spacing between transitions (= module size).
    row0 = binary[0, :]
    transitions = np.where(np.diff(row0.astype(int)) != 0)[0]
    if len(transitions) < 2:
        raise ValueError("Could not detect module transitions in row 0.")

    module_size = int(np.median(np.diff(transitions)))
    n_modules   = round(w / module_size)
    print(f"[*] Detected module size : {module_size} px")
    print(f"[*] Grid size            : {n_modules}x{n_modules} modules")
    print(f"[*] QR Version           : {(n_modules - 21) // 4 + 1}")

    # ── 3. Sample the binary grid ────────────────────────────────────────────
    grid = np.zeros((n_modules, n_modules), dtype=np.uint8)
    for r in range(n_modules):
        for c in range(n_modules):
            px = c * module_size + module_size // 2
            py = r * module_size + module_size // 2
            grid[r, c] = 1 if binary[py, px] > 0 else 0

    # ── 4. XOR with checkerboard mask ────────────────────────────────────────
    checkerboard = np.fromfunction(
        lambda r, c: (r + c) % 2, (n_modules, n_modules), dtype=int
    ).astype(np.uint8)
    corrected = np.bitwise_xor(grid, checkerboard)

    # ── 5. Render corrected QR image ─────────────────────────────────────────
    cell   = module_size
    quiet  = 4 * cell                          # 4-module quiet zone
    side   = n_modules * cell + 2 * quiet
    canvas = np.full((side, side), 255, dtype=np.uint8)

    for r in range(n_modules):
        for c in range(n_modules):
            val = 0 if corrected[r, c] else 255
            canvas[
                quiet + r * cell : quiet + (r + 1) * cell,
                quiet + c * cell : quiet + (c + 1) * cell,
            ] = val

    if save_corrected:
        out_path = "flag.png"
        cv2.imwrite(out_path, canvas)
        print(f"[*] Corrected QR saved  : {out_path}")


decode_checkerboard_qr('quick-response.png')