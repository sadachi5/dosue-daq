"""
trial.py
任意座標 (x_mm, z_mm) へステージを移動するお試しスクリプト．
5 mm 単位に限定せず，argparse で移動量を mm 単位で受け取る．
"""

import argparse
from actuator import Mark102

def main() -> None:
    parser = argparse.ArgumentParser(description="Mark‑102 位置移動テスト")
    parser.add_argument("--port", default="COM3", help="シリアルポート名")
    parser.add_argument("--baud", type=int, default=19200, help="ボーレート")
    parser.add_argument("--x", type=float, default=0.0, help="x 方向の移動量 [mm]")
    parser.add_argument("--z", type=float, default=0.0, help="z 方向の移動量 [mm]")
    args = parser.parse_args()

    with Mark102(args.port, args.baud) as stg:
        stg.move_rel_xy(args.x, args.z)

if __name__ == "__main__":
    main()
