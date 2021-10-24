class NavSection:
    def __init__(self, name, order=100):
        self.name = name
        self.order = order
        self.items = []

    def add_item(self, item):
        self.items.append(item)

class NavItem:
    def __init__(self, name, url, icon="fas fa-fw fa-smile", title=None):
        self.name = name
        self.url = url
        self.icon = icon
        self.title = title or name