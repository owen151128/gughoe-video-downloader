# -*- coding: utf-8 -*-
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QWidget


class PyQtWrapper:
    @staticmethod
    def font(size) -> QFont:
        font = QLineEdit().font()
        font.setPointSize(size)
        return font

    @staticmethod
    def line_edit(parent, placeholder_text, font=None) -> QLineEdit:
        line_edit = QLineEdit(parent)
        line_edit.setPlaceholderText(placeholder_text)
        if font is not None:
            line_edit.setFont(font)

        return line_edit

    @staticmethod
    def button(text, font=None, fixed_height=None, click_handler=None) -> QPushButton:
        button = QPushButton(text)
        if font is not None:
            button.setFont(font)
        if fixed_height is not None:
            button.setFixedHeight(fixed_height)
        if click_handler is not None:
            button.clicked.connect(click_handler)

        return button

    @staticmethod
    def label(text, font=None) -> QLabel:
        label = QLabel(text)
        if font is not None:
            label.setFont(font)

        return label

    @staticmethod
    def h_layout_with_widgets(widgets) -> QHBoxLayout:
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)

        return layout

    @staticmethod
    def h_layout_with_layouts(layouts) -> QHBoxLayout:
        layout = QHBoxLayout()
        for element in layouts:
            layout.addLayout(element)

        return layout

    @staticmethod
    def v_layout_with_widgets(widgets) -> QVBoxLayout:
        layout = QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)

        return layout

    @staticmethod
    def v_layout_with_layouts(layouts) -> QVBoxLayout:
        layout = QVBoxLayout()
        for element in layouts:
            layout.addLayout(element)

        return layout

    @staticmethod
    def frame(layout) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.WinPanel)
        frame.setLayout(layout)

        return frame

    @staticmethod
    def clear_layout(layout):
        while layout.count() > 1:
            item = layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
