#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  FrameWork.py
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


import os
import re


class Runtime(object):
	""" 
	This class initialize system variables and paths. The release()
	method, take a path as root directory to reset all path related 
	atributes. This is usefull to change alternative root directory 
	given for example by -R getopt switch. These method also set 
	architecture relates atributes like a real architecture and
	package arquitecture relation.
	"""

	#
	# Initialize attributes with non empty values
	#
	def __init__(self):
		self.home = None
		self.tmp = None
		self.setup = None
		self.data = None
		self.database = None
		self.struct = None
		self.archs = None
		self.realarch = None
		self.pkgarch = None
		self.sections = None
		self.fhs = None
		self.schema = None
		self.vendor = None
		self.distro = None
		self.pkgtypes = None
		self.config = "/etc/spkg/spkg.conf"

	#
	# release all attribute variables with aprpiate values
	#
	def release(self, newroot):
		"""
			Release all previusly initializade values with new apropiate
			results
		"""
		
		try:
			if os.path.islink(self.config):
				self.config = os.path.realpath(os.readlink(self.config))
			
			conf = open(self.config, "r")
		except (IOError, OSError):
			return -1

		for i in conf:
			if not i.startswith("/"):
				l = str(i).strip('\n').split("=")
				if l[0].capitalize().startswith("Vendor"):
					if str(l[1]):
						self.vendor = str(l[1]).lstrip()
					else:
						self.vendor = "Generic"
					
				if l[0].capitalize().startswith("Distro"):
					if str(l[1]):
						self.distro = str(l[1]).lstrip()
					else:
						self.distro = "Generic Linux Distribution"

				if l[0].capitalize().startswith("Sections"):
					if str(l[1]):
						self.sections = tuple(str(l[1]).lstrip().split(","))
					else:
						self.sections = ("main", "contrib", "outside")
								
				if l[0].capitalize().startswith("Pkgarchs"):
					if str(l[1]):			
						self.archs = tuple(str(l[1]).lstrip().split(","))
					else:
						self.archs = ("x32", "x64", "noarch")

				if l[0].capitalize().startswith("Pkgtypes"):
					if str(l[1]):
						self.pkgtypes = tuple(str(l[1]).lstrip().split(","))
					else:
						self.pkgtypes = ("pkg", "subpkg", "binpkg", "fakepkg", "metapkg")

		self.home = newroot + "/var/spkg"
		self.tmp = self.home + "/tmp"
		self.setup = self.home + "/setup"
		self.cache = self.home + "/cache"
		self.mfiles = self.home + "/manifests"
		self.data = self.home + "/data"
		self.database = self.data + "/pkg.db"
		self.struct = (
			self.home, 
			self.tmp, 
			self.data, 
			self.setup,
			self.mfiles,
			self.cache,
			self.database
		)

		self.realarch = os.uname()[4]

		if ( self.realarch == "x86_64" ):
			self.pkgarch = "x64"
		elif re.findall(r'(pentium[1-4]|i[3-9]86)', self.realarch):
			self.pkgarch = "x32"
		
		if (self.pkgarch == None):
			return False
		
		fhs = (
			"/var/tmp",
			"/var/spool",
			"/var/opt",
			"/var/mail",
			"/var/log/news",
			"/var/log",
			"/var/local",
			"/var/lib/misc",
			"/var/lib/locate",
			"/var/lib",
			"/var/cache",
			"/var",
			"/usr/src",
			"/usr/share/zoneinfo",
			"/usr/share/terminfo",
			"/usr/share/misc",
			"/usr/share/man/man8",
			"/usr/share/man/man7",
			"/usr/share/man/man6",
			"/usr/share/man/man5",
			"/usr/share/man/man4",
			"/usr/share/man/man3",
			"/usr/share/man/man2",
			"/usr/share/man/man1",
			"/usr/share/man",
			"/usr/share/locale",
			"/usr/share/info",
			"/usr/share/fonts",
			"/usr/share/doc",
			"/usr/share",
			"/usr/sbin",
			"/usr/man",
			"/usr/local/src",
			"/usr/local/share/zoneinfo",
			"/usr/local/share/terminfo",
			"/usr/local/share/misc",
			"/usr/local/share/man/man8",
			"/usr/local/share/man/man7",
			"/usr/local/share/man/man6",
			"/usr/local/share/man/man5",
			"/usr/local/share/man/man4",
			"/usr/local/share/man/man3",
			"/usr/local/share/man/man2",
			"/usr/local/share/man/man1",
			"/usr/local/share/man",
			"/usr/local/share/locale",
			"/usr/local/share/info",
			"/usr/local/share/fonts",
			"/usr/local/share/doc",
			"/usr/local/share",
			"/usr/local/sbin",
			"/usr/local/man",
			"/usr/local/lib",
			"/usr/local/info",
			"/usr/local/include",
			"/usr/local/doc",
			"/usr/local/bin",
			"/usr/local",
			"/usr/lib",
			"/usr/info",
			"/usr/include",
			"/usr/doc",
			"/usr/bin/run-parts",
			"/usr/bin",
			"/usr",
			"/tmp",
			"/sys",
			"/srv",
			"/sbin",
			"/run",
			"/root",
			"/proc",
			"/opt",
			"/mnt",
			"/media/floppy",
			"/media/cdrom",
			"/media",
			"/lib",
			"/home",
			"/etc/rcS.d",
			"/etc/rc.d",
			"/etc/rc.conf.d",
			"/etc/rc6.d",
			"/etc/rc5.d",
			"/etc/rc4.d",
			"/etc/rc3.d",
			"/etc/rc2.d",
			"/etc/rc1.d",
			"/etc/rc0.d",
			"/etc/opt",
			"/etc/network.d",
			"/etc/mtab",
			"/etc/default",
			"/etc/cron.weekly",
			"/etc/cron.monthly",
			"/etc/cron.hourly",
			"/etc/cron.daily",
			"/etc/cron.d",
			"/etc",
			"/dev",
			"/boot",
			"/bin/which",
			"/bin"
		)

		schema = (
		"""
CREATE TABLE IF NOT EXISTS Packages(
	id_spkg		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	Name		VARCHAR(54) NOT NULL,
	Version		VARCHAR(64) NOT NULL,
	Release		INTEGER NOT NULL,
	Arch		INTEGER NOT NULL,
	Section		INTEGER NOT NULL,
	PkgType		INTEGER NOT NULL,
	Node		INTEGER NOT NULL,
	State		INTEGER DEFAULT '0',
	License		VARCHAR(128) NOT NULL,
	Md5Sum		VARCHAR(128) NOT NULL UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS Archs(
	id_arch		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	ArchName	VARCHAR(16) NOT NULL UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS Sections(
	id_section	INTEGER NOT NULL PRIMARY KEY UNIQUE,
	SecName		VARCHAR(16) NOT NULL UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS PkgTypes(
	id_type		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	PkgType		VARCHAR(16) NOT NULL UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS Nodes(
	id_node		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	NodeName	VARCHAR(64) UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS Packagers(
	id_pkgr		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	PkgrName	VARCHAR(64) NOT NULL UNIQUE,
	PkgrMail	VARCHAR(64) NOT NULL UNIQUE,
	PkgrNic		VARCHAR(64) NOT NULL UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS Package_has_Packagers(
	id_row		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	id_pkgr		INTEGER NOT NULL UNIQUE,
	id_spkg		INTEGER NOT NULL UNIQUE
);
		""",
		"""
CREATE TABLE IF NOT EXISTS DepTypes(
	id_type		INTEGER NOT NULL PRIMARY KEY UNIQUE,
	DepName		VARCHAR(64) NOT NULL UNIQUE
);
		""",

		"""
CREATE TABLE IF NOT EXISTS Package_has_depends(
	id_row		INTEGER PRIMARY KEY NOT NULL UNIQUE,
	id_deptype	INTEGER NOT NULL,
	id_spkg		INTEGER NOT NULL,
	Depends		VARCHAR(255) NOT NULL
);
		""",
		"""
CREATE TABLE IF NOT EXISTS Contents(
	id_content	INTEGER NOT NULL PRIMARY KEY UNIQUE,
	id_spkg		INTEGER NOT NULL,
	Content		VARCHAR(255)
);
		"""
		)
		
		self.fhs = fhs
		self.schema = schema
		
		return True



class SpkgFile():
	"""
		Not yet impemented ;)
	"""
	pass



class Manifest():
	"""
		Take manifest file as argument, extract values from them and
		update attributes with thes values. This class pass real manifest
		file to abstract computer dates
	"""
	
	def __init__(self):
		self.name = None
		self.ver = None
		self.arch = None
		self.sec = None
		self.ptype = None
		self.hold = None
		self.node = None
		self.pkgrs = None
		self.lics = None
		self.rdeps = None
		self.confc = None
		self.bdeps = None
		self.ldeps = None
		self.contn = None
