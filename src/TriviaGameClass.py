from PyQt5.QtGui import QIcon
import src.TriviaGameAPI as TGAPI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import random
import copy


def CargarOpcionesMultiples(i: dict, orig: dict):
	"""
	Cargar las opciones múltiples // Loads the multiple choices
	
	#### Parametros:
	* @param i Diccionario en idioma traducido // Dictionary on translated language
	* @param orig Diccionario en idioma original // Dictionary on original language

	#### Returns:

	* return (opciones: list, opción correcta: int) // (options: list with the options loaded and shuffled, corr: position of the correct answer)
	"""
	
	opciones = [i['correct_answer'] + " - " + orig['correct_answer'], i['incorrect_answers'][0] + " - " + orig['incorrect_answers'][0], i['incorrect_answers'][1] + " - " + orig['incorrect_answers'][1], i['incorrect_answers'][2] + " - " + orig['incorrect_answers'][2]]
	random.shuffle(opciones)

	for j in range(4):
		if i['correct_answer'] in opciones[j]:
			corr=j
			break

	return opciones, corr


#! Class MyMainWindow
class MyMainWindow(QMainWindow):

	#! Declaración de Widgets // Widgets declaration 
	__labelCantidadPreguntas=None	#? Label amount of questions
	__inputCantPreguntas=None		#? Input amount of questions
	__aboutButton=None				#? About button
	__labelCategoria=None			#? Label categories
	__comboBoxCategoria=None		#? Category comboBox
	__botonConfirmarCantidad=None	#? Confirm amount and category button
	__preguntaN=None				#? Label with the Question
	__groupBox=None
	__layoutGB=None					#? layout of the group box
	__botonConfirmarRespuesta=None	#? confirm answer button
	__botonSiguiente=None			#? button next


	#! Declaración de Variables // Variables declaration
	__dictCategorias={'Todas': 0, 'Conocimiento General': 9, 'Entr.: Libros': 10, 'Entr.: Pelis': 11, 'Entr.: Musica': 12, 'Entr.: Musicales': 13, 'Entr.: Tele': 14, 'Entr.: Video Juegos': 15, 'Entr.: Juegos de mesa': 16, 'Ciencia y nat.': 17, 'Ciencia: Computadoras': 18, 'Ciencia: Matemática': 19, 'Mitología': 20, 'Deportes': 21, 'Geografía': 22, 'Historia': 23, 'Política': 24, 'Arte': 25, 'Celebridades': 26, 'Animales': 27, 'Vehículos': 28, 'Ciencia: Gadgets': 30, 'Entr.: Dibujos y animaciones': 32} #? Dict with the categories, sorry they are in Spanish
	__pos=None					#? Current position of the responseList
	__responseNumber=None		#? Response number of the API call
	__responseList=None			#? A list with the API results
	__bResultado: bool			#? To compare if the final answer is right or wrong
	__lRB=[]					#? List of radio buttons (will have the answer choices)
	__opcCorrecta=None			#? position of the __lRB with the right answer


	#! Inicialización // Initialization of the mainWidget
	def __init__(self, parent = None):
		super().__init__(parent)

		self.setWindowTitle("Trivia Game")
		self.setGeometry(600, 400, 0, 0)

		wid = QWidget(self)
		self.setCentralWidget(wid)
		layout = QGridLayout()
		wid.setLayout(layout)

		#! Init Widgets
		self.__labelCantidadPreguntas=QLabel('Cantidad de preguntas:')		#? Says "Amount of questions"
		self.__inputCantPreguntas=QSpinBox()
		self.__aboutButton=QPushButton(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxInformation')), '')
		self.__labelCategoria=QLabel('Categorias:')							#? Says "Categories"
		self.__comboBoxCategoria=QComboBox()
		self.__botonConfirmarCantidad=QPushButton('Confirmar')				#? Says "Confirm"
		self.__groupBox=QGroupBox()
		self.__preguntaN=QLabel('Pregunta N°:\nQuestion N°:')
		self.__botonConfirmarRespuesta=QPushButton('Confirmar Respuesta')	#? Says "Confirm Answer"
		self.__botonSiguiente=QPushButton('Siguiente')						#? Says "Next"
		self.__layoutGB=QVBoxLayout()

		#! Init vars
		self.__pos=0
		self.__bResultado=False

		#! Setting widgets properties
		self.__inputCantPreguntas.setMaximum(50)
		self.__inputCantPreguntas.setMinimum(1)

		self.__aboutButton.setMaximumSize(25, 25)
		self.__aboutButton.setMinimumSize(25, 25)
		self.__aboutButton.setFlat(True)

		self.__comboBoxCategoria.addItems(self.__dictCategorias.keys())

		self.__preguntaN.setStyleSheet("font-weight: bold;")
		self.__preguntaN.setWordWrap(True)

		self.__groupBox.setMinimumHeight(150)
		self.__groupBox.adjustSize()
		
		self.__layoutGB.setAlignment(Qt.AlignHCenter)

		#! Button Connections
		self.__aboutButton.clicked.connect(self.__aboutButton_Clicked)
		self.__botonConfirmarCantidad.clicked.connect(self.botonConfirmarCantidad_Clicked)
		self.__botonSiguiente.clicked.connect(self.__botonSiguiente_Clicked)
		self.__botonConfirmarRespuesta.clicked.connect(self.__btnConfirmarRespuesta_Clicked)

		self.__botonSiguiente.setDisabled(True)
		self.__botonConfirmarRespuesta.setDisabled(True)

		#! Adding widgets to layout
		layout.addWidget(self.__labelCantidadPreguntas, 0, 0, 1, 1)		#? Says "Number of Questions:"
		layout.addWidget(self.__inputCantPreguntas, 0, 1, 1, 3)
		layout.addWidget(self.__aboutButton, 0, 4, 1, 1)
		layout.addWidget(self.__labelCategoria, 1, 0, 1, 1)
		layout.addWidget(self.__comboBoxCategoria, 1, 1, 1, 2)
		layout.addWidget(self.__botonConfirmarCantidad, 1, 3, 1, 2)
		layout.addWidget(self.__preguntaN, 2, 0, 1, -1)
		layout.addWidget(self.__groupBox, 3, 0, 1, -1)
		layout.addWidget(self.__botonConfirmarRespuesta, 4, 0, 1, 1)
		layout.addWidget(self.__botonSiguiente, 4, 3, 1, 2)

		layout.setRowStretch(2, 0)
		layout.setRowStretch(3, 1)
		layout.setColumnStretch(0, 0)

		self.setFixedWidth(500)


	#! Func: Boton Confirmar Cantidad // Confirm amount button
	def botonConfirmarCantidad_Clicked(self):

		cant=self.__inputCantPreguntas.value()
		
		self.__responseNumber, self.__responseList = TGAPI.apiGet(cant, self.__dictCategorias[self.__comboBoxCategoria.currentText()])
		
		if(self.__responseNumber==0):
			self.__pos=0
			self.__botonSiguiente_Clicked()
		else:
			warning_dialog=QErrorMessage()
			warning_dialog.showMessage('No se obtuvieron preguntas\nError: '+self.__responseNumber)		#* Message that advice of an error
			warning_dialog.exec_()


	#! Func: Boton Siguiente // Next button
	def __botonSiguiente_Clicked(self):

		self.__bResultado=False
		self.__botonSiguiente.setDisabled(True)

		rtrad=copy.deepcopy(self.__responseList[self.__pos])		#* rtrad will contain a copy of the current responseList item translated
		bTranslated=TGAPI.traducir_resultados(rtrad)
		
		if not bTranslated:
			qdTranslated=QErrorMessage()
			qdTranslated.setWindowTitle('Información de la Traducción')
			qdTranslated.showMessage('No se pudo traducir en su totalidad')			#* Message that advice if could translate or not
			qdTranslated.exec_()

		self.__preguntaN.setText('Pregunta N°{0}: {1}\nQuestion N°{0}: {2}'.format(self.__pos+1, rtrad['question'], self.__responseList[self.__pos]['question']))

		if(rtrad['type']=='múltiple' or rtrad['type']=='multiple'):
			self.__crearGroupBoxM(rtrad)
		else:
			self.__crearGroupBoxB(rtrad)

		self.__pos+=1

		self.__groupBox.setLayout(self.__layoutGB)
		self.__botonConfirmarRespuesta.setDisabled(False)			#* Habilito el boton Confirmar respuesta // Enable Confirm answer button


	#! Func: Boton Confirmar Respuesta // Confirm answer button
	def __btnConfirmarRespuesta_Clicked(self):

		posi=0														#? Posición de la respuesta seleccionada // Position of the selected answer

		#* Gets the position of the selected answer and check if it right
		for i in range(len(self.__lRB)):
			if self.__lRB[i].isChecked()==True:
				if i==self.__opcCorrecta:
					self.__bResultado=True
				posi=i
				break

		#* Show if the selected answer is right or wrong
		if self.__bResultado==True:
			self.__lRB[posi].setText(self.__lRB[posi].text()+' (✓)')
			self.__lRB[posi].setStyleSheet("QRadioButton{color: green; font-weight: bold;}")
		else:
			self.__lRB[posi].setText(self.__lRB[posi].text()+' (X)')
			self.__lRB[posi].setStyleSheet("QRadioButton{color: red; font-weight: bold;}")
			self.__lRB[self.__opcCorrecta].setText(self.__lRB[self.__opcCorrecta].text()+' (✓)')
			self.__lRB[self.__opcCorrecta].setStyleSheet("QRadioButton{color: green; font-weight: bold;}")

		self.__botonConfirmarRespuesta.setDisabled(True) 
		
		#* Si no hay mas preguntas se deshabilita el boton siguiente // if no more questions the "Next" button will be disabled
		if self.__pos<len(self.__responseList):
			self.__botonSiguiente.setDisabled(False)


	#! Func: Mostrar información // Show information
	def __aboutButton_Clicked(self):
		qdAboutWindow=MyAboutWindow(self)
		qdAboutWindow.show()


	#! Func: Limpiar el layout de Group Box // Clean the layout of Group Box
	def __limpiarGB(self):
		self.__lRB.clear()
		for i in reversed(range(self.__layoutGB.count())): 
			self.__layoutGB.itemAt(i).widget().setParent(None)


	#! Func: Crear Group Box Múltiple // Create the group box of the type multiple
	def __crearGroupBoxM(self, rtrad):
		self.__limpiarGB()

		opciones, self.__opcCorrecta = CargarOpcionesMultiples(rtrad, self.__responseList[self.__pos])

		for i in range(4):
			self.__lRB.append(QRadioButton(str(opciones[i])))
			self.__layoutGB.addWidget(self.__lRB[i])


	#! Func: Crear Group Box Boolean // Create the group box of the type boolean
	def __crearGroupBoxB(self, rtrad):
		self.__limpiarGB()

		self.__lRB.append(QRadioButton('Verdadero'))
		self.__lRB.append(QRadioButton('Falso'))

		self.__layoutGB.addWidget(self.__lRB[0])
		self.__layoutGB.addWidget(self.__lRB[1])

		if rtrad['correct_answer'] in ['Verdadero', 'Cierto', 'Verdadera', 'True']:
			self.__opcCorrecta=0
		else:
			self.__opcCorrecta=1


#! Class AboutWindow
class MyAboutWindow(QMainWindow):
	def __init__(self, parent=None) -> None:
		super().__init__(parent=parent)

		version=1.0
		gitLabURL="<a href=\"https://gitlab.com/FCampo\">@FCampo</a>"

		self.setWindowTitle('About Trivia Game')

		wid = QWidget(self)
		self.setCentralWidget(wid)
		layout=QGridLayout()
		wid.setLayout(layout)

		labelVersion=QLabel("version: v" + str(version))
		labelName=QLabel("By Francisco L. Campo")
		labelGitLab=QLabel("GitLab: " + gitLabURL)
		exitButton=QPushButton('Cerrar')

		labelGitLab.setOpenExternalLinks(True)

		labelName.setDisabled(True)

		exitButton.clicked.connect(self.__exitButton_Clicked)

		layout.addWidget(labelVersion, 0, 0, 1, -1)
		layout.addWidget(labelGitLab, 1, 0, 1, -1)
		layout.addWidget(labelName, 2, 0, 1, 1)
		layout.addWidget(exitButton, 2, 5, 1, -1)

		layout.setRowStretch(0, 0)
		layout.setRowStretch(1, 0)
		layout.setRowStretch(2, 0)

		self.adjustSize()
		self.setFixedSize(self.size())

	def __exitButton_Clicked(self):
		self.hide()