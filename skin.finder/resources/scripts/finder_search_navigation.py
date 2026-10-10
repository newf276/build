"""Position search sections explicitly; never scroll the entire results panel."""
import sys
import xbmc
import xbmcgui

ROWS = (27011, 27012, 27013, 27017, 270171)
HEIGHTS = {27011:667, 27012:667, 27013:667, 27017:305, 270171:667}

def next_row(current, direction, available):
    if not available:
        return 804
    if direction in ('enter', 'reset', 'init') or current not in available:
        return available[0]
    i = available.index(current)
    if direction == 'down':
        return available[(i + 1) % len(available)]
    return available[i - 1] if i else 804

def positions(current, available):
    """Keep the active row complete; following sections can preview beneath it."""
    result = {r:(0, False) for r in ROWS}
    if current not in available:
        current = available[0] if available else 0
    if not current:
        return result
    y = 0
    for row in available[available.index(current):]:
        result[row] = (y, y < 890)
        y += HEIGHTS[row]
    return result

def populated():
    return [r for r in ROWS if int(xbmc.getInfoLabel('Container(%d).NumItems' % r) or '0') > 0]

def place(current, available):
    window = xbmcgui.Window(11121)
    if current in available:
        window.setProperty('finder.search.anchor', str(current))
    for row, (y, show) in positions(current, available).items():
        window.setProperty('finder.search.%d.y' % row, str(y if show else 2000))
        window.setProperty('finder.search.%d.show' % row, 'true' if show else 'false')

def watch_results():
    """Observe late provider arrivals until this search window closes."""
    window = xbmcgui.Window(11121)
    import time
    token = str(time.time_ns())
    window.setProperty('finder.search.watcher', token)
    window.setProperty('finder.search.anchor', str(ROWS[0]))
    place(ROWS[0], list(ROWS))
    monitor = xbmc.Monitor()
    previous = None
    while xbmc.getCondVisibility('Window.IsActive(1121)') and window.getProperty('finder.search.watcher') == token:
        available = populated()
        anchor = int(window.getProperty('finder.search.anchor') or ROWS[0])
        signature = (tuple(available), anchor)
        if signature != previous:
            place(anchor, available)
            previous = signature
        if monitor.waitForAbort(0.2):
            break
    if window.getProperty('finder.search.watcher') == token:
        window.clearProperty('finder.search.watcher')

def main():
    if not xbmc.getCondVisibility('Window.IsActive(1121)'):
        return
    direction = sys.argv[1] if len(sys.argv) > 1 else 'enter'
    current = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    if direction == 'init':
        watch_results()
        return
    if direction == 'reset':
        xbmc.sleep(350)
    available = populated()
    target = current if direction == 'position' else next_row(current, direction, available)
    place(target, available)
    if direction not in ('position', 'init'):
        xbmc.sleep(100)  # Let Kodi apply row positioning before transferring focus.
        xbmc.executebuiltin('SetFocus(%d%s)' % (target, ',0,absolute' if direction in ('reset','enter') or target < current else ''))

if __name__ == '__main__':
    main()
