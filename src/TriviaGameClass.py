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

	return (opciones: list, opción correcta: int) // (options: list with the options loaded and shuffled, corr: position of the correct answer)
	"""
	
	opciones = [i['correct_answer'] + " - " + orig['correct_answer'], i['incorrect_answers'][0] + " - " + orig['incorrect_answers'][0], i['incorrect_answers'][1] + " - " + orig['incorrect_answers'][1], i['incorrect_answers'][2] + " - " + orig['incorrect_answers'][2]]
	random.shuffle(opciones)

	for j in range(4):
		if i['correct_answer'] in opciones[j]:
			corr=j
			break

	return opciones, corr


class MyMainWindow(QMainWindow):

	#! Declaración de Widgets // Widgets declaration 
	__inputCantPreguntas=None		#? Input amount of questions
	__botonConfirmarCantidad=None	#? Confirm amount and category button
	__botonSiguiente=None			#? button next
	__groupBox=None
	__botonConfirmarRespuesta=None	#? confirm answer button
	__layoutGB=None					#? layout of the group box
	__comboBoxCategoria=None		#? Category comboBox
	__preguntaN=None				#? Label with the Question


	#! Declaración de Variables // Variables declaration
	__dictCategorias={"Todas": 0, "Conocimiento General": 9, 'Entr.: Libros': 10, 'Entr.: Pelis': 11, 'Entr.: Musica': 12, 'Entr.: Musicales': 13, 'Entr.: Tele': 14, 'Entr.: Video Juegos': 15, 'Entr.: Juegos de mesa': 16, 'Ciencia y nat.': 17, 'Ciencia: Computadoras': 18, 'Ciencia: Matemática': 19, 'Mitología': 20, 'Deportes': 21, 'Geografía': 22, 'Historia': 23, 'Política': 24, 'Arte': 25, 'Celebridades': 26, 'Animales': 27, 'Vehículos': 28, 'Ciencia: Gadgets': 30, 'Entr.: Dibujos y animaciones': 32} #? Dict with the categories, sorry they are in Spanish
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
		self.setGeometry(300, 200, 600, 370)

		wid = QWidget(self)
		self.setCentralWidget(wid)
		layout = QGridLayout()
		wid.setLayout(layout)

		self.__inputCantPreguntas=QSpinBox()
		self.__botonConfirmarCantidad=QPushButton('Confirmar')				#? Says "Confirm"
		self.__botonSiguiente=QPushButton('Siguiente')						#? Says "Next"
		self.__botonConfirmarRespuesta=QPushButton('Confirmar Respuesta')	#? Says "Confirm Answer"
		self.__groupBox=QGroupBox()
		self.__bResultado=False
		self.__layoutGB = QVBoxLayout()
		self.__comboBoxCategoria=QComboBox()
		self.__preguntaN=QLabel('Pregunta N°:\nQuestion N°:')

		self.__preguntaN.setStyleSheet("font-weight: bold;")
		self.__preguntaN.setFixedHeight(50)
		self.__preguntaN.adjustSize()

		self.__inputCantPreguntas.enterEvent
		
		self.__layoutGB.setAlignment(Qt.AlignHCenter)

		self.__botonSiguiente.setDisabled(True)
		self.__pos=0

		self.__inputCantPreguntas.setMaximum(50)
		self.__inputCantPreguntas.setMinimum(1)
		self.__comboBoxCategoria.addItems(self.__dictCategorias.keys())

		self.__botonConfirmarCantidad.clicked.connect(self.botonConfirmarCantidad_Clicked)
		self.__botonSiguiente.clicked.connect(self.__botonSiguiente_Clicked)
		self.__botonConfirmarRespuesta.clicked.connect(self.__btnConfirmarRespuesta_Clicked)

		self.__botonConfirmarRespuesta.setDisabled(True)

		layout.addWidget(QLabel("Cantidad de preguntas: "), 0, 0, 1, 1)		#? Says "Number of Questions:"
		layout.addWidget(self.__inputCantPreguntas, 0, 1, 1, -1)
		layout.addWidget(self.__comboBoxCategoria, 1, 0, 1, 2)
		layout.addWidget(self.__botonConfirmarCantidad, 1, 2, 1, -1)
		layout.addWidget(self.__preguntaN, 2, 0, 1, -1)
		layout.addWidget(self.__groupBox, 3, 0, 1, -1)
		layout.addWidget(self.__botonConfirmarRespuesta, 4, 0, -1, 1)
		layout.addWidget(self.__botonSiguiente, 4, 2, -1, -1)


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