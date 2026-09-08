# -*- coding: utf-8 -*-
import os
import shutil
import xbmc, xbmcaddon, xbmcgui, xbmcvfs
import sqlite3
import zipfile
import tempfile
import xml.etree.ElementTree as ET

dialog = xbmcgui.Dialog()
translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addon_info = addon.getAddonInfo
addon_path = translatePath(addon_info('path'))
addon_data = translatePath('special://profile/addon_data/')
addon_icon = translatePath('special://home/addons/script.finder.helper/resources/icon.png')

#Skin Backup/Restore Variables
db_dst_dir = xbmcvfs.translatePath("special://profile/addon_data/script.finder.helper/")
home = translatePath('special://home/')
user_path = os.path.join(home, 'userdata/')
data_path = os.path.join(user_path, 'addon_data/')
skin_path = translatePath('special://skin/')
skin = ET.parse(os.path.join(skin_path, 'addon.xml'))
root = skin.getroot()
skin_id = root.attrib['id']

#GUI/FAV Variables
gui_file = 'guisettings.xml'
fav_file = 'favourites.xml'

#Menu/Widget Default Configs
dst_cfg = xbmcvfs.translatePath('special://skin/xml/')
dst_db = os.path.join(addon_data, 'script.finder.helper/')

finder_mdblist_library_cfg = os.path.join(skin_path, 'resources/pre_configs/Finder_MDBlist_Library/menus_widgets/')
finder_mdblist_library_db = os.path.join(skin_path, 'resources/pre_configs/Finder_MDBlist_Library/database/')

finder_mdblist_watchlist_cfg = os.path.join(skin_path, 'resources/pre_configs/Finder_MDBlist_Watchlist/menus_widgets/')
finder_mdblist_watchlist_db = os.path.join(skin_path, 'resources/pre_configs/Finder_MDBlist_Watchlist/database/')

finder_tmdb_watchlist_cfg = os.path.join(skin_path, 'resources/pre_configs/Finder_TMDB_Watchlist/menus_widgets/')
finder_tmdb_watchlist_db = os.path.join(skin_path, 'resources/pre_configs/Finder_TMDB_Watchlist/database/')

finder_trakt_library_cfg = os.path.join(skin_path, 'resources/pre_configs/Finder_Trakt_Library/menus_widgets/')
finder_trakt_library_db = os.path.join(skin_path, 'resources/pre_configs/Finder_Trakt_Library/database/')

finder_trakt_watchlist_cfg = os.path.join(skin_path, 'resources/pre_configs/Finder_Trakt_Watchlist/menus_widgets/')
finder_trakt_watchlist_db = os.path.join(skin_path, 'resources/pre_configs/Finder_Trakt_Watchlist/database/')



# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def get_keyboard_text(default=""): #Open Kodi keyboard and return input
    kb = xbmc.Keyboard(default, "Enter name for your backup")
    kb.doModal()
    if kb.isConfirmed():
        text = kb.getText().strip()
        return text if text else None
    return None

#Create directory if it doesn't exist
def ensure_dir(path):
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdirs(path)

#Copy file
def copy_file(src, dst):
    try:
        ensure_dir(os.path.dirname(dst))
        xbmcvfs.copy(src, dst)
    except Exception as e:
        dialog.notification("Backup Error", str(e), xbmcgui.NOTIFICATION_ERROR, 3000)

# Check if an addon is installed
def addon_installed(addon_id):
    try:
        xbmcaddon.Addon(addon_id)
        return True
    except:
        return False

# Copy all files from source to destination
def copy_all_files(src_dir, dst_dir):
    # Make sure destination exists
    os.makedirs(dst_dir, exist_ok=True)

    # Loop through items in source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        # Copy only files (skip subdirectories)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            
# Delete files starting with
def delete_files_starting_with(directory, prefix):
    # Ensure directory ends with slash
    if not directory.endswith(("/", "\\")):
        directory += "/"

    # List the directory contents
    try:
        dirs, files = xbmcvfs.listdir(directory)
    except Exception as e:
        xbmc.log(f"Error reading directory: {e}", xbmc.LOGERROR)
        return

    # Loop through files and delete those starting with prefix
    for file_name in files:
        if file_name.startswith(prefix):
            full_path = os.path.join(directory, file_name)
            xbmcvfs.delete(full_path)

# Apply Default Config XML files
def apply_default_config_xmls():
    src = xbmcvfs.translatePath('special://skin/resources/default_configs/')
    dst = xbmcvfs.translatePath('special://skin/xml/')

    if not src.endswith(("/", "\\")):
        src += "/"

    if not dst.endswith(("/", "\\")):
        dst += "/"

    if not xbmcvfs.exists(src):
        xbmc.log(f"Finder Plus: default config path missing: {src}", xbmc.LOGERROR)
        return False

    dirs, files = xbmcvfs.listdir(src)

    for file_name in files:
        if file_name.startswith('script-finder') and file_name.endswith('.xml'):
            src_file = src + file_name
            dst_file = dst + file_name
            xbmcvfs.copy(src_file, dst_file)

    return True

# Write Main Menu icons to settings
def write_pre_config_main_menu_icons(cfg_src):
    icon_settings = {
        "script-finder-main_menu_movies.xml": "movie.main_menu_icon",
        "script-finder-main_menu_tvshows.xml": "tvshow.main_menu_icon",
        "script-finder-main_menu_custom1.xml": "custom1.main_menu_icon",
        "script-finder-main_menu_custom2.xml": "custom2.main_menu_icon",
        "script-finder-main_menu_custom3.xml": "custom3.main_menu_icon",
        "script-finder-main_menu_custom4.xml": "custom4.main_menu_icon",
        "script-finder-main_menu_custom5.xml": "custom5.main_menu_icon",
        "script-finder-main_menu_custom6.xml": "custom6.main_menu_icon",
    }

    for file_name, skin_key in icon_settings.items():
        xml_path = os.path.join(cfg_src, file_name)

        if not os.path.exists(xml_path):
            continue

        try:
            with open(xml_path, "r", encoding="utf-8") as f:
                data = f.read()

            start = data.find("<thumb>")
            end = data.find("</thumb>", start)

            if start == -1 or end == -1:
                continue

            icon = data[start + len("<thumb>"):end].strip().replace('"', "'")

            if icon:
                xbmc.executebuiltin(f'Skin.SetString({skin_key},"{icon}")')
                xbmc.sleep(50)

        except Exception as e:
            xbmc.log(f"Finder Plus: failed to read pre-config icon from {xml_path}. Reason: {e}",xbmc.LOGERROR)

# Apply Pre-Config XML files
def apply_pre_config(cfg_src, db_src, search_provider):
    apply_default_config_xmls()
    enable_pre_config_home_menu_toggles()
    xbmc.executebuiltin(f'Skin.SetString(current_search_provider,"{search_provider}")')
    copy_all_files(cfg_src, dst_cfg)
    write_pre_config_main_menu_icons(dst_cfg)
    copy_all_files(db_src, dst_db)

	
# -------------------------------------------------
# BACKUP HELPERS
# -------------------------------------------------
def choose_backup_directory():
    path = xbmcgui.Dialog().browseSingle(3, "Choose Backup Directory", "")

    if not path:
        return

    xbmc.executebuiltin('Skin.SetString(backup_directory,"%s")' % path)
    dialog.ok("Finder Plus", "Backup directory saved.[CR][CR]Location:[CR][COLOR=gold]%s[/COLOR]" % os.path.normpath(path))

def get_backup_directory():
    path = xbmc.getInfoLabel("Skin.String(backup_directory)")

    if path:
        return xbmcvfs.translatePath(path)

    return xbmcvfs.translatePath("special://home/backups/Finder_Plus/")

def get_backup_subdir(folder_name):
    path = os.path.join(get_backup_directory(), folder_name)
    ensure_dir(path)
    return path

def backup_file(src, dst, backup_name):
    if not xbmcvfs.exists(src):
        xbmcgui.Dialog().notification("Finder Plus", "No %s file found." % backup_name, addon_icon, 3000)
        return False

    if xbmcvfs.exists(dst):
        if not xbmcgui.Dialog().yesno("Finder Plus", "A %s backup already exists.\n\nDo you want to overwrite it?" % backup_name):
            return False

        if not xbmcvfs.delete(dst):
            xbmc.log("Failed to delete existing %s backup: %s" % (backup_name, dst), xbmc.LOGERROR)
            xbmcgui.Dialog().notification("Finder Plus", "Failed to overwrite existing backup.", addon_icon, 3000)
            return False

    if not xbmcvfs.copy(src, dst):
        xbmc.log("Failed to backup %s from %s to %s" % (backup_name, src, dst), xbmc.LOGERROR)
        xbmcgui.Dialog().notification("Finder Plus", "Backup Failed", addon_icon, 3000)
        return False

    xbmcgui.Dialog().notification("Finder Plus", "Backup Complete", addon_icon, 3000)
    return True

def restore_file(src, dst, backup_name):
    if not xbmcvfs.exists(src):
        xbmcgui.Dialog().notification("Finder Plus", "No %s backup found." % backup_name, addon_icon, 3000)
        return False

    if not xbmcgui.Dialog().yesno("Finder Plus", "Are you sure?"):
        return False

    if xbmcvfs.exists(dst):
        if not xbmcvfs.delete(dst):
            xbmc.log("Failed to delete existing %s file: %s" % (backup_name, dst), xbmc.LOGERROR)
            xbmcgui.Dialog().notification("Finder Plus", "Restore Failed", addon_icon, 3000)
            return False

    if not xbmcvfs.copy(src, dst):
        xbmc.log("Failed to restore %s from %s to %s" % (backup_name, src, dst), xbmc.LOGERROR)
        xbmcgui.Dialog().notification("Finder Plus", "Restore Failed", addon_icon, 3000)
        return False

    return True

def import_backup(folder_name, file_name, backup_name):
    src = dialog.browseSingle(1, "Select %s" % backup_name, "")
    if not src:
        return

    dst = os.path.join(get_backup_subdir(folder_name), file_name)

    if os.path.exists(dst):
        if not dialog.yesno("Finder Plus", "A %s backup already exists.\n\nOverwrite it?" % backup_name):
            return

        xbmcvfs.delete(dst)

    copy_file(src, dst)

    if dialog.yesno("Finder Plus", "%s imported successfully.\n\nRestore it now?" % backup_name):
        if folder_name == "gui_bkup":
            restore_gui()
        else:
            restore_favs()
            
def export_backup(folder_name, backup_name):
    backup_dir = get_backup_subdir(folder_name)

    files = xbmcvfs.listdir(backup_dir)[1]
    if not files:
        dialog.ok("Export Error", "No %s backup found." % backup_name)
        return

    backup_file = files[0]
    src = os.path.join(backup_dir, backup_file)

    dest_dir = dialog.browseSingle(3, "Choose Export Location", "")
    if not dest_dir:
        return

    dst = os.path.join(dest_dir, backup_file)

    copy_file(src, dst)

    dialog.notification("Finder Plus", "%s exported." % backup_name, addon_icon, 3000)


# -------------------------------------------------
# GUI & FAVS BACKUP/RESTORE FUNCTIONS
# -------------------------------------------------
# Backup GUI settings
def backup_gui():
    if not xbmcgui.Dialog().yesno("Finder Plus", "Are you sure?"):
        return

    src = os.path.join(user_path, gui_file)
    dst = os.path.join(get_backup_subdir("gui_bkup"), gui_file)

    backup_file(src, dst, "GUI settings")

# Restore GUI settings
def restore_gui(gui_save=None):
    if gui_save is None:
        gui_save = get_backup_subdir("gui_bkup")

    src = os.path.join(gui_save, gui_file)
    dst = os.path.join(user_path, gui_file)

    if not restore_file(src, dst, "GUI settings"):
        return
    
    xbmcgui.Dialog().notification("Finder Plus", "Restore Complete", addon_icon, 3000)
    xbmcgui.Dialog().ok("Finder Plus", "To save changes you now need to force close Kodi.\n\nPress OK to force close Kodi.")
    os._exit(1)

# Backup Favourites
def backup_favs():
    if not xbmcgui.Dialog().yesno("Finder Plus", "Are you sure?"):
        return

    src = os.path.join(user_path, fav_file)
    dst = os.path.join(get_backup_subdir("favs_bkup"), fav_file)

    backup_file(src, dst, "favourites")

# Restore Favourites
def restore_favs():
    src = os.path.join(get_backup_subdir("favs_bkup"), fav_file)
    dst = os.path.join(user_path, fav_file)

    if not restore_file(src, dst, "favourites"):
        return

    xbmcgui.Dialog().notification("Finder Plus", "Restore Complete", addon_icon, 3000)
    xbmcgui.Dialog().ok("Finder Plus", "To save changes you now need to force close Kodi.\n\nPress OK to force close Kodi.")
    os._exit(1)

# Restore Skin Settings
def restore_skin(skin_save):
    if not os.path.exists(skin_save):
        xbmcgui.Dialog().notification("Finder Plus", "No default skin settings found.", addon_icon, 3000)
        return

    if not xbmcgui.Dialog().yesno("Finder Plus", "Restore the default skin settings.\nAre you sure?"):
        return

    skin_data = os.path.join(data_path, skin_id)
    base_path = translatePath("special://home/addons/skin.finder/")
    src = os.path.join(base_path, "resources", "default_colors", "finder_plus", "defaults.xml")
    dst = os.path.join(base_path, "colors", "defaults.xml")

    try:
        shutil.copytree(skin_save, skin_data, dirs_exist_ok=True)
        copy_file(src, dst)
    except Exception as e:
        xbmc.log("Failed to restore %s. Reason: %s" % (skin_data, e), xbmc.LOGERROR)
        xbmcgui.Dialog().notification("Finder Plus", "Restore Failed", addon_icon, 3000)
        return

    xbmcgui.Dialog().notification("Finder Plus", "Restore Complete", addon_icon, 3000)
    xbmcgui.Dialog().ok("Finder Plus", "To save changes you now need to force close Kodi.\n\nPress OK to force close Kodi.")
    os._exit(1)


# -------------------------------------------------
# USER-CONFIG BACKUP FUNCTION
# -------------------------------------------------
def backup_config():
    backup_name = get_keyboard_text()
    if not backup_name:
        dialog.ok("Backup Canceled", "No backup name was entered.")
        return

    base_backup_dir = get_backup_subdir("User_Configs")
    backup_dir = os.path.join(base_backup_dir, backup_name)
    zip_path = backup_dir + ".zip"

    skin_backup_dir = os.path.join(backup_dir, "skin_files")
    skin_settings_backup_dir = os.path.join(backup_dir, "skin_settings")

    for d in (skin_backup_dir, skin_settings_backup_dir):
        ensure_dir(d)

    # Paths
    xml_dir = xbmcvfs.translatePath("special://skin/xml/")
    db_src = xbmcvfs.translatePath("special://profile/addon_data/script.finder.helper/cpath_cache.db")

    # Backup Menus/Widgets and main menu order
    for file in xbmcvfs.listdir(xml_dir)[1]:
        file_lower = file.lower()
        if "script-finder" in file_lower or file_lower == "includes_mainmenu.xml":
            src = os.path.join(xml_dir, file)
            dst = os.path.join(skin_backup_dir, file)
            copy_file(src, dst)

    # Backup database
    if xbmcvfs.exists(db_src):
        copy_file(db_src, os.path.join(backup_dir, "cpath_cache.db"))

    # Backup skin settings   
    if os.path.exists(os.path.join(data_path, skin_id)) and os.path.exists(os.path.join(skin_settings_backup_dir)):
        try:
            shutil.copytree(os.path.join(data_path, skin_id),os.path.join(skin_settings_backup_dir, skin_id),dirs_exist_ok=True)
        except Exception as e:
            xbmc.log('Failed to backup %s. Reason: %s' % (os.path.join(skin_settings_backup_dir, skin_id), e),xbmc.LOGINFO)

    # Create zip
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_dir)
                    zipf.write(file_path, arcname)

        shutil.rmtree(backup_dir, ignore_errors=True)

    except Exception as e:
        xbmc.log('Failed to create backup zip %s. Reason: %s' % (zip_path, e), xbmc.LOGINFO)
        dialog.ok("Backup Failed", "Failed to create backup zip.")
        return

    display_path = os.path.normpath(zip_path)

    dialog.ok("Backup Completed",f"Backup saved as: [COLOR=gold]{backup_name}.zip[/COLOR][CR]"f"Location:[CR][COLOR=gold]{display_path}[/COLOR]")


# -------------------------------------------------
# USER-CONFIG RESTORE FUNCTION
# -------------------------------------------------
def restore_config():
    base_backup_dir = get_backup_subdir("User_Configs")

    # Open the configured backup directory and allow browsing elsewhere
    zip_path = dialog.browseSingle(1, "Choose Backup To Restore", "", ".zip", False, False, base_backup_dir)

    if not zip_path:
        return

    if not zip_path.lower().endswith(".zip"):
        dialog.ok("Restore Error", "Selected file is not a ZIP archive.")
        return

    selected_backup = os.path.basename(zip_path)
    extract_path = os.path.join(base_backup_dir, "_restore_temp")

    try:
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path, ignore_errors=True)

        ensure_dir(extract_path)

        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(extract_path)

        backup_path = extract_path
        skin_backup_path = os.path.join(backup_path, "skin_files/")
        skin_settings_backup_path = os.path.join(backup_path, "skin_settings/")

        # Restore skin XML files
        xml_dir = xbmcvfs.translatePath("special://skin/xml/")

        delete_files_starting_with(dst_cfg, 'script-finder')
        
        if xbmcvfs.exists(skin_backup_path):
            for file in xbmcvfs.listdir(skin_backup_path)[1]:
                src = os.path.join(skin_backup_path, file)
                dst = os.path.join(xml_dir, file)
                copy_file(src, dst)

        #Restore skin settings            
        if os.path.exists(os.path.join(data_path, skin_id)):
            try:
                shutil.copytree(os.path.join(skin_settings_backup_path, skin_id), os.path.join(data_path, skin_id), dirs_exist_ok=True)
            except Exception as e:
                xbmc.log('Failed to restore %s. Reason: %s' % (os.path.join(data_path, skin_id), e), xbmc.LOGINFO)

        #Restore database
        ensure_dir(db_dst_dir)
        db_src = os.path.join(backup_path, "cpath_cache.db")
        if xbmcvfs.exists(db_src):
            copy_file(db_src, os.path.join(db_dst_dir, "cpath_cache.db"))

    except Exception as e:
        xbmc.log('Failed to restore backup zip %s. Reason: %s' % (zip_path, e), xbmc.LOGINFO)
        dialog.ok("Restore Failed", "Failed to restore backup zip.")
        return

    finally:
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path, ignore_errors=True)
    
    dialog.ok("Restore Complete", f"Restored backup:   [COLOR=gold]{selected_backup}[/COLOR]")
    xbmc.executebuiltin("ReloadSkin()")


# -------------------------------------------------
# USER-CONFIG EXPORT FUNCTION
# -------------------------------------------------
def export_config():
    base_backup_dir = get_backup_subdir("User_Configs")

    backups = [f for f in xbmcvfs.listdir(base_backup_dir)[1] if f.lower().endswith(".zip")]
    if not backups:
        dialog.ok("Export Error", "No backups available to export.")
        return

    index = dialog.select("Select Backup To Export", backups)
    if index < 0:
        return

    backup_name = backups[index]
    backup_path = os.path.join(base_backup_dir, backup_name)

    dest_dir = dialog.browseSingle(3, "Choose Export Location", "") # Select directory

    if not dest_dir:
        return

    if not dest_dir.endswith(("/", "\\")):
        dest_dir += "/"

    export_path = os.path.join(dest_dir, backup_name)

    try:
        if os.path.exists(export_path):
            os.remove(export_path)

        copy_file(backup_path, export_path)

    except Exception as e:
        dialog.ok("Export Error", f"Failed to export backup:\n{e}")
        return

    dialog.notification("Finder Plus",f"Backup exported as:\n{backup_name}",addon_icon,3000)

    
# -------------------------------------------------
# USER-CONFIG IMPORT FUNCTION
# -------------------------------------------------
def import_config():
    zip_path = dialog.browseSingle(1, "Select Finder Plus Backup ZIP", "", ".zip", False, False)

    if not zip_path:
        return

    if not zip_path.lower().endswith(".zip"):
        dialog.ok("Import Error", "Selected file is not a ZIP archive.")
        return

    base_backup_dir = get_backup_subdir("User_Configs")
    ensure_dir(base_backup_dir)

    backup_name = os.path.basename(zip_path)
    final_dst = os.path.join(base_backup_dir, backup_name)

    if os.path.exists(final_dst):
        overwrite = dialog.yesno("Backup Exists",f"A backup named '{backup_name}' already exists.\n\nOverwrite it?")
        if not overwrite:
            return
        os.remove(final_dst)

    try:
        copy_file(zip_path, final_dst)
    except Exception as e:
        dialog.ok("Import Error", f"Failed to import backup:\n{e}")
        return

    if dialog.yesno("Import Complete",f"Backup '{backup_name}' imported successfully.\n\nRestore it now?"):
        restore_config()


# -------------------------------------------------
# Enable Pre-Config Main Menu Toggles
# -------------------------------------------------
def enable_pre_config_home_menu_toggles():
    """
    Enables Movies, TV Shows, and Custom1-6
    Disables the default Kodi menu items not used by pre-configs
    """
    enabled_settings = [
        "HomeMenuNoMoviesButton",
        "HomeMenuNoTVShowsButton",
        "HomeMenuNoCustom1Button",
        "HomeMenuNoCustom2Button",
        "HomeMenuNoCustom3Button",
        "HomeMenuNoCustom4Button",
        "HomeMenuNoCustom5Button",
        "HomeMenuNoCustom6Button",
        "HomeMenuNoProgramsButton",
        "HomeMenuNoFavButton",
    ]

    disabled_settings = [
        "HomeMenuNoMusicButton",
        "HomeMenuNoMusicVideoButton",
        "HomeMenuNoTVButton",
        "HomeMenuNoRadioButton",
        "HomeMenuNoPicturesButton",
        "HomeMenuNoVideosButton",
        "HomeMenuNoGamesButton",
        "HomeMenuNoWeatherButton",
    ]

    for setting in enabled_settings:
        if xbmc.getCondVisibility(f"Skin.HasSetting({setting})"):
            xbmc.executebuiltin(f"Skin.Reset({setting})")
            xbmc.sleep(50)

    for setting in disabled_settings:
        if not xbmc.getCondVisibility(f"Skin.HasSetting({setting})"):
            xbmc.executebuiltin(f"Skin.SetBool({setting})")
            xbmc.sleep(50)


# -------------------------------------------------
# Main Menu Labels
# -------------------------------------------------
def load_all_menu_labels():
    """
    Reads all main menu labels from cpath_cache.db and assigns them
    to Skin.String() values for use in XML.
    """
    db_path = translatePath("special://profile/addon_data/script.finder.helper/cpath_cache.db")

    if not xbmcvfs.exists(db_path):
        return

    MENU_MAP = {
        "movie":   ("MenuMovieLabelDB",   "Movies"),
        "tvshow":  ("MenuTVShowLabelDB",  "TV Shows"),
        "custom1": ("MenuCustom1LabelDB", "Custom 1"),
        "custom2": ("MenuCustom2LabelDB", "Custom 2"),
        "custom3": ("MenuCustom3LabelDB", "Custom 3"),
        "custom4": ("MenuCustom4LabelDB", "Custom 4"),
        "custom5": ("MenuCustom5LabelDB", "Custom 5"),
        "custom6": ("MenuCustom6LabelDB", "Custom 6"),
    }

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        for key, (skin_key, default_label) in MENU_MAP.items():

            setting_key = f"{key}.main_menu"

            cur.execute("SELECT cpath_header FROM custom_paths WHERE cpath_setting = ? LIMIT 1",(setting_key,))
            row = cur.fetchone()

            if row and row[0]:
                label = row[0]
                source = "DB"
            else:
                label = default_label
                source = "DEFAULT"

            safe = label.replace('"', "'")
            xbmc.executebuiltin(f'Skin.SetString({skin_key},"{safe}")')

        conn.close()

    except Exception as e:
        xbmc.log(f"DB Error loading menu labels: {e}", xbmc.LOGERROR)

        
# -------------------------------------------------
# PRE-MADE CONFIGURATIONS
# -------------------------------------------------
def preconfig_addon_notinstalled(addon):
	dialog.notification("Finder Plus", f"{addon} must be installed to use this pre-config.", addon_icon, 5000)
	
def run_pre_config_mode(config):
    config = str(config or "").strip().lower()

    configs = {
        "finder_mdblist_library":   {"label": "Finder MDBlist Library",    "cfg": finder_mdblist_library_cfg, "db": finder_mdblist_library_db, "search_provider": "5"},
        "finder_mdblist_watchlist":   {"label": "Finder MDBlist Watchlist",    "cfg": finder_mdblist_watchlist_cfg, "db": finder_mdblist_watchlist_db, "search_provider": "5"},
        "finder_tmdb_watchlist":   {"label": "Finder TMDB Watchlist",    "cfg": finder_tmdb_watchlist_cfg,    "db": finder_tmdb_watchlist_db,    "search_provider": "5"},
        "finder_trakt_library":   {"label": "Finder Trakt Library",    "cfg": finder_trakt_library_cfg,       "db": finder_trakt_library_db,       "search_provider": "5"},
        "finder_trakt_watchlist":   {"label": "Finder Trakt Watchlist",    "cfg": finder_trakt_watchlist_cfg,       "db": finder_trakt_watchlist_db,       "search_provider": "5"},
    }

    selected = configs.get(config)

    if not selected:
        dialog.ok("Finder Plus", "The selected pre-configuration is not available.")
        return

    mode_label = selected["label"]
    cfg_src = selected["cfg"]
    db_src = selected["db"]

    if not dialog.yesno("Finder Plus", f"Are you sure you want to apply the '[COLOR gold]{mode_label}[/COLOR]' pre-configuration?[CR][CR]This will overwrite your current menus and widgets.", nolabel="No", yeslabel="Yes"):
        return

    if not os.path.isdir(cfg_src) or not os.path.isdir(db_src):
        dialog.ok("Finder Plus", f"The files required for the '[COLOR gold]{mode_label}[/COLOR]' pre-configuration could not be found.")
        return

    apply_pre_config(cfg_src, db_src, selected["search_provider"])
    load_all_menu_labels()
    xbmc.executebuiltin("Skin.SetBool(noiconsilhouettes)")
    xbmc.executebuiltin("ReloadSkin()")
    dialog.notification("Finder Plus", f"{mode_label} config applied!", addon_icon, 3000)
