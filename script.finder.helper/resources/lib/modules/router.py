# -*- coding: utf-8 -*-
import os
import sys
import xbmc, xbmcgui, xbmcvfs
from urllib.parse import parse_qsl

dialog = xbmcgui.Dialog()
translatePath = xbmcvfs.translatePath
home = translatePath('special://home/')

#GUI Backup/restore paths
gui_save_path = os.path.join(home, 'backups/')
gui_save_user = os.path.join(gui_save_path, 'gui_bkup/')

#FAVS Backup/restore paths
fav_save_path = os.path.join(home, 'backups/')
fav_save_user = os.path.join(fav_save_path, 'favs_bkup/')

    
def routing():
    raw_params = "&".join(
        argument.lstrip("?")
        for argument in sys.argv[1:]
        if argument
    )
    params = dict(parse_qsl(raw_params, keep_blank_values=True))
    _get = params.get
    mode = _get("mode", "check_for_update")

    # -------------------------------------------------
    # Default modes
    # -------------------------------------------------
    if mode == "widget_monitor":
        from modules.widget_utils import widget_monitor

        return widget_monitor(params.get("list_id"))

    if "actions" in mode:
        from modules import actions

        return exec("actions.%s(params)" % mode.split(".")[1])

    if mode == "check_for_update":
        from modules.version_monitor import check_for_update

        return check_for_update()

    if mode == "check_for_profile_change":
        from modules.version_monitor import check_for_profile_change

        return check_for_profile_change(_get("skin_id"))

    if mode == "manage_widgets":
        from modules.cpath_maker import CPaths

        return CPaths(_get("cpath_setting")).manage_widgets()

    if mode == "manage_widget_menus":
        from modules.cpath_maker import manage_widget_menus

        return manage_widget_menus()

    if mode == "manage_main_menu_path":
        from modules.cpath_maker import CPaths

        return CPaths(_get("cpath_setting")).manage_main_menu_path()

    if mode == "manage_submenus":
        from modules.cpath_maker import manage_submenus

        return manage_submenus()

    if mode == "set_topbar_custom_menu_heading":
        from modules.cpath_maker import set_topbar_custom_menu_heading

        return set_topbar_custom_menu_heading()

    if mode == "manage_topbar_custom_menu_icon":
        from modules.cpath_maker import manage_topbar_custom_menu_icon

        return manage_topbar_custom_menu_icon()

    if mode == "manage_topbar_custom_menu":
        from modules.cpath_maker import manage_topbar_custom_menu

        return manage_topbar_custom_menu()

    if mode == "manage_main_menu_order":
        from modules.main_menu_order import manage_main_menu_order

        return manage_main_menu_order()

    if mode == "manage_submenu":
        from modules.cpath_maker import CPaths

        return CPaths(_get("cpath_setting")).manage_submenu()

    if mode == "manage_main_menu_icon":
        from modules.cpath_maker import manage_main_menu_icon

        return manage_main_menu_icon(_get("cpath_setting"))

    if mode == "starting_widgets":
        from modules.cpath_maker import starting_widgets

        return starting_widgets()

    if mode == "remake_all_cpaths":
        silent = params.get("silent", "false").lower() == "true"
        from modules.cpath_maker import remake_all_cpaths

        return remake_all_cpaths(silent=silent)

    if mode == "search_input":
        from modules.search_utils import SPaths

        return SPaths().search_input()

    if mode == "remove_all_spaths":
        from modules.search_utils import SPaths

        return SPaths().remove_all_spaths()

    if mode == "re_search":
        from modules.search_utils import SPaths

        return SPaths().re_search()

    if mode == "open_search_window":
        from modules.search_utils import SPaths

        return SPaths().open_search_window()

    if mode == "set_api_key":
        from modules.MDbList import set_api_key

        return set_api_key()

    if mode == "delete_all_ratings":
        from modules.MDbList import MDbListAPI

        return MDbListAPI().delete_all_ratings()

    if mode == "modify_keymap":
        from modules.custom_actions import modify_keymap

        return modify_keymap()

    if mode == "play_trailer":
        from modules.MDbList import play_trailer

        return play_trailer()

    if mode == "fix_black_screen":
        from modules.custom_actions import fix_black_screen

        return fix_black_screen()


    # -------------------------------------------------
    # Change Search Provider in Search Results Window
    # -------------------------------------------------
    if mode == 'select_search_provider':
        from modules.search_utils import SPaths

        return SPaths().change_search_provider()


    # -------------------------------------------------
    # Search From History
    # -------------------------------------------------
    if mode == 'search_from_history':
        from modules.search_utils import SPaths

        return SPaths().search_from_history()


    # -------------------------------------------------
    # Set Backup Directory
    # -------------------------------------------------
    if mode == "set_backup_directory":
        from modules.backup_restore import choose_backup_directory

        return choose_backup_directory()


    # -------------------------------------------------
    # Choose Skin Color
    # -------------------------------------------------
    if mode == "choose_color":
        from modules.custom_actions import choose_color

        return choose_color()

    if mode == "set_color":
        from modules.custom_actions import set_skin_color

        return set_skin_color(color=_get("color"), reload_skin=True, show_notification=True)


    # -------------------------------------------------
    # Set Background and Logo
    # -------------------------------------------------
    if mode == "set_image":
        from modules.custom_actions import set_image

        return set_image(target=_get("target", "other"))

    if mode == "set_image_logo":
        from modules.custom_actions import set_image_logo

        return set_image_logo()


    # ----------------------------------------------------------
    # Apply Look & Feel Experience
    # ----------------------------------------------------------
    if mode == "apply_lookfeel":
        from modules.custom_actions import apply_lookfeel

        keep_artwork = _get("keep_artwork", "false").lower() == "true"
        keep_color = _get("keep_color", "false").lower() == "true"

        return apply_lookfeel(_get("lookfeel"), keep_artwork=keep_artwork, keep_color=keep_color)


    # ----------------------------------------------------------
    # Choose Look & Feel Experience
    # ----------------------------------------------------------
    if mode == "choose_lookfeel":
        from modules.custom_actions import choose_lookfeel

        return choose_lookfeel()

    if mode == "choose_cinema_section":
        from modules.custom_actions import choose_cinema_section

        return choose_cinema_section()

    if mode == "focus_cinema_section":
        from modules.custom_actions import focus_cinema_section

        return focus_cinema_section()

    if mode == "select_cinema_section":
        from modules.custom_actions import select_cinema_section

        return select_cinema_section(_get("section_id"))

    if mode == "prepare_cinema_sections":
        from modules.custom_actions import prepare_cinema_sections

        return prepare_cinema_sections()

    if mode == "open_cinema_sections":
        from modules.custom_actions import open_cinema_sections

        return open_cinema_sections()

    # -------------------------------------------------
    # Power Mode Select
    # -------------------------------------------------
    if mode == "power_mode_select":
        choices = ["Force Close", "Quit Kodi", "Show Shutdown Menu"]

        ret = dialog.select("Power Button Mode", choices)

        if ret >= 0:
            value = choices[ret]
            xbmc.executebuiltin(f"Skin.SetString(PowerButtonMode,{value})")
        return


    # -------------------------------------------------
    # OSD Audio Button Select
    # -------------------------------------------------
    if mode == "osd_audio_button_select":
            choices = ["Next audio stream", "Audio settings", "Disabled"]

            ret = dialog.select("Audio Button Behavior", choices)

            if ret >= 0:
                    value = choices[ret]
                    xbmc.executebuiltin(f"Skin.SetString(OSDAudioButtonMode,{value})")
            return


    # -------------------------------------------------
    # OSD Subtitle Button Select
    # -------------------------------------------------
    if mode == "osd_subtitle_button_select":
            choices = ["Next subtitle", "Subtitle settings", "Disabled"]

            ret = dialog.select("Subtitle Button Behavior", choices)

            if ret >= 0:
                    value = choices[ret]
                    xbmc.executebuiltin(f"Skin.SetString(OSDSubtitleButtonMode,{value})")
            return


    # -------------------------------------------------
    # Force Close Kodi
    # -------------------------------------------------
    if mode == "force_close":
        from modules.custom_actions import force_close

        return force_close()


    # -------------------------------------------------
    # Enable/Disable kodi splash
    # -------------------------------------------------
    if mode == "splash_on":
        from modules.custom_actions import splash, addon_icon
        dialog.notification('Finder Plus', 'Splash Enabled!', addon_icon, 3000)
        return splash('true')

    if mode == "splash_off":
        from modules.custom_actions import splash, addon_icon
        dialog.notification('Finder Plus', 'Splash Disabled!', addon_icon, 3000)
        return splash('false')


    # -------------------------------------------------
    # Tools Menu
    # -------------------------------------------------
    # Clear Thumbnails/Packages
    if mode == "clear_thumbnails":
        from modules.custom_actions import clear_thumbnails

        return clear_thumbnails()

    if mode == "clear_pkgs":
        from modules.custom_actions import clear_packages

        return clear_packages()


    # Configure Video Cache Settings
    if mode == "advanced_set":
        from modules.custom_actions import advanced_settings

        return advanced_settings()


    # Backup & Restore Custom Configs
    if mode == "backup_config":
        from modules.backup_restore import backup_config

        return backup_config()

    if mode == "restore_config":
        from modules.backup_restore import restore_config

        return restore_config()


    # Import & Export Custom Configs
    if mode == "import_config":
        from modules.backup_restore import import_config

        return import_config()

    if mode == "export_config":
        from modules.backup_restore import export_config

        return export_config()

    
    # Backup & Restore GUI settings
    if mode == "backup_gui":
        from modules.backup_restore import backup_gui

        return backup_gui()

    if mode == "restore_gui":
        from modules.backup_restore import restore_gui

        return restore_gui()


    # Import/Export GUI Settings
    if mode == "import_gui":
        from modules.backup_restore import import_backup

        return import_backup("gui_bkup", "guisettings.xml", "GUI settings")

    if mode == "export_gui":
        from modules.backup_restore import export_backup

        return export_backup("gui_bkup", "GUI settings")


    # Backup & Restore Favourites
    if mode == "backup_favs":
        from modules.backup_restore import backup_favs
        
        return backup_favs()

    if mode == "restore_favs":
        from modules.backup_restore import restore_favs
        
        return restore_favs()


    # Import/Export Favourites
    if mode == "import_favs":
        from modules.backup_restore import import_backup

        return import_backup("favs_bkup", "favourites.xml", "favourites")

    if mode == "export_favs":
        from modules.backup_restore import export_backup

        return export_backup("favs_bkup", "favourites")


    # Restore default GUI & Skin settings
    if mode == "restore_gui_dflt":
            from modules.backup_restore import restore_gui

            kodi_version = xbmc.getInfoLabel("System.BuildVersion")

            if kodi_version.startswith("22"):
                    saved_defaults = translatePath("special://skin/resources/gui_skin_dflt/K22/")
            elif kodi_version.startswith("21"):
                    saved_defaults = translatePath("special://skin/resources/gui_skin_dflt/K21/")
            else:
                    dialog.notification("Finder Plus", "Unsupported Kodi version.", xbmcgui.NOTIFICATION_ERROR, 3000)
                    return

            return restore_gui(saved_defaults)

    if mode == "restore_skin_dflt":
            from modules.backup_restore import restore_skin

            saved_defaults = translatePath("special://skin/resources/gui_skin_dflt/skin.finder/")

            return restore_skin(saved_defaults)

        
    # Set Pre-Made Configurations
    if mode == "pre_config":
        xbmc.executebuiltin("ActivateWindow(1158)")
        return

    if mode =="addon_not_installed":
        from modules.backup_restore import preconfig_addon_notinstalled

        return preconfig_addon_notinstalled(_get("addon"))
    
    if mode == "apply_pre_config":
        from modules.backup_restore import run_pre_config_mode

        return run_pre_config_mode(_get("config"))


    # Focus settings
    if mode == "tmdbh_mdblist_api":
        from modules.custom_actions import tmdbh_mdblist_api

        return tmdbh_mdblist_api()

    if mode == "rurl_settings_rd":
        from modules.custom_actions import rurl_settings_rd

        return rurl_settings_rd()

    if mode == "rurl_settings_pm":
        from modules.custom_actions import rurl_settings_pm

        return rurl_settings_pm()

    if mode == "rurl_settings_ad":
        from modules.custom_actions import rurl_settings_ad

        return rurl_settings_ad()
