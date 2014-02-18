import warnings
import tablib

#Verificar que el formato es compatible o si se cumplen con los requeiminetos
try:
	from tablib.compat import openpyxl
	XLSX_IMPORT = True
except ImportError:
	try:
		import openpyxl
		XLSX_IMPORT = True
	except ImportError:
		warnings.warn("XLSX: No compat and/or openpyxl not installed", ImportWarning)
		XLSX_IMPORT = False

from django.utils.importlib import import_module

class Formato(object):

	def get_title(self):
		return type(self)

	def create_dataset(self, in_stream):
		"""
		TODO:
		"""
		raise NotImplementedError()

	def export_data(self, dataset):
		"""
		TODO:
		"""
		raise NotImplementedError()

	def is_binary(self):
		"""
		El formato es binario?
		"""
		return True

	def get_read_mode(self):
		"""
		Como se abrira/leera el archivo?
		"""
		return 'rb'

	def get_extension(self):
		"""
		Cual es la extension del archivo?
		"""
		return ""

	def importable(self):
		return False

	def exportable(self):
		return False

class TablibFormatos(Formato):
	TABLIB_MODULE = None

	def get_format(self):
		"""
		Que modulo deberemos de importar?
		"""
		return import_module(self.TABLIB_MODULE)

	def get_title(self):
		"""
		Dependiendo del modulo importado, obtener el titulo del pkg. See formats._???? in tablib
		"""
		return self.get_format().title

	def create_dataset(self, in_stream):
		"""
		"""
		data = tablib.Dataset()
		self.get_format().import_set(data, in_stream)
		return data

	def export_data(self, dataset):
		return self.get_format().export_set(dataset)

	def get_extension(self):
		#See tablib.formats._???  extentions('ext',)
		return self.get_format().extentions[0]

	def importable(self):
		return hasattr(self.get_format(), 'import_set')

	def exportable(self):
		return hasattr(self.get_format(), 'export_set')

class Texto(TablibFormatos):
	"""
	Para el formato de cualquier texto
	"""
	def get_read_mode(self):
		return 'rU'

	def is_binary(self):
		return False

class CSV(TablibFormatos):
	"""
	Para el formato csv (comma-separated-values).is_binary = True in python
	"""
	TABLIB_MODULE = 'tablib.formats._csv'

	def get_read_mode(self):
		return 'rb'

	def is_binary(self):
		return True

class JSON(Texto):
	"""
	JSON format
	"""
	TABLIB_MODULE = 'tablib.formats._json'

class HTML(Texto):
	"""
	html support
	"""
	TABLIB_MODULE = 'tablib.formats._html'

class XLSX(TablibFormatos):
	"""
	xlsx 2007+
	"""
	TABLIB_MODULE = 'tablib.formats._xlsx'

	def importable(self):
		return XLSX_IMPORT

	def create_dataset(self, in_stream):
		"""
		TODO:
		"""
		
