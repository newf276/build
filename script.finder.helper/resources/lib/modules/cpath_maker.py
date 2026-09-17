# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcvfs
import json
import sqlite3 as database
import xml.etree.ElementTree as ET
from threading import Thread
from modules import xmls

dialog = xbmcgui.Dialog()
window = xbmcgui.Window(10000)
Listitem = xbmcgui.ListItem
max_widgets = 10
max_submenu_items = 8
max_topbar_custom_menu_items = 8

submenu_types = ("movie", "tvshow", "custom1", "custom2", "custom3", "custom4", "custom5", "custom6",)

submenu_include_names = {item: "%sSubmenu" % item.capitalize() for item in submenu_types}
submenu_xml_names = {item: "script-finder-submenu_%s" % item for item in submenu_types}

settings_path = xbmcvfs.translatePath("special://profile/addon_data/script.finder.helper/")
database_path = xbmcvfs.translatePath("special://profile/addon_data/script.finder.helper/cpath_cache.db")
(
    movies_widgets_xml,
    tvshows_widgets_xml,
    custom1_widgets_xml,
    custom2_widgets_xml,
    custom3_widgets_xml,
    custom4_widgets_xml,
    custom5_widgets_xml,
    custom6_widgets_xml,
) = (
    "script-finder-widget_movies",
    "script-finder-widget_tvshows",
    "script-finder-widget_custom1",
    "script-finder-widget_custom2",
    "script-finder-widget_custom3",
    "script-finder-widget_custom4",
    "script-finder-widget_custom5",
    "script-finder-widget_custom6",
)
(
    movies_main_menu_xml,
    tvshows_main_menu_xml,
    custom1_main_menu_xml,
    custom2_main_menu_xml,
    custom3_main_menu_xml,
    custom4_main_menu_xml,
    custom5_main_menu_xml,
    custom6_main_menu_xml,
) = (
    "script-finder-main_menu_movies",
    "script-finder-main_menu_tvshows",
    "script-finder-main_menu_custom1",
    "script-finder-main_menu_custom2",
    "script-finder-main_menu_custom3",
    "script-finder-main_menu_custom4",
    "script-finder-main_menu_custom5",
    "script-finder-main_menu_custom6",
)
default_xmls = {
    "movie.widget": (movies_widgets_xml, xmls.default_widget, "MovieWidgets"),
    "tvshow.widget": (tvshows_widgets_xml, xmls.default_widget, "TVShowWidgets"),
    "custom1.widget": (custom1_widgets_xml, xmls.default_widget, "Custom1Widgets"),
    "custom2.widget": (custom2_widgets_xml, xmls.default_widget, "Custom2Widgets"),
    "custom3.widget": (custom3_widgets_xml, xmls.default_widget, "Custom3Widgets"),
    "custom4.widget": (custom4_widgets_xml, xmls.default_widget, "Custom4Widgets"),
    "custom5.widget": (custom5_widgets_xml, xmls.default_widget, "Custom5Widgets"),
    "custom6.widget": (custom6_widgets_xml, xmls.default_widget, "Custom6Widgets"),
    
    "movie.main_menu": (movies_main_menu_xml, xmls.default_main_menu, "MoviesMainMenu"),
    "tvshow.main_menu": (tvshows_main_menu_xml, xmls.default_main_menu, "TVShowsMainMenu",),
    "custom1.main_menu": (custom1_main_menu_xml, xmls.default_main_menu, "Custom1MainMenu",),
    "custom2.main_menu": (custom2_main_menu_xml, xmls.default_main_menu, "Custom2MainMenu",),
    "custom3.main_menu": (custom3_main_menu_xml, xmls.default_main_menu, "Custom3MainMenu",),
    "custom4.main_menu": (custom4_main_menu_xml, xmls.default_main_menu, "Custom4MainMenu",),
    "custom5.main_menu": (custom5_main_menu_xml, xmls.default_main_menu, "Custom5MainMenu",),
    "custom6.main_menu": (custom6_main_menu_xml, xmls.default_main_menu, "Custom6MainMenu",),
}
main_include_dict = {
    "movie": {"main_menu": None, "widget": "MovieWidgets"},
    "tvshow": {"main_menu": None, "widget": "TVShowWidgets"},
    "custom1": {"main_menu": None, "widget": "Custom1Widgets"},
    "custom2": {"main_menu": None, "widget": "Custom2Widgets"},
    "custom3": {"main_menu": None, "widget": "Custom3Widgets"},
    "custom4": {"main_menu": None, "widget": "Custom4Widgets"},
    "custom5": {"main_menu": None, "widget": "Custom5Widgets"},
    "custom6": {"main_menu": None, "widget": "Custom6Widgets"},
}
widget_types = (
    ("Poster", "WidgetListPoster"),
    ("BigPoster", "WidgetListBigPoster"),
    ("Landscape", "WidgetListLandscape"),
    ("BigLandscape", "WidgetListBigLandscape"),
    ("LandscapeInfo", "WidgetListEpisodes"),
    ("BigLandscapeInfo", "WidgetListBigEpisodes"),
    ("Category", "WidgetListCategory"),
)
default_path = "finder://root"

FINDER_HELPER_ACTIONS = (
	("Import Configuration", "Import a Finder Plus configuration", "import_config"),
	("Export Configuration", "Export a Finder Plus configuration", "export_config"),
	("Backup Configuration", "Back up the current configuration", "backup_config"),
	("Restore Configuration", "Restore a backed-up configuration", "restore_config"),
	("Backup Favourites", "Back up Kodi favourites", "backup_favs"),
        ("Restore Favourites", "Restore Kodi favourites", "restore_favs"),
        ("Import Favourites", "Import Kodi favourites", "import_favs"),
        ("Export Favourites", "Export Kodi favourites", "export_favs"),
	("Backup GUI Settings", "Back up the current Kodi GUI settings", "backup_gui"),
	("Restore GUI Settings", "Restore backed-up Kodi GUI settings", "restore_gui"),
        ("Import GUI Settings", "Import GUI Settings", "import_gui"),
        ("Export GUI Settings", "Export GUI Settings", "export_gui"),
	("Restore Default GUI", "Restore the default Kodi GUI settings", "restore_gui_dflt"),
	("Restore Default Skin", "Restore the default Finder Plus settings", "restore_skin_dflt"),
	("Clear Packages", "Remove cached Kodi package files", "clear_pkgs"),
	("Clear Thumbnails", "Clear Kodi's thumbnail cache", "clear_thumbnails"),
        ("Search input", "Open the Finder search keyboard", "search_input"),
	("Change Background", "Choose a custom background image", "set_image"),
	("Change Logo", "Choose a custom logo image", "set_image_logo"),
	("Video Cache Configuration", "Configure Kodi video cache settings", "advanced_set"),
	("Set Backup Directory", "Choose the directory used for backups", "set_backup_directory"),
	("Force Close Kodi", "Force Kodi to close", "force_close"),
)

FINDER_DIALOGS = (
        ("Maintenance & Tools", 1106),
	("Authorize Services", 1111),
        ("Trakt", 1108),
	("Real-Debrid", 1113),
	("Premiumize", 1114),
	("All-Debrid", 1115),
	("TorBox", 1116),
	("OffCloud", 1117),
	("Maintenance", 1120),
        ("Custom Configs", 1126),
        ("Pre-Made Configs", 1158),
	("Clear Add-on Cache", 1122),
	("Backup & Restore", 1123),
	("Favourites Backup & Restore", 1155),
	("GUI Settings Backup & Restore", 1156),
	("Backup & Restore Configs", 1124),
	("Import & Export Configs", 1125),
        ("Restore Skin/GUI Defaults", 1157),
	("Manage Your Configs", 1126),
        ("Search", 1107),
	("Choose Look & Feel", 1152),
	("Choose Colour Preset", 1154),
)


def choose_finder_dialog():
	list_items = []

	for label, window_id in FINDER_DIALOGS:
		listitem = Listitem(label, "Open the %s dialog" % label, offscreen=True)
		listitem.setArt({"icon": "DefaultAddonProgram.png"})
		listitem.setProperty(
			"item",
			json.dumps({
				"label": label,
				"file": "ActivateWindow(%s)" % window_id,
				"thumbnail": "DefaultAddonProgram.png",
			}),
		)
		list_items.append(listitem)

	choice = dialog.select("Finder Dialogs", list_items, useDetails=True)
	if choice == -1:
		return {}

	return json.loads(list_items[choice].getProperty("item"))


def choose_finder_helper_action():
	list_items = []

	for label, description, mode in FINDER_HELPER_ACTIONS:
		listitem = Listitem(label, description, offscreen=True)
		listitem.setArt({"icon": "DefaultAddonProgram.png"})
		listitem.setProperty(
			"item",
			json.dumps({
				"label": label,
				"file": "RunScript(script.finder.helper,mode=%s)" % mode,
				"thumbnail": "DefaultAddonProgram.png",
			}),
		)
		list_items.append(listitem)

	choice = dialog.select("Finder Helper", list_items, useDetails=True)
	if choice == -1:
		return {}

	return json.loads(list_items[choice].getProperty("item"))



def is_favourites_path(path):
	return path in ("favourites://", "plugin://script.finder.helper/?mode=favourites_widget",)


def get_widget_content_path(path):
	if is_favourites_path(path):
		return "plugin://script.finder.helper/?mode=favourites_widget"
	return path


def is_builtin_action(value):
	value = str(value or "").strip()
	if not value or "(" not in value or not value.endswith(")"):
		return False

	action_name = value.split("(", 1)[0].replace(".", "").replace("_", "")
	return action_name.isalnum()


def is_valid_manual_entry(value, allow_actions=False):
	value_lower = str(value or "").strip().lower()

	allowed_prefixes = (
		"plugin://",
		"library://",
		"videodb://",
		"musicdb://",
		"special://",
		"sources://",
		"pvr://",
		"addons://",
		"androidapp://",
		"favourites://",
	)

	if value_lower.startswith(allowed_prefixes):
		return True

	return bool(allow_actions and is_builtin_action(value_lower))


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def show_busy_dialog():
    return xbmc.executebuiltin("ActivateWindow(busydialognocancel)")


def hide_busy_dialog():
    xbmc.executebuiltin("Dialog.Close(busydialognocancel)")
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    
def get_main_menu_icon(media_type):
    skin_keys = {
        "movie": "movie.main_menu_icon",
        "tvshow": "tvshow.main_menu_icon",
        "custom1": "custom1.main_menu_icon",
        "custom2": "custom2.main_menu_icon",
        "custom3": "custom3.main_menu_icon",
        "custom4": "custom4.main_menu_icon",
        "custom5": "custom5.main_menu_icon",
        "custom6": "custom6.main_menu_icon",
    }
    default_icons = {
        "movie": "icons/sidemenu/movies.png",
        "tvshow": "icons/sidemenu/tv.png",
        "custom1": "icons/sidemenu/tv.png",
        "custom2": "icons/sidemenu/tv.png",
        "custom3": "icons/sidemenu/tv.png",
        "custom4": "icons/sidemenu/tv.png",
        "custom5": "icons/sidemenu/tv.png",
        "custom6": "icons/sidemenu/tv.png",
    }

    key = skin_keys.get(media_type)
    value = xbmc.getInfoLabel("Skin.String(%s)" % key) if key else ""
    if not value:
        value = default_icons.get(media_type, "")
    return value


def get_activate_window(path):
	if not path or path == "noop":
		return "noop"

	path = str(path).strip()
	path_lower = path.lower()

	if is_builtin_action(path):
		return path

	if path_lower.startswith(("musicdb://", "library://music")):
		return "ActivateWindow(Music,%s,return)" % path

	if path_lower.startswith("pvr://tv"):
		return "ActivateWindow(TV,%s,return)" % path

	if path_lower.startswith("pvr://radio"):
		return "ActivateWindow(Radio,%s,return)" % path

	if path_lower.startswith(("addons://", "androidapp://")):
		return "ActivateWindow(AddonBrowser,%s,return)" % path

	if path_lower.startswith("sources://music"):
		return "ActivateWindow(Music,%s,return)" % path

	if path_lower.startswith(("plugin://", "videodb://", "library://video", "sources://video", "special://videoplaylists")):
		return "ActivateWindow(Videos,%s,return)" % path

	return "ActivateWindow(Videos,%s,return)" % path


def get_home_menu_disabled_setting(media_type):
	visible_settings = {
		"movie": "HomeMenuNoMoviesButton",
		"tvshow": "HomeMenuNoTVShowsButton",
		"custom1": "HomeMenuNoCustom1Button",
		"custom2": "HomeMenuNoCustom2Button",
		"custom3": "HomeMenuNoCustom3Button",
		"custom4": "HomeMenuNoCustom4Button",
		"custom5": "HomeMenuNoCustom5Button",
		"custom6": "HomeMenuNoCustom6Button",
	}
	return visible_settings.get(media_type)


def home_menu_disabled(media_type):
	visible_setting = get_home_menu_disabled_setting(media_type)
	return bool(visible_setting and xbmc.getCondVisibility("Skin.HasSetting(%s)" % visible_setting))


def get_plugin_addon_id(path):
	if not path or not path.startswith("plugin://"):
		return ""
	try:
		return path.split("/")[2]
	except:
		return ""


def get_widget_addon_visible_condition(path):
	addon_id = get_plugin_addon_id(path)
	if not addon_id:
		return ""
	return "System.HasAddon(%s)" % addon_id


def add_widget_addon_visible_condition(body, visible_condition):
	if not visible_condition:
		return body
	return body.replace('<include content="', '<include condition="%s" content="' % visible_condition, 1)

# -------------------------------------------------
# DIRECTORY HELPER
# -------------------------------------------------
def get_favourites_directory():
	favourites_file = "special://profile/favourites.xml"
	if not xbmcvfs.exists(favourites_file):
		return []

	try:
		with xbmcvfs.File(favourites_file, "r") as xml_file:
			xml_data = xml_file.read()

		root = ET.fromstring(xml_data)
	except Exception:
		return []

	results = []
	for favourite in root.findall("favourite"):
		action = str(favourite.text or "").strip()
		if not action:
			continue

		label = favourite.get("name") or "Favourite"
		thumbnail = favourite.get("thumb") or "DefaultFavourites.png"
		results.append({
			"label": label,
			"file": action,
			"thumbnail": thumbnail,
			"filetype": "action",
		})

	return results


def files_get_directory(directory, properties=["title", "file", "thumbnail"]):
    if directory == "favourites://":
        return get_favourites_directory()

    if directory == "finder://root":
        return [
            {"label": "Video add-ons", "file": "addons://sources/video/", "thumbnail": "DefaultAddon.png", "filetype": "directory"},
            {"label": "Programs", "file": "addons://sources/executable/", "thumbnail": "DefaultAddon.png", "filetype": "directory"},
            {"label": "Skin playlists", "file": "special://skin/playlists/", "thumbnail": "DefaultPlaylist.png", "filetype": "directory"},
            {"label": "User playlists", "file": "special://profile/playlists/", "thumbnail": "DefaultPlaylist.png", "filetype": "directory"},
            {"label": "Video library", "file": "library://video/", "thumbnail": "DefaultFolder.png", "filetype": "directory"},
            {"label": "Video sources", "file": "sources://video/", "thumbnail": "DefaultFolder.png", "filetype": "directory"},
            {"label": "Music add-ons", "file": "addons://sources/audio/", "thumbnail": "DefaultAddon.png", "filetype": "directory"},
            {"label": "Music library", "file": "library://music/", "thumbnail": "DefaultMusicAlbums.png", "filetype": "directory"},
            {"label": "Music sources", "file": "sources://music/", "thumbnail": "DefaultFolder.png", "filetype": "directory"},
            {"label": "Pictures", "file": "sources://pictures/", "thumbnail": "DefaultPicture.png", "filetype": "directory"},
            {"label": "Live TV", "file": "pvr://tv/", "thumbnail": "DefaultTVShows.png", "filetype": "directory"},
            {"label": "Radio", "file": "pvr://radio/", "thumbnail": "DefaultMusicSongs.png", "filetype": "directory"},
            {"label": "Favourites", "file": "favourites://", "thumbnail": "DefaultFavourites.png", "filetype": "directory"},
        ]

    if directory == "library://video/":
        return [
            {"label": "Movies", "file": "videodb://movies/", "thumbnail": "DefaultMovies.png", "filetype": "directory"},
            {"label": "TV shows", "file": "videodb://tvshows/", "thumbnail": "DefaultTVShows.png", "filetype": "directory"},
            {"label": "Music videos", "file": "videodb://musicvideos/", "thumbnail": "DefaultMusicVideos.png", "filetype": "directory"},
            {"label": "Recently added movies", "file": "videodb://recentlyaddedmovies/", "thumbnail": "DefaultFolder.png", "filetype": "directory"},
            {"label": "Recently added episodes", "file": "videodb://recentlyaddedepisodes/", "thumbnail": "DefaultFolder.png", "filetype": "directory"},
            {"label": "In-progress TV shows", "file": "videodb://inprogresstvshows", "thumbnail": "DefaultFolder.png", "filetype": "directory"},
        ]

    if directory == "library://music/":
        return [
            {"label": "Genres", "file": "musicdb://genres/", "thumbnail": "DefaultMusicGenres.png", "filetype": "directory"},
            {"label": "Artists", "file": "musicdb://artists/", "thumbnail": "DefaultMusicArtists.png", "filetype": "directory"},
            {"label": "Albums", "file": "musicdb://albums/", "thumbnail": "DefaultMusicAlbums.png", "filetype": "directory"},
            {"label": "Songs", "file": "musicdb://songs/", "thumbnail": "DefaultMusicSongs.png", "filetype": "directory"},
            {"label": "Top 100", "file": "musicdb://top100/", "thumbnail": "DefaultMusicTop100.png", "filetype": "directory"},
            {"label": "Recently added albums", "file": "musicdb://recentlyaddedalbums/", "thumbnail": "DefaultMusicRecentlyAdded.png", "filetype": "directory"},
            {"label": "Recently played albums", "file": "musicdb://recentlyplayedalbums/", "thumbnail": "DefaultMusicRecentlyPlayed.png", "filetype": "directory"},
            {"label": "Compilations", "file": "musicdb://compilations/", "thumbnail": "DefaultMusicCompilations.png", "filetype": "directory"},
            {"label": "Years", "file": "musicdb://years/", "thumbnail": "DefaultMusicYears.png", "filetype": "directory"},
            {"label": "Singles", "file": "musicdb://singles/", "thumbnail": "DefaultMusicSongs.png", "filetype": "directory"},
        ]

    allowed_prefixes = (
        "plugin://",
        "library://",
        "videodb://",
        "musicdb://",
        "special://",
        "sources://",
        "pvr://",
        "addons://",
        "androidapp://",
        "favourites://",
    )

    command = {"jsonrpc": "2.0", "id": "Finder", "method": "Files.GetDirectory", "params": {"directory": directory, "media": "files", "properties": properties,},}

    try:
        files = get_jsonrpc(command).get("files", [])
        results = [i for i in files if i.get("file", "").startswith(allowed_prefixes) and (i.get("filetype") == "directory" or i.get("file", "").lower().endswith(".xsp"))]
    except:
        results = None

    return results


def get_jsonrpc(request):
    response = xbmc.executeJSONRPC(json.dumps(request))
    result = json.loads(response)
    return result.get("result", None)

# -------------------------------------------------
# CUSTOM PATH MANAGER
# -------------------------------------------------
class CPaths:

    def __init__(self, cpath_setting):
        self.connect_database()
        self.cpath_setting = cpath_setting
        self.cpath_lookup = "'%s'" % (self.cpath_setting + "%")
        self.media_type, self.path_type = self.cpath_setting.split(".", 1)
        if self.path_type == "submenu":
            self.main_include = submenu_include_names.get(self.media_type)
        elif self.cpath_setting == "topbar.custom_menu":
            self.main_include = "TopBarCustomMenuItems"
        else:
            self.main_include = main_include_dict[self.media_type][self.path_type]
        self.refresh_cpaths, self.last_cpath = False, None

    def connect_database(self):
        if not xbmcvfs.exists(settings_path):
            xbmcvfs.mkdir(settings_path)
        self.dbcon = database.connect(database_path, timeout=20)
        self.dbcon.execute("CREATE TABLE IF NOT EXISTS custom_paths (cpath_setting text unique, cpath_path text, cpath_header text, cpath_type text, cpath_label text)")
        self.dbcur = self.dbcon.cursor()

    def add_cpath_to_database(self, cpath_setting, cpath_path, cpath_header, cpath_type, cpath_label):
        self.refresh_cpaths = True
        self.dbcur.execute("INSERT OR REPLACE INTO custom_paths VALUES (?, ?, ?, ?, ?)", (cpath_setting, cpath_path, cpath_header, cpath_type, cpath_label))
        self.dbcon.commit()

    def update_cpath_in_database(self, cpath_setting, cpath_path, cpath_header, cpath_type, cpath_label):
        self.refresh_cpaths = True
        self.dbcur.execute(
            "UPDATE custom_paths SET cpath_path = ?, cpath_header = ?, cpath_type = ?, cpath_label = ? WHERE cpath_setting = ?",
            (cpath_path, cpath_header, cpath_type, cpath_label, cpath_setting),
        )
        self.dbcon.commit()

    def remove_cpath_from_database(self, cpath_setting):
        self.refresh_cpaths = True
        self.dbcur.execute("DELETE FROM custom_paths WHERE cpath_setting = ?", (cpath_setting,))
        self.dbcon.commit()

    def fetch_current_cpaths(self):
        results = self.dbcur.execute("SELECT * FROM custom_paths WHERE cpath_setting LIKE %s" % self.cpath_lookup).fetchall()
        try:
            results.sort(key=lambda k: int(k[0].split(".")[-1]))
        except:
            pass

        current_dict = {}
        for item in results:
            try:
                key = int(item[0].split(".")[-1])
            except:
                key = item[0]

            current_dict[key] = {
                "cpath_setting": item[0],
                "cpath_path": item[1],
                "cpath_header": item[2],
                "cpath_type": item[3],
                "cpath_label": item[4],
            }

        return current_dict

    def fetch_one_cpath(self, cpath_setting):
        result = self.dbcur.execute("SELECT * FROM custom_paths WHERE cpath_setting = ?", (cpath_setting,)).fetchone()
        if result is None:
            return None

        return {
            "cpath_setting": result[0],
            "cpath_path": result[1],
            "cpath_header": result[2],
            "cpath_type": result[3],
            "cpath_label": result[4],
        }


    # -------------------------------------------------
    # PATH BROWSING
    # -------------------------------------------------
    def path_browser(self, label="", file=default_path, thumbnail="", allow_no_path=False, allow_actions=False, allow_dialogs=False):
        show_busy_dialog()
        label = self.clean_header(label)
        results = files_get_directory(file)
        hide_busy_dialog()

        list_items = []

        # Only show "No Path" when we're using this for main menu paths
        if allow_no_path and file == default_path:
            no_path_item = Listitem("[COLOR dodgerblue]-- No Path --[/COLOR]", "Disable action / use no path", offscreen=True)
            no_path_item.setArt({"icon": ""})
            no_path_item.setProperty("item", json.dumps({"label": "No Path", "file": "noop", "thumbnail": ""}))
            list_items.append(no_path_item)

        if file != default_path:
            listitem = Listitem("Use [COLOR dodgerblue]%s[/COLOR] as path" % label, "Set as path", offscreen=True)
            listitem.setArt({"icon": thumbnail})
            listitem.setProperty("item", json.dumps({"label": label, "file": file, "thumbnail": thumbnail}))
            list_items.append(listitem)

        for i in results or []:
            stripped_label = i["label"].replace("[B]", "").replace("[/B]", "")
            while "[COLOR" in stripped_label:
                start = stripped_label.find("[COLOR")
                end = stripped_label.find("]", start) + 1
                stripped_label = stripped_label[:start] + stripped_label[end:]
            stripped_label = stripped_label.replace("[/COLOR]", "")

            is_action = i.get("filetype") == "action"
            item_label = stripped_label if is_action else "%s »" % stripped_label
            item_description = "Use favourite" if is_action else "Browse path..."

            listitem = Listitem(item_label, item_description, offscreen=True)
            listitem.setArt({"icon": i["thumbnail"]})
            listitem.setProperty("item", json.dumps({
                "label": i["label"],
                "file": i["file"],
                "thumbnail": i["thumbnail"],
                "filetype": i.get("filetype", "directory"),
            }))
            list_items.append(listitem)

        if file == default_path:
            if allow_dialogs:
                helper_item = Listitem("Finder Helper", "Choose a Finder Helper action", offscreen=True)
                helper_item.setArt({"icon": "DefaultAddonProgram.png"})
                helper_item.setProperty("item", json.dumps({
                    "label": "Finder Helper",
                    "file": "__finder_helper__",
                    "thumbnail": "DefaultAddonProgram.png",
                }))
                list_items.append(helper_item)

                dialogs_item = Listitem("Finder Dialogs", "Choose a Finder dialog", offscreen=True)
                dialogs_item.setArt({"icon": "DefaultAddonProgram.png"})
                dialogs_item.setProperty("item", json.dumps({
                    "label": "Finder Dialogs",
                    "file": "__finder_dialogs__",
                    "thumbnail": "DefaultAddonProgram.png",
                }))
                list_items.append(dialogs_item)

            manual_item = Listitem("Enter path manually", "Type a Kodi path or built-in action", offscreen=True)
            manual_item.setArt({"icon": "DefaultKeyboard.png"})
            manual_item.setProperty("item", json.dumps({"label": "Manual entry", "file": "__manual_entry__", "thumbnail": ""}))
            list_items.append(manual_item)

        choice = dialog.select("Choose path", list_items, useDetails=True)
        if choice == -1:
            return {}

        choice = json.loads(list_items[choice].getProperty("item"))

        # If user chose "No Path", just return that directly
        if choice["file"] == "noop":
            return choice

        if choice.get("filetype") == "action":
            if not allow_actions:
                dialog.ok("Favourites", "Individual favourites cannot be used as widget paths.")
                return self.path_browser(label=label, file=file, thumbnail=thumbnail, allow_no_path=allow_no_path, allow_actions=allow_actions, allow_dialogs=allow_dialogs)
            return choice

        if choice["file"] == "__finder_helper__":
            if not allow_actions:
                dialog.ok("Finder Helper", "Finder Helper actions cannot be used for widgets.")
                return self.path_browser(label=label, file=file, thumbnail=thumbnail, allow_no_path=allow_no_path, allow_actions=allow_actions, allow_dialogs=allow_dialogs)

            helper_action = choose_finder_helper_action()
            if helper_action:
                return helper_action

            return self.path_browser(label=label, file=file, thumbnail=thumbnail, allow_no_path=allow_no_path, allow_actions=allow_actions, allow_dialogs=allow_dialogs)

        if choice["file"] == "__finder_dialogs__":
            dialog_action = choose_finder_dialog()
            if dialog_action:
                return dialog_action

            return self.path_browser(label=label, file=file, thumbnail=thumbnail, allow_no_path=allow_no_path, allow_actions=allow_actions, allow_dialogs=allow_dialogs)

        if choice["file"] == "__manual_entry__":
            heading = "Enter Kodi path or action" if allow_actions else "Enter Kodi path"
            manual_entry = dialog.input(heading, type=xbmcgui.INPUT_ALPHANUM).strip()

            if not manual_entry:
                return {}

            if not is_valid_manual_entry(manual_entry, allow_actions=allow_actions):
                example = (
                    "Enter a valid Kodi path or one of these actions:[CR][CR]"
                    "[COLOR gold]ActivateWindow(...)[/COLOR][CR]"
                    "[COLOR gold]RunScript(...)[/COLOR]"
                    if allow_actions else
                    "Enter a valid Kodi directory path such as:[CR][CR]"
                    "[COLOR gold]plugin://plugin.video.example/[/COLOR]"
                )
                dialog.ok("Invalid Entry", example)
                return self.path_browser(label=label, file=file, thumbnail=thumbnail, allow_no_path=allow_no_path, allow_actions=allow_actions, allow_dialogs=allow_dialogs)

            return {
                "label": manual_entry,
                "file": manual_entry,
                "thumbnail": "",
            }

        if choice["file"] == file:
            return choice

        return self.path_browser(label=choice["label"], file=choice["file"], thumbnail=choice["thumbnail"], allow_no_path=allow_no_path, allow_actions=allow_actions, allow_dialogs=allow_dialogs)


    # -------------------------------------------------
    # GENERATE XMLs
    # -------------------------------------------------
    def make_main_menu_xml(self, active_cpaths, reload_skin=True):
        if not self.refresh_cpaths:
            return
        if not active_cpaths:
            self.make_default_xml()
            return
        media_types = {
            "movie": (movies_main_menu_xml, xmls.main_menu_movies_xml, "movie.main_menu",),
            "tvshow": (tvshows_main_menu_xml, xmls.main_menu_tvshows_xml, "tvshow.main_menu",),
            "custom1": (custom1_main_menu_xml, xmls.main_menu_custom1_xml, "custom1.main_menu",),
            "custom2": (custom2_main_menu_xml, xmls.main_menu_custom2_xml, "custom2.main_menu",),
            "custom3": (custom3_main_menu_xml, xmls.main_menu_custom3_xml, "custom3.main_menu",),
            "custom4": (custom4_main_menu_xml, xmls.main_menu_custom4_xml, "custom4.main_menu",),
            "custom5": (custom5_main_menu_xml, xmls.main_menu_custom5_xml, "custom5.main_menu",),
            "custom6": (custom6_main_menu_xml, xmls.main_menu_custom6_xml, "custom6.main_menu",),
        }
        media_values = media_types.get(self.media_type)
        if not media_values:
            return
        if home_menu_disabled(self.media_type):
            self.make_default_xml(reload_skin=reload_skin)
            return
        menu_xml_file, main_menu_xml, key = media_values
        xml_file = "special://skin/xml/%s.xml" % (menu_xml_file)
        main_menu_icon = get_main_menu_icon(self.media_type)

        cpath_entry = active_cpaths[key]
        main_menu_path = cpath_entry["cpath_path"]

        main_menu_onclick = get_activate_window(main_menu_path)

        final_format = main_menu_xml.format(main_menu_path=main_menu_path, main_menu_onclick=main_menu_onclick, cpath_header=cpath_entry.get("cpath_header", ""), main_menu_icon=main_menu_icon,)

        visible_settings = {
                "movie": "HomeMenuNoMoviesButton",
                "tvshow": "HomeMenuNoTVShowsButton",
                "custom1": "HomeMenuNoCustom1Button",
                "custom2": "HomeMenuNoCustom2Button",
                "custom3": "HomeMenuNoCustom3Button",
                "custom4": "HomeMenuNoCustom4Button",
                "custom5": "HomeMenuNoCustom5Button",
                "custom6": "HomeMenuNoCustom6Button",
        }

        visible_setting = visible_settings.get(self.media_type)

        if visible_setting:
                final_format = final_format.replace("<visible>Skin.HasSetting(%s)</visible>" % visible_setting, "<visible>!Skin.HasSetting(%s)</visible>" % visible_setting)

        if "&amp;" not in final_format:
            final_format = final_format.replace("&", "&amp;")
        self.write_xml(xml_file, final_format, reload_skin=reload_skin)
        self.update_skin_strings()

    def make_widget_xml(self, active_cpaths, reload_skin=True):
        if not self.refresh_cpaths:
            return
        if not active_cpaths:
            self.make_default_xml()
            return
        media_type_to_xml = {
            "movie": movies_widgets_xml,
            "tvshow": tvshows_widgets_xml,
            "custom1": custom1_widgets_xml,
            "custom2": custom2_widgets_xml,
            "custom3": custom3_widgets_xml,
            "custom4": custom4_widgets_xml,
            "custom5": custom5_widgets_xml,
            "custom6": custom6_widgets_xml,
        }
        xml_filename = media_type_to_xml.get(self.media_type)
        xml_file = "special://skin/xml/%s.xml" % xml_filename
        media_type_id = {
            "movie": 19010,
            "tvshow": 22010,
            "custom1": 23010,
            "custom2": 24010,
            "custom3": 25010,
            "custom4": 26010,
            "custom5": 27010,
            "custom6": 28010,
        }
        list_id = media_type_id.get(self.media_type)
        if home_menu_disabled(self.media_type):
            self.make_default_xml(reload_skin=reload_skin)
            return
        final_format = xmls.media_xml_start.format(main_include=self.main_include)
        favourites_added = False
        duplicate_favourites = []
        for k, v in active_cpaths.items():
            original_path = v["cpath_path"]
            if is_favourites_path(original_path):
                if favourites_added:
                    duplicate_favourites.append(v["cpath_setting"])
                    continue
                favourites_added = True
            cpath_list_id = list_id + k
            cpath_path, cpath_header, cpath_type, cpath_label = (get_widget_content_path(original_path), v["cpath_header"], v["cpath_type"], v["cpath_label"],)
            body = (xmls.stacked_media_xml_body if "Stacked" in cpath_label else xmls.media_xml_body)
            body = body.format(cpath_type=cpath_type, cpath_path=cpath_path, cpath_header=cpath_header, cpath_list_id=cpath_list_id,)
            body = add_widget_addon_visible_condition(body, get_widget_addon_visible_condition(cpath_path))
            if "&amp;" not in body:
                final_format += body.replace("&", "&amp;")
        final_format += xmls.media_xml_end
        for cpath_setting in duplicate_favourites:
            self.remove_cpath_from_database(cpath_setting)
        self.write_xml(xml_file, final_format, reload_skin=reload_skin)

    def write_xml(self, xml_file, final_format, reload_skin=True):
        with xbmcvfs.File(xml_file, "w") as f:
            f.write(final_format)
        if reload_skin:
            Thread(target=self.reload_skin).start()

    # -------------------------------------------------
    # MENU, WIDGET, AND SUBMENU MANAGEMENT
    # -------------------------------------------------
    def handle_path_browser_results(self, cpath_setting, context):
        result = self.path_browser(allow_no_path=(context == "main_menu"), allow_actions=(context in ("main_menu", "submenu")))
        if not result:
            return None
        cpath_path = result.get("file", None)
        if not cpath_path:
            return None
        default_header = result.get("label", None)
        if context == "widget":
            cpath_header = self.widget_header(default_header)
            if not cpath_header:
                return None
            self.create_and_update_widget(cpath_setting, cpath_path, cpath_header)
        else:
            cpath_header = self.main_menu_header(default_header)
            if not cpath_header:
                return None
            self.add_cpath_to_database(cpath_setting, cpath_path, cpath_header, "", "")
            self.update_skin_strings()
        return True

    def manage_action_and_check(self, cpath_setting, context):
        action_choice = self.manage_action(cpath_setting, context)
        if action_choice == "clear_path":
            self.make_default_xml()
            dialog.ok("Finder", "Path cleared")
            return None
        if action_choice is None:
            return None
        return True

    def manage_main_menu_path(self):
        active_cpaths = self.fetch_current_cpaths()
        if active_cpaths and not self.manage_action_and_check(self.cpath_setting, "main_menu"):
            return
        if not self.handle_path_browser_results(self.cpath_setting, "main_menu"):
            return self.make_main_menu_xml(active_cpaths)
        self.make_main_menu_xml(self.fetch_current_cpaths())

    def manage_widgets(self):
        active_cpaths = self.fetch_current_cpaths()
        widget_choices = ["Widget %s : %s" % (count, active_cpaths.get(count, {}).get("cpath_label", "")) for count in range(1, 11)]
        choice = dialog.select("Choose widget", widget_choices)
        if choice == -1:
            return self.make_widget_xml(active_cpaths)
        active_cpath_check = choice + 1
        if active_cpath_check in active_cpaths:
            cpath_setting = active_cpaths[active_cpath_check]["cpath_setting"]
            if not self.manage_action_and_check(cpath_setting, "widget"):
                return self.manage_widgets()
        else:
            cpath_setting = "%s.%s" % (self.cpath_setting, active_cpath_check)
        if not self.handle_path_browser_results(cpath_setting, "widget"):
            return self.manage_widgets()
        return self.manage_widgets()

    def make_submenu_xml(self, active_cpaths, reload_skin=True):
        if not self.refresh_cpaths:
            return
        xml_name = submenu_xml_names.get(self.media_type)
        include_name = submenu_include_names.get(self.media_type)
        if not xml_name or not include_name:
            return
        xml_file = "special://skin/xml/%s.xml" % xml_name
        final_format = xmls.submenu_xml_start.format(include_name=include_name)
        for key in sorted(active_cpaths):
            item = active_cpaths[key]
            submenu_path = item.get("cpath_path", "")
            submenu_label = item.get("cpath_header", "")
            body = xmls.submenu_xml_body.format(submenu_label=submenu_label, submenu_onclick=get_activate_window(submenu_path),)
            if "&amp;" not in body:
                body = body.replace("&", "&amp;")
            final_format += body
        final_format += xmls.submenu_xml_end
        submenu_setting = "Finder.Submenu.%s" % self.media_type
        if active_cpaths:
            xbmc.executebuiltin("Skin.SetBool(%s)" % submenu_setting)
        else:
            xbmc.executebuiltin("Skin.Reset(%s)" % submenu_setting)
        self.write_xml(xml_file, final_format, reload_skin=reload_skin)

    def manage_submenu(self):
        active_cpaths = self.fetch_current_cpaths()
        submenu_choices = ["Submenu %s : %s" % (count, active_cpaths.get(count, {}).get("cpath_header", "")) for count in range(1, max_submenu_items + 1)]
        choice = dialog.select("Choose submenu item", submenu_choices)
        if choice == -1:
            return self.make_submenu_xml(active_cpaths)

        position = choice + 1
        cpath_setting = "%s.%s" % (self.cpath_setting, position)
        if position in active_cpaths:
            self.manage_action(cpath_setting, "submenu")
        else:
            result = self.path_browser(allow_actions=True, allow_dialogs=True)
            if result:
                label = dialog.input("Set submenu label", defaultt=result.get("label", ""))
                if label:
                    self.add_cpath_to_database(cpath_setting, result.get("file", ""), label, "", "")

        self.make_submenu_xml(self.fetch_current_cpaths())
        return self.manage_submenu()

    def make_topbar_custom_menu_xml(self, active_cpaths, reload_skin=True, topbar_icon=None):
        xml_file = "special://skin/xml/script-finder-topbar_custom_menu.xml"
        topbar_icon = topbar_icon or xbmc.getInfoLabel("Skin.String(TopBarCustomMenuIcon)") or "icons/system.png"
        topbar_icon = topbar_icon.replace("&", "&amp;")
        final_format = xmls.topbar_custom_menu_xml_start.format(topbar_icon=topbar_icon)
        dialog_helper_modes = {
            "open_search_dialog": 1107,
            "open_trakt_authorization_dialog": 1108,
            "open_authorization_dialog": 1111,
            "open_realdebrid_authorization_dialog": 1113,
            "open_premiumize_authorization_dialog": 1114,
            "open_alldebrid_authorization_dialog": 1115,
            "open_torbox_authorization_dialog": 1116,
            "open_offcloud_authorization_dialog": 1117,
            "open_maintenance_dialog": 1120,
            "open_addon_cache_dialog": 1122,
            "choose_lookfeel": 1152,
            "choose_color": 1154,
            "pre_config": 1158,
        }

        for key in sorted(active_cpaths):
            item = active_cpaths[key]
            menu_path = item.get("cpath_path", "")
            menu_label = item.get("cpath_header", "")
            dialog_id = next((window_id for mode, window_id in dialog_helper_modes.items() if menu_path == "RunScript(script.finder.helper,mode=%s)" % mode), None)
            # Direct dialog paths returned by the Finder Dialogs chooser.
            if dialog_id is None and menu_path.startswith("ActivateWindow(") and menu_path.endswith(")"):
                window_id = menu_path[len("ActivateWindow("):-1].strip()
                if window_id.isdigit():
                    dialog_id = int(window_id)
            menu_close = "<onclick>Dialog.Close(all)</onclick>"

            if dialog_id:
                menu_close = (
                    "<onclick>SetProperty(Finder.DirectDialog%s,true,home)</onclick>\n"
                    "\t\t\t<onclick>Dialog.Close(1170)</onclick>"
                ) % dialog_id

            body = xmls.topbar_custom_menu_xml_body.format(menu_label=menu_label, menu_close=menu_close, menu_onclick=get_activate_window(menu_path))
            if "&amp;" not in body:
                body = body.replace("&", "&amp;")
            final_format += body

        final_format += xmls.topbar_custom_menu_xml_end
        self.write_xml(xml_file, final_format, reload_skin=reload_skin)

    def set_topbar_custom_menu_heading(self):
        current_heading = xbmc.getInfoLabel("Skin.String(TopBarCustomMenuLabel)") or "Custom Menu"
        heading = dialog.input("Set custom dialog heading", defaultt=current_heading).strip()
        if not heading:
            return
        xbmc.executebuiltin("Skin.SetString(TopBarCustomMenuLabel,%s)" % heading)

    def manage_topbar_custom_menu_icon(self):
        default_icon = "icons/system.png"

        choices = [
            "Set / change icon",
            "Restore default icon",
        ]
        choice = dialog.select("Custom menu icon", choices)
        if choice == -1:
            return

        if choice == 0:
            last_folder = xbmc.getInfoLabel("Skin.String(finder.last_icon_folder)")
            if not last_folder or not xbmcvfs.exists(last_folder):
                last_folder = "special://skin/extras/topbar/"

            icon = dialog.browse(2, "Select custom menu icon", "pictures", ".png|.jpg|.jpeg|.gif|.tbn", False, False, last_folder)
            if not icon or not icon.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".tbn")):
                return

            xbmc.executebuiltin("Skin.SetString(finder.last_icon_folder,%s)" % (icon.rsplit("/", 1)[0] + "/"))
            xbmc.executebuiltin("Skin.SetString(TopBarCustomMenuIcon,%s)" % icon)
            self.make_topbar_custom_menu_xml(self.fetch_current_cpaths(), topbar_icon=icon)
            return

        xbmc.executebuiltin("Skin.SetString(TopBarCustomMenuIcon,%s)" % default_icon)
        self.make_topbar_custom_menu_xml(self.fetch_current_cpaths(), topbar_icon=default_icon)

    def manage_topbar_custom_menu(self):
        active_cpaths = self.fetch_current_cpaths()
        menu_choices = ["Custom menu %s : %s" % (count, active_cpaths.get(count, {}).get("cpath_header", "")) for count in range(1, max_topbar_custom_menu_items + 1)]

        choice = dialog.select("Manage custom menu", menu_choices)
        if choice == -1:
            return

        position = choice + 1
        cpath_setting = "%s.%s" % (self.cpath_setting, position)

        if position in active_cpaths:
            self.manage_action(cpath_setting, "topbar_custom_menu")
        else:
            result = self.path_browser(allow_actions=True, allow_dialogs=True)
            if result:
                label = dialog.input("Set custom menu label", defaultt=result.get("label", ""))
                if label:
                    self.add_cpath_to_database(cpath_setting, result.get("file", ""), label, "", "")

        if self.refresh_cpaths:
            self.make_topbar_custom_menu_xml(self.fetch_current_cpaths())

        return self.manage_topbar_custom_menu()

    # -------------------------------------------------
    # WIDGET CONFIGURATION
    # -------------------------------------------------
    def widget_header(self, default_header):
        header = dialog.input("Set widget label", defaultt=default_header)
        return header or None

    def main_menu_header(self, default_header):
        header = dialog.input("Set Main Menu label", defaultt=default_header)
        return header or None

    def get_widget_type(self, cpath_type):
        for widget_type, widget_list_type in widget_types:
            if widget_list_type == cpath_type:
                return widget_type
            elif "Stacked" in cpath_type and widget_list_type in cpath_type:
                return widget_type
        return None

    def widget_type(self, label="Choose widget display type", type_limit=7, cpath_path=None):
        available_widget_types = (widget_types[0:2] if is_favourites_path(cpath_path) else widget_types[0:type_limit])
        choice = dialog.select(label, [i[0] for i in available_widget_types])
        if choice == -1:
            return None
        return available_widget_types[choice]

    # -------------------------------------------------
    # SKIN SETTINGS AND ACTIONS
    # -------------------------------------------------
    def update_skin_strings(self):
        movie_cpath = self.fetch_one_cpath("movie.main_menu")
        tvshow_cpath = self.fetch_one_cpath("tvshow.main_menu")
        custom1_cpath = self.fetch_one_cpath("custom1.main_menu")
        custom2_cpath = self.fetch_one_cpath("custom2.main_menu")
        custom3_cpath = self.fetch_one_cpath("custom3.main_menu")
        custom4_cpath = self.fetch_one_cpath("custom4.main_menu")
        custom5_cpath = self.fetch_one_cpath("custom5.main_menu")
        custom6_cpath = self.fetch_one_cpath("custom6.main_menu")
        
        movie_cpath_header = movie_cpath.get("cpath_header") if movie_cpath else None
        tvshow_cpath_header = tvshow_cpath.get("cpath_header") if tvshow_cpath else None
        custom1_cpath_header = (custom1_cpath.get("cpath_header") if custom1_cpath else None)
        custom2_cpath_header = (custom2_cpath.get("cpath_header") if custom2_cpath else None)
        custom3_cpath_header = (custom3_cpath.get("cpath_header") if custom3_cpath else None)
        custom4_cpath_header = (custom4_cpath.get("cpath_header") if custom4_cpath else None)
        custom5_cpath_header = (custom5_cpath.get("cpath_header") if custom5_cpath else None)
        custom6_cpath_header = (custom6_cpath.get("cpath_header") if custom6_cpath else None)
        
        default_movie_string_id = 342
        default_tvshow_string_id = 20343
        default_custom1_string = "Custom 1"
        default_custom2_string = "Custom 2"
        default_custom3_string = "Custom 3"
        default_custom4_string = "Custom 4"
        default_custom5_string = "Custom 5"
        default_custom6_string = "Custom 6"
        
        default_movie_value = (xbmc.getLocalizedString(default_movie_string_id) if not movie_cpath_header else movie_cpath_header)
        default_tvshow_value = (xbmc.getLocalizedString(default_tvshow_string_id) if not tvshow_cpath_header else tvshow_cpath_header)
        default_custom1_value = (default_custom1_string if not custom1_cpath_header else custom1_cpath_header)
        default_custom2_value = (default_custom2_string if not custom2_cpath_header else custom2_cpath_header)
        default_custom3_value = (default_custom3_string if not custom3_cpath_header else custom3_cpath_header)
        default_custom4_value = (default_custom4_string if not custom4_cpath_header else custom4_cpath_header)
        default_custom5_value = (default_custom5_string if not custom5_cpath_header else custom5_cpath_header)
        default_custom6_value = (default_custom6_string if not custom6_cpath_header else custom6_cpath_header)
        from modules.backup_restore import load_all_menu_labels

        load_all_menu_labels()

        xbmc.executebuiltin("Skin.SetString(MenuMovieLabelDB,%s)" % default_movie_value)
        xbmc.executebuiltin("Skin.SetString(MenuTVShowLabelDB,%s)" % default_tvshow_value)
        xbmc.executebuiltin("Skin.SetString(MenuCustom1LabelDB,%s)" % default_custom1_value)
        xbmc.executebuiltin("Skin.SetString(MenuCustom2LabelDB,%s)" % default_custom2_value)
        xbmc.executebuiltin("Skin.SetString(MenuCustom3LabelDB,%s)" % default_custom3_value)
        xbmc.executebuiltin("Skin.SetString(MenuCustom4LabelDB,%s)" % default_custom4_value)
        xbmc.executebuiltin("Skin.SetString(MenuCustom5LabelDB,%s)" % default_custom5_value)
        xbmc.executebuiltin("Skin.SetString(MenuCustom6LabelDB,%s)" % default_custom6_value)

    def manage_action(self, cpath_setting, context="widget"):
        choices = [("Rename", "rename_path"), ("Remake", "remake_path"), ("Remove", "clear_path"),]
        if context in ("widget", "submenu", "topbar_custom_menu"):
            choices = [("Move up", "move_up"), ("Move down", "move_down"),] + choices
        if context == "widget":
            choices.insert(2, ("Display type", "display_type"))

        choice = dialog.select("%s options" % self.path_type.capitalize().replace("_", " "), [i[0] for i in choices],)
        if choice == -1:
            return None

        action = choices[choice][1]
        if action in ["move_up", "move_down"]:
            parts = cpath_setting.split(".")
            if len(parts) < 3 or not parts[-1].isdigit():
                dialog.ok("Finder", "Cannot move this %s" % context)
                return None
            current_order = int(parts[-1])
            if context == "widget":
                max_items = max_widgets
            elif context == "submenu":
                max_items = max_submenu_items
            else:
                max_items = max_topbar_custom_menu_items
            if current_order == 1 and action == "move_up":
                new_order = max_items
            elif current_order == max_items and action == "move_down":
                new_order = 1
            else:
                new_order = (current_order - 1 if action == "move_up" else current_order + 1)
            self.swap_widgets(parts, current_order, new_order)

        elif action == "remake_path":
            self.remove_cpath_from_database(cpath_setting)
            result = self.path_browser(allow_no_path=(context == "main_menu"), allow_actions=(context in ("main_menu", "submenu", "topbar_custom_menu")), allow_dialogs=(context in ("submenu", "topbar_custom_menu")))
            if result:
                cpath_path = result.get("file", None)
                if context == "widget":
                    self.handle_widget_remake(result, cpath_setting)
                elif context == "submenu":
                    label = dialog.input("Set submenu label", defaultt=result.get("label", ""))
                    if label:
                        self.add_cpath_to_database(cpath_setting, cpath_path, label, "", "")
                elif context == "topbar_custom_menu":
                    label = dialog.input("Set custom menu label", defaultt=result.get("label", ""))
                    if label:
                        self.add_cpath_to_database(cpath_setting, cpath_path, label, "", "")
                elif context == "main_menu":
                    default_header = result.get("label", None)
                    cpath_header = self.main_menu_header(default_header)
                    if not cpath_header:
                        return None
                    self.add_cpath_to_database(cpath_setting, cpath_path, cpath_header, "", "")
                    self.make_main_menu_xml(self.fetch_current_cpaths())
                    dialog.ok("Finder", "Main menu remade")

        elif action == "rename_path":
            result = self.fetch_one_cpath(cpath_setting)
            if not result:
                return None
            cpath_path = result.get("cpath_path", None)
            cpath_type = result.get("cpath_type", None)
            cpath_label = result.get("cpath_label", None)
            if not cpath_path:
                return None
            default_header = result.get("cpath_header", None)
            if context == "widget":
                cpath_header = self.widget_header(default_header)
                if not cpath_header:
                    return None
                widget_type = self.get_widget_type(result["cpath_type"])
                if not widget_type:
                    return None
                if "Stacked" in cpath_type:
                    cpath_label = "%s | Stacked (%s) | Category" % (cpath_header, widget_type,)
                else:
                    cpath_label = "%s | %s" % (cpath_header, widget_type)
                self.update_cpath_in_database(cpath_setting, cpath_path, cpath_header, result["cpath_type"], cpath_label,)
            elif context == "submenu":
                cpath_header = dialog.input("Set submenu label", defaultt=default_header or "")
                if cpath_header:
                    self.update_cpath_in_database(cpath_setting, cpath_path, cpath_header, "", "")
            elif context == "topbar_custom_menu":
                cpath_header = dialog.input("Set custom menu label", defaultt=default_header or "")
                if cpath_header:
                    self.update_cpath_in_database(cpath_setting, cpath_path, cpath_header, "", "")
            elif context == "main_menu":
                cpath_header = self.main_menu_header(default_header)
                if not cpath_header or cpath_header.strip() == "":
                    cpath_map = {
                        "movie.main_menu": xbmc.getLocalizedString(342),
                        "tvshow.main_menu": xbmc.getLocalizedString(20343),
                        "custom1.main_menu": "Custom 1",
                        "custom2.main_menu": "Custom 2",
                        "custom3.main_menu": "Custom 3",
                        "custom4.main_menu": "Custom 4",
                        "custom5.main_menu": "Custom 5",
                        "custom6.main_menu": "Custom 6",
                    }
                    cpath_header = cpath_map.get(cpath_setting, "Default main menu label not found")
                self.update_cpath_in_database(cpath_setting, cpath_path, cpath_header, "", "")
                self.make_main_menu_xml(self.fetch_current_cpaths())

        elif action == "display_type":
            result = self.fetch_one_cpath(cpath_setting)
            if not result:
                return None
            cpath_path = result.get("cpath_path", None)
            cpath_header = result.get("cpath_header", None)
            if not cpath_path:
                return None
            self.create_and_update_widget(cpath_setting, cpath_path, cpath_header, add_to_db=False)

        elif action == "clear_path":
            self.remove_cpath_from_database(cpath_setting)
            if context == "main_menu":
                self.make_default_xml()
                dialog.ok("Finder", "Path cleared")
        return None

    def swap_widgets(self, parts, current_order, new_order):
        current_widget = f"{parts[0]}.{parts[1]}.{current_order}"
        adjacent_widget = f"{parts[0]}.{parts[1]}.{new_order}"
        self.refresh_cpaths = True
        self.dbcur.execute("UPDATE custom_paths SET cpath_setting = ? WHERE cpath_setting = ?", (f"{parts[0]}.{parts[1]}.temp", current_widget),)
        self.dbcur.execute("UPDATE custom_paths SET cpath_setting = ? WHERE cpath_setting = ?", (current_widget, adjacent_widget),)
        self.dbcur.execute("UPDATE custom_paths SET cpath_setting = ? WHERE cpath_setting = ?", (adjacent_widget, f"{parts[0]}.{parts[1]}.temp"),)
        self.dbcon.commit()

    def handle_widget_remake(self, result, cpath_setting):
        cpath_path, default_header = result.get("file", None), result.get("label", None)
        cpath_header = self.widget_header(default_header)
        self.create_and_update_widget(cpath_setting, cpath_path, cpath_header)

    def create_and_update_widget(self, cpath_setting, cpath_path, cpath_header, add_to_db=True):
        widget_type = self.widget_type(cpath_path=cpath_path)
        if not widget_type:
            return
        if widget_type[0] == "Category" and dialog.yesno("Stacked widget", "Make [COLOR accent_color][B]%s[/B][/COLOR] a stacked widget?" % cpath_header,):
            widget_type = self.widget_type(label="Choose stacked widget display type", cpath_path=cpath_path)
            if not widget_type:
                return
            cpath_type, cpath_label = "%sStacked" % widget_type[1], "%s | Stacked (%s) | Category" % (cpath_header, widget_type[0])
        else:
            cpath_type, cpath_label = widget_type[1], "%s | %s" % (cpath_header, widget_type[0],)
        if add_to_db:
            self.add_cpath_to_database(cpath_setting, cpath_path, cpath_header, cpath_type, cpath_label)
        else:
            self.update_cpath_in_database(cpath_setting, cpath_path, cpath_header, cpath_type, cpath_label)

    # -------------------------------------------------
    # SKIN RELOAD AND REBUILD
    # -------------------------------------------------
    def reload_skin(self):
        if window.getProperty("finder.clear_path_refresh") == "true":
            return
        window.setProperty("finder.clear_path_refresh", "true")
        while xbmcgui.getCurrentWindowId() == 10035:
            xbmc.sleep(500)
        window.setProperty("finder.clear_path_refresh", "")
        xbmc.sleep(200)
        xbmc.executebuiltin("ReloadSkin()")
        starting_widgets()

    def clean_header(self, header):
        return header.replace("[B]", "").replace("[/B]", "").replace(" >>", "")

    def remake_main_menus(self):
        self.refresh_cpaths = True
        active_cpaths = self.fetch_current_cpaths()
        if active_cpaths:
            self.make_main_menu_xml(active_cpaths)
        else:
            self.make_default_xml()

    def remake_widgets(self):
        self.refresh_cpaths = True
        active_cpaths = self.fetch_current_cpaths()
        if active_cpaths:
            self.make_widget_xml(active_cpaths)
        else:
            self.make_default_xml()

    def make_default_xml(self, reload_skin=True):
            item = default_xmls[self.cpath_setting]

            if self.path_type == "widget":
                final_format = '''<?xml version="1.0" encoding="UTF-8"?>
    <includes>
        <include name="%s">
            <control type="group">
                <width>1</width>
                <height>1</height>
                <visible>false</visible>
            </control>
        </include>
    </includes>''' % item[2]

            elif self.path_type == "main_menu":
                final_format = '''<?xml version="1.0" encoding="UTF-8"?>
    <includes>
        <include name="%s">
            <item>
                <label>Empty</label>
                <onclick>noop</onclick>
                <visible>false</visible>
            </item>
        </include>
    </includes>''' % item[2]

            else:
                final_format = item[1].format(includes_type=item[2])

            xml_file = "special://skin/xml/%s.xml" % item[0]

            with xbmcvfs.File(xml_file, "w") as f:
                f.write(final_format)

            self.update_skin_strings()

            if reload_skin:
                Thread(target=self.reload_skin).start()


# -------------------------------------------------
# MENU MANAGEMENT
# -------------------------------------------------
def _eligible_menu_types():
    from modules.main_menu_order import get_eligible_configurable_menu_types

    return get_eligible_configurable_menu_types()


def manage_submenus():
    menu_types = _eligible_menu_types()
    if not menu_types:
        dialog.ok("Finder", "No configured main menu items are currently enabled.")
        return
    choice = dialog.select("Choose main menu item", [item[0] for item in menu_types])
    if choice == -1:
        return
    return CPaths("%s.submenu" % menu_types[choice][1]).manage_submenu()


def manage_widget_menus():
    menu_types = _eligible_menu_types()
    if not menu_types:
        dialog.ok("Finder", "No configured main menu items are currently enabled.")
        return
    choice = dialog.select("Choose main menu item", [item[0] for item in menu_types])
    if choice == -1:
        return
    return CPaths("%s.widget" % menu_types[choice][1]).manage_widgets()


def set_topbar_custom_menu_heading():
    return CPaths("topbar.custom_menu").set_topbar_custom_menu_heading()


def manage_topbar_custom_menu_icon():
    return CPaths("topbar.custom_menu").manage_topbar_custom_menu_icon()


def manage_topbar_custom_menu():
    return CPaths("topbar.custom_menu").manage_topbar_custom_menu()


# -------------------------------------------------
# MAIN MENU ICON MANAGEMENT
# -------------------------------------------------
def manage_main_menu_icon(cpath_setting):
    # Popup UI to manage main menu icon
    media_type = cpath_setting.split(".")[0]
    heading_map = {
        "movie": "Movies main menu icon",
        "tvshow": "TV Shows main menu icon",
        "custom1": "Custom 1 main menu icon",
        "custom2": "Custom 2 main menu icon",
        "custom3": "Custom 3 main menu icon",
        "custom4": "Custom 4 main menu icon",
        "custom5": "Custom 5 main menu icon",
        "custom6": "Custom 6 main menu icon",
    }
    heading = heading_map.get(media_type, "Main menu icon")

    current_icon = xbmc.getInfoLabel("Skin.String(%s)" % cpath_setting)

    items = []

    li_set = Listitem("Set / change icon", offscreen=True)
    if current_icon:
        li_set.setArt({"icon": current_icon, "thumb": current_icon})
        li_set.setLabel2(current_icon)
    items.append(li_set)

    li_clear = Listitem("Clear custom icon", offscreen=True)
    if current_icon:
        li_clear.setArt({"icon": current_icon, "thumb": current_icon})
    items.append(li_clear)

    choice = dialog.select(heading, items, useDetails=True)
    if choice == -1:
        return

    # OPTION 1: Set / change icon
    if choice == 0:
        last_folder = xbmc.getInfoLabel("Skin.String(finder.last_icon_folder)")
        if not last_folder or not xbmcvfs.exists(last_folder):
            last_folder = "special://skin/extras/icons/"

        icon = dialog.browse(2, "Select icon image", "pictures", ".png|.jpg|.jpeg|.gif|.tbn", False, False, last_folder,)
        if not icon:
            return

        folder_only = icon.rsplit("/", 1)[0] + "/"
        xbmc.executebuiltin("Skin.SetString(finder.last_icon_folder,%s)" % folder_only)

        xbmc.executebuiltin("Skin.SetString(%s,%s)" % (cpath_setting, icon))
        xbmcgui.Dialog().notification("Finder", "Main menu icon updated", icon, 3000)

    # OPTION 2: Clear icon
    elif choice == 1 and current_icon:
        xbmc.executebuiltin("Skin.SetString(%s,)" % cpath_setting)
        xbmcgui.Dialog().notification("Finder", "Main menu icon cleared", "", 3000)

    xbmc.sleep(150)
    main_menu_key = "%s.main_menu" % media_type
    CPaths(main_menu_key).remake_main_menus()

    
# -------------------------------------------------
# REMAKE MENUS/WIDGETS
# -------------------------------------------------
def remake_all_cpaths(silent=False):
    for item in (
        "movie.widget",
        "tvshow.widget",
        "custom1.widget",
        "custom2.widget",
        "custom3.widget",
        "custom4.widget",
        "custom5.widget",
        "custom6.widget",
    ):
        cpaths = CPaths(item)
        cpaths.refresh_cpaths = True
        active_cpaths = cpaths.fetch_current_cpaths()
        if active_cpaths:
            cpaths.make_widget_xml(active_cpaths, reload_skin=False)
        else:
            cpaths.make_default_xml(reload_skin=False)

    for item in (
        "movie.main_menu",
        "tvshow.main_menu",
        "custom1.main_menu",
        "custom2.main_menu",
        "custom3.main_menu",
        "custom4.main_menu",
        "custom5.main_menu",
        "custom6.main_menu",
    ):
        cpaths = CPaths(item)
        cpaths.refresh_cpaths = True
        active_cpaths = cpaths.fetch_current_cpaths()
        if active_cpaths:
            cpaths.make_main_menu_xml(active_cpaths, reload_skin=False)
        else:
            cpaths.make_default_xml(reload_skin=False)

    for media_type in submenu_types:
        submenu = CPaths("%s.submenu" % media_type)
        submenu.refresh_cpaths = True
        submenu.make_submenu_xml(submenu.fetch_current_cpaths(), reload_skin=False)

    topbar_menu = CPaths("topbar.custom_menu")
    topbar_menu.refresh_cpaths = True
    topbar_menu.make_topbar_custom_menu_xml(
        topbar_menu.fetch_current_cpaths(),
        reload_skin=False,
    )

    from modules.main_menu_order import reset_main_menu_order
    reset_main_menu_order(reload_skin=False)

    xbmc.executebuiltin("ReloadSkin()")
    starting_widgets()

    if not silent:
        xbmcgui.Dialog().ok("Finder", "Menus and widgets remade")


# -------------------------------------------------
# WIDGET STARTUP
# -------------------------------------------------
def starting_widgets():
    window = xbmcgui.Window(10000)
    window.setProperty("finder.starting_widgets", "finished")
    for item in (
        "movie.widget",
        "tvshow.widget",
        "custom1.widget",
        "custom2.widget",
        "custom3.widget",
        "custom4.widget",
        "custom5.widget",
        "custom6.widget",
    ):
        try:
            active_cpaths = CPaths(item).fetch_current_cpaths()
            if not active_cpaths:
                continue
            widget_type = item.split(".")[0]
            widget_type_id = {
                "movie": 19010,
                "tvshow": 22010,
                "custom1": 23010,
                "custom2": 24010,
                "custom3": 25010,
                "custom4": 26010,
                "custom5": 27010,
                "custom6": 28010,
            }
            base_list_id = widget_type_id.get(widget_type)
            for count in range(1, 11):
                active_widget = active_cpaths.get(count, {})
                if not active_widget:
                    continue
                if "Stacked" not in active_widget["cpath_label"]:
                    continue
                cpath_setting = active_widget["cpath_setting"]
                if not cpath_setting:
                    continue
                try:
                    list_id = base_list_id + int(cpath_setting.split(".")[2])
                except:
                    continue
                try:
                    first_item = files_get_directory(active_widget["cpath_path"])[0]
                except:
                    continue
                if not first_item:
                    continue
                cpath_label, cpath_path = first_item["label"], first_item["file"]
                window.setProperty("finder.%s.label" % list_id, cpath_label)
                window.setProperty("finder.%s.path" % list_id, cpath_path)
        except:
            pass
    try:
        del window
    except:
        pass
