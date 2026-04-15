#!/usr/bin/env python3
"""
Real-ESRGAN 기반 텍스처 4K 업스케일 모듈
DDS → RGBA 분리 → RGB 모델 업스케일 + Alpha bicubic → PNG 저장
"""

import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image


_model_cache = None


def load_model(model_path: str):
    """spandrel로 모델 로드 (싱글톤 캐시)."""
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    from spandrel import ModelLoader

    print(f"[모델] 로딩: {model_path}")
    model = ModelLoader().load_from_file(model_path)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device).eval()
    print(f"[모델] 로드 완료 ({device.upper()})")

    _model_cache = model
    return model


def upscale_file(
    src_path: Path,
    dst_path: Path,
    model_path: str,
    scale: int = 4,
) -> dict:
    """단일 파일 업스케일.

    Returns:
        {"src": str, "dst": str, "original_size": str, "upscaled_size": str, "time": float}
    """
    model = load_model(model_path)
    device = model.device

    # DDS/PNG 로드 → RGBA
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img).astype(np.float32) / 255.0

    rgb_tensor = torch.from_numpy(arr[:, :, :3]).permute(2, 0, 1).unsqueeze(0)
    alpha_tensor = torch.from_numpy(arr[:, :, 3:4]).permute(2, 0, 1).unsqueeze(0)

    start = time.time()

    # RGB 업스케일 (모델)
    with torch.no_grad():
        upscaled_rgb = model(rgb_tensor.to(device)).cpu()

    # Alpha 업스케일 (bicubic)
    _, _, uh, uw = upscaled_rgb.shape
    upscaled_alpha = torch.nn.functional.interpolate(
        alpha_tensor, size=(uh, uw), mode="bicubic", align_corners=False
    ).clamp(0, 1)

    elapsed = time.time() - start

    # 합성 → 저장
    combined = torch.cat([upscaled_rgb, upscaled_alpha], dim=1)
    result_arr = combined.squeeze(0).permute(1, 2, 0).clamp(0, 1).numpy()
    result_arr = (result_arr * 255).astype(np.uint8)
    result_img = Image.fromarray(result_arr, "RGBA")

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    result_img.save(dst_path)

    return {
        "src": str(src_path),
        "dst": str(dst_path),
        "original_size": f"{img.size[0]}x{img.size[1]}",
        "upscaled_size": f"{result_img.size[0]}x{result_img.size[1]}",
        "time": round(elapsed, 2),
    }


def upscale_batch(
    file_list: list[str],
    source_dir: Path,
    output_dir: Path,
    model_path: str,
    scale: int = 4,
    output_format: str = "png",
) -> list[dict]:
    """배치 업스케일.

    Args:
        file_list: 파일명 리스트 (source_dir 기준)
        source_dir: 소스 디렉토리
        output_dir: 출력 디렉토리
        model_path: 모델 파일 경로
        scale: 업스케일 배율
        output_format: 출력 포맷

    Returns:
        결과 리스트 [{src, dst, original_size, upscaled_size, time}, ...]
    """
    results = []
    total = len(file_list)

    for i, filename in enumerate(file_list, 1):
        src_path = source_dir / filename
        dst_name = Path(filename).stem + f"_x{scale}.{output_format}"
        dst_path = output_dir / dst_name

        print(f"[{i}/{total}] {filename}")
        try:
            result = upscale_file(src_path, dst_path, model_path, scale)
            results.append(result)
            print(f"  {result['original_size']} → {result['upscaled_size']} ({result['time']}s)")
        except Exception as e:
            print(f"  [오류] {filename}: {e}")
            results.append({"src": str(src_path), "error": str(e)})

    return results


# ── CLI ────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DDS 텍스처 4K 업스케일")
    parser.add_argument("input", help="입력 파일 또는 디렉토리")
    parser.add_argument("-o", "--output", required=True, help="출력 디렉토리")
    parser.add_argument("-m", "--model", required=True, help="모델 파일 경로")
    parser.add_argument("-s", "--scale", type=int, default=4, help="업스케일 배율")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if input_path.is_file():
        dst = output_dir / (input_path.stem + f"_x{args.scale}.png")
        result = upscale_file(input_path, dst, args.model, args.scale)
        print(f"완료: {result['original_size']} → {result['upscaled_size']} ({result['time']}s)")
    elif input_path.is_dir():
        files = [f.name for f in input_path.iterdir() if f.suffix.lower() in {".dds", ".png", ".tga"}]
        upscale_batch(files, input_path, output_dir, args.model, args.scale)
    else:
        print(f"[오류] 경로를 찾을 수 없음: {input_path}")
