# markdown
import domino.vendor.markdown2 as markdown2

# built-ins
import os

# gui
from PySide2 import QtWebEngineWidgets


class MarkdownView(QtWebEngineWidgets.QWebEngineView):

    def __init__(self, markdown_text):
        super(MarkdownView, self).__init__()
        self.setHtml(self.markdown_to_html(markdown_text))

    def _css(self):
        css_path = os.path.join(os.path.dirname(__file__), "github-markdown-dark.css")

        with open(css_path, "r") as f:
            css = f.read()
        return css

    def _html(self, markdown_text):
        # https://github.com/richleland/pygments-css native.css
        # github-markdown-dark.css
        html = """
<style>
.codehilite .hll { background-color: #404040 }
.codehilite  { background: #202020; color: #d0d0d0 }
.codehilite .c { color: #999999; font-style: italic } /* Comment */
.codehilite .err { color: #a61717; background-color: #e3d2d2 } /* Error */
.codehilite .esc { color: #d0d0d0 } /* Escape */
.codehilite .g { color: #d0d0d0 } /* Generic */
.codehilite .k { color: #6ab825; font-weight: bold } /* Keyword */
.codehilite .l { color: #d0d0d0 } /* Literal */
.codehilite .n { color: #d0d0d0 } /* Name */
.codehilite .o { color: #d0d0d0 } /* Operator */
.codehilite .x { color: #d0d0d0 } /* Other */
.codehilite .p { color: #d0d0d0 } /* Punctuation */
.codehilite .ch { color: #999999; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #999999; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #cd2828; font-weight: bold } /* Comment.Preproc */
.codehilite .cpf { color: #999999; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #999999; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #e50808; font-weight: bold; background-color: #520000 } /* Comment.Special */
.codehilite .gd { color: #d22323 } /* Generic.Deleted */
.codehilite .ge { color: #d0d0d0; font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #d22323 } /* Generic.Error */
.codehilite .gh { color: #ffffff; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #589819 } /* Generic.Inserted */
.codehilite .go { color: #cccccc } /* Generic.Output */
.codehilite .gp { color: #aaaaaa } /* Generic.Prompt */
.codehilite .gs { color: #d0d0d0; font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #ffffff; text-decoration: underline } /* Generic.Subheading */
.codehilite .gt { color: #d22323 } /* Generic.Traceback */
.codehilite .kc { color: #6ab825; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #6ab825; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #6ab825; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #6ab825 } /* Keyword.Pseudo */
.codehilite .kr { color: #6ab825; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #6ab825; font-weight: bold } /* Keyword.Type */
.codehilite .ld { color: #d0d0d0 } /* Literal.Date */
.codehilite .m { color: #3677a9 } /* Literal.Number */
.codehilite .s { color: #ed9d13 } /* Literal.String */
.codehilite .na { color: #bbbbbb } /* Name.Attribute */
.codehilite .nb { color: #24909d } /* Name.Builtin */
.codehilite .nc { color: #447fcf; text-decoration: underline } /* Name.Class */
.codehilite .no { color: #40ffff } /* Name.Constant */
.codehilite .nd { color: #ffa500 } /* Name.Decorator */
.codehilite .ni { color: #d0d0d0 } /* Name.Entity */
.codehilite .ne { color: #bbbbbb } /* Name.Exception */
.codehilite .nf { color: #447fcf } /* Name.Function */
.codehilite .nl { color: #d0d0d0 } /* Name.Label */
.codehilite .nn { color: #447fcf; text-decoration: underline } /* Name.Namespace */
.codehilite .nx { color: #d0d0d0 } /* Name.Other */
.codehilite .py { color: #d0d0d0 } /* Name.Property */
.codehilite .nt { color: #6ab825; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #40ffff } /* Name.Variable */
.codehilite .ow { color: #6ab825; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #666666 } /* Text.Whitespace */
.codehilite .mb { color: #3677a9 } /* Literal.Number.Bin */
.codehilite .mf { color: #3677a9 } /* Literal.Number.Float */
.codehilite .mh { color: #3677a9 } /* Literal.Number.Hex */
.codehilite .mi { color: #3677a9 } /* Literal.Number.Integer */
.codehilite .mo { color: #3677a9 } /* Literal.Number.Oct */
.codehilite .sa { color: #ed9d13 } /* Literal.String.Affix */
.codehilite .sb { color: #ed9d13 } /* Literal.String.Backtick */
.codehilite .sc { color: #ed9d13 } /* Literal.String.Char */
.codehilite .dl { color: #ed9d13 } /* Literal.String.Delimiter */
.codehilite .sd { color: #ed9d13 } /* Literal.String.Doc */
.codehilite .s2 { color: #ed9d13 } /* Literal.String.Double */
.codehilite .se { color: #ed9d13 } /* Literal.String.Escape */
.codehilite .sh { color: #ed9d13 } /* Literal.String.Heredoc */
.codehilite .si { color: #ed9d13 } /* Literal.String.Interpol */
.codehilite .sx { color: #ffa500 } /* Literal.String.Other */
.codehilite .sr { color: #ed9d13 } /* Literal.String.Regex */
.codehilite .s1 { color: #ed9d13 } /* Literal.String.Single */
.codehilite .ss { color: #ed9d13 } /* Literal.String.Symbol */
.codehilite .bp { color: #24909d } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #447fcf } /* Name.Function.Magic */
.codehilite .vc { color: #40ffff } /* Name.Variable.Class */
.codehilite .vg { color: #40ffff } /* Name.Variable.Global */
.codehilite .vi { color: #40ffff } /* Name.Variable.Instance */
.codehilite .vm { color: #40ffff } /* Name.Variable.Magic */
.codehilite .il { color: #3677a9 } /* Literal.Number.Integer.Long */

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
        markdown_text = markdown2.markdown(markdown_text, extras=['fenced-code-blocks'])
        return self._html(markdown_text)
