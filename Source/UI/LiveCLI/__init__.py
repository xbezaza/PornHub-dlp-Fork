from Source.Core.Downloader import VideoDownloader
from dublib.CLI.Terminalyzer import Command, ParametersTypes, ParsedCommandData, Terminalyzer
from dublib.CLI.TextStyler import Colors, Decorations, TextStyler
from dublib.Methods.Filesystem import ReadTextFile
from dublib.Methods.System import Clear
import shlex
import os
try: import readline
except ImportError: pass

class LiveCLI:
    @property
    def commands(self) -> list[Command]:
        CommandsList = list()
        Com = Command("clear", "Cleare console.")
        CommandsList.append(Com)
        Com = Command("exit", "Exit live mode.")
        CommandsList.append(Com)
        return CommandsList

    def __ProcessCommand(self, command: ParsedCommandData):
        if command.name == "exit": exit(0)
        elif command.name == "clear": Clear()

    def __ProcessMacros(self, macros: str) -> bool:
        IsProcessed = False
        if self.__Downloader.check_link(macros):
            IsProcessed = True
            self.__Downloader.download_video(macros, self.__Settings["quality"])
        elif os.path.exists(macros):
            IsProcessed = True
            Links = ReadTextFile(macros, "\n")
            Links = filter(lambda Element: bool(Element), Links)
            for Link in Links: self.__Downloader.download_video(Link, self.__Settings["quality"])
        return IsProcessed

    def __init__(self, settings: dict):
        self.__Settings = settings.copy()
        self.__Analyzer = Terminalyzer()
        self.__Downloader = VideoDownloader(settings)
        self.__Analyzer.enable_help()
        
    def run(self):
        Clear()
        ExitBold = TextStyler("exit").decorate.bold
        print(TextStyler("PornHub-dlp v2.0.3 [Fork by NurbiSQD]").decorate.bold)
        print(f"Вы находитесь в Live-режиме консольного интерфейса. Для выхода выполните {ExitBold} или нажмите Ctrl + C.")
        print("Введите ссылку на видеоролик или путь к текстовому файлу, из которого нужно извлечь список ссылок.")
        
        contacts = self.__Settings.get("contacts", {})
        print(f"Fork Author: NurbiSQD")
        if contacts.get("discord"): print(f"Discord: {contacts['discord']}")
        if contacts.get("telegram"): print(f"Telegram: {contacts['telegram']}")
        if contacts.get("email"): print(f"Email: {contacts['email']}")
        print()

        while True:
            Input = None
            try:
                Input = input("PornHub-dlp  >  ").strip()
            except KeyboardInterrupt:
                print("exit")
                exit(0)

            if Input:
                if self.__ProcessMacros(Input): continue
                self.__Analyzer.set_source(shlex.split(Input))
                ParsedCommand = self.__Analyzer.check_commands(self.commands)
                if ParsedCommand: self.__ProcessCommand(ParsedCommand)
                elif not Input.startswith("help"): print(TextStyler("[ERROR] Неизвестная команда.").colorize.red)