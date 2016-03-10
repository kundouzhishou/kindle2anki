# -*- coding: utf-8 -*-

import json
import types
import os

class Highlight(object):
	def __init__(self, name, usage, time):
		self.name = name
		self.usage = usage
		self.time = time

	def dump_json(self):
		return {"name":self.name,"usage":self.usage,"time":self.time}

	@staticmethod
	def parse_json(data):
		return Highlight(data["name"], data["usage"],data["time"])

class Book(object):
	def __init__(self, name):
		self.name = name
		self.words = []

	def dump_json(self):
		data = {"book":self.name,"highlights":[]}
		for word in self.words:
			# print("add word")
			data["highlights"].append(word.dump_json())
		return data

	@staticmethod
	def parse_json(data):
		b = Book("")
		b.name = data["book"]
		for word in data["highlights"]:
			w = Highlight.parse_json(word)
			b.words.append(w)
		return b

class Clipping(object):
	def __init__(self, name):
		f = open(name, "rb+")
		self.highlights = list()
		book = ""
		info = ""
		content = ""
		index = 0
		while(True):
			line = f.readline()
			line = line.decode("utf-8-sig").encode("utf-8")
			if len(line) == 0:
				break

			if "=====" in line:
				index = 0
				continue 

			if line in ['\n', '\r\n']:
				continue

			line = line.strip()

			if index == 0:
				book = line
			elif index == 1:
				info = line
			elif index == 2:
				content = line

			if index == 2:
				self.highlights.append({"book":book,"content":content,"info":info})

			index += 1


class BookWrapper(object):

	def __init__(self, name, fdir):
		self.__name = name
		self.__path = fdir + name
		if os.path.exists(self.__path):
			f = open(self.__path, "rb+")
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

	def add_highlight(self, name, usage, info):
		if self.__contains(name):
			return

		word = Highlight(name, usage, info)
		self.__book.words.append(word)
		# print("add word:" + name)


	def dump(self):
		s = json.dumps(self.__book.dump_json())
		f = open(self.__path,"wb+")
		f.write(s)
		f.close()
		print("save : %s" % s)

	def __contains(self, name):
		for word in self.__book.words:
			if word.name == name:
				return True

		return False



if __name__ == "__main__":
	b = BookWrapper("test", "books/")
	b.add_highlight("hehe","ehehe 11",11)
	# b.add_highlight("hehe","ehehe 11",11)
	b.dump()

	# Clipping("My Clippings.txt")
