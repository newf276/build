# Finder Skin 1.1.03

Finder Skin is the companion skin for plugin.video.finder, with Finder-native menus, Search, widgets, ratings and information windows.

Use the supplied Finder Add-on 1.0.08.12 with Finder Skin 1.1.03. Keep existing userdata and accounts when upgrading. See SETUP_GUIDE.txt and changelog.txt for current guidance; earlier release sections below are historical.

Finder and Finder Skin Setup Guide — 1.0.08

1. Install plugin.video.finder and skin.finder from Newf276's repository or the supplied ZIPs. Both public versions are 1.0.08. Existing higher-numbered test builds may need manual ZIP selection. Restart Kodi after installing; keep your settings and accounts.
2. Activate Finder Skin, then choose Finder + Finder Skin from Tools -> Finder Interface Setup. Standalone Finder is also supported. The integrated features do not require a separate Finder/FENtastic helper.
3. Choose Finder, Trakt or PunchPlay as Primary Tracker. Authorize the chosen service. PunchPlay first-run setup synchronizes watched history and supported lists; keep Repair PunchPlay Watched Database for repair when needed.
4. In Finder -> My Lists, select Authorize TMDb, Authorize Trakt or Authorize PunchPlay for a signed-out account. Yes launches its existing sign-in flow. No suppresses automatic recovery reminders; a manual selection can ask again. Leave and reopen My Lists after signing in.
5. Choose a Finder Skin Pre-Config matching your tracker and preferred home layout, then customize menus/widgets in Skin Settings. The home paths remain Finder-native.
6. Default home WideInfoWall layout is under Skin Settings -> Widgets. Search stays Poster View 54; movie/TV lists use List View 50 and normal navigation uses Wide List View 55. Category pill sizing is preserved.
7. Open First Unwatched Episode is enabled by default under Finder Settings -> Content -> General. Supported shows open to and focus the first aired unwatched episode while watched episodes remain available. Disable it for normal browsing.
8. Use ExtendedInfo from Finder's context menu or Kodi Info for Finder items in Finder Skin. Play/Browse, Options, Sync and Play Trailer use Finder capabilities. Actor biographies, credits, related titles, seasons, videos and artwork are available where metadata exists.
9. Native Finder trailers do not require the YouTube add-on. MPEG-DASH is disabled; progressive MP4/HLS playback is used. Individual videos can be restricted or unavailable.
10. Enable top-right weather in Skin Settings and configure Kodi's weather service/location using the provided shortcut.
11. MDbList provides ratings only, not watched tracking. The shared ratings key is included automatically. Skin Settings -> Ratings / Trailers lets you enter a personal key or restore the shared key.
12. Use Finder Tools for cache maintenance, account settings, Tips for Use and log upload. Clear Progress is available on supported In Progress items. Do not clear databases merely to install this release. If troubleshooting, confirm both versions and provide a debug log.
13. Tools also provides two reset levels: yellow Reset Finder Settings to Defaults restores preferences while preserving accounts, API credentials, setup state, watched data, personal lists and caches; red Factory Reset Finder is destructive and returns Finder to the first-run Welcome flow after the next full Kodi restart.

Credits: Angelitto (TMDbMovies ExtendedInfo, adapted with permission); silentbob2 (Forge); Tikipeter (Fen/Fen Light lineage); ivarbrandt and Zaxxon709 (skin lineage); Team Kodi (Kodi/Estuary). Existing licenses and notices remain included.

## Watched and Progress Indicators

Supported Finder views use four status states: outlined circle with center dot for untouched items, half-filled circle for partially watched TV shows, eye for an exact movie/episode with a stored resume point, and the existing circle/check for completed items. Watched/total TV episode counts remain visible on the supported Home layout.

Artwork and Playback Defaults

- Enabled top-bar weather and WideInfoWall home widgets by default.
- Added Artwork background choices: Default 1 (redblur.jpg, black), Default 2 (blueblur.jpg), or Select Your Own.
- Kept only the two bundled backgrounds and added blue/greyscale Kodi logo choices.
- Disabled media fanart backgrounds by default; users can still enable them.
- Removed skin/weather/genre fanart-pack selection, pack rendering and raindrop backgrounds.
- Included the shared MDbList ratings key automatically, with personal-key entry and a Restore Shared Key option.
- Enabled OSD auto close (5 seconds), bottom seek bar, video info on pause and stream filename on pause.
- Applied these revised defaults once on first startup; later user choices are preserved.

Tip: Configure a Kodi weather service to populate the enabled top-bar weather display. Choose your background and blue/greyscale Kodi logo under Skin Settings -> Artwork. Personal images must remain accessible to Kodi.
