# -*- coding: utf-8 -*-

import json
import types
import os

class Word(object):
	def __init__(self, name, usage, time):
		self.name = name
		self.usage = usage
		self.time = time

	def dump_json(self):
		return {"name":self.name,"usage":self.usage,"time":self.time}

	@staticmethod
	def parse_json(data):
		return Word(data["name"], data["usage"],data["time"])

class Book(object):
	def __init__(self, name):
		self.name = name
		self.words = []

	def dump_json(self):
		data = {"name":self.name,"words":[]}
		for word in self.words:
			print("add word")
			data["words"].append(word.dump_json())
		return data

	@staticmethod
	def parse_json(data):
		b = Book("")
		b.name = data["name"]
		for word in data["words"]:
			w = Word.parse_json(word)
			b.words.append(w)
		return b

class BookWrapper(object):

	def __init__(self, name):
		self.__name = name
		if os.path.exists(name):
			f = open(name, "rb+")
			self.__content = f.read()
			if len(self.__content) == 0:
				self.__book = Book(name)
			else:
				json_data = json.loads(self.__content)
				self.__book = Book.parse_json(json_data)
			f.close()
		else:
			self.__book = Book(name)

		# print("init : %s" % self.__book)

	def add_word(self, name, usage, time):
		if self.__contains(name):
			return

		word = Word(name, usage, time)
		self.__book.words.append(word)
		print("add word:" + name)


	def dump(self):
		s = json.dumps(self.__book.dump_json())
		f = open(self.__book.name,"wb+")
		f.write(s)
		f.close()
		print("save : %s" % s)

	def __contains(self, name):
		for word in self.__book.words:
			if word.name == name:
				return True

		return False



if __name__ == "__main__":
	b = BookWrapper("test")
	b.add_word("hehe","ehehe 11",11)
	# b.add_word("hehe","ehehe 11",11)
	b.dump()
