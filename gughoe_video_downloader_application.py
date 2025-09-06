# -*- coding: utf-8 -*-

import uuid

from functools import partial
from tempfile import TemporaryDirectory
from pathlib import Path

from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QProgressDialog, QMessageBox

from assembly_info_fetcher import AssemblyInfoFetcher
from assembly_video_downloader import AssemblyVideoDownloader
from background_worker import BackgroundWorker
from ffmpeg_wrapper import FfmpegWrapper
from py_qt_wrapper import PyQtWrapper


class GughoeVideoDownloaderApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.input_url_line_edit = None
        self.default_font = None
        self.fetch_button = None
        self.progress_dialog = None
        self.progress_dialog_signal = None
        self.top_horizonal_layout = None
        self.main_vertical_layout = None
        self.parsed_result_frame = None
        self.parsed_result_vertical_layout = None

        self.assembly_info_fetcher = None
        self.current_video_info = None
        self.current_streaming_info_list = []
        self.background_workers = []

        self._initialize_input_url_edit()
        self._initialize_fetch_button()
        self._initialize_layouts()

        self.setWindowTitle("Gughoe Video Downloader")
        self.resize(800, 768)
        self._move_center()

        self.show()

    def _initialize_input_url_edit(self):
        self.input_url_line_edit = PyQtWrapper.line_edit(self, "이곳에 다운로드할 국회 url 을 입력하세요")
        self.default_font = PyQtWrapper.font(20)
        self.input_url_line_edit.setFont(self.default_font)
        font_metrics = QFontMetrics(self.default_font)
        text_height = font_metrics.height()
        self.input_url_line_edit.setFixedHeight(text_height + 12)

    def _initialize_fetch_button(self):
        self.fetch_button = PyQtWrapper.button(
            "파싱",
            self.default_font,
            self.input_url_line_edit.sizeHint().height() + 24,
            self._on_fetch_button_clicked
        )

    def _initialize_layouts(self):
        self.top_horizonal_layout = PyQtWrapper.h_layout_with_widgets([self.input_url_line_edit, self.fetch_button])
        self.main_vertical_layout = PyQtWrapper.v_layout_with_layouts([self.top_horizonal_layout])

        self.parsed_result_vertical_layout = QVBoxLayout()
        self.parsed_result_frame = PyQtWrapper.frame(self.parsed_result_vertical_layout)
        self.main_vertical_layout.addWidget(self.parsed_result_frame)

        self.setLayout(self.main_vertical_layout)

    def _move_center(self):
        frame_geometry = self.frameGeometry()
        center_position = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_position)
        self.move(frame_geometry.topLeft())

    def _disable_fetch_button(self):
        self.setEnabled(False)
        self.fetch_button.setText("가져오는중...")
        PyQtWrapper.clear_layout(self.parsed_result_vertical_layout)

    def _enable_fetch_button(self):
        self.fetch_button.setText("파싱")
        self.setEnabled(True)

    def _fetch_assembly_video_info(self):
        self.assembly_info_fetcher = AssemblyInfoFetcher(self.input_url_line_edit.text().strip())
        self.current_video_info = self.assembly_info_fetcher.fetch_assembly_video_info()

    def _on_fetch_assembly_video_info_done(self, data):
        self._load_parsed_result()
        self._enable_fetch_button()
        self.background_workers.clear()

    def _on_fetch_button_clicked(self):
        self._disable_fetch_button()
        background_worker = BackgroundWorker(self._fetch_assembly_video_info)
        background_worker.result_ready.connect(self._on_fetch_assembly_video_info_done)
        background_worker.start()
        self.background_workers.append(background_worker)

    def _load_parsed_result(self):
        self.current_streaming_info_list.clear()
        for index, video_item in enumerate(self.current_video_info.video_item_list):
            current_streaming_info = self.assembly_info_fetcher.fetch_assembly_streaming_info(
                self.current_video_info.mc,
                self.current_video_info.ct1,
                self.current_video_info.ct2,
                self.current_video_info.ct3,
                video_item.number,
                video_item.wv,
            )
            self.current_streaming_info_list.append(current_streaming_info)
            title_h_layout = PyQtWrapper.h_layout_with_widgets([PyQtWrapper.label(video_item.title, self.default_font)])
            title_h_layout.addStretch(1)
            streaming_resolution_input = PyQtWrapper.combo_box(
                current_streaming_info.stream_list.keys(),
                current_streaming_info.default_stream_key,
                self.default_font,
            )
            title_h_layout.addWidget(streaming_resolution_input)
            v_layout = PyQtWrapper.v_layout_with_layouts([title_h_layout])

            streaming_resolution_input.setProperty("streaming_index", index)
            download_button = PyQtWrapper.button(
                "다운로드",
                self.default_font,
                click_handler=partial(lambda checked, combo=streaming_resolution_input:
                                      self._on_download_button_clicked(combo))
            )

            time_h_layout = PyQtWrapper.h_layout_with_widgets([
                PyQtWrapper.label(
                    f"{video_item.play_time} ({video_item.real_time})",
                    self.default_font
                )
            ])
            time_h_layout.addStretch(1)
            time_h_layout.addWidget(download_button)
            v_layout.addLayout(time_h_layout)

            self.parsed_result_vertical_layout.addWidget(PyQtWrapper.frame(v_layout))

    def _show_progress_dialog(self, title, message):
        self.progress_dialog = QProgressDialog(message, None, 0, 100, self)
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()

    def _close_progress_dialog(self):
        self.progress_dialog.close()

    def _on_progress_dialog_update(self, value):
        self.progress_dialog.setValue(value)

    def _download_assembly_video(self, m3u8_url):
        with TemporaryDirectory() as temp_dir:
            ts_list_path = AssemblyVideoDownloader.download_assembly_video_ts(
                m3u8_url,
                self.progress_dialog_signal,
                Path(temp_dir)
            )
            FfmpegWrapper().convert_ts_to_mp4(
                Path(ts_list_path).resolve(),
                Path(".").resolve() / f"{uuid.uuid4().hex}.mp4"
            )

    def _convert_ts_to_mp4(self):
        self._close_progress_dialog()
        QMessageBox.information(self, "정보", "다운로드 완료!")

    # streaming_info dict 에 m3u8 value 를 가져오기 위한 key 값
    def _on_download_button_clicked(self, combo_box):
        self._show_progress_dialog("현황", "다운로드중...")
        background_worker = BackgroundWorker(
            self._download_assembly_video,
            self.current_streaming_info_list[
                combo_box.property("streaming_index")].stream_list[combo_box.currentText()
            ]
        )
        self.progress_dialog_signal = background_worker.progress_signal
        background_worker.progress_signal.connect(self._on_progress_dialog_update)
        background_worker.result_ready.connect(self._convert_ts_to_mp4)
        self.background_workers.append(background_worker)
        background_worker.start()
