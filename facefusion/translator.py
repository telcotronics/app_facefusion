import importlib
from typing import Optional

from facefusion.types import Language, LocalePoolSet, Locales

LOCALE_POOL_SET : LocalePoolSet = {}
# Modificación para soportar traducción a español por defecto e interceptar las traducciones en el lookup.
CURRENT_LANGUAGE : Language = 'es'

# Diccionario de traducción dinámica de etiquetas de inglés a español
SPANISH_TRANSLATIONS = {
	# Botones y etiquetas principales
	'APPLY': 'APLICAR',
	'CLEAR': 'LIMPIAR',
	'REFRESH': 'ACTUALIZAR',
	'START': 'INICIAR PROCESO',
	'STOP': 'DETENER',
	'SOURCE': 'ROSTRO DE ORIGEN (FOTO)',
	'TARGET': 'IMAGEN O VIDEO DE DESTINO',
	'OUTPUT': 'RESULTADO DE SALIDA',
	'PREVIEW': 'VISTA PREVIA',
	'TERMINAL': 'CONSOLA DE LOGS',
	'WEBCAM': 'CÁMARA WEB',
	
	# Parámetros generales
	'OPTIONS': 'OPCIONES GENERALES',
	'PROCESSORS': 'PROCESADORES ACTIVOS',
	'LOG LEVEL': 'NIVEL DE LOGS',
	
	# Parámetros del Detector Facial
	'FACE DETECTOR MODEL': 'MODELO DE DETECTOR FACIAL',
	'FACE DETECTOR SIZE': 'TAMAÑO DE DETECTOR FACIAL',
	'FACE DETECTOR MARGIN': 'MARGEN DE DETECTOR FACIAL',
	'FACE DETECTOR SCORE': 'PUNTUACIÓN DE DETECTOR FACIAL',
	'FACE DETECTOR ANGLES': 'ÁNGULOS DE DETECTOR FACIAL',
	
	# Puntos faciales y oclusores
	'FACE LANDMARKER MODEL': 'MODELO DE PUNTOS FACIALES',
	'FACE LANDMARKER SCORE': 'PUNTUACIÓN DE PUNTOS FACIALES',
	'FACE OCCLUDER MODEL': 'MODELO DE OCLUSOR FACIAL',
	'FACE PARSER MODEL': 'MODELO DE ANALIZADOR FACIAL',
	
	# Selector de Rostro
	'FACE SELECTOR MODE': 'MODO DE SELECTOR FACIAL',
	'FACE SELECTOR ORDER': 'ORDEN DE SELECTOR FACIAL',
	'FACE SELECTOR AGE': 'EDAD DE SELECTOR FACIAL',
	'FACE SELECTOR GENDER': 'GÉNERO DE SELECTOR FACIAL',
	'FACE SELECTOR RACE': 'ETNIA DE SELECTOR FACIAL',
	'REFERENCE FACE DISTANCE': 'DISTANCIA DE ROSTRO DE REFERENCIA',
	'REFERENCE FACE': 'ROSTRO DE REFERENCIA',
	
	# Configuración de salida
	'OUTPUT PATH': 'RUTA DEL ARCHIVO DE SALIDA',
	'TEMP FRAME FORMAT': 'FORMATO DE FOTOGRAMA TEMPORAL',
	'OUTPUT IMAGE QUALITY': 'CALIDAD DE IMAGEN DE SALIDA',
	'OUTPUT IMAGE SCALE': 'ESCALA DE IMAGEN DE SALIDA',
	'OUTPUT AUDIO ENCODER': 'CODIFICADOR DE AUDIO',
	'OUTPUT AUDIO QUALITY': 'CALIDAD DE AUDIO',
	'OUTPUT AUDIO VOLUME': 'VOLUMEN DE AUDIO',
	'OUTPUT VIDEO ENCODER': 'CODIFICADOR DE VIDEO',
	'OUTPUT VIDEO PRESET': 'PREAJUSTE DE VIDEO',
	'OUTPUT VIDEO QUALITY': 'CALIDAD DE VIDEO',
	'OUTPUT VIDEO SCALE': 'ESCALA DE VIDEO',
	'OUTPUT VIDEO FPS': 'FPS DE VIDEO',
	
	# Vista previa y recorte
	'PREVIEW MODE': 'MODO DE VISTA PREVIA',
	'PREVIEW RESOLUTION': 'RESOLUCIÓN DE VISTA PREVIA',
	'PREVIEW FRAME': 'FOTOGRAMA DE VISTA PREVIA',
	'TRIM FRAME': 'RECORTE DE FOTOGRAMAS',
	
	# Ejecución y memoria
	'EXECUTION PROVIDERS': 'PROVEEDORES DE EJECUCIÓN (CPU/CUDA)',
	'EXECUTION THREAD COUNT': 'HILOS DE EJECUCIÓN',
	'SYSTEM MEMORY LIMIT': 'LÍMITE DE MEMORIA RAM (GB)',
	'VIDEO MEMORY STRATEGY': 'ESTRATEGIA DE MEMORIA DE VIDEO',
	
	# Proveedores de descarga
	'DOWNLOAD PROVIDERS': 'PROVEEDORES DE DESCARGA',
	
	# Modificadores y procesadores específicos
	'FACE SWAPPER MODEL': 'MODELO DE INTERCAMBIO (SWAPPER)',
	'FACE SWAPPER PIXEL BOOST': 'RESOLUCIÓN BOOST DE INTERCAMBIO',
	'FACE SWAPPER WEIGHT': 'PESO DE INTERCAMBIO DE ROSTRO',
	'FACE ENHANCER MODEL': 'MODELO DE MEJORA DE ROSTRO (ENHANCER)',
	'FACE ENHANCER BLEND': 'MEZCLA DE MEJORA DE ROSTRO',
	'FACE ENHANCER WEIGHT': 'PESO DE MEJORA DE ROSTRO',
	'FRAME ENHANCER MODEL': 'MODELO DE MEJORA DE FOTOGRAMA',
	'FRAME ENHANCER BLEND': 'MEZCLA DE MEJORA DE FOTOGRAMA',
	'LIP SYNCER MODEL': 'MODELO DE SINCRONIZACIÓN DE LABIOS (LIP-SYNC)',
	'LIP SYNCER WEIGHT': 'PESO DE SINCRONIZACIÓN DE LABIOS',
	'FRAME COLORIZER MODEL': 'MODELO DE COLOREADO DE FOTOGRAMA',
	'FRAME COLORIZER SIZE': 'TAMAÑO DE COLOREADO',
	'FRAME COLORIZER BLEND': 'MEZCLA DE COLOREADO',
	'AGE MODIFIER MODEL': 'MODELO DE MODIFICADOR DE EDAD',
	'AGE MODIFIER DIRECTION': 'DIRECCIÓN DE EDAD',
	'BACKGROUND REMOVER MODEL': 'MODELO DE ELIMINACIÓN DE FONDO',
	'EXPRESSION RESTORER MODEL': 'MODELO DE RESTAURACIÓN DE EXPRESIÓN',
	'EXPRESSION RESTORER FACTOR': 'FACTOR DE RESTAURACIÓN',
	'EXPRESSION RESTORER AREAS': 'ÁREAS DE RESTAURACIÓN',
	'FACE DEBUGGER ITEMS': 'ELEMENTOS DE DEPURACIÓN DE ROSTRO',
	'FACE EDITOR MODEL': 'MODELO DE EDITOR FACIAL',
	'VOICE EXTRACTOR MODEL': 'MODELO DE EXTRACTOR DE VOZ',
	
	# Parámetros del Editor Facial
	'FACE EDITOR EYEBROW DIRECTION': 'DIRECCIÓN DE CEJAS',
	'FACE EDITOR EYE GAZE HORIZONTAL': 'MIRADA HORIZONTAL',
	'FACE EDITOR EYE GAZE VERTICAL': 'MIRADA VERTICAL',
	'FACE EDITOR EYE OPEN RATIO': 'APERTURA DE OJOS',
	'FACE EDITOR LIP OPEN RATIO': 'APERTURA DE LABIOS',
	'FACE EDITOR MOUTH GRIM': 'MUECA DE BOCA',
	'FACE EDITOR MOUTH POUT': 'BOCA FRUNCIDA',
	'FACE EDITOR MOUTH PURSE': 'BOCA APRETADA',
	'FACE EDITOR MOUTH SMILE': 'SONRISA',
	'FACE EDITOR MOUTH POSITION HORIZONTAL': 'POSICIÓN HORIZONTAL DE BOCA',
	'FACE EDITOR MOUTH POSITION VERTICAL': 'POSICIÓN VERTICAL DE BOCA',
	'FACE EDITOR HEAD PITCH': 'INCLINACIÓN DE CABEZA (PITCH)',
	'FACE EDITOR HEAD YAW': 'GIRO DE CABEZA (YAW)',
	'FACE EDITOR HEAD ROLL': 'ROTACIÓN DE CABEZA (ROLL)',
	
	# Estados y mensajes de log en consola/UI
	'conda is not activated': 'Conda no está activado',
	'creating temporary resources': 'creando recursos temporales',
	'extracting frames': 'extrayendo fotogramas',
	'extracting frames succeeded': 'extracción de fotogramas completada',
	'extracting frames failed': 'error al extraer fotogramas',
	'analysing': 'analizando',
	'extracting': 'extrayendo',
	'streaming': 'transmitiendo',
	'processing': 'procesando',
	'merging': 'fusionando',
	'downloading': 'descargando',
	'choose an image for the source': 'selecciona una imagen de origen (rostro)',
	'choose a video for the target': 'selecciona un video de destino',
	'choose an image or video for the target': 'selecciona una imagen o video de destino',
	'specify the output image or video within a directory': 'especifica el archivo de salida en un directorio',
	'match the target and output extension': 'la extensión de salida debe coincidir con la de destino',
	'no source face detected': 'no se detectó ningún rostro de origen',
}


def __autoload__(module_name : str) -> None:
	try:
		__locales__ = importlib.import_module(module_name + '.locales')
		load(__locales__.LOCALES, module_name)
	except ImportError:
		pass


def load(__locales__ : Locales, module_name : str) -> None:
	LOCALE_POOL_SET[module_name] = __locales__


def get(notation : str, module_name : str = 'facefusion') -> Optional[str]:
	if module_name not in LOCALE_POOL_SET:
		__autoload__(module_name)

	# Primero intentamos obtener la traducción para el idioma actual en el archivo locales
	current_lang_pool = LOCALE_POOL_SET.get(module_name).get(CURRENT_LANGUAGE)
	val = None
	if current_lang_pool:
		val = current_lang_pool
		for fragment in notation.split('.'):
			if isinstance(val, dict) and fragment in val:
				val = val.get(fragment)
			else:
				val = None
				break
	
	# Si no se encontró en el idioma actual, usamos inglés como respaldo (fallback)
	if not isinstance(val, str):
		en_pool = LOCALE_POOL_SET.get(module_name).get('en')
		if en_pool:
			val = en_pool
			for fragment in notation.split('.'):
				if isinstance(val, dict) and fragment in val:
					val = val.get(fragment)
				else:
					val = None
					break

	# Si es de tipo string y el idioma actual es español, buscamos su traducción dinámica en el mapa
	if isinstance(val, str):
		if CURRENT_LANGUAGE == 'es':
			# Si el valor exacto está en el mapa, lo traducimos
			if val in SPANISH_TRANSLATIONS:
				return SPANISH_TRANSLATIONS[val]
			# O bien si está en mayúsculas y existe traducción
			elif val.upper() in SPANISH_TRANSLATIONS:
				return SPANISH_TRANSLATIONS[val.upper()]
		return val

	return None

