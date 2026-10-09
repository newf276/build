"""Track query changes while results stay open; retain five selectable searches."""
import json
import xbmc
import xbmcgui

CAPACITY = 5
RUNNING = 'Finder.HistoryTracker.Running'
RECOVERED_QUERIES = ['Wondwer Woman', 'Wonder Woman', 'Leanne', 'Silo', 'spiderman']


def updated_history(query, slots):
    if not query.strip():
        return [value for value in slots if value][:CAPACITY]
    return ([query] + [value for value in slots if value and value != query])[:CAPACITY]


def save_query(query, refresh=True):
    if not query.strip():
        return False
    slots = [xbmc.getInfoLabel('Skin.String(SearchHistory.%d)' % i) for i in range(1, CAPACITY + 1)]
    history = updated_history(query, slots)
    changed = slots != history + [''] * (CAPACITY - len(history))
    for i in range(1, CAPACITY + 1):
        value = history[i - 1] if i <= len(history) else ''
        if slots[i - 1] != value:
            xbmc.executebuiltin('Skin.SetString(SearchHistory.%d,%s)' % (i, json.dumps(value, ensure_ascii=False)), True)
    count = str(len(history))
    if xbmc.getInfoLabel('Skin.String(SearchHistoryCount)') != count:
        xbmc.executebuiltin('Skin.SetString(SearchHistoryCount,%s)' % count, True)
        changed = True
    if changed and refresh:
        xbmc.executebuiltin('Container.Refresh')
        xbmc.log('Finder history: saved %d recent searches' % len(history), xbmc.LOGDEBUG)
    return changed


def main():
    if xbmc.getSkinDir() != 'skin.finder' or xbmc.getCondVisibility('Skin.HasSetting(Finder.SubmitHistory20)'):
        return
    home = xbmcgui.Window(10000)
    if home.getProperty(RUNNING):
        return
    home.setProperty(RUNNING, 'true')
    monitor = xbmc.Monitor()
    last_query = None
    try:
        # One-time recovery of submitted terms verified in the user's test log.
        # Never repeat this after Clear History or overwrite a newly populated list.
        if not xbmc.getCondVisibility('Skin.HasSetting(Finder.HistoryRecovered15)'):
            populated = sum(bool(xbmc.getInfoLabel('Skin.String(SearchHistory.%d)' % i)) for i in range(1, CAPACITY + 1))
            if populated <= 1:
                recovered_changed = False
                for recovered in RECOVERED_QUERIES:
                    recovered_changed = save_query(recovered, refresh=False) or recovered_changed
                if recovered_changed:
                    xbmc.executebuiltin('Container.Refresh')
            xbmc.executebuiltin('Skin.SetBool(Finder.HistoryRecovered15)', True)
        # Container.Refresh does not reload the window; observe subsequent submissions.
        while not monitor.abortRequested() and xbmc.getCondVisibility('Window.IsActive(1121)') and not xbmc.getCondVisibility('Skin.HasSetting(Finder.SubmitHistory20)'):
            query = xbmc.getInfoLabel('Skin.String(SearchInput)')
            if query != last_query:
                last_query = query
                save_query(query)
            if monitor.waitForAbort(0.2):
                break
    finally:
        home.clearProperty(RUNNING)


if __name__ == '__main__':
    main()
