from nonebot import load_all_plugins, get_plugin_by_module_name

if get_plugin_by_module_name("GenshinUID"):
    load_all_plugins(
        [
            'GenshinUID.genshinuid_abyss',
            'GenshinUID.genshinuid_adv',
            'GenshinUID.genshinuid_check',
            'GenshinUID.genshinuid_collection',
            'GenshinUID.genshinuid_config',
            'GenshinUID.genshinuid_enka',
            'GenshinUID.genshinuid_etcimg',
            'GenshinUID.genshinuid_eventlist',
            'GenshinUID.genshinuid_gachalog',
            'GenshinUID.genshinuid_guide',
            'GenshinUID.genshinuid_help',
            'GenshinUID.genshinuid_map',
            'GenshinUID.genshinuid_meta',
            'GenshinUID.genshinuid_mhybbscoin',
            'GenshinUID.genshinuid_mys',
            'GenshinUID.genshinuid_note',
            'GenshinUID.genshinuid_resin',
            'GenshinUID.genshinuid_resource',
            'GenshinUID.genshinuid_roleinfo',
            'GenshinUID.genshinuid_signin',
            'GenshinUID.genshinuid_user',
            'GenshinUID.genshinuid_wikitext',
        ],
        [],
    )
