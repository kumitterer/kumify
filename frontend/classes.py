class NavSection:
    def __init__(self, name, order=100):
        self.name = name
        self.order = order
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_html(self, active=None):
        html = f"""
            <!-- Heading -->
            <div class="sidebar-heading">{self.name}</div>
            """

        self.items.sort(key=lambda x: x.order)

        for item in self.items:
            html += f"""
            <!-- Nav Item -->
            <li class="nav-item """ + ("active" if item.name == active else "") + f""">
                <a class="nav-link" href="{item.url}">
                    <i class="{item.icon}"></i>
                    <span>{item.name}</span>
                </a>
            </li>
            """

        return html

class NavItem:
    def __init__(self, name, url, icon="fas fa-fw fa-smile", title=None, order=100):
        self.name = name
        self.url = url
        self.icon = icon
        self.title = title or name
        self.order = order