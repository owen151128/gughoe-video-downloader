# -*- coding: utf-8 -*-

class VideoInfo:
    # 각 데이터는 국회 비디오 정보 요청 api 에서 받아온 값입니다.
    # 무슨 값인지 모르는 값은 파라미터 명으로 셋팅합니다.
    def __init__(self, mc, ct1, ct2, ct3):
        self.mc = mc
        self.ct1 = ct1
        self.ct2 = ct2
        self.ct3 = ct3
        self.video_item_list = []
