# -*- coding: utf-8 -*-

media_xml_start = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="{main_include}">'

media_xml_end = "\
\n    </include>\
\n</includes>"

media_xml_body = '\
\n        <include content="{cpath_type}">\
\n            <param name="content_path" value="{cpath_path}"/>\
\n            <param name="widget_header" value="{cpath_header}"/>\
\n            <param name="widget_target" value="videos"/>\
\n            <param name="list_id" value="{cpath_list_id}"/>\
\n        </include>'

history_xml_body = "\
\n        <item>\
\n            <label>$NUMBER[{spath}]</label>\
\n            <onclick>RunScript(script.finder.helper,mode=re_search)</onclick>\
\n        </item>"


stacked_media_xml_body = '\
\n        <include content="WidgetListCategoryStacked">\
\n            <param name="content_path" value="{cpath_path}"/>\
\n            <param name="widget_header" value="{cpath_header}"/>\
\n            <param name="widget_target" value="videos"/>\
\n            <param name="list_id" value="{cpath_list_id}"/>\
\n        </include>\
\n        <include content="{cpath_type}">\
\n            <param name="content_path" value="$INFO[Window(Home).Property(finder.{cpath_list_id}.path)]"/>\
\n            <param name="widget_header" value="$INFO[Window(Home).Property(finder.{cpath_list_id}.label)]"/>\
\n            <param name="widget_target" value="videos"/>\
\n            <param name="list_id" value="{cpath_list_id}1"/>\
\n        </include>'

main_menu_movies_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="MoviesMainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[19000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">movies</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoMoviesButton)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_tvshows_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="TVShowsMainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[22000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">tvshows</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoTVShowsButton)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_custom1_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="Custom1MainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[23000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">custom1</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoCustom1Button)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_custom2_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="Custom2MainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[24000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">custom2</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoCustom2Button)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_custom3_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="Custom3MainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[25000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">custom3</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoCustom3Button)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_custom4_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="Custom4MainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[26000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">custom4</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoCustom4Button)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_custom5_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="Custom5MainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[27000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">custom5</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoCustom5Button)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

main_menu_custom6_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="Custom6MainMenu">\
\n        <item>\
\n            <label>{cpath_header}</label>\
\n            <onclick>{main_menu_onclick}</onclick>\
\n            <property name="menu_id">$NUMBER[28000]</property>\
\n            <thumb>{main_menu_icon}</thumb>\
\n            <property name="id">custom6</property>\
\n            <visible>!Skin.HasSetting(HomeMenuNoCustom6Button)</visible>\
\n        </item>\
\n    </include>\
\n</includes>'

search_history_xml = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="SearchHistory">\
\n        <item>\
\n            <label>{spath}</label>\
\n            <onclick>RunScript(script.finder.helper,mode=re_search)</onclick>\
\n        </item>\
\n    </include>\
\n</includes>'

default_widget = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="{includes_type}">\
\n    </include>\
\n</includes>'

default_main_menu = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="{includes_type}">\
\n    </include>\
\n</includes>'

default_history = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="{includes_type}">\
\n    </include>\
\n</includes>'


submenu_xml_start = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n    <include name="{include_name}">'

submenu_xml_body = '\
\n        <item>\
\n            <label>{submenu_label}</label>\
\n            <onclick>{submenu_onclick}</onclick>\
\n        </item>'

submenu_xml_end = "\
\n    </include>\
\n</includes>"

topbar_custom_menu_xml_start = '\
<?xml version="1.0" encoding="UTF-8"?>\
\n<includes>\
\n\t<include name="FinderTopBarCustomMenuButton">\
\n\t\t<include content="IconButton">\
\n\t\t\t<param name="control_id" value="811"/>\
\n\t\t\t<param name="onclick" value="ActivateWindow(1170)"/>\
\n\t\t\t<param name="icon" value="{topbar_icon}"/>\
\n\t\t\t<param name="label" value="$INFO[Skin.String(TopBarCustomMenuLabel)]"/>\
\n\t\t\t<param name="visible" value="Skin.HasSetting(Enable.TopBarCustomMenu)"/>\
\n\t\t</include>\
\n\t</include>\
\n\t<include name="TopBarCustomMenuItems">'

topbar_custom_menu_xml_body = '\
\n\t\t<item>\
\n\t\t\t<label>{menu_label}</label>\
\n\t\t\t{menu_close}\
\n\t\t\t<onclick>{menu_onclick}</onclick>\
\n\t\t</item>'

topbar_custom_menu_xml_end = "\
\n\t</include>\
\n</includes>"

