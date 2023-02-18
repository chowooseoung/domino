# markdown
import markdown

# built-ins
import os

# gui
from PySide2 import QtWebEngineWidgets


class MarkdownView(QtWebEngineWidgets.QWebEngineView):

    def __init__(self, markdown_text):
        super(MarkdownView, self).__init__()
        self.setHtml(self.markdown_to_html(markdown_text))

    def _css(self):
        css_path = os.path.join(os.path.dirname(__file__), "github-markdown-light.css")

        with open(css_path, "r") as f:
            css = f.read()
        return css

    def _html(self, markdown_text):
        html = """
<style>
%s
    .markdown-body {
        box-sizing: border-box;
        min-width: 200px;
        max-width: 980px;
        margin: 0 auto;
        padding: 45px;
    }

    @media (max-width: 767px) {
        .markdown-body {
            padding: 15px;
        }
    }
</style>
<article class="markdown-body">
%s
</article>
""" % (self._css(), markdown_text)
        return html

    def markdown_to_html(self, markdown_text):
        markdown_text = markdown.markdown(markdown_text, extensions=['codehilite', 'fenced_code'])
        return self._html(markdown_text)
