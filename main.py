# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from gughoe_video_downloader_application import GughoeVideoDownloaderApplication


def main():
    application = QApplication(sys.argv)
    gughoe_video_downloader = GughoeVideoDownloaderApplication()
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
