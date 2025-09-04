# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform

from pathlib import Path


class FfmpegWrapper:
    def __init__(self):
        self.ffmpeg_path = self._get_ffmpeg_path()

    @staticmethod
    def _get_ffmpeg_path() -> Path:
        # PyInstaller 로 빌드된 경우
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS  # PyInstaller 가 언패킹된 폴더
        else:
            base_path = f"{Path(".")}"

        base_path = Path(base_path)
        ffmpeg_binary_name = "ffmpeg"
        if platform.system() == "Windows":
            ffmpeg_binary_name += ".exe"

        return base_path / ffmpeg_binary_name

    def convert_ts_to_mp4(self, ts_list_file_path: Path, mp4_path: Path) -> str:
        try:
            result = subprocess.run([
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", f"{ts_list_file_path.resolve()}",
                "-c", "copy",
                mp4_path
            ], check=True, capture_output=True, text=True)
            return f"{result.stdout}/{result.stderr}"
        except BaseException as e:
            return f"pyException / {e}"
