"""
	Fenomscrapers Module
"""

from newfsscrapers.modules.control import addonPath, addonVersion, joinPath
from newfsscrapers.modules.textviewer import TextViewerXML


def get():
	newfsscrapers_path = addonPath()
	newfsscrapers_version = addonVersion()
	changelogfile = joinPath(newfsscrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]newfsscrapers -  v%s - ChangeLog[/B]' % newfsscrapers_version
	windows = TextViewerXML('textviewer.xml', newfsscrapers_path, heading=heading, text=text)
	windows.run()
	del windows
