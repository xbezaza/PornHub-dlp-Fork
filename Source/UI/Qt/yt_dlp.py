from Source.Core.Downloader import VideoDownloader
from PyQt6.QtCore import QObject, pyqtSignal

class yt_dlp(QObject):
    finished = pyqtSignal(int)

    def __init__(self, directory: str, link: str, sorting: bool, quality: str, settings: dict = None):
        super().__init__()
        self.__SaveDirectory = directory
        self.__Link = link
        self.__SortByUploader = sorting
        self.__Quality = quality
        self.__Downloader = VideoDownloader(settings)
        self.__Downloader.enable_sorting(self.__SortByUploader)

    def run(self):
        Status = self.__Downloader.download_video(self.__Link, self.__Quality)
        self.finished.emit(Status.code)