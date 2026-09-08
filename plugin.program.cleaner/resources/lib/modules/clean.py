import os
import shutil
import time
import xbmc
import xbmcgui
import xbmcvfs

from .addonvar import addon_name, addon_icon


def _translate(path):
    try:
        return xbmcvfs.translatePath(path)  # Kodi 19+
    except Exception:
        return xbmc.translatePath(path)     # legacy fallback


def _log(msg):
    try:
        xbmc.log('%s: %s' % (addon_name, msg), xbmc.LOGINFO)
    except Exception:
        pass


user_path = _translate('special://home/userdata')
cache_path = _translate('special://home/cache')
temp_path = _translate('special://temp')
database_path = _translate('special://database')


def _purge_tree(path, skip_files=None, skip_dirs=None):
    skip_files = set(skip_files or [])
    skip_dirs = set(skip_dirs or [])

    if not path or not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path):
        for f in files:
            if f in skip_files:
                continue
            fp = os.path.join(root, f)
            try:
                os.unlink(fp)
            except Exception as e:
                _log('Failed deleting file %s: %s' % (fp, e))

        for d in dirs:
            if d in skip_dirs:
                continue
            dp = os.path.join(root, d)
            try:
                shutil.rmtree(dp, ignore_errors=True)
            except Exception as e:
                _log('Failed deleting dir %s: %s' % (dp, e))


def clear_cache(show_notification=True):
    keep = set([
        'xbmc.log', 'xbmc.old.log',
        'kodi.log', 'kodi.old.log',
        'archive_cache', 'commoncache.db', 'commoncache.socket', 'temp'
    ])

    _purge_tree(cache_path, skip_files=keep, skip_dirs=set(['archive_cache', 'temp']))
    _purge_tree(temp_path, skip_files=keep, skip_dirs=set(['archive_cache', 'temp']))

    if show_notification:
        xbmcgui.Dialog().notification(addon_name, 'Cache cleared', addon_icon, 3000)


def clear_packages(show_notification=True):
    packages_path = _translate('special://home/addons/packages')
    _purge_tree(packages_path)

    if show_notification:
        xbmcgui.Dialog().notification(addon_name, 'Packages cleared', addon_icon, 3000)


def clear_thumbnails(show_notification=True):
    confirm = xbmcgui.Dialog().yesno(
        addon_name,
        'This will delete all thumbnails and texture database.\nKodi will close when done.\n\nContinue?',
        yeslabel='OK',
        nolabel='Cancel'
    )
    if not confirm:
        return False

    thumbs_userdata = os.path.join(user_path, 'Thumbnails')
    thumbs_special = _translate('special://thumbnails')

    try:
        _purge_tree(thumbs_special)
    except Exception as e:
        _log('Failed wiping special thumbnails path: %s' % e)

    try:
        _purge_tree(thumbs_userdata)
    except Exception as e:
        _log('Failed wiping userdata thumbnails path: %s' % e)

    try:
        tex_db = os.path.join(database_path, 'Textures13.db')
        if os.path.exists(tex_db):
            os.unlink(tex_db)
    except Exception as e:
        _log('Failed deleting Textures13.db: %s' % e)

    xbmcgui.Dialog().ok(addon_name, 'Thumbnail cleanup complete.\nKodi will now close.')
    xbmc.executebuiltin('Quit')
    return True


def run_startup_clean_if_enabled():
    try:
        import xbmcaddon
        a = xbmcaddon.Addon()

        if a.getSetting('startupclean_enable') != 'true':
            return

        ran_any = False

        if a.getSetting('startupclean_cache') == 'true':
            clear_cache(show_notification=False)
            ran_any = True

        if a.getSetting('startupclean_packages') == 'true':
            clear_packages(show_notification=False)
            ran_any = True

        if ran_any:
            xbmcgui.Dialog().notification(addon_name, 'Startup clean completed', addon_icon, 3000)
            _log('Startup clean completed.')
    except Exception as e:
        _log('run_startup_clean_if_enabled failed: %s' % e)


def run_scheduled_clean_if_due():
    """
    Scheduled AutoClean:
    - Detects autoclean_enable toggle transitions and resets lastrun=0 on change.
    - Runs first-time when lastrun==0 (hour-gated, unless hour=-1).
    - Runs scheduled by days/hour after that.
    - Never touches thumbnails.
    - Updates lastrun ONLY after successful actions.
    - Shows completion notification.
    """
    try:
        import xbmcaddon
        a = xbmcaddon.Addon()

        def _b(k, d=False):
            v = a.getSetting(k)
            return (v.lower() == 'true') if v else d

        def _i(k, d=0):
            try:
                return int(a.getSetting(k))
            except Exception:
                return d

        # legacy cleanup
        try:
            if a.getSetting('autoclean_thumbs') != '':
                a.setSetting('autoclean_thumbs', '')
        except Exception:
            pass

        enabled = _b('autoclean_enable', False)

        # Track transitions and reset lastrun when enable state changes.
        prev = a.getSetting('autoclean_prev_enable')
        curr = 'true' if enabled else 'false'

        if prev == '':
            a.setSetting('autoclean_prev_enable', curr)
        elif prev != curr:
            a.setSetting('autoclean_lastrun', '0')
            a.setSetting('autoclean_prev_enable', curr)
            _log('AutoClean enable toggled (%s -> %s); reset lastrun to 0.' % (prev, curr))

        # If disabled, stop here.
        if not enabled:
            return

        now = int(time.time())
        last_run = _i('autoclean_lastrun', 0)
        days = max(1, _i('autoclean_days', 7))

        # -1 means "any hour"
        hour = _i('autoclean_hour', -1)
        if hour < -1 or hour > 23:
            hour = -1

        now_hour = time.localtime(now).tm_hour

        first_run_due = (last_run <= 0)
        schedule_due = False if first_run_due else (now >= (last_run + (days * 86400)))

        # hour gate (only enforce when a specific hour is set)
        if hour != -1 and now_hour < hour:
            return

        if not first_run_due and not schedule_due:
            return

        did_clean = False
        actions = []

        if _b('autoclean_packages', True):
            clear_packages(show_notification=False)
            did_clean = True
            actions.append('Packages')

        if _b('autoclean_cache', True):
            clear_cache(show_notification=False)
            did_clean = True
            actions.append('Cache')

        if not did_clean:
            _log('AutoClean due but no actions enabled; lastrun unchanged.')
            return

        # LAST step only
        a.setSetting('autoclean_lastrun', str(now))

        action_text = ' + '.join(actions)
        if first_run_due:
            msg = f'AutoClean complete (first run): {action_text}'
            _log('AutoClean first run completed; lastrun=%s actions=%s' % (now, action_text))
        else:
            msg = f'AutoClean complete: {action_text}'
            _log('AutoClean scheduled run completed; lastrun=%s actions=%s' % (now, action_text))

        xbmcgui.Dialog().notification(addon_name, msg, addon_icon, 3500)

    except Exception as e:
        _log('run_scheduled_clean_if_due failed: %s' % e)