from Source.UI.Qt.QtWindow import QtWindow
from Source.UI.LiveCLI import LiveCLI

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtGui

import enum
import sys

#==========================================================================================#
# >>>>> ДОПОЛНИТЕЛЬНЫЕ ТИПЫ ДАННЫХ <<<<< #
#==========================================================================================#

class Interfaces(enum.Enum):
	"""Типы интерфейсов."""

	GTK = "gtk"
	Qt = "qt"
	LiveCLI = "live"

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Application:
	"""Менеджер запуска приложения."""

	#==========================================================================================#
	# >>>>> ИНИЦИАЛИЗАТОРЫ ОКНА <<<<< #
	#==========================================================================================#	

	def __InitializeLiveCLI(self):
		"""Инициализирует Live CLI режим приложения."""

		LiveCLI(self.__Settings).run()

	def __InitializeQt(self):
		"""Инициализирует приложение Qt."""

		Application = QApplication(sys.argv)
		Application.setWindowIcon(QtGui.QIcon("icon.ico"))
		Window = QtWindow(self.__Settings)
		Window.show()
		Application.exec()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, settings: dict):
		"""
		Менеджер запуска приложения.
			settings — словарь глобальных настроек.
		"""
		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Settings = settings.copy()
		
	def run(self, toolkit: Interfaces | None = None):
		"""
		Запускает приложение.
			toolkit — выбранный интерфейс.
		"""

		toolkit = toolkit or Interfaces.LiveCLI
		
		{
			Interfaces.LiveCLI: self.__InitializeLiveCLI,
			Interfaces.Qt: self.__InitializeQt
		}[toolkit]()