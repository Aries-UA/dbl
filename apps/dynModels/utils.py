# -*- coding: utf-8 -*-

import os
import yaml

from django.contrib import admin
from django.db import models, connection
from south.db import db
from django.utils.importlib import import_module
from django.core.urlresolvers import clear_url_caches
from django.conf import settings

from apps.dynModels.settings import *

class LoadModels(object):
	""" Класс загрузки файла """

	is_load = True
	models = None
	name = None

	def __init__(self, name=None):
		self.name = name
		###
		with open(self.getFileName()) as f:
			try:
				self.models = yaml.load(f)
			except yaml.YAMLError:
				self.is_load = False
			###
			f.close()

	def getFileName(self):
		return '/'.join([PATH_YAML, self.name])

class DynamicModels(LoadModels):
	""" Класс генератор для динамических моделей """

	tables = []

	def __init__(self, name=None):
		if name:
			super(DynamicModels, self).__init__(name)
			###
			self.setModels()

	def addInfo(self, name, table):
		""" добвление информации о созданной модели """
		row = {'name':name, 'table':table,}
		###
		if row not in self.tables: self.tables.append(row)

	def setModels(self):
		""" Определение и установка данных """
		if self.is_load:
			for model in self.models:
				class_model = self.getClass(model, self.models[model])
				###
				self.createTable(class_model)
				self.addColumns(class_model)
				self.adminRegister(class_model)

	def getClass(self, model, dict_model):
		""" Создание класса модели """
		name = dict_model.get('title')
		table = 'dynModels_%s' % model
		###
		self.addInfo(name, table)
		###
		attrs = {}
		###
		class Meta:
			app_label = 'dynModels'
			db_table = table
			managed = False
			verbose_name = name
			verbose_name_plural = name
		###
		attrs['Meta'] = Meta
		attrs['__module__'] = 'apps.dynModels.models'
		attrs['__unicode__'] = lambda self: u'%s' % self.id
		###
		for f in dict_model.get('fields'):
			f_id = f.get('id')
			f_title = f.get('title')
			f_type = f.get('type')
			###
			if f_id and f_title and f_type:
				if f_type == 'int':
					attrs[f_id] = models.IntegerField(f_title, blank=True, null=True, default=0)
				elif f_type == 'char':
					attrs[f_id] = models.CharField(f_title, max_length=255, blank=True, default='')
		###
		return type(model, (models.Model,), attrs)

	def createTable(self, class_model):
		""" Создание таблицы в базе данных """
		name = class_model._meta.db_table
		###
		if connection.introspection.table_name_converter(name) not in connection.introspection.table_names():
			db.create_table(name, [(f.name, f) for f in class_model._meta.fields])

	def addColumns(self, class_model):
		""" Добавление/удаление колонок """
		name = class_model._meta.db_table
		###
		descr = connection.introspection.get_table_description(connection.cursor(), name)
		columns = [c[0] for c in descr]
		###
		for f in class_model._meta.fields:
			if f.name not in columns:
				db.add_column(name, f.name, f)

	def adminRegister(self, class_model):
		""" Регистрация модели в админке """
		try:
			admin.site.unregister(class_model)
		except:
			pass
		###
		admin.site.register(class_model)
		###
		reload(import_module(settings.ROOT_URLCONF))
		clear_url_caches()

	def get(self, name=None):
		""" Возврат модели по имени """
		current = None
		###
		for model in admin.site._registry.keys():
			if name == model._meta.db_table:
				current = model
				break
		###
		return current

	def getModelsName(self):
		""" Список динамических моделей """
		return self.tables
