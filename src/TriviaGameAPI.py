import requests as req
import html
import translators as trad


lang = 'es-ar' #! This variable has the language to translate, change it to the language you want.


def apiGet(cantidad: int = 1, categoria: int = 0):
	"""
	Obtener datos de la API // Get data from the API

	#### Parametros:
	* @param cantidad: Cantidad de preguntas a traer por la api // Number of questions that the API brings
	* @param categoria: N° de la categoria a elegir 0: todas, [9; 32]: Categorias disponibles // N° of the category chosen 0: any, [9; 32]: available categories

	#### Returns:
	return (respuesta, resultado)

	En caso exitoso respuesta = 0 y resultado contiene el json con el resultado. // if success: respuesta = 0 and resultado contains the results
	Si falla respuesta = (1, 2, 3 o 4) y resultado = None // if fail: respuesta = failed response number and resultados = None
	"""

	if cantidad>50: cantidad=50

	apiURL = "https://opentdb.com/api.php?amount={0}&category={1}".format(cantidad, categoria)

	r = req.get(apiURL).json()

	#? Decodifico la pregunta y respuestas // Decode de question and answers
	for i in r['results']:
		i['question']=html.unescape(i['question'])
		if i['type']=='multiple':
			i['correct_answer']=html.unescape(i['correct_answer'])
			i['incorrect_answers'][0]=html.unescape(i['incorrect_answers'][0])
			i['incorrect_answers'][1]=html.unescape(i['incorrect_answers'][1])
			i['incorrect_answers'][2]=html.unescape(i['incorrect_answers'][2])

	response = r['response_code']

	if response == 0:
		resultado = r['results']
	else:
		resultado = None

	return response, resultado


def traducir_resultados(i: dict) -> None:
	"""
	Traducir resultados // Translate results
	
	#### Parametros:
	* @param i: Diccionario con el resultado // Dictionary with the results
	"""
	
	try:
		for k in i.keys():
			if k != 'incorrect_answers':
				i[k] = trad.google(str(i[k]), from_language='en', to_language=lang)
			else:
				if i['type']!='booleano':
					i[k][0]=trad.google(str(i[k][0]), from_language='en', to_language=lang)
					i[k][1]=trad.google(str(i[k][1]), from_language='en', to_language=lang)
					i[k][2]=trad.google(str(i[k][2]), from_language='en', to_language=lang)
	except:
		print('No se pudo traducir') #? Says "Couldn't translate"