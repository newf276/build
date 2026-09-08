# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ElementTree
from urllib.parse import parse_qsl, urlencode

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs


FAVOURITES_FILE = xbmcvfs.translatePath("special://profile/favourites.xml")


def _read_favourites():
	if not xbmcvfs.exists(FAVOURITES_FILE):
		return []

	try:
		with xbmcvfs.File(FAVOURITES_FILE, "r") as favourites_file:
			root = ElementTree.fromstring(favourites_file.read())
	except Exception as exc:
		xbmc.log("[script.finder.helper] Unable to read favourites.xml: %s" % exc, xbmc.LOGERROR,)
		return []

	results = []
	for favourite in root.findall("favourite"):
		action = (favourite.text or "").strip()
		if not action:
			continue
		results.append({"name": favourite.get("name", "Favourite"), "thumb": favourite.get("thumb", ""), "action": action,})
	return results


def _media_type(action):
	action_lower = action.lower()
	if "media_type=movie" in action_lower:
		return "movie"
	if "build_season_list" in action_lower or "media_type=tvshow" in action_lower:
		return "tvshow"
	return "video"


def _run_favourite(index):
	favourites = _read_favourites()
	try:
		action = favourites[int(index)]["action"]
	except (IndexError, TypeError, ValueError):
		return

	xbmc.executebuiltin(action)


def _list_favourites(handle, base_url):
	favourites = _read_favourites()
	xbmcplugin.setContent(handle, "videos")

	for index, favourite in enumerate(favourites):
		name = favourite["name"]
		thumb = favourite["thumb"]
		action = favourite["action"]
		is_playable = action.lower().startswith("playmedia(")

		list_item = xbmcgui.ListItem(label=name)
		list_item.setArt({"poster": thumb, "thumb": thumb, "icon": thumb, "landscape": thumb, "fanart": thumb,})
		list_item.setInfo("video", {"title": name})
		list_item.setProperty("IsFavouriteWidget", "true")

		if is_playable:
			list_item.setProperty("IsPlayable", "true")

		item_url = "%s?%s" % (base_url, urlencode({"mode": "run_favourite", "index": index}),)
		xbmcplugin.addDirectoryItem( handle=handle, url=item_url, listitem=list_item, isFolder=False,)

	xbmcplugin.endOfDirectory(handle, cacheToDisc=False)


def plugin_routing():
	handle = int(sys.argv[1])
	params = dict(parse_qsl(sys.argv[2].lstrip("?"), keep_blank_values=True))
	mode = params.get("mode", "favourites_widget")

	if mode == "run_favourite":
		_run_favourite(params.get("index"))
		xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
		return

	_list_favourites(handle, sys.argv[0])
