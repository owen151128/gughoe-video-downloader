# -*- coding: utf-8 -*-

class VideoItem:
    # 각 데이터는 국회 비디오 정보 요청 api 에서 받아온 값입니다.
    # 무슨 값인지 모르는 값은 파라미터 명으로 셋팅합니다.
    def __init__(self, title, play_time, real_time, number, wv):
        self.title = title
        self.play_time = play_time
        self.real_time = real_time
        self.number = number
        self.wv = wv
