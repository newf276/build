#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import xbmc
import xbmcgui

from resources.lib.modules.utils import Log
from resources.lib.modules.quick_whitelist import AddWhiteList,RemoveWhiteList








if __name__ == '__main__':
	Log(xbmc.getInfoLabel('System.CurrentWindow'))
	addonid = sys.listitem.getProperty('Addon.ID')
	Log(addonid)
	arg    = sys.argv[1]
	if addonid:
		if arg == 'add':
			AddWhiteList(addonid)
		elif arg == 'remove':
			RemoveWhiteList(addonid)

