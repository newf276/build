# -*- coding: utf-8 -*-
import sys

if sys.argv and sys.argv[0].startswith("plugin://"):
	from modules.favourites_widget import plugin_routing

	plugin_routing()
else:
	from modules.router import routing

	routing()
