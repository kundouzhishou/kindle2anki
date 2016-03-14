# -*- coding: utf-8 -*-

import json
import types
import os
import re

class Highlight(object):
	def __init__(self, name, usage, location, time):
		self.name = name
		self.usage = usage
		self.time = time
		self.location = location

	def dump_json(self):
		return {"name":self.name,"usage":self.usage,"time":self.time,"location":self.location}

	def dump_anki(self):
		return "{0}\t{1}\t{2}\t{3}".format(self.name, self.usage, self.location, self.time)

	@staticmethod
	def parse_json(data):
		return Highlight(data["name"], data["usage"],data["time"],data["location"])

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

	def dump_anki(self):
		data = ""
		for word in self.words:
			data += word.dump_anki() + "\n"

		return data

	def dump_html(self):
		data = ""
		row = '<tr>\n<th>{0}</th>\n<th>{1}</th>\n<th>{2}</th>\n<th>{3}</th>\n</tr>\n'
		for word in self.words:
			data += row.format(word.name,word.usage,word.time,word.location)
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
				print(info)
				self.highlights.append({"book":book,"content":content,"location":self.__get_location(info),"time":self.__get_time(info)})

			index += 1

		print(self.highlights)

	def __get_location(self, info):
		match = re.search(r'(\w+) \|',info)
		if match:
			return match.group(1)
		else:
			return ""


	def __get_time(self, info):
		match = re.search(r'\| (.*)',info)
		if match:
			return match.group(1)
		else:
			return ""


class BookWrapper(object):

	def __init__(self, name, fdir):
		self.__name = name
		self.__path = fdir + name
		self.__book = Book(name)

	def add_highlight(self, name, usage, location,time):
		if self.__contains(name):
			return

		word = Highlight(name, usage, location,time)
		self.__book.words.append(word)
		# print("add word:" + name)


	def dump(self):
		s = json.dumps(self.__book.dump_json())
		f = open(self.__path,"wb+")
		f.write(s)
		f.close()
		print("save : %s" % s)

		f = open(self.__path + ".k2a", "wb+")
		f.write(self.__book.dump_anki())
		f.close()

		f = open(self.__path + ".html", "wb+")
		tf = open("template.html","rb+")
		data = tf.read().format(self.__book.dump_html())
		f.write(data)
		tf.close()
		f.close()

	def __contains(self, name):
		for word in self.__book.words:
			if word.name == name:
				return True

		return False



if __name__ == "__main__":
	# b = BookWrapper("test", "books/")
	# b.add_highlight("hehe","ehehe 11",11)
	# b.add_highlight("hehe","ehehe 11",11)
	# b.dump()

	Clipping("input/My Clippings.txt")
