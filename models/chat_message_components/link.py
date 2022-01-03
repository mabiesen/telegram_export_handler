import webbrowser
from urllib.parse import urlparse

class Link(object):

    def __init__(self, url):
        self.url = url

    def domain(self):
        domain = urlparse(self.url)
        return domain

    def open(self):
        webbrowser.open(self.url)

    def as_html(self):
        return f'<a href="#{self.url}">#{self.url}</a>'

    def __eq__(self, other):
        return self.url == other.url
