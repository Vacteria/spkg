#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spkg.py
#
#  Copyright 2013 Miguel A. Reynoso <miguel@sys32>
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
#  Foundation, Inrt., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import os
import sys
import gettext
import getopt

import FrameWork as Fwk
import Sql3 as Sql

_ = gettext.gettext	
gettext.install("spkg", "/usr/share/locale")
#TRANSLATION_DOMAIN = "spkg"
#LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")
#gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

hexver = sys.hexversion
if hexver < 0x02070000 or hexver >= 0x03000000 :
	print _('Spkg requires >= 2.6 & < 3.0 python version. Your version is %s') %hexver
	sys.exit(-1)

class LocalMessages(object):
	"""
		This class is usefull to handler common used meesages like a
		simple catalog. This mode is needed for easly program translation
		with gettext() module
	"""
	
	#
	# initialize atributtes
	#
	def __init__(self):
		self.err = _('ERROR   :')
		self.warn = _('WARNING :')
		self.msg = _('MESSAGE :')
		self.dbg = _('DEBUG   :')
		self.not_found = _("Not found")
		self.db_not_found = _("No such database")
		self.file_not_found = _("File not found")
		self.dir_not_found = _("Directory not found")
		self.file_found = _('File found')
		self.dir_found = _('Directory found')
		self.is_a_file = _("Looks like file")
		self.is_not_a_file = _("Does not looks like a regular file")
		self.is_a_dir = _("Looks like directory")
		self.is_not_a_dir = _("Does not looks like a directory")
		self.is_not_a_dir = _("Does not looks like a directory")
		self.file_is_empty = _("File looks like empty")
		self.dir_is_empty = _("Directory looks like empty")
		self.file_exists = _("File already exists")
		self.dir_exists = _("Directory already exists")
		self.making_dir = _("Making directory")
		self.making_file = _("Making file")
		self.making_db = _("Making database")
		self.openning_file = _("Openning file")
		self.openning_db = _("Openning database")
		self.openning = _("Openning ...")
		self.exiting = _("Exiting ...")
		self.aborting = _("Aborting ...")
		self.searching_realpath = _('Searching real path')
		self.realpath_found = _('The real path was found')
		self.failed_to_open_file = _("Failed to open file")
		self.failed_to_open_dir = _("Filed to open directory")
		self.failed_to_open_db = _("Filed to open datbase")
		self.failed_to_making_file = _("Failed to make file")
		self.failed_to_making_dir = _("Failed to make directory")
		self.failed_to_copy_file = _("Failed to copy file")
		self.failed_to_copy_dir = _("Failed to copy dir")
		self.failed_to_move_file = _("Failed to move file")
		self.failed_to_move_dir = _("Failed to move dir")
		self.failed_to_release_paths = _('Failed to release system paths')
		self.need_arg = _('Requires at least one argument')
		self.opt_need_arg = _('option need an argument')
		self.unknow_opt = _('unknow option')
		self.failed_to_run_query = _('Run database query failed')
		
	def usage(self):
		"""
			Print skpg usage help and exit
		"""
		print _(
	"""	
 Sinopsys :
  Oficial local package manager and database query information
  for Vacteria GNU/linux

 Usage :
  spkg [params] [packages]

 Parameters :
  -i, --install   Install a packages
  -r, --remove    Remove installed packages
  -u, --upgrade   Upgrade installed packages
  -e, --extract   Extract a package files
  -m, --mkpkg     Make packages with given directory
  -q, --query     Run a query local database
  -I, --initdb    Initialize a new empty database
  -R, --root      Set root directory
  -F, --format    Formaters for query
  -v, --verbose   Show many possible messages
  -s, --silent    Only show fatal errors
  --norundeps     Install packages skipping runtime depends
  --noconflicts   Install packages skipping runtime conflicts
  --nosetup       Install and unistall packages without execute "setup" file
  --notriggers    Install and unistall packages without triggers execution
	"""
		)
		

class Runargs(object):
	"""
		This class initialize runtime variables parsed by getopt()
	"""
	
	def __init__(self):
		self.progname = None
		self.root = "/"
		self.selector = None
		self.qmode = None
		self.qformat = None
		self.verbose = False
		self.silent = False
		self.rundeps = True
		self.conflicts = True
		self.setup = True
		self.triggers = True
		self.selectors = {}



def start_database(msg, rt, ra):
	#
	# First check directory tree and make missing
	#
	for d in rt.struct[:-1]:
		if not os.path.isdir(d):
			if ra.verbose:
				print msg.dbg, msg.making_dir, d
			
			os.makedirs(d)
		else:
			if ra.verbose :
				print msg.dbg, d, msg.dir_exists
	
	#
	# Set especial permissions for directories
	#
	os.chmod(rt.setup, 0700)
	os.chmod(rt.tmp, 01777)
	
	#
	# If database exist ask for default action.
	#
	if os.path.isfile(rt.database):
		try :
			sys.stdout.write(msg.warn + _(' The database already exists. Press enter to override or Ctrl+C to exit') )
			raw_input()
		except KeyboardInterrupt :
			print "\n"+msg.exiting
			return -1
	
	#
	# Create a database
	#
	if ra.verbose:
		print msg.dbg, msg.making_db

	#
	# Instance  a Object to handle database
	#
	db = Sql.DataBase()
	
	#
	# Open one connection to database
	#
	if not db.open(rt.database):
		if rt.verbose:
			print msg.dbg, msg.openning_database
			
		print msg.err, msg.failed_to_open_db
		return -1
	
	#
	# Run default multiple querys
	#
	if not db.new(rt.schema):
		print msg.err, msg.failed_to_run_query

	#
	# Close database
	#
	db.close()



def query_info(msg, rt, ra):
	if ra.qmode in ("ra", "arch"):
		return rt.realarch
	elif ra.qmode in ("pa", "pkgarch"):
		return rt.pkgarch
	elif ra.qmode in ("sa", "sup-archs"):
		return ' '.join(str(i) for i in rt.archs)
	elif ra.qmode in ("ss", "sup-sections"):
		return ' '.join(str(i) for i in rt.sections)
	elif ra.qmode in ("sp", "sup-packages"):
		return ' '.join(str(i) for i in rt.pkgtypes)
	elif ra.qmode in ("ve", "vendor"):
		return rt.vendor
	elif ra.qmode in ("di", "distro"):
		return rt.distro


def make_package(msg, rt, ra, pkgv):
	for d in pkgv:
		if not os.path.exists(d):
			print msg.err, d, msg.dir_not_found
			return True
			
		if os.path.islink(d):
			if ra.verbose:
				print msg.dbg, msg.searching_realpath
			
			if os.path.realpath(os.readlink(d)):
				d = os.path.realpath(os.readlink(d))
				if ra.verbose:
					print msg.dbg, msg.reapath_found, d
		else:
			d = os.path.realpath(d)

		if not os.path.isdir(d):
			print msg.err, d, msg.is_not_a_dir
			return False
		
		if ra.verbose:
			print msg.dbg, d, msg.dir_found
		
		if os.path.isdir(d+"/data") and os.path.isfile(d+"/control"):
			os.chdir(d)
			
		
	return True


def main(argv):
	#
	# Instance object to handle messages
	#
	msg = LocalMessages()

	#
	# Define program seletors
	#
	selectors = {
		1:"install",
		2:"remove",
		3:"config",
		4:"extract",
		5:"makepkg",
		6:"help",
		7:"query=",
		8:"initdb"
	}
	
	#
	# Define program swicthes
	#
	switches = {
		1:"root=",
		2:"format=",
		3:"verbose",
		4:"silent"
	}
	
	#
	# Define program short options for selectors and switches
	#
	short_opts = "irucemhq:IR:F:vs"
	
	#
	# Use selectors and swicthes dictionary values to implement
	# program long options
	#
	long_opts = [ selectors.values(), switches.values() ]
	
	#
	# Parse all arguments
	#
	try :
		opts, args = getopt.gnu_getopt(argv[1:], short_opts, long_opts)
	except getopt.error, e :
		if 'requires argument' in e.msg:
			print msg.err, "-"+e.opt, msg.opt_need_arg
		
		if 'not recognized' in e.msg:
			print msg.err, msg.unknow_opt, "-"+e.opt

		sys.exit(-1)
		

	#
	# Instance runtime object
	#
	rt = Fwk.Runtime()
	
	#
	# Instance switches from getopt
	#
	ra = Runargs()

	#
	# Set program name
	#
	rt.progname = argv[0]
	
	#
	# Update selector dict
	#
	ra.selectors.update(selectors)
	
	#
	# Parse all options and set founded values
	#
	for o,a in opts :
		if o in ("-i", "--install"):
			ra.selector = 1
		elif o in ("-r", "--remove"):
			ra.selector = 2
		elif o in ("-u", "--config"):
			ra.selector = 3
		elif o in ("-e", "--extract"):
			ra.selector = 4
		elif o in ("-m", "--mkpkg"):
			ra.selector = 5
		elif o in ("-h", "--help"):
			ra.selector = 6
		elif o in ("-q", "--query"):
			ra.selector = 7
			ra.qmode = a
		elif o in ("-I", "--initdb"):
			ra.selector = 8
		elif o in ("-R", "--root"):
			ra.root = a
		elif o in ("-F", "--format"):
			ra.qformat = a
		elif o in ("-v", "--verbose"):
			ra.verbose = True
		elif o in ("-s", "--silent"):
			ra.silent = True
		elif o in ("--norundeps"):
			ra.rundeps = False
		elif o in ("--conflicts"):
			ra.conflicts = False
		elif o in ("--setup"):
			ra.setup = False
		elif o in ("--triggers"):
			ra.triggers = False
		
	#		
	# Release root atribute and dependent paths
	#
	if not rt.release(ra.root):
		print msg.err, msg.failed_to_release_paths
		sys.exit(-1)
	
	
	#
	# Test a selector
	#
	if(ra.selector == None):
			print rt.progname, msg.need_arg
			sys.exit(-1)
			
	#
	# Test administrative privileges fo expecific selectors
	#
	if ra.selector in (1,2,3,8):
		if(os.getuid() != 0):
			print msg.err, _('--%s need administrative privileges') %ra.selectors[ra.selector]
			sys.exit(-1)
	
	#
	# Test database and directories for especific selectors
	#
	if ra.selector in (1,2,3):
			for d in rt.struct:
				if not os.path.exists(d):
					print msg.err, d, msg.dir_not_found, _('Please use --initdb first')
					sys.exit(-1)


	#
	# Execute apropiate function defined by selector
	#
	pkgv = args

	if(ra.selector == 5):
		make_package(msg, rt, ra, pkgv)
	if(ra.selector == 6):
		msg.usage()
		sys.exit(0)
	if(ra.selector == 7):
		print query_info(msg, rt, ra)
	elif(ra.selector == 8):
		start_database(msg, rt, ra)

	return 0

if __name__ == '__main__':
	sys.exit(main())

