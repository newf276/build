import json
from os import path
import xbmcaddon

from .addonvar import texts_path, addon_icon, addon_fanart
from .utils import add_dir
from .colors import colors

COLOR1 = colors.color_text1
COLOR2 = colors.color_text2

AUTH_FILE = path.join(texts_path, 'authorize.json')

def open_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def _load_auth():
    try:
        data = json.loads(open_file(AUTH_FILE))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {"supported_addons": []}

def _is_installed(addon_id):
    try:
        xbmcaddon.Addon(addon_id)
        return True
    except Exception:
        return False

def authorize_menu():
    data = _load_auth()
    addons = data.get('supported_addons', [])

    add_dir(COLOR1('<><> [B]Authorize Services[/B] <><>'),
            '', '', addon_icon, addon_fanart, COLOR1('***Authorize Services***'))

    for addon in addons:
        addon_id = addon.get('id', '')
        if not addon_id or not _is_installed(addon_id):
            continue
        name = addon.get('name', addon_id)
        add_dir(COLOR2(name), '', 27, addon_icon, addon_icon, COLOR2(name), name2=addon_id)

def authorize_submenu(name, icon):
    data = _load_auth()
    addons = data.get('supported_addons', [])

    target = None
    for addon in addons:
        if addon.get('id') == name:
            target = addon
            break
    if not target:
        return

    services = target.get('services', {})
    order = ['mdblist', 'tmdb', 'trakt', 'alldebrid', 'premiumize', 'realdebrid', 'torbox']

    for key in order:
        actions = services.get(key, [])
        for action in actions:
            typ = action.get('type')
            value = action.get('value')
            label = action.get('label', 'Authorize')
            if not typ or not value:
                continue

            if typ == 'plugin':
                cmd = 'RunPlugin({})'.format(value)
            elif typ == 'builtin':
                cmd = value
            else:
                continue

            add_dir(COLOR2(label), cmd, 25, icon or addon_icon, icon or addon_icon, label, isFolder=False)