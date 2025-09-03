# -*- coding: utf-8 -*-

import time
import urllib

import requests

from urllib.parse import urlparse, urlencode, parse_qs

from streaming_info import StreamingInfo
from video_info import VideoInfo
from video_item import VideoItem


class Consts:
    INFO_FETCH_PATH = "/main/service/movie.do"


class AssemblyInfoFetcher:
    def __init__(self, assembly_target_url: str):
        parsed = urlparse(assembly_target_url)
        self.base_url = parsed.scheme + "://" + parsed.netloc
        self.path = parsed.path
        self.params = parsed.params
        # parse_qs 결과가 key str, value list 이므로, key str, value str 로 변환
        self.queries = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        self.requests_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
        }

    def _to_query_string(self, additional_params: dict = None, exclude_params: list = None) -> str:
        if additional_params is None:
            additional_params = {}

        # dict 합체 및 제외 항목 제거
        final_query = {
            k: v for k, v in (self.queries | additional_params).items() if k not in exclude_params
        }

        return urllib.parse.urlencode(final_query)

    @staticmethod
    def _get_timestamp() -> int:
        return int(time.time())

    @staticmethod
    def _parse_assembly_info_response(response) -> VideoInfo:
        mc = response["mc"]
        ct1 = response["ct1"]
        ct2 = response["ct2"]
        ct3 = response["ct3"]
        assembly_video_info = VideoInfo(mc, ct1, ct2, ct3)

        for movie in response["movieList"]:
            assembly_video_info.video_item_list.append(
                VideoItem(movie["movieTitle"], movie["playTime"], movie["realTime"], movie["no"], movie["wv"])
            )

        return assembly_video_info

    def fetch_assembly_video_info(self) -> VideoInfo:
        additional_params = {
            "cmd": "movieInfo",
            "no": "",
            "vv": f"{self._get_timestamp()}",
        }
        query_string = self._to_query_string(additional_params, ["menu"])
        fetch_url = f"{self.base_url}{Consts.INFO_FETCH_PATH}?{query_string}&"
        result = requests.get(fetch_url, headers=self.requests_headers)
        result.raise_for_status()
        assembly_video_info = self._parse_assembly_info_response(result.json())

        return assembly_video_info

    # number 는 no 에 해당하는 인자로 index 값으로 추정
    # wv 는 wv 에 해당하는 인자
    def fetch_assembly_streaming_info(self, mc, ct1, ct2, ct3, number, wv) -> StreamingInfo:
        query = {
            "cmd": "fileInfo",
            "mc": mc,
            "ct1": ct1,
            "ct2": ct2,
            "ct3": ct3,
            "no": number,
            "wv": wv,
            "xreferer": "",
            "vv": f"{self._get_timestamp()}",
        }
        query_string = urllib.parse.urlencode(query)
        fetch_url = f"{self.base_url}{Consts.INFO_FETCH_PATH}?{query_string}&"
        result = requests.get(fetch_url, headers=self.requests_headers)
        result.raise_for_status()
        stream_list = result.json()["filePath"]
        default_stream_key = stream_list.get("default") or ""
        stream_list.pop("default")

        return StreamingInfo(default_stream_key, stream_list)
