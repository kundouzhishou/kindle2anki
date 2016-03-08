# -*- coding: utf-8 -*-

import sqlite3
import json
import kindle2anki as k2a
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

conn = sqlite3.connect("vocab.db")
cursor = conn.cursor()
cursor.execute("select * from words")
words = cursor.fetchall()
print(words)
cursor.execute("select * from lookups")
lookups = cursor.fetchall()
print(lookups)
cursor.execute("select * from book_info")
bookinfos = cursor.fetchall()
print(bookinfos)

cursor.close()
conn.close()

def gen_book(book):
	bid = book[0]
	name = book[4]
	author = book[5]
	print("bid = %s, name = %s, author = %s" % (bid, name, author))

	book_wrapper = k2a.BookWrapper(name, "books/")
	for lookup in lookups:
		l_id = lookup[0]
		l_name = lookup[1]
		l_bid = lookup[2]
		l_usage = lookup[5].replace("ĄŻs",'\'').replace("ĄŽ",'"')

		print(l_id)
		print(l_name)
		print(l_bid)
		print(l_usage)

		if l_bid == bid:
			for word in words:
				w_id = word[0]
				w_ori = word[2]
				w_time = word[5]
				if w_id == l_name:
					book_wrapper.add_word(w_ori, l_usage, w_time)


	book_wrapper.dump()


for book in bookinfos:
	gen_book(book)


print("finish ...")

# b = k2a.BookWrapper("books/Animal farm")
# b.dump()



