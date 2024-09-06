from pygments.style import Style as PyStyle
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)
from rich.style import Style

__all__ = [
    "MonokaiProStyle",
    "ARKO_STYLE",
    "BACKGROUND",
    "FOREGROUND",
    "BLACK",
    "GREY",
    "LIGHT_GREY",
    "DARK_GREY",
    "RED",
    "BRIGHT_RED",
    "MAGENTA",
    "BRIGHT_MAGENTA",
    "GREEN",
    "BRIGHT_GREEN",
    "YELLOW",
    "BRIGHT_YELLOW",
    "ORANGE",
    "PURPLE",
    "BLUE",
    "BRIGHT_BLUE",
    "CYAN",
    "BRIGHT_CYAN",
    "WHITE",
    "BRIGHT_WHITE",
]

BACKGROUND = "#272822"
FOREGROUND = "#F8F8F2"

BLACK = "#1A1A1A"
DARK_GREY = "#363537"
LIGHT_GREY = "#69676C"
GREY = "#595959"

RED = "#FF6188"
BRIGHT_RED = "#FF8AA1"

MAGENTA = "#FC61D3"
BRIGHT_MAGENTA = "#FF77E0"

GREEN = "#7BD88F"
BRIGHT_GREEN = "#8FECB3"

YELLOW = "#FFD866"
BRIGHT_YELLOW = "#FFFF8C"

ORANGE = "#FC9867"
PURPLE = "#AB9DF2"

BLUE = "#81A1C1"
BRIGHT_BLUE = "#94BFF3"

CYAN = "#78DCE8"
BRIGHT_CYAN = "#9FDCE8"

WHITE = "#E5E9F0"
BRIGHT_WHITE = "#FFFFFF"

BACKGROUND_COLOR = DARK_GREY
HIGHLIGHT_COLOR = "#49483E"


class MonokaiProStyle(PyStyle):
    name = "monokai pro"
    background_color = BACKGROUND_COLOR
    highlight_color = HIGHLIGHT_COLOR

    styles = {
        # No corresponding class for the following:
        Text: WHITE,  # class:  ''
        Error: "#fc618d bg:#1e0010",  # class: 'err'
        Comment: LIGHT_GREY,  # class: 'c'
        Comment.Multiline: YELLOW,  # class: 'cm'
        Keyword: RED,  # class: 'k'
        Keyword.Namespace: GREEN,  # class: 'kn'
        Operator: RED,  # class: 'o'
        Punctuation: WHITE,  # class: 'p'
        Name: WHITE,  # class: 'n'
        Name.Attribute: GREEN,  # class: 'na' - to be revised
        Name.Builtin: CYAN,  # class: 'nb'
        Name.Builtin.Pseudo: ORANGE,  # class: 'bp'
        Name.Class: GREEN,  # class: 'nc' - to be revised
        Name.Decorator: PURPLE,  # class: 'nd' - to be revised
        Name.Exception: GREEN,  # class: 'ne'
        Name.Function: GREEN,  # class: 'nf'
        Name.Property: ORANGE,  # class: 'py'
        Number: PURPLE,  # class: 'm'
        Literal: PURPLE,  # class: 'l'
        Literal.Date: ORANGE,  # class: 'ld'
        String: YELLOW,  # class: 's'
        String.Regex: ORANGE,  # class: 'sr'
        Generic.Deleted: YELLOW,  # class: 'gd',
        Generic.Emph: "italic",  # class: 'ge'
        Generic.Inserted: GREEN,  # class: 'gi'
        Generic.Strong: "bold",  # class: 'gs'
        Generic.Subheading: LIGHT_GREY,  # class: 'gu'
    }


ARKO_STYLE: dict[str, Style] = {
    # base
    "none": Style.null(),
    "reset": Style(
        color=FOREGROUND,
        bgcolor=BACKGROUND,
        dim=False,
        bold=False,
        italic=False,
        underline=False,
        blink=False,
        blink2=False,
        reverse=False,
        conceal=False,
        strike=False,
    ),
    # base style
    "dim": Style(dim=True),
    "bright": Style(dim=False),
    "bold": Style(bold=True),
    "strong": Style(bold=True),
    "code": Style(reverse=True, bold=True),
    "italic": Style(italic=True),
    "emphasize": Style(italic=True),
    "underline": Style(underline=True),
    "blink": Style(blink=True),
    "blink2": Style(blink2=True),
    "reverse": Style(reverse=True),
    "strike": Style(strike=True),
    # color
    "black": Style(color=BLACK),
    "dark_grey": Style(color=DARK_GREY),
    "light_grey": Style(color=LIGHT_GREY),
    "grey": Style(color=GREY),
    "red": Style(color=RED),
    "green": Style(color=GREEN),
    "yellow": Style(color=YELLOW),
    "magenta": Style(color=MAGENTA),
    "blue": Style(color=BLUE),
    "cyan": Style(color=CYAN),
    "bright_cyan": Style(color=BRIGHT_CYAN),
    "white": Style(color=WHITE),
    # inspect
    "inspect.async_def": Style(italic=True, color=BRIGHT_CYAN),
    "inspect.attr": Style(color=YELLOW, italic=True),
    "inspect.attr.dunder": Style(color=YELLOW, italic=True, dim=True),
    "inspect.callable": Style(bold=True, color=RED),
    "inspect.def": Style(italic=True, color=BRIGHT_CYAN),
    "inspect.class": Style(italic=True, color=BRIGHT_CYAN),
    "inspect.error": Style(bold=True, color=RED),
    "inspect.equals": Style(),
    "inspect.help": Style(color=CYAN),
    "inspect.doc": Style(dim=True),
    "inspect.value.border": Style(color=GREEN),
    # live
    "live.ellipsis": Style(bold=True, color=RED),
    # layout
    "layout.tree.row": Style(dim=False, color=RED),
    "layout.tree.column": Style(dim=False, color=BLUE),
    # log
    "logging.keyword": Style(bold=True, color=ORANGE),
    "logging.level.notset": Style(color=DARK_GREY, dim=True),
    "logging.level.trace": Style(color=GREY),
    "logging.level.debug": Style(color=LIGHT_GREY, bold=True),
    "logging.level.info": Style(color=WHITE),
    "logging.level.success": Style(color=GREEN),
    "logging.level.warning": Style(color=YELLOW),
    "logging.level.error": Style(color=RED),
    "logging.level.critical": Style(color=RED, bgcolor="#1E0010", bold=True),
    "log.level": Style.null(),
    "log.time": Style(color=CYAN, dim=False, bold=True),
    "log.message": Style.null(),
    "log.path": Style(dim=True),
    "log.line_no": Style(color=CYAN, bold=True, italic=False, dim=True),
    # repr
    "repr.ellipsis": Style(color=YELLOW),
    "repr.indent": Style(color=GREEN, dim=True),
    "repr.error": Style(color=RED, bold=True),
    "repr.str": Style(color=GREEN, italic=False, bold=False),
    "repr.brace": Style(bold=True),
    "repr.comma": Style(bold=True),
    "repr.ipv4": Style(bold=True, color=BRIGHT_GREEN),
    "repr.ipv6": Style(bold=True, color=BRIGHT_GREEN),
    "repr.eui48": Style(bold=True, color=BRIGHT_GREEN),
    "repr.eui64": Style(bold=True, color=BRIGHT_GREEN),
    "repr.tag_start": Style(bold=True),
    "repr.tag_name": Style(color=BRIGHT_MAGENTA, bold=True),
    "repr.tag_contents": Style(color="default"),
    "repr.tag_end": Style(bold=True),
    "repr.attrib_name": Style(color=YELLOW, italic=False),
    "repr.attrib_equal": Style(bold=True),
    "repr.attrib_value": Style(color=MAGENTA, italic=False),
    "repr.number": Style(color=CYAN, bold=True, italic=False),
    "repr.number_complex": Style(color=CYAN, bold=True, italic=False),  # same
    "repr.bool_true": Style(color=BRIGHT_GREEN, italic=True),
    "repr.bool_false": Style(color=BRIGHT_RED, italic=True),
    "repr.none": Style(color=MAGENTA, italic=True),
    "repr.url": Style(underline=True, color=BRIGHT_BLUE, italic=False, bold=False),
    "repr.uuid": Style(color=BRIGHT_YELLOW, bold=False),
    "repr.call": Style(color=MAGENTA, bold=True),
    "repr.path": Style(color=MAGENTA),
    "repr.filename": Style(color=BRIGHT_MAGENTA),
    "rule.line": Style(color=BRIGHT_GREEN),
    "rule.text": Style.null(),
    # json
    "json.brace": Style(bold=True),
    "json.bool_true": Style(color=BRIGHT_GREEN, italic=True),
    "json.bool_false": Style(color=BRIGHT_RED, italic=True),
    "json.null": Style(color=MAGENTA, italic=True),
    "json.number": Style(color=CYAN, bold=True, italic=False),
    "json.str": Style(color=GREEN, italic=False, bold=False),
    "json.key": Style(color=BLUE, bold=True),
    # prompt
    "prompt": Style.null(),
    "prompt.choices": Style(color=MAGENTA, bold=True),
    "prompt.default": Style(color=CYAN, bold=True),
    "prompt.invalid": Style(color=RED),
    "prompt.invalid.choice": Style(color=RED),
    # pretty
    "pretty": Style.null(),
    # scope
    "scope.border": Style(color=BLUE),
    "scope.key": Style(color=YELLOW, italic=True),
    "scope.key.special": Style(color=YELLOW, italic=True, dim=True),
    "scope.equals": Style(color=RED),
    # table
    "table.header": Style(bold=True),
    "table.footer": Style(bold=True),
    "table.cell": Style.null(),
    "table.title": Style(italic=True),
    "table.caption": Style(italic=True, dim=True),
    # traceback
    "traceback.error": Style(color=RED, italic=True),
    "traceback.border.syntax_error": Style(color=BRIGHT_RED),
    "traceback.border": Style(color=RED),
    "traceback.text": Style.null(),
    "traceback.title": Style(color=RED, bold=True),
    "traceback.exc_type": Style(color=BRIGHT_RED, bold=True),
    "traceback.exc_value": Style.null(),
    "traceback.offset": Style(color=BRIGHT_RED, bold=True),
    # bar
    "bar.back": Style(color="grey23"),
    "bar.complete": Style(color="rgb(249,38,114)"),
    "bar.finished": Style(color="rgb(114,156,31)"),
    "bar.pulse": Style(color="rgb(249,143,36)"),
    # progress
    "progress.description": Style.null(),
    "progress.filesize": Style(color=GREEN),
    "progress.filesize.total": Style(color=GREEN),
    "progress.download": Style(color=GREEN),
    "progress.elapsed": Style(color=YELLOW),
    "progress.percentage": Style(color=MAGENTA),
    "progress.remaining": Style(color=CYAN),
    "progress.data.speed": Style(color=RED),
    "progress.spinner": Style(color=GREEN),
    "status.spinner": Style(color=GREEN),
    # tree
    "tree": Style(),
    "tree.line": Style(),
    # markdown
    "markdown.paragraph": Style(),
    "markdown.text": Style(),
    "markdown.em": Style(italic=True),
    "markdown.emph": Style(italic=True),
    "markdown.strong": Style(bold=True),
    "markdown.code": Style(bgcolor=BLACK, color=BRIGHT_WHITE),
    "markdown.code_block": Style(dim=True, color=CYAN, bgcolor=BLACK),
    "markdown.block_quote": Style(color=MAGENTA),
    "markdown.list": Style(color=CYAN),
    "markdown.item": Style(),
    "markdown.item.bullet": Style(color=YELLOW, bold=True),
    "markdown.item.number": Style(color=YELLOW, bold=True),
    "markdown.hr": Style(color=YELLOW),
    "markdown.h1.border": Style(),
    "markdown.h1": Style(bold=True),
    "markdown.h2": Style(bold=True, underline=True),
    "markdown.h3": Style(bold=True),
    "markdown.h4": Style(bold=True, dim=True),
    "markdown.h5": Style(underline=True),
    "markdown.h6": Style(italic=True),
    "markdown.h7": Style(italic=True, dim=True),
    "markdown.link": Style(color=BRIGHT_BLUE),
    "markdown.link_url": Style(color=BLUE),
    "markdown.s": Style(strike=True),
    # iso8601
    "iso8601.date": Style(color=BLUE),
    "iso8601.time": Style(color=MAGENTA),
    "iso8601.timezone": Style(color=YELLOW),
}
