"""
actuator.py
Mark‑102 2 軸ステージコントローラを pyserial で操作するクラス群．
"""

from __future__ import annotations
import time
import serial
from typing import Tuple, Optional

# ---------- ハード依存パラメータ ----------
DEFAULT_BAUDRATE = 19200        # DIP SW 既定値
DEFAULT_TIMEOUT  = 0.2          # 受信待ちタイムアウト[s]
CMD_DELAY        = 0.10         # 連続送信を避ける待機[s]

# SGSP26‑200 (Half‑step) : 1 パルス ≒ 2 µm → 0.002 mm/pulse  :contentReference[oaicite:0]{index=0}
HALF_STEP_MM_PER_PULSE = 0.002

class Mark102:
    """Mark‑102 コントローラ（2 軸）を簡易に操作するヘルパークラス."""

    def __init__(
        self,
        port: str,
        baudrate: int = DEFAULT_BAUDRATE,
        mm_per_pulse: float = HALF_STEP_MM_PER_PULSE,
    ) -> None:
        self._ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            rtscts=True,
            timeout=DEFAULT_TIMEOUT,
        )
        self._mm_per_pulse = mm_per_pulse

    # -------------- 汎用低レベル I/O -----------------
    def _write(self, cmd: str) -> None:
        """コマンド送信（CRLF を自動付与）"""
        full = f"{cmd}\r\n"
        self._ser.write(full.encode())
        time.sleep(CMD_DELAY)

    def _query(self, cmd: str) -> str:
        """問い合わせコマンドを送信し応答を返す"""
        self._write(cmd)
        return self._ser.readline().decode().strip()

    # -------------- 基本操作 -----------------
    def home(self, axis: int, direction: str = "+") -> None:
        """指定軸を機械原点へ戻す（H コマンド）"""
        self._write(f"H:{axis}{direction}")   # H:1+ など
        self._write("G:")                     # Drive
        self._wait_ready()

    def move_rel(self, axis: int, mm: float) -> None:
        """指定軸を相対移動．mm に正負符号で方向を指定"""
        pulses = round(abs(mm) / self._mm_per_pulse)
        sign   = "+" if mm >= 0 else "-"
        self._write(f"M:{axis}{sign}P{pulses}")
        self._write("G:")
        self._wait_ready()

    def move_rel_xy(self, x_mm: float, z_mm: float) -> None:
        """2 軸同時相対移動（W 指定）"""
        p_x = round(abs(x_mm) / self._mm_per_pulse)
        p_z = round(abs(z_mm) / self._mm_per_pulse)
        s_x = "+" if x_mm >= 0 else "-"
        s_z = "+" if z_mm >= 0 else "-"
        self._write(f"M:W{s_x}P{p_x}{s_z}P{p_z}")
        self._write("G:")
        self._wait_ready()

    def get_position(self) -> Tuple[int, int]:
        """現在パルス位置を返す（Q コマンド）"""
        resp = self._query("Q:")              # "12345,-6789" など
        x_str, z_str = resp.split(",")
        return int(x_str), int(z_str)

    def close(self) -> None:
        """シリアルポートを閉じる"""
        self._ser.close()

    # -------------- 内部ヘルパ -----------------
    def _wait_ready(self, check_interval: float = 0.2) -> None:
        """! コマンドで Busy / Ready をポーリングし移動完了を待つ"""
        while True:
            status = self._query("!:")        # returns 'B' or 'R'  :contentReference[oaicite:1]{index=1}
            if status.upper().startswith("R"):
                break
            time.sleep(check_interval)

    # ---------- コンテキストマネージャ ----------
    def __enter__(self) -> "Mark102":
        return self

    def __exit__(self, exc_type, exc, tb) -> Optional[bool]:
        self.close()
        # 例外は上位へ伝播
        return None
