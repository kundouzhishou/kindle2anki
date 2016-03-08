import sqlite3
import json

class Book(object):
	def __init__(self, name):
		self.__f = open(name, "wb+")
		self.__content = self.__f.read()
		if len(self.__content) == 0:
			self.__data = {}
		else:
			self.__data = json.load(self.__content)
		print("data = %s" % self.__data)

	def dump(self):
		s = json.dumps(self.__data)
		self.__f.write(s)


conn = sqlite3.connect("vocab.db")
cursor = conn.cursor()
cursor.execute("select * from words")
words = cursor.fetchall()
print(words)
cursor.execute("select * from lookups")
lookups = cursor.fetchall()
print(lookups)

# result = 
# for word in words:


cursor.close()
conn.close()

print("finish ...")

b = Book("Animal farm")
b.dump()



