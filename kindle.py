# -*- coding: utf-8 -*-

import sqlite3
import json
import kindle2anki as k2a
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

conn = sqlite3.connect("input/vocab.db")
cursor = conn.cursor()
cursor.execute("select * from words")
words = cursor.fetchall()
# print(words)
cursor.execute("select * from lookups")
lookups = cursor.fetchall()
# print(lookups)
cursor.execute("select * from book_info")
bookinfos = cursor.fetchall()
print(bookinfos)

cursor.close()
conn.close()

clipping = k2a.Clipping("input/My Clippings.txt")

def gen_book(book):
	bid = book[0]
	name = book[4]
	author = book[5]
	print("bid = %s, name = %s, author = %s" % (bid, name, author))
	book_wrapper = k2a.BookWrapper(name, "books/")

	for highlight in clipping.highlights:
		h_content = highlight["content"]
		h_book = highlight["book"]
		h_location = highlight["location"]
		h_time = highlight["time"]

		if name not in h_book:
			continue

		exist = False
		for word in words:
			w_id = word[0]
			w_ori = word[2]
			w_time = word[5]
			if w_ori in h_content:
				for lookup in lookups:
					l_name = lookup[1]
					l_bid = lookup[2]
					# l_usage = lookup[5].replace("ĄŻs",'\'').replace("ĄŽ",'"').replace("ĄŻ",'"')
					l_usage = lookup[5].replace("ĄŽ",'"').replace("ĄŻ",'"')
					# l_usage = lookup[5]
					if l_bid == bid and w_id == l_name:
						book_wrapper.add_highlight(w_ori, l_usage, h_location, h_time)
						exist = True
						break
			if exist:
				break
		if not exist:
			book_wrapper.add_highlight(h_content,"", h_location, h_time)

	book_wrapper.dump()

def gen_highlights():
	books = {}
	
	for highlight in clipping.highlights:
		h_content = highlight["content"]
		h_book = highlight["book"]
		h_location = highlight["location"]
		h_time = highlight["time"]

		if h_book not in books:
			books[h_book] = k2a.BookWrapper(h_book, "highlights/")
		book_wrapper = books[h_book]
		book_wrapper.add_highlight(h_content,"", h_location, h_time)

	for book in books.values():
		book.dump()

def gen_voc():
	for book in bookinfos:
		gen_book(book)

gen_highlights()

print("finish ...")

# b = k2a.BookWrapper("books/Animal farm")
# b.dump()



