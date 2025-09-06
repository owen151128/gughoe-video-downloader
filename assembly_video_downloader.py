# -*- coding: utf-8 -*-

import subprocess

from pathlib import Path
from urllib.parse import urljoin

import requests
import m3u8


class AssemblyVideoDownloader:
    @staticmethod
    def _normalize_to_progress(value, max_value):
        if max_value == 0:
            return 0
        ratio = value / max_value
        ratio = max(0.0, min(1.0, ratio))  # 0~1 범위로 클램핑
        return int(ratio * 100)

    @staticmethod
    def download_assembly_video_ts(m3u8_url, progress_signal, download_dir: Path = None) -> str:
        master_m3u8 = m3u8.load(m3u8_url)
        if not master_m3u8.is_variant:
            return "m3u8 url is not variant"
        if len(master_m3u8.playlists) < 1:
            return "M3U8 URL does not contain any playlists"
        absolute_media_url = urljoin(master_m3u8.base_uri, master_m3u8.playlists[0].uri)
        ts_list = m3u8.load(absolute_media_url)
        if not download_dir.exists():
            download_dir.mkdir()
        working_dir = Path(download_dir).resolve()
        ts_list_file_path = working_dir / "ts_list.txt"
        with open(ts_list_file_path, "w") as ts_list_file:
            for i, segment in enumerate(ts_list.segments):
                ts_url = segment.absolute_uri
                ts_file_path = Path(download_dir) / f"segment_{i}.ts"
                print(f"Downloading {ts_url} to {ts_file_path}")
                ts_data = requests.get(ts_url).content
                with open(ts_file_path, "wb") as f:
                    f.write(ts_data)
                ts_list_file.write(f"file '{ts_file_path.resolve()}'\n")
                progress_signal.emit(AssemblyVideoDownloader._normalize_to_progress(i, len(ts_list.segments)))

        return str(ts_list_file_path.resolve())
