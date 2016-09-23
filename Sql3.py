#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Sql3.py
#  
#  Copyright 2013 Miguel A. Reynoso <miguel@vacteria.org>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sqlite3


class DataBase(object):
	"""
	This class is designed by take common database actions.
	"""

	def __init__(self):
		self.con = None
		self.cur = None


	def open(self, db):
		try :
			self.con = sqlite3.connect(db)
			self.cur = self.con.cursor()
		except :
			if(self.con != None):
				self.con.close()
				
			return False

		return True
	
	
	def new(self, sc):
		if self.con == None or self.cur == None:
			return False
		
		try :		
			for query in sc:
				self.con.execute(query)
			
			self.con.commit()
		except sqlite3.Error, e :
			if self.con:
				self.con.rollback()
			
			print e.args[0]
			return False

		return True
		
	
	def shell(self, query, *args):
		if self.con == None or self.cur == None:
			return False
		
		size=len(args)
		query.lstrip().upper()

		try :
			if(size == 0):
				self.cur.execute(query)
			elif (size > 0):
				self.cur.execute(query, args)

			if query.startswith("SELECT"):
				results = self.cur.fetchall()
				for item in results:
					print '|'.join(str(i) for i in item)
			
			if query.startswith("INSERT") or query.startswith("UPDATE"):
				self.con.commit()
				
		except sqlite3.Error, e :
			if self.con:
				self.con.rollback()
			
			print e.args[0]
			return False

		return True



	def query(self, query, *args):
		if self.con == None or self.cur == None:
			return False
		
		size=len(args)
		query.lstrip().upper()

		try :			
			if(size == 0):
				self.cur.execute(query)
			elif (size > 0):
				self.cur.execute(query, args)

			if query.startswith("SELECT"):
				fmt = "['%s']"%"', '".join([t[0] for t in self.cur.fetchall()])
				return fmt
				
			if query.startswith("INSERT") or query.startswith("UPDATE"):
				self.con.commit()
				
		except sqlite3.Error, e :
			if self.con:
				self.con.rollback()
			
			print e.args[0]
			return False

		return True
		

	def close(self):
		if self.con == None or self.cur == None:
			return False
			
		self.con.close()

		return True
