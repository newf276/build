# -*- coding: utf-8 -*-
from caches.settings_cache import default_setting_values, get_setting, set_setting
from modules.kodi_utils import get_property, logger, translate_path


def tmdb_api_key():
	return get_setting("finder.tmdb_api", "")


def trakt_client():
	return get_setting("finder.trakt.client", "")


def trakt_secret():
	return get_setting("finder.trakt.secret", "")


def trakt_user_active():
	return get_setting("finder.trakt.user", "empty_setting") not in (None, "empty_setting", "")


def tmdblist_user_active():
	return get_setting("finder.tmdb.account_id", "empty_setting") not in (None, "empty_setting", "")


def results_format():
	results_window_numbers_dict = {"List": 2000, "Rows": 2001, "WideList": 2002}
	window_format = str(get_setting("finder.results.list_format", "List"))
	if window_format not in results_window_numbers_dict:
		window_format = "List"
		set_setting("results.list_format", window_format)
	window_number = results_window_numbers_dict[window_format]
	return window_format.lower(), window_number


def store_resolved_to_cloud(debrid_service, pack):
	setting_value = int(get_setting("finder.store_resolved_to_cloud.%s" % debrid_service.lower(), "0"))
	return setting_value in (1, 2) if pack else setting_value == 1


def enabled_debrids_check(debrid_service):
	if not get_setting("finder.%s.enabled" % debrid_service) == "true":
		return False
	return authorized_debrid_check(debrid_service)


def authorized_debrid_check(debrid_service):
	if get_setting("finder.%s.token" % debrid_service) in (None, "", "empty_setting"):
		return False
	return True


def easynews_active():
	if get_setting("finder.provider.easynews", "false") == "true":
		easynews_status = easynews_authorized()
	else:
		easynews_status = False
	return easynews_status


def easynews_authorized():
	easynews_user = get_setting("finder.easynews.username", "empty_setting")
	easynews_password = get_setting("finder.easynews.password", "empty_setting")
	if easynews_user in ("empty_setting", "") or easynews_password in ("empty_setting", ""):
		return False
	return True


def easynews_language_filter():
	enabled = get_setting("finder.easynews.filter_lang") == "true"
	if enabled:
		filters = get_setting("finder.easynews.lang_filters").split(", ")
	else:
		filters = []
	return enabled, filters


def easynews_playback_method(query):
	method = int(get_setting("finder.easynews.playback_method", "0"))
	queries = {
		"retry": lambda: method in (1, 3),
		"non_seek": lambda: method in (2, 3),
		"direct_play": lambda: method in (2, 3) and get_setting("finder.easynews.playback_method_limited", "false") != "true",
	}
	return queries[query]()


def easynews_playback_method_retries():
	return int(get_setting("finder.easynews.playback_method_retries", "1")) + 1


def playback_key():
	return get_setting("finder.playback_key", "0")


def playback_settings():
	return (int(get_setting("finder.playback.watched_percent", "90")), int(get_setting("finder.playback.resume_percent", "5")))


def limit_resolve():
	return get_setting("finder.playback.limit_resolve", "false") == "true"


def movies_directory():
	return translate_path(get_setting("finder.movies_directory"))


def tv_show_directory():
	return translate_path(get_setting("finder.tv_shows_directory"))


def download_directory(media_type):
	download_directories_dict = {
		"movie": "finder.movie_download_directory",
		"episode": "finder.tvshow_download_directory",
		"thumb_url": "finder.image_download_directory",
		"image_url": "finder.image_download_directory",
		"image": "finder.image_download_directory",
		"premium": "finder.premium_download_directory",
		None: "finder.premium_download_directory",
		"None": False,
	}
	return translate_path(get_setting(download_directories_dict[media_type]))


def show_unaired_watchlist():
	return get_setting("finder.show_unaired_watchlist", "true") == "true"


def lists_cache_duraton():
	return int(get_setting("finder.lists_cache_duraton", "48"))


def auto_start_finder():
	return get_setting("finder.auto_start_finder", "false") == "true"


def source_folders_directory(media_type, source):
	setting = "finder.%s.movies_directory" % source if media_type == "movie" else "finder.%s.tv_shows_directory" % source
	if get_setting(setting) not in ("", "None", None):
		return translate_path(get_setting(setting))
	else:
		return False


def avoid_episode_spoilers():
	return get_setting("finder.avoid_episode_spoilers", "false") == "true"


def paginate(is_home):
	paginate_lists = int(get_setting("finder.paginate.lists", "0"))
	if is_home:
		return paginate_lists in (2, 3)
	else:
		return paginate_lists in (1, 3)


def page_limit(is_home):
	return int(get_setting({True: "finder.paginate.limit_widgets", False: "finder.paginate.limit_addon"}[is_home], "20"))


def quality_filter(setting):
	return get_setting("finder.%s" % setting).split(", ")


def sort_to_top_filter(autoplay):
	return {0: False, 1: False if autoplay else True, 2: True if autoplay else False, 3: True}[int(get_setting("finder.filter.sort_to_top", "0"))]


def audio_filters():
	setting = get_setting("finder.filter_audio")
	if setting in ("empty_setting", ""):
		return []
	return setting.split(", ")


def preferred_filters():
	setting = get_setting("finder.filter.preferred_filters")
	if setting in ("empty_setting", ""):
		return []
	return setting.split(", ")


def include_prerelease_results():
	return int(get_setting("finder.filter.include_prerelease", "0")) == 0


def auto_enable_subs():
	return get_setting("finder.playback.auto_enable_subs", "false") == "true"


def stingers_show():
	return get_setting("finder.stinger_alert.show", "false") == "true"


def stingers_use_chapters():
	return get_setting("finder.stinger_alert.use_chapters", "false") == "true"


def stingers_percentage():
	return int(get_setting("finder.stinger_alert.window_percentage", "90"))


def skip_markers_enabled():
	return get_setting("finder.skip_markers.enabled", "false") == "true"


def skip_markers_types():
	types = []
	if get_setting("finder.skip_markers.intro", "true") == "true":
		types.append("intro")
	if get_setting("finder.skip_markers.recap", "true") == "true":
		types.append("recap")
	if get_setting("finder.skip_markers.outro", "true") == "true":
		types.append("outro")
	return tuple(types)


def skip_markers_min_confidence():
	# Stored as an integer percent (0-100) so it edits with the numeric setting picker.
	return int(get_setting("finder.skip_markers.min_confidence", "70")) / 100.0


def skip_markers_min_submissions():
	return int(get_setting("finder.skip_markers.min_submissions", "1"))


def skip_markers_use_chapters():
	return get_setting("finder.skip_markers.use_chapters", "false") == "true"


def skip_markers_aniskip_enabled():
	return get_setting("finder.skip_markers.aniskip", "true") == "true"


def skip_button_duration():
	return int(get_setting("finder.skip_markers.button_duration", "8"))


def include_anime_tvshow():
	return get_setting("finder.include_anime_tvshow", "false") == "true"


def auto_play(media_type):
	return get_setting("finder.auto_play_%s" % media_type, "false") == "true"


def autoplay_next_episode():
	if auto_play("episode") and get_setting("finder.autoplay_next_episode", "false") == "true":
		return True
	else:
		return False


def autoscrape_next_episode():
	if not auto_play("episode") and get_setting("finder.autoscrape_next_episode", "false") == "true":
		return True
	else:
		return False


def autoscrape_confirm():
	return get_setting("finder.autoscrape_confirm", "false") == "true"


def autoplay_prescrape(scrape_provider):
	return get_setting("finder.autoplay.%s" % scrape_provider, "false") == "true"


def auto_nextep_settings(play_type):
	play_type = "autoplay" if play_type == "autoplay_nextep" else "autoscrape"
	window_percentage = 100 - int(get_setting("finder.%s_next_window_percentage" % play_type, "95"))
	use_chapters = get_setting("finder.%s_use_chapters" % play_type, "true") == "true"
	watching_check = int(get_setting("finder.autoplay_watching_check", "3"))
	scraper_time = int(get_setting("finder.results.timeout", "20")) + 20
	if play_type == "autoplay":
		alert_method = int(get_setting("finder.autoplay_alert_method", "0"))
		default_action = {"0": "play", "1": "cancel", "2": "pause"}[get_setting("finder.autoplay_default_action", "1")]
	else:
		alert_method, default_action = "", ""
	return {
		"scraper_time": scraper_time,
		"window_percentage": window_percentage,
		"alert_method": alert_method,
		"default_action": default_action,
		"use_chapters": use_chapters,
		"watching_check": watching_check,
	}


def filter_status(filter_type):
	return int(get_setting("finder.filter.%s" % filter_type, "0"))


def limit_number_quality():
	return int(get_setting("finder.results.limit_number_quality", "0"))


def limit_number_total():
	return int(get_setting("finder.results.limit_number_total", "0"))


def trakt_sync_interval():
	setting = get_setting("finder.trakt.sync_interval", "60")
	interval = int(setting) * 60
	return setting, interval


def lists_sort_order(setting):
	return int(get_setting("finder.sort.%s" % setting, "0"))


def tmdblists_sort_order(setting):
	if setting == "recommendations":
		return None
	return str(get_setting("finder.tmdbsort.%s" % setting, "4"))


def personal_lists_sort_unseen_to_top():
	return get_setting("finder.personal_list.sort_unseen_to_top") == "true"


def personal_lists_unseen_highlight():
	if get_setting("finder.personal_list.highlight_unseen", "false") == "false":
		return None
	return get_setting("finder.personal_list.unseen_highlight", "FF4DDBFF")


def personal_lists_show_author():
	return get_setting("finder.personal_list.show_author", "true") == "true"


def show_specials():
	return get_setting("finder.show_specials", "false") == "true"


def single_ep_unwatched_episodes():
	return get_setting("finder.single_ep_unwatched_episodes", "false") == "true"


def single_ep_display_format(is_external):
	if is_external:
		setting, default = "finder.single_ep_display_widget", "1"
	else:
		setting, default = "finder.single_ep_display", ""
	return int(get_setting(setting, default))


def extras_enable_extra_ratings():
	return get_setting("finder.extras.enable_extra_ratings", "true") == "true"


def extras_enabled_ratings():
	return get_setting("finder.extras.enabled_ratings", "Meta, Tom/Critic, Tom/User, IMDb, TMDb").split(", ")


def extras_enable_item_ratings():
	return get_setting("finder.extras.enable_item_ratings", "false") == "true"


def extras_enable_scrollbars():
	return get_setting("finder.extras.enable_scrollbars", "false")


def extras_enabled():
	setting = get_setting("finder.extras.enabled", "2000,2050,2051,2052,2053,2054,2056,2057,2058,2059,2060,2061,2062")
	if setting in ("", None, "noop", []):
		return []
	split_setting = setting.split(",")
	return [int(i) for i in split_setting]


def extras_order():
	setting = get_setting("finder.extras.order", "2000,2050,2051,2052,2053,2054,2056,2057,2058,2059,2060,2061,2062")
	if setting in ("", None, "noop", []):
		return []
	split_setting = setting.split(",")
	return [int(i) for i in split_setting]


def recommend_service():
	return int(get_setting("finder.recommend_service", "0"))


def recommend_seed():
	return int(get_setting("finder.recommend_seed", "5"))


def tv_progress_location():
	return int(get_setting("finder.tv_progress_location", "0"))


def check_prescrape_sources(scraper, media_type):
	if scraper in ("easynews", "rd_cloud", "pm_cloud", "ad_cloud", "tb_cloud", "folders"):
		return get_setting("finder.check.%s" % scraper) == "true"
	if get_setting("finder.check.%s" % scraper) == "true" and auto_play(media_type):
		return True
	else:
		return False


def external_scraper_info():
	module = get_setting("finder.external_scraper.module")
	if module in ("empty_setting", ""):
		return None, ""
	return module, module.split(".")[-1]


def filter_by_name(scraper):
	if get_property("fs_filterless_search") == "true":
		return False
	return get_setting("finder.%s.title_filter" % scraper, "false") == "true"


def uncached_min_seeders():
	return int(get_setting("finder.results.uncached_min_seeders", "0"))


def size_sort_weighted():
	return get_setting("finder.results.size_sort_weighted", "false") == "true"


def results_sort_order():
	sort_direction = -1 if get_setting("finder.results.size_sort_direction") == "0" else 1
	return (
		lambda k: (k["quality_rank"], k["provider_rank"], sort_direction * k["size_rank"]),  # Quality, Provider, Size
		lambda k: (k["quality_rank"], sort_direction * k["size_rank"], k["provider_rank"]),  # Quality, Size, Provider
		lambda k: (k["provider_rank"], k["quality_rank"], sort_direction * k["size_rank"]),  # Provider, Quality, Size
		lambda k: (k["provider_rank"], sort_direction * k["size_rank"], k["quality_rank"]),  # Provider, Size, Quality
		lambda k: (sort_direction * k["size_rank"], k["quality_rank"], k["provider_rank"]),  # Size, Quality, Provider
		lambda k: (sort_direction * k["size_rank"], k["provider_rank"], k["quality_rank"]),  # Size, Provider, Quality
	)[int(get_setting("finder.results.sort_order", "1"))]


def active_internal_scrapers():
	settings = ["provider.external", "provider.easynews", "provider.folders"]
	settings_append = settings.append
	for item in [("rd", "provider.rd_cloud"), ("pm", "provider.pm_cloud"), ("ad", "provider.ad_cloud"), ("tb", "provider.tb_cloud")]:
		if enabled_debrids_check(item[0]):
			settings_append(item[1])
	active = [i.split(".")[1] for i in settings if get_setting("finder.%s" % i) == "true"]
	return active


def provider_sort_ranks():
	fo_priority = int(get_setting("finder.folders.priority", "6"))
	en_priority = int(get_setting("finder.en.priority", "7"))
	rd_priority = int(get_setting("finder.rd.priority", "8"))
	ad_priority = int(get_setting("finder.ad.priority", "9"))
	pm_priority = int(get_setting("finder.pm.priority", "10"))
	tb_priority = int(get_setting("finder.tb.priority", "10"))
	return {
		"easynews": en_priority,
		"real-debrid": rd_priority,
		"premiumize.me": pm_priority,
		"alldebrid": ad_priority,
		"torbox": tb_priority,
		"rd_cloud": rd_priority,
		"pm_cloud": pm_priority,
		"ad_cloud": ad_priority,
		"tb_cloud": tb_priority,
		"folders": fo_priority,
	}


def sort_to_top(provider):
	sort_to_top_dict = {
		"folders": "finder.results.sort_folders_first",
		"rd_cloud": "finder.results.sort_rdcloud_first",
		"pm_cloud": "finder.results.sort_pmcloud_first",
		"ad_cloud": "finder.results.sort_adcloud_first",
		"tb_cloud": "finder.results.sort_tbcloud_first",
	}
	return get_setting(sort_to_top_dict[provider]) == "true"


def auto_resume(media_type, autoplay_status):
	return {0: False, 1: True, 2: autoplay_status}[int(get_setting("finder.auto_resume_%s" % media_type))]


def scraping_settings():
	highlight_type = int(get_setting("finder.highlight.type", "0"))
	if highlight_type == 2:
		highlight = get_setting("finder.scraper_single_highlight", "FF008EB2")
		return {"highlight_type": 1, "4k": highlight, "1080p": highlight, "720p": highlight, "sd": highlight}
	easynews_highlight, debrid_cloud_highlight, folders_highlight = "", "", ""
	rd_highlight, pm_highlight, ad_highlight, tb_highlight = "", "", "", ""
	highlight_4K, highlight_1080P, highlight_720P, highlight_SD = "", "", "", ""
	if highlight_type == 0:
		easynews_highlight = get_setting("finder.provider.easynews_highlight", "FF00B3B2")
		debrid_cloud_highlight = get_setting("finder.provider.debrid_cloud_highlight", "FF7A01CC")
		folders_highlight = get_setting("finder.provider.folders_highlight", "FFB36B00")
		rd_highlight = get_setting("finder.provider.rd_highlight", "FF3C9900")
		pm_highlight = get_setting("finder.provider.pm_highlight", "FFFF3300")
		ad_highlight = get_setting("finder.provider.ad_highlight", "FFE6B800")
		tb_highlight = get_setting("finder.provider.tb_highlight", "FF01662A")
	else:
		highlight_4K = get_setting("finder.scraper_4k_highlight", "FFFF00FE")
		highlight_1080P = get_setting("finder.scraper_1080p_highlight", "FFE6B800")
		highlight_720P = get_setting("finder.scraper_720p_highlight", "FF3C9900")
		highlight_SD = get_setting("finder.scraper_SD_highlight", "FF0166FF")
	return {
		"highlight_type": highlight_type,
		"easynews": easynews_highlight,
		"real-debrid": rd_highlight,
		"premiumize": pm_highlight,
		"alldebrid": ad_highlight,
		"torbox": tb_highlight,
		"rd_cloud": debrid_cloud_highlight,
		"pm_cloud": debrid_cloud_highlight,
		"ad_cloud": debrid_cloud_highlight,
		"tb_cloud": debrid_cloud_highlight,
		"folders": folders_highlight,
		"4k": highlight_4K,
		"1080p": highlight_1080P,
		"720p": highlight_720P,
		"sd": highlight_SD,
	}


def external_cache_check():
	return get_setting("finder.external.cache_check") == "true"


def omdb_api_key():
	return get_setting("finder.omdb_api", "empty_setting")


def default_all_episodes():
	return int(get_setting("finder.default_all_episodes", "0"))


def max_threads():
	if not get_setting("finder.limit_concurrent_threads", "false") == "true":
		return 60
	return int(get_setting("finder.max_threads", "60"))


def get_meta_filter():
	return get_setting("finder.meta_filter", "true")


def mpaa_region():
	return get_setting("finder.mpaa_region", "US")


def widget_hide_next_page():
	return get_setting("finder.widget_hide_next_page", "false") == "true"


def widget_hide_watched():
	return get_setting("finder.widget_hide_watched", "false") == "true"


def mixed_include_anime():
	return get_setting("finder.mixed_include_anime", "false") == "true"


def calendar_sort_order():
	return int(get_setting("finder.trakt.calendar_sort_order", "0"))


def ignore_articles():
	return get_setting("finder.ignore_articles", "false") == "true"


def jump_to_enabled():
	return get_setting("finder.paginate.jump_to", "true") == "true"


def date_offset():
	return int(get_setting("finder.datetime.offset", "0")) + 5


def media_open_action(media_type):
	return int(get_setting("finder.media_open_action_%s" % media_type, "0"))


def watched_indicators():
	if not trakt_user_active():
		return 0
	return int(get_setting("finder.watched_indicators", "0"))


def flatten_episodes():
	return get_setting("finder.trakt.flatten_episodes", "false") == "true"


def nextep_method():
	return int(get_setting("finder.nextep.method", "0"))


def nextep_limit_history():
	return get_setting("finder.nextep.limit_history", "false") == "true"


def nextep_limit():
	return int(get_setting("finder.nextep.limit", "20"))


def nextep_include_unwatched():
	return int(get_setting("finder.nextep.include_unwatched", "0"))


def nextep_include_airdate():
	return get_setting("finder.nextep.include_airdate", "false") == "true"


def nextep_airing_today():
	return get_setting("finder.nextep.airing_today", "false") == "true"


def nextep_include_unaired():
	return get_setting("finder.nextep.include_unaired", "false") == "true"


def nextep_sort_key():
	return {0: "last_played", 1: "first_aired", 2: "name"}[int(get_setting("finder.nextep.sort_type", "0"))]


def nextep_sort_direction():
	return int(get_setting("finder.nextep.sort_order", "0")) == 0


def update_delay():
	return int(get_setting("finder.update.delay", "45"))


def update_action():
	return int(get_setting("finder.update.action", "2"))


_RESCRAPE_DEFAULTS = [
	("cache_ignored", "1", "0"),
	("imdb_year", "1", "1"),
	("with_all", "1", "2"),
	("episode_group", "1", "3"),
	("ignore_filters", "1", "4"),
]


def rescrape_settings():
	return sorted(
		[
			(i[0], int(get_setting("finder.rescrape.%s" % i[0], i[1])), int(get_setting("finder.rescrape.%s.order" % i[0], i[2])))
			for i in _RESCRAPE_DEFAULTS
			if int(get_setting("finder.rescrape.%s" % i[0], i[1])) in (1, 2)
		],
		key=lambda x: x[2],
	)


def all_rescrape_settings():
	return sorted(
		[(i[0], int(get_setting("finder.rescrape.%s" % i[0], i[1])), int(get_setting("finder.rescrape.%s.order" % i[0], i[2]))) for i in _RESCRAPE_DEFAULTS],
		key=lambda x: x[2],
	)


def cm_enabled():
	default = (
		"extras,play_trailer,options,playback_options,browse_movie_set,browse_seasons,browse_episodes,recommended,related,more_like_this,similar,in_trakt_list,"
		"trakt_manager,personal_manager,tmdb_manager,favorites_manager,quick_add,mark_watched,unmark_previous_episode,exit,refresh"
	)
	setting = get_setting("finder.context_menu.enabled", default)
	if setting in ("", None, "noop", "[]"):
		return default.split(",")
	return setting.split(",")


def cm_current_order():
	default = (
		"extras,play_trailer,options,playback_options,browse_movie_set,browse_seasons,browse_episodes,recommended,related,more_like_this,similar,in_trakt_list,"
		"trakt_manager,personal_manager,tmdb_manager,favorites_manager,quick_add,mark_watched,unmark_previous_episode,exit,refresh"
	)
	setting = get_setting("finder.context_menu.order", default)
	if setting in ("", None, "noop", "[]"):
		return default.split(",")
	return setting.split(",")


def cm_sort_order():
	try:
		setting = {i: c for c, i in enumerate([i for i in cm_current_order() if i in cm_enabled()])}
	except:
		setting = cm_default_order()
	return setting


def cm_default_order():
	return {i: c for c, i in enumerate(default_setting_values("context_menu.order")["setting_default"].split(","))}


def rpdb_info(media_type):
	if media_type == "extras":
		active = extras_enable_item_ratings()
	else:
		active = int(get_setting("finder.rpdb_enabled", "0")) in {"movie": (1, 3), "tvshow": (2, 3)}[media_type]
	if active:
		return {"rpdb_api_key": get_setting("finder.rpdb_api"), "rpdb_format": get_setting("finder.rpdb_format")}
	else:
		return {"rpdb_api_key": None, "rpdb_format": None}


def use_season_name():
	return get_setting("finder.use_season_name", "false") == "true"
