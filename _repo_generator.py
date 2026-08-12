""" 
    Put this script in the root folder of your repo and it will
    zip up all addon folders, create a new zip in your zips folder
    and then update the md5 and addons.xml file
"""

import hashlib
import os
import shutil
import sys
import zipfile
from xml.etree import ElementTree

SCRIPT_VERSION = 5
KODI_VERSIONS = ["krypton", "leia", "matrix", "nexus", "omega", "22", "repo"]
IGNORE = [
    ".git",
    ".github",
    ".gitignore",
    ".DS_Store",
    "thumbs.db",
    ".idea",
    "venv",
]
_COLOR_ESCAPE = "\x1b[{}m"
_COLORS = {
    "black": "30",
    "red": "31",
    "green": "4;32",
    "yellow": "3;33",
    "blue": "34",
    "magenta": "35",
    "cyan": "1;36",
    "grey": "37",
    "endc": "0",
}


def _setup_colors():
    """Return True if terminal supports color, False otherwise."""
    def vt_codes_enabled_in_windows_registry():
        try:
            import winreg
        except ImportError:
            return False
        try:
            # Changed KEY_ALL_ACCESS to KEY_READ to avoid permission issues
            reg_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Console", access=winreg.KEY_READ
            )
            reg_key_value, _ = winreg.QueryValueEx(reg_key, "VirtualTerminalLevel")
            return reg_key_value == 1
        except:
            return False

    def is_a_tty():
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def legacy_support():
        console = 0
        color = 0
        if sys.platform in ["linux", "linux2", "darwin"]:
            pass
        elif sys.platform == "win32":
            color = os.system("color")
            from ctypes import windll
            k = windll.kernel32
            console = k.SetConsoleMode(k.GetStdHandle(-11), 7)
        return any([color == 1, console == 1])

    return any([
        is_a_tty(),
        sys.platform != "win32",
        "ANSICON" in os.environ,
        "WT_SESSION" in os.environ,
        os.environ.get("TERM_PROGRAM") == "vscode",
        vt_codes_enabled_in_windows_registry(),
        legacy_support(),
    ])


_SUPPORTS_COLOR = _setup_colors()


def color_text(text, color):
    """Return an ANSI-colored string, if supported."""
    return (
        '{}{}{}'.format(
            _COLOR_ESCAPE.format(_COLORS[color]),
            text,
            _COLOR_ESCAPE.format(_COLORS["endc"]),
        )
        if _SUPPORTS_COLOR else text
    )


def convert_bytes(num):
    """Convert bytes to human-readable strings."""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


class Generator:
    """Generates a new addons.xml file and its md5 hash file."""
    def __init__(self, release):
        self.release_path = os.path.abspath(release)
        self.zips_path = os.path.join(self.release_path, "zips")

        if not os.path.exists(self.zips_path):
            os.makedirs(self.zips_path)

        self._remove_binaries()

        addons_xml_path = os.path.join(self.zips_path, "addons.xml")
        md5_path = os.path.join(self.zips_path, "addons.xml.md5")

        if self._generate_addons_file(addons_xml_path):
            print("Successfully updated {}".format(color_text(addons_xml_path, 'yellow')))
            if self._generate_md5_file(addons_xml_path, md5_path):
                print("Successfully updated {}".format(color_text(md5_path, 'yellow')))

    def _remove_binaries(self):
        """Removes compiled Python files before packing."""
        for parent, dirnames, filenames in os.walk(self.release_path):
            for fn in filenames:
                if fn.lower().endswith(("pyo", "pyc")):
                    compiled = os.path.join(parent, fn)
                    try:
                        os.remove(compiled)
                    except:
                        pass
            # Filter directories in-place to prevent walking down __pycache__
            for dir_name in list(dirnames):
                if "pycache" in dir_name.lower():
                    compiled = os.path.join(parent, dir_name)
                    try:
                        shutil.rmtree(compiled)
                        dirnames.remove(dir_name)
                    except:
                        pass

    def _create_zip(self, addon_id, version):
        """Creates a zip file in the zips directory for the given addon."""
        addon_folder = os.path.join(self.release_path, addon_id)
        zip_folder = os.path.join(self.zips_path, addon_id)
        
        if not os.path.exists(zip_folder):
            os.makedirs(zip_folder)

        final_zip = os.path.join(zip_folder, "{0}-{1}.zip".format(addon_id, version))
        
        # Force overwrite or skip if existing can be toggled here
        zip_file = zipfile.ZipFile(final_zip, "w", compression=zipfile.ZIP_DEFLATED)
        root_len = len(os.path.dirname(os.path.abspath(addon_folder)))

        for root, dirs, files in os.walk(addon_folder):
            # In-place filtering modifications fix item skipping
            dirs[:] = [d for d in dirs if d not in IGNORE]
            
            filtered_files = []
            for f in files:
                if not any(f.startswith(ign) for ign in IGNORE):
                    filtered_files.append(f)

            archive_root = os.path.abspath(root)[root_len:]

            for f in filtered_files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.normpath(os.path.join(archive_root, f))
                zip_file.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)

        zip_file.close()
        size = convert_bytes(os.path.getsize(final_zip))
        print("Zip created for {} ({}) - {}".format(
            color_text(addon_id, 'cyan'),
            color_text(version, 'green'),
            color_text(size, 'yellow'),
        ))

    def _copy_meta_files(self, addon_id, version):
        """Copy metadata and art assets to the target zips subfolder."""
        addon_dir = os.path.join(self.release_path, addon_id)
        target_dir = os.path.join(self.zips_path, addon_id)
        
        copyfiles = ["addon.xml", "icon.png", "fanart.jpg", "changelog.txt"]
        
        try:
            tree = ElementTree.parse(os.path.join(addon_dir, "addon.xml"))
            root = tree.getroot()
            for ext in root.findall("extension"):
                if ext.get("point") in ["xbmc.addon.metadata", "kodi.addon.metadata"]:
                    assets = ext.find("assets")
                    if assets is not None:
                        for art in assets:
                            if art.text:
                                copyfiles.append(os.path.normpath(art.text))
        except Exception:
            pass # Use defaults if XML fails to read assets

        for file in set(copyfiles):
            src = os.path.join(addon_dir, file)
            dest = os.path.join(target_dir, file)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(src, dest)

    def _generate_addons_file(self, addons_xml_path):
        """Compiles all distinct addon.xml structures into a single file."""
        root = ElementTree.Element("addons")
        
        for addon_id in os.listdir(self.release_path):
            addon_dir = os.path.join(self.release_path, addon_id)
            xml_path = os.path.join(addon_dir, "addon.xml")
            
            if addon_id in IGNORE or addon_id == "zips" or not os.path.isdir(addon_dir):
                continue
                
            if os.path.exists(xml_path):
                try:
                    tree = ElementTree.parse(xml_path)
                    addon_root = tree.getroot()
                    version = addon_root.get("version")
                    
                    # Core actions
                    self._create_zip(addon_id, version)
                    self._copy_meta_files(addon_id, version)
                    
                    root.append(addon_root)
                except Exception as e:
                    print(color_text(f"Error packing {addon_id}: {e}", 'red'))

        # Write out XML master file
        try:
            indent(root) # Clean layout formatting
            new_tree = ElementTree.ElementTree(root)
            new_tree.write(addons_xml_path, encoding="utf-8", xml_declaration=True)
            return True
        except Exception as e:
            print(color_text(f"Failed writing XML file: {e}", "red"))
            return False

    def _generate_md5_file(self, xml_path, md5_path):
        """Generates MD5 hash check file for verification lookup."""
        try:
            with open(xml_path, "rb") as f:
                md5_hash = hashlib.md5(f.read()).hexdigest()
            with open(md5_path, "w", encoding="utf-8") as f:
                f.write(md5_hash)
            return True
        except Exception as e:
            print(color_text(f"Failed to generate MD5: {e}", "red"))
            return False


def indent(elem, level=0):
    """Helper to pretty-print XML trees across modern Python engines."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == "__main__":
    # Executes code against current execution folder path target
    Generator(os.getcwd())
