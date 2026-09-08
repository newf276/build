# -*- coding: utf-8 -*-
import os
import re

import xbmc
import xbmcgui
import xbmcvfs


MENU_ITEMS = {
	"FinderMainMenuMovies": ("Movies", "!Skin.HasSetting(HomeMenuNoMoviesButton)"),
	"FinderMainMenuTVShows": ("TV Shows", "!Skin.HasSetting(HomeMenuNoTVShowsButton)"),
	"FinderMainMenuCustom1": ("Custom 1", "!Skin.HasSetting(HomeMenuNoCustom1Button)"),
	"FinderMainMenuCustom2": ("Custom 2", "!Skin.HasSetting(HomeMenuNoCustom2Button)"),
	"FinderMainMenuCustom3": ("Custom 3", "!Skin.HasSetting(HomeMenuNoCustom3Button)"),
	"FinderMainMenuCustom4": ("Custom 4", "!Skin.HasSetting(HomeMenuNoCustom4Button)"),
	"FinderMainMenuCustom5": ("Custom 5", "!Skin.HasSetting(HomeMenuNoCustom5Button)"),
	"FinderMainMenuCustom6": ("Custom 6", "!Skin.HasSetting(HomeMenuNoCustom6Button)"),
	"FinderMainMenuMusic": ("Music", "!Skin.HasSetting(HomeMenuNoMusicButton)"),
	"FinderMainMenuDisc": ("Disc", "System.HasMediaDVD"),
	"FinderMainMenuMusicVideos": ("Music videos", "!Skin.HasSetting(HomeMenuNoMusicVideoButton)"),
	"FinderMainMenuLiveTV": ("Live TV", "!Skin.HasSetting(HomeMenuNoTVButton)"),
	"FinderMainMenuRadio": ("Radio", "!Skin.HasSetting(HomeMenuNoRadioButton)"),
	"FinderMainMenuGames": ("Games", "System.GetBool(gamesgeneral.enable) + !Skin.HasSetting(HomeMenuNoGamesButton)"),
	"FinderMainMenuAddons": ("Add-ons", "!Skin.HasSetting(HomeMenuNoProgramsButton)"),
	"FinderMainMenuPictures": ("Pictures", "!Skin.HasSetting(HomeMenuNoPicturesButton)"),
	"FinderMainMenuVideos": ("Videos", "!Skin.HasSetting(HomeMenuNoVideosButton)"),
	"FinderMainMenuFavourites": ("Favourites", "!Skin.HasSetting(HomeMenuNoFavButton)"),
	"FinderMainMenuWeather": ("Weather", "!Skin.HasSetting(HomeMenuNoWeatherButton)"),
}

DEFAULT_MENU_ORDER = (
	"FinderMainMenuMovies",
	"FinderMainMenuTVShows",
	"FinderMainMenuCustom1",
	"FinderMainMenuCustom2",
	"FinderMainMenuCustom3",
	"FinderMainMenuCustom4",
	"FinderMainMenuCustom5",
	"FinderMainMenuCustom6",
	"FinderMainMenuMusic",
	"FinderMainMenuDisc",
	"FinderMainMenuMusicVideos",
	"FinderMainMenuLiveTV",
	"FinderMainMenuRadio",
	"FinderMainMenuGames",
	"FinderMainMenuAddons",
	"FinderMainMenuPictures",
	"FinderMainMenuVideos",
	"FinderMainMenuFavourites",
	"FinderMainMenuWeather",
)

MENU_BLOCK_RE = re.compile(r'(?P<indent>^[\t ]*)<include name="FinderMainMenuItems">\s*(?P<content>.*?)\s*</include>', re.MULTILINE | re.DOTALL,)
INCLUDE_RE = re.compile(r'<include content="([^"]+)"/>')
LABEL_RE = re.compile(r"<label>(.*?)</label>", re.IGNORECASE | re.DOTALL)

CONFIGURABLE_MENU_TYPES = (
	("Movies", "movie", "FinderMainMenuMovies"),
	("TV Shows", "tvshow", "FinderMainMenuTVShows"),
	("Custom 1", "custom1", "FinderMainMenuCustom1"),
	("Custom 2", "custom2", "FinderMainMenuCustom2"),
	("Custom 3", "custom3", "FinderMainMenuCustom3"),
	("Custom 4", "custom4", "FinderMainMenuCustom4"),
	("Custom 5", "custom5", "FinderMainMenuCustom5"),
	("Custom 6", "custom6", "FinderMainMenuCustom6"),
)

CONFIGURED_MENU_FILES = {
	"FinderMainMenuMovies": "script-finder-main_menu_movies.xml",
	"FinderMainMenuTVShows": "script-finder-main_menu_tvshows.xml",
	"FinderMainMenuCustom1": "script-finder-main_menu_custom1.xml",
	"FinderMainMenuCustom2": "script-finder-main_menu_custom2.xml",
	"FinderMainMenuCustom3": "script-finder-main_menu_custom3.xml",
	"FinderMainMenuCustom4": "script-finder-main_menu_custom4.xml",
	"FinderMainMenuCustom5": "script-finder-main_menu_custom5.xml",
	"FinderMainMenuCustom6": "script-finder-main_menu_custom6.xml",
}


def _menu_file():
	skin_path = xbmcvfs.translatePath("special://skin/")
	return os.path.join(skin_path, "xml", "Includes_MainMenu.xml")


def _menu_block(text):
	match = MENU_BLOCK_RE.search(text)
	if not match:
		raise ValueError("FinderMainMenuItems include was not found")
	return match


def _read_order(text):
	match = _menu_block(text)
	order = INCLUDE_RE.findall(match.group("content"))
	return [item for item in order if item in MENU_ITEMS]


def _write_order(path, text, order):
	match = _menu_block(text)
	indent = match.group("indent")
	item_indent = indent + "\t"
	lines = ['%s<include name="FinderMainMenuItems">' % indent]
	lines.extend('%s<include content="%s"/>' % (item_indent, item) for item in order)
	lines.append('%s</include>' % indent)
	replacement = "\n".join(lines)
	updated = text[:match.start()] + replacement + text[match.end():]
	with xbmcvfs.File(path, "w") as menu_file:
		menu_file.write(updated)


def _has_configured_menu_item(item):
	filename = CONFIGURED_MENU_FILES.get(item)
	if not filename:
		return True

	path = os.path.join(xbmcvfs.translatePath("special://skin/"), "xml", filename)
	try:
		with xbmcvfs.File(path) as menu_file:
			text = menu_file.read()
	except Exception as exc:
		xbmc.log("Finder Helper: Unable to inspect %s: %s" % (filename, exc), xbmc.LOGWARNING)
		return False

	compact = re.sub(r"\s+", "", text).lower()
	if "<item>" not in compact:
		return False
	if "<label>empty</label>" in compact:
		return False
	if "<visible>false</visible>" in compact:
		return False
	return True


def _get_menu_label(item):
	filename = CONFIGURED_MENU_FILES.get(item)
	if not filename:
		return MENU_ITEMS[item][0]

	path = os.path.join(xbmcvfs.translatePath("special://skin/"), "xml", filename)
	try:
		with xbmcvfs.File(path) as menu_file:
			text = menu_file.read()
	except Exception as exc:
		xbmc.log("Finder Helper: Unable to read label from %s: %s" % (filename, exc), xbmc.LOGWARNING)
		return MENU_ITEMS[item][0]

	match = LABEL_RE.search(text)
	if not match:
		return MENU_ITEMS[item][0]

	label = match.group(1).strip()
	if not label or label.lower() == "empty":
		return MENU_ITEMS[item][0]

	return label


def get_eligible_configurable_menu_types():
	configurable_types = {
		item: media_type
		for label, media_type, item in CONFIGURABLE_MENU_TYPES
	}

	try:
		with xbmcvfs.File(_menu_file()) as menu_file:
			menu_order = _read_order(menu_file.read())
	except Exception as exc:
		xbmc.log("Finder Helper: Unable to read configurable main menu order: %s" % exc, xbmc.LOGWARNING)
		menu_order = [item for label, media_type, item in CONFIGURABLE_MENU_TYPES]

	return [
		(_get_menu_label(item), configurable_types[item])
		for item in menu_order
		if item in configurable_types
		and xbmc.getCondVisibility(MENU_ITEMS[item][1])
		and _has_configured_menu_item(item)
	]


def _enabled_order(order):
	return [item for item in order if xbmc.getCondVisibility(MENU_ITEMS[item][1]) and _has_configured_menu_item(item)]


def _merge_enabled_order(full_order, enabled_order):
	enabled_items = set(enabled_order)
	enabled_iter = iter(enabled_order)
	return [next(enabled_iter) if item in enabled_items else item for item in full_order]


def _move(order, index, direction):
	target = index + direction
	if target < 0 or target >= len(order):
		return index
	order[index], order[target] = order[target], order[index]
	return target


def _save_and_reload(dialog, path, text, full_order, enabled_order):
	try:
		updated_order = _merge_enabled_order(full_order, enabled_order)
		_write_order(path, text, updated_order)
	except Exception as exc:
		xbmc.log("Finder Helper: Unable to save main menu order: %s" % exc, xbmc.LOGERROR)
		dialog.ok("Finder", "Unable to save the main menu order.")
		return
	xbmc.executebuiltin("ReloadSkin()")


def manage_main_menu_order():
	dialog = xbmcgui.Dialog()
	path = _menu_file()
	try:
		with xbmcvfs.File(path) as menu_file:
			text = menu_file.read()
		full_order = _read_order(text)
	except Exception as exc:
		xbmc.log("Finder Helper: Unable to read main menu order: %s" % exc, xbmc.LOGERROR)
		dialog.ok("Finder", "Unable to read the main menu order file.")
		return

	if len(full_order) != len(MENU_ITEMS):
		dialog.ok("Finder", "The main menu order file is incomplete.")
		return

	enabled_order = _enabled_order(full_order)
	if not enabled_order:
		dialog.ok("Finder", "No main menu items are currently enabled.")
		return

	original_enabled_order = list(enabled_order)
	selected = 0
	while True:
		labels = ["%d. %s" % (index + 1, _get_menu_label(item)) for index, item in enumerate(enabled_order)]
		selected = dialog.select("Manage main menu order", labels, preselect=selected)
		if selected < 0:
			if enabled_order != original_enabled_order:
				_save_and_reload(dialog, path, text, full_order, enabled_order)
			return

		action = dialog.select(_get_menu_label(enabled_order[selected]), ["Move up", "Move down"])
		if action == 0:
			selected = _move(enabled_order, selected, -1)
		elif action == 1:
			selected = _move(enabled_order, selected, 1)

def reset_main_menu_order(reload_skin=False):
	path = _menu_file()
	try:
		with xbmcvfs.File(path) as menu_file:
			text = menu_file.read()
		current_order = _read_order(text)
		if len(current_order) != len(DEFAULT_MENU_ORDER):
			raise ValueError("Main menu order file is incomplete")
		_write_order(path, text, DEFAULT_MENU_ORDER)
	except Exception as exc:
		xbmc.log("Finder Helper: Unable to reset main menu order: %s" % exc, xbmc.LOGERROR)
		return False
	if reload_skin:
		xbmc.executebuiltin("ReloadSkin()")
	return True

