"""
	Fenomscrapers Module
"""

from newfsscrapers.modules.control import addonPath, addonVersion, joinPath
from newfsscrapers.modules.textviewer import TextViewerXML


def get(file):
	newfsscrapers_path = addonPath()
	newfsscrapers_version = addonVersion()
	helpFile = joinPath(newfsscrapers_path, 'resources', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]newfsscrapers -  v%s - %s[/B]' % (newfsscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', newfsscrapers_path, heading=heading, text=text)
	windows.run()
	del windows
