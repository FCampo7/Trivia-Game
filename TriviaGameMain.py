"""
? Algunos comentarios generales // Some general comments:

* English:
* This is my firs project with class and API calls in Python.
* The purpose of this was merely learn and practice Python, and the use of libraries such as PyQt5 and API calls.
* Trivia Game is in Spanish and English because some translations are inconsistent or unfamiliar in Spanish, such as names of songs, movies, series or games. Keep in mind that it is translated by a runtime library. Could and mostly will be slower due this issue.

! Apologies for the Spanglish mix in general.

* Español:
* Este es mi primer proyecto con clases y llamadas API en python.
* El propósito de esto era simplemente aprender y practicar Python, y el uso de librerias como PyQt5 y llamados a API.
* TriviaGame esta en Español e Ingles porque algunas traducciones son incoherentes o poco familiares en Español, como los nombres de canciones, películas, series o juegos. Tenga en mente que es traducido por una libreria en tiempo de ejecución. Podría ser y en su mayoría será más lento debido a este problema.

! Disculpas por la mezcla de Spanglish en general.
"""

from src.TriviaGameClass import *

def main():
	app=QApplication([])
	main=MyMainWindow()

	main.show()
	app.exec_()
	return

if __name__=="__main__":
	main()
# end if