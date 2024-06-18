def get_menu_context(request):
    menu = [
        {'title': 'Музыканты', 'url_name': 'musicians'},
        {'title': 'Композиции', 'url_name': 'albums'},
    ]

    return {'main_menu': menu}

