# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QVBoxLayout, QFrame

from assembly_info_fetcher import AssemblyInfoFetcher
from py_qt_wrapper import PyQtWrapper


class GughoeVideoDownloaderApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.input_url_line_edit = None
        self.default_font = None
        self.fetch_button = None
        self.top_horizonal_layout = None
        self.main_vertical_layout = None
        self.parsed_result_frame = None
        self.parsed_result_vertical_layout = None

        self.current_video_info = None

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

    def _load_parsed_result(self):
        for video_item in self.current_video_info.video_item_list:
            title_h_layout = PyQtWrapper.h_layout_with_widgets([PyQtWrapper.label(video_item.title, self.default_font)])
            title_h_layout.addStretch(1)
            v_layout = PyQtWrapper.v_layout_with_layouts([title_h_layout])

            download_button = PyQtWrapper.button(
                "다운로드",
                self.default_font,
                click_handler=self._on_download_button_clicked
            )
            button_h_layout = QHBoxLayout()
            button_h_layout.addStretch(1)
            button_h_layout.addWidget(download_button)
            v_layout.addLayout(button_h_layout)

            v_layout.addWidget(PyQtWrapper.label(
                f"{video_item.play_time} ({video_item.real_time})",
                self.default_font
            ))

            self.parsed_result_vertical_layout.addWidget(PyQtWrapper.frame(v_layout))

    def _enable_fetch_button(self):
        self.fetch_button.setText("파싱")
        self.setEnabled(True)

    def _on_fetch_button_clicked(self):
        self._disable_fetch_button()
        assembly_info_fetcher = AssemblyInfoFetcher(self.input_url_line_edit.text().strip())
        self.current_video_info = assembly_info_fetcher.fetch_assembly_video_info()
        self._load_parsed_result()
        self._enable_fetch_button()

    def _on_download_button_clicked(self):
        pass
