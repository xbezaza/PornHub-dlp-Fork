from dublib.Engine.Bus import ExecutionError, ExecutionStatus
from dublib.Methods.Filesystem import NormalizePath
import urllib.request
import subprocess
import zipfile
import json
import sys
import os
import re

class VideoDownloader:

    def __CheckLibs(self):
        if not os.path.exists(f"yt-dlp/{self.__LibName}"):
            if not os.path.exists("yt-dlp"): 
                os.makedirs("yt-dlp")
            print("Downloading yt-dlp...  ", end=" ", flush=True)
            urllib.request.urlretrieve(
                "https://github.com/yt-dlp/yt-dlp/releases/latest/download/" + self.__LibName, 
                "yt-dlp/" + self.__LibName
            )
            print("Done.")

            if sys.platform == "linux":
                print("Making yt-dlp executable...  ", end=" ")
                os.system("chmod u+x yt-dlp/yt-dlp")
                print("Done.")

        if sys.platform == "win32" and not os.path.exists("yt-dlp/ffmpeg.exe"):
            print("Downloading ffmpeg 7.1 Essentials (Windows build)...  ", end=" ", flush=True)
            urllib.request.urlretrieve(
                "https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-essentials_build.zip", 
                "yt-dlp/ffmpeg-essentials.zip"
            )
            print("Done.")

            with zipfile.ZipFile("yt-dlp/ffmpeg-essentials.zip", "r") as ZipReader:
                print("Extracting files... ", flush=True)
                with open("yt-dlp/ffmpeg.exe", "wb") as FileWriter: 
                    FileWriter.write(ZipReader.read("ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"))
                print("ffmpeg.exe")
                with open("yt-dlp/ffprobe.exe", "wb") as FileWriter: 
                    FileWriter.write(ZipReader.read("ffmpeg-7.1-essentials_build/bin/ffprobe.exe"))
                print("ffprobe.exe")
                print("Done.")

                try:
                    os.remove("yt-dlp/ffmpeg-essentials.zip")
                    print("Temporary files removed.")
                except: 
                    pass

    def __init__(self, settings: dict = None):
        self.__IsSortingEnabled = None
        self.__DownloadsDirectory = "Downloads"
        self.__LibName = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"
        self.__CookiesPath = None
        self.__UserAgent = None
        self.__Settings = settings or {}
        
        if self.__Settings:
            if "cookies_path" in self.__Settings:
                self.__CookiesPath = self.__Settings["cookies_path"]
            if "user_agent" in self.__Settings:
                self.__UserAgent = self.__Settings["user_agent"]

        self.__CheckLibs()

    def check_link(self, link: str) -> bool:
        return bool(re.match(r"https:\/\/.{0,4}?pornhub\.com\/view_video\.php\?viewkey=\S+\b", link))

    def download_video(self, link: str, quality: int | str) -> ExecutionStatus:
        Status = ExecutionStatus(0)
        quality = self.get_video_height(quality)
        VideoInfoStatus = self.get_video_info(link)

        if VideoInfoStatus.code != 0: 
            return VideoInfoStatus
        
        if self.__DownloadsDirectory == "Downloads" and not os.path.exists(self.__DownloadsDirectory): 
            os.makedirs(self.__DownloadsDirectory)

        FfmpegPath = ""
        CookiesArg = ""
        UserAgentArg = ""
        SleepArgs = ""

        if sys.platform == "win32": 
            FfmpegPath = "--ffmpeg-location \"" + os.path.abspath("yt-dlp/ffmpeg.exe") + "\""

        if self.__CookiesPath and os.path.exists(self.__CookiesPath):
            CookiesArg = "--cookies \"" + os.path.abspath(self.__CookiesPath) + "\""
        else:
            print("WARNING: No cookies file found. Downloads may fail.")

        if self.__UserAgent:
            UserAgentArg = "--user-agent \"" + self.__UserAgent + "\""

        SleepArgs = "--sleep-interval 5 --max-sleep-interval 10 --retry-sleep 5"

        try:
            Data = VideoInfoStatus.value
            Filename = Data.get("title", "video")
            Uploader = ""
            
            if self.__IsSortingEnabled: 
                Uploader = "/" + Data.get("uploader", "Unknown")
            
            Path = os.path.abspath("yt-dlp/" + self.__LibName)
            
            cmd = [
                Path,
                "-f", f"bv*[height<={quality}]+ba/b[height<={quality}]",
                "-o", f"{self.__DownloadsDirectory}{Uploader}/{Filename}.%(ext)s",
                "--no-playlist",
                "--sleep-interval", "5",
                "--max-sleep-interval", "10",
                "--retry-sleep", "5"
            ]

            if CookiesArg:
                cmd.extend(["--cookies", os.path.abspath(self.__CookiesPath)])
            if UserAgentArg:
                cmd.extend(["--user-agent", self.__UserAgent])
            if FfmpegPath:
                cmd.extend(["--ffmpeg-location", os.path.abspath("yt-dlp/ffmpeg.exe")])
            cmd.extend([
                "--referer", link,
                "--add-header", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "--add-header", "Accept-Language: en-us,en;q=0.5",
                "--add-header", "Sec-Fetch-Mode: navigate",
                link
            ])

            print("Executing:", " ".join(cmd))
            result = subprocess.run(cmd, check=True, capture_output=False, text=True)
            
        except subprocess.CalledProcessError as e:
            Status = ExecutionError(e.returncode, f"Unable to download video. Exit code: {e.returncode}. Check cookies, user-agent, and connection.")
        except Exception as ExceptionData:
            Status = ExecutionError(-1, str(ExceptionData))

        return Status

    def enable_sorting(self, status: bool):
        self.__IsSortingEnabled = status

    def get_video_height(self, quality: int | str) -> int | None:
        quality = str(quality)

        QualityTypes = {
            "4k": 4096,
            "2k": 2048,
            "fullhd": 1080,
            "hd": 720,
            "480p": 480,
            "360p": 360,
            "240p": 240
        }
        Quality = None
        
        if quality.isdigit() and len(quality) == 1:
            Index = int(quality)
            Quality = tuple(QualityTypes.values())[Index]
        elif quality.isdigit():
            Quality = int(quality)
        elif quality.lower() in QualityTypes.keys():
            Quality = QualityTypes[quality.lower()]

        return Quality

    def get_video_info(self, link: str) -> ExecutionStatus:
        Status = ExecutionStatus(0)

        try:
            Path = os.path.abspath("yt-dlp/" + self.__LibName)
            
            cmd = [Path, "--dump-json", "--no-playlist"]
            
            if self.__CookiesPath and os.path.exists(self.__CookiesPath):
                cmd.extend(["--cookies", os.path.abspath(self.__CookiesPath)])
            
            if self.__UserAgent:
                cmd.extend(["--user-agent", self.__UserAgent])
            
            cmd.append(link)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            Status.value = json.loads(result.stdout)

        except subprocess.CalledProcessError as e:
            Status = ExecutionError(e.returncode, f"Failed to get video info: {e.stderr}")
        except Exception as ExceptionData:
            Status = ExecutionError(-1, str(ExceptionData))

        return Status

    def set_downloads_directory(self, path: str):
        if not os.path.exists(path): 
            raise FileNotFoundError(path)
        self.__DownloadsDirectory = NormalizePath(path)

    def set_cookies_path(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError("Cookies file not found: " + path)
        self.__CookiesPath = path

    def set_user_agent(self, ua: str):
        self.__UserAgent = ua