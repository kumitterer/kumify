from django.template.loader import render_to_string

import random


class NavSection:
    def __init__(self, name, order=100):
        self.name = name
        self.order = order
        self.items: list[NavItem | NavCollapse] = []

    def add_item(self, item):
        self.items.append(item)

    def get_html(self, active=None) -> str:
        html = f"""
            <!-- Heading -->
            <div class="sidebar-heading">{self.name}</div>
            """

        self.items.sort(key=lambda x: x.order)

        for item in self.items:
            html += item.get_html()

        return html


class NavItem:
    def __init__(self, name, url, icon="fas fa-fw fa-smile", title=None, order=100):
        self.name = name
        self.url = url
        self.icon = icon
        self.title = title or name
        self.order = order

    def get_html(self, active=None) -> str:
        return f"""
            <!-- Nav Item -->
            <li class="nav-item">
                <a class="nav-link{" active" if self.name == active else ""}" href="{self.url}">
                    <i class="{self.icon}"></i>
                    <span>{self.name}</span>
                </a>
            </li>
            """


class NavCollapse:
    def __init__(self, name, icon="fas fa-fw fa-smile", order=100):
        self.name = name
        self.icon = icon
        self.order = order
        self.items: list[NavItem] = []

    def add_item(self, item):
        self.items.append(item)

    def get_html(self, active=None) -> str:
        element_id = random.randint(1000, 9999)

        html = f"""
            <!-- Nav Item - {self.name} -->
            <li class="nav-item">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapse{element_id}" aria-expanded="true" aria-controls="collapse{element_id}">
                    <i class="{self.icon}"></i>
                    <span>{self.name}</span>
                </a>
                <div id="collapse{element_id}" class="collapse" aria-labelledby="heading{element_id}" data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
            """

        self.items.sort(key=lambda x: x.order)

        for item in self.items:
            html += (
                """
                <a class="collapse-item"""
                + (" active" if item.name == active else "")
                + f""""
                href="{item.url}">
                <i class="{item.icon}"></i>
                {item.name}</a>
                """
            )

        html += """
                    </div>
                </div>
            </li>
            """

        return html


class DashboardSection:
    def __init__(self, name, template, context=None):
        self.name = name
        self.template = template
        self.context = context or {}
        self.styles = []
        self.scripts = []

    def get_html(self, request):
        return render_to_string(self.template, self.context, request)

    def add_style(self, style):
        self.styles.append(style)

    def add_script(self, script):
        self.scripts.append(script)
