"""
scan.py
XZ 平面（20 mm × 20 mm）の中央を原点とし，
x → –x → z → –z の順に 5 mm ステップでジグザグ走査を行う．
各測定点で measure.py を同期実行する．
"""

from pathlib import Path
import subprocess
from actuator import Mark102

# ------------------- 設定パラメータ -------------------
PORT         = "COM3"           # 実際のポートへ変更
BAUD         = 19200
STEP_MM      = 5.0              # 変更可能
SCAN_RANGE   = 20.0             # 全稼働ストローク
MEASURE_PATH = Path("measure.py")
# ------------------------------------------------------

def run_measure() -> None:
    """外部測定スクリプトを同期実行するだけのラッパー"""
    subprocess.run(["python", str(MEASURE_PATH)], check=True)

def xz_scan() -> None:
    """xz 平面をジグザグに掃引し，measure.py を呼び出す"""
    half = SCAN_RANGE / 2.0

    with Mark102(PORT, BAUD) as stg:
        # 原点は「中央」と仮定しているため，ここではホーム動作のみ
        stg.home(axis=1, direction="-")
        stg.home(axis=2, direction="-")

        # ---- X 正方向 ----
        x = 0.0
        while x < half:
            stg.move_rel(axis=1, mm=STEP_MM)
            x += STEP_MM
            run_measure()

        # 原点へ戻る
        stg.move_rel(axis=1, mm=-x)
        x = 0.0

        # ---- X 負方向 ----
        while abs(x) < half:
            stg.move_rel(axis=1, mm=-STEP_MM)
            x -= STEP_MM
            run_measure()

        stg.move_rel(axis=1, mm=-x)  # 原点復帰

        # ---- Z 正方向 ----
        z = 0.0
        while z < half:
            stg.move_rel(axis=2, mm=STEP_MM)
            z += STEP_MM
            run_measure()

        stg.move_rel(axis=2, mm=-z)

        # ---- Z 負方向 ----
        while abs(z) < half:
            stg.move_rel(axis=2, mm=-STEP_MM)
            z -= STEP_MM
            run_measure()

        # 原点復帰
        stg.move_rel(axis=2, mm=-z)

    print("Finished Scanning")

if __name__ == "__main__":
    xz_scan()
