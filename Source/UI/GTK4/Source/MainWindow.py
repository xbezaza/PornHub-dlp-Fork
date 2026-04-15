import gi

# Запрос требуемых версий библиотек.
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

# Главное окно.
class MainWindow(Gtk.ApplicationWindow):

	#==========================================================================================#
	# >>>>> МЕТОДЫ ВЗАИМОДЕЙСТВИЯ ИНТЕРФЕЙСА <<<<< #
	#==========================================================================================#

	# Изменяет статус загрузки.
	def __ChangeDownloadingStatus(self):

		# Если нажата кнопка начала загрузки.
		if "🌎" in self.__Button_Downloading.get_label():
			# Изменение статуса.
			self.__IsDownloading = True
			# Изменение текста кнопки.
			self.__Button_Downloading.set_label("🟥  Stop")
		else:
			# Изменение статуса.
			self.__IsDownloading = False
			# Изменение текста кнопки.
			self.__Button_Downloading.set_label("🌎  Start")

	#==========================================================================================#
	# >>>>> МЕТОДЫ ГЕНЕРАЦИИ ИНТЕРФЕЙСА <<<<< #
	#==========================================================================================#

	# Строит интерфейс.
	def __BuildInterface(self):

		# Настройка главного контейнера.
		self.__MainBox.set_spacing(20)
		self.set_child(self.__MainBox)
		
		# HeaderBar.
		self.Header = Adw.HeaderBar()
		self.set_titlebar(self.Header)
		self.set_default_size(720, 480)
		HeaderLabel = Gtk.Label()
		HeaderLabel.set_markup("<b>PornHub Downloader</b>")
		self.Header.set_title_widget(HeaderLabel)

		# Построение верхней панели.
		self.__BuildUpPanel()

	# Строит верхнюю панель.
	def __BuildUpPanel(self):

		# Box: верхняя панель.
		UpPanelBox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
		UpPanelBox.set_spacing(7)
		UpPanelBox.set_homogeneous(True)

		# Button: открытие файла.
		Button_Open = Gtk.Button(label = "🗃️  Open")
		Button_Open.set_margin_start(7)
		Button_Open.set_margin_top(7)
		
		# Button: управление загрузкой.
		self.__Button_Downloading = Gtk.Button(label = "🌎  Start")
		self.__Button_Downloading.set_margin_end(7)
		self.__Button_Downloading.set_margin_top(7)
		self.__Button_Downloading.connect("clicked", lambda _: self.__ChangeDownloadingStatus())

		# Помещение элементов в контейнеры.
		UpPanelBox.append(Button_Open)
		UpPanelBox.append(self.__Button_Downloading)
		self.__MainBox.append(UpPanelBox)

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	# Конструктор.
	def __init__(self, *args, **kwargs):
		# Наследование конструктора базового класса.
		super().__init__(*args, **kwargs)
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Состояние: выполняется ли загрузка.
		self.__IsDownloading = False
		# Главный контейнер.
		self.__MainBox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)

		# Инициализация интерфейса.
		self.__BuildInterface()

		# # Контейнер: содержимое.
		# ContentBox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
		# ContentBox.set_spacing(10)
		# # Заголовок ввода.
		# Label_Input = Gtk.Label()
		# Label_Input.set_markup("<b>Input</b>")
		# ContentBox.append(Label_Input)
		# # Поле ввода.
		# TextView_Input = Gtk.TextView()
		# TextView_Input.get_buffer().set_text("\n")
		# TextView_Input.set_size_request(1080, 300)
		# #ContentBox.append(TextView_Input)
		# # Скролл-окно.
		# ScrolledWindow_Input = Gtk.ScrolledWindow()
		# ScrolledWindow_Input.set_child(TextView_Input)
		# ContentBox.append(ScrolledWindow_Input)
		# # Заголовок ввода.
		# Label_Input = Gtk.Label()
		# Label_Input.set_markup("<b>Output</b>")
		# ContentBox.append(Label_Input)
		# # Поле вывода.
		# TextView_Output = Gtk.TextView()
		# TextView_Output.get_buffer().set_text("\n")
		# TextView_Output.set_editable(False)
		# ContentBox.append(TextView_Output)
		
		# self.__MainBox.append(ContentBox)
