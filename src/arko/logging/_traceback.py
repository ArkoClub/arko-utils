from types import ModuleType, TracebackType

from pydantic_settings import BaseSettings
from pygments.style import Style as PyStyle
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    String,
    Text as TextToken,
    Token,
)

# noinspection PyProtectedMember
from rich._loop import loop_last
from rich.console import Console, ConsoleOptions, ConsoleRenderable, RenderResult
from rich.constrain import Constrain
from rich.highlighter import ReprHighlighter
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.theme import Theme
from rich.traceback import Traceback as _Traceback
from typing_extensions import Iterable

__all__ = ("Traceback", "TracebacksConfig")


class TracebacksConfig(BaseSettings):
    width: int | None = None
    code_with: int = 88
    extra_lines: int = 3
    theme: str | type[PyStyle] | None = None
    word_wrap: bool = True
    show_locals: bool = True
    suppress: Iterable[str | ModuleType] = ()
    max_frames: int | None = 20

    class LocalsConfig(BaseSettings):
        max_length: int = 10
        max_string: int = 80
        hide_dunder: bool = True
        hide_sunder: bool = False

    locals_config: LocalsConfig = LocalsConfig()


class Traceback(_Traceback):
    @classmethod
    def from_config(
        cls,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
        config: TracebacksConfig,
    ) -> "Traceback":
        return cls.from_exception(
            exc_type,
            exc_value,
            traceback,
            width=config.width,
            code_width=config.code_with,
            extra_lines=config.extra_lines,
            theme=config.theme,
            word_wrap=config.word_wrap,
            show_locals=config.show_locals,
            suppress=config.suppress,
            max_frames=config.max_frames,
            locals_max_string=config.locals_config.max_string,
            locals_max_length=config.locals_config.max_length,
            locals_hide_sunder=config.locals_config.hide_sunder,
            locals_hide_dunder=config.locals_config.hide_dunder,
        )

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        theme = self.theme
        background_style = theme.get_background_style()
        token_style = theme.get_style_for_token

        traceback_theme = Theme(
            {
                "pretty": token_style(TextToken),
                "pygments.text": token_style(Token),
                "pygments.string": token_style(String),
                "pygments.function": token_style(Name.Function),
                "pygments.number": token_style(Number),
                "repr.indent": token_style(Comment) + Style(dim=True),
                "repr.str": token_style(String),
                "repr.brace": token_style(TextToken) + Style(bold=True),
                "repr.number": token_style(Number),
                "repr.bool_true": token_style(Keyword.Constant),
                "repr.bool_false": token_style(Keyword.Constant),
                "repr.none": token_style(Keyword.Constant),
                "scope.border": token_style(String.Delimiter),
                "scope.equals": token_style(Operator),
                "scope.key": token_style(Name),
                "scope.key.special": token_style(Name.Constant) + Style(dim=True),
            },
            inherit=False,
        )

        highlighter = ReprHighlighter()
        for last, stack in loop_last(reversed(self.trace.stacks)):
            if stack.frames:
                stack_renderable: ConsoleRenderable = Panel(
                    self._render_stack(stack),
                    title="[traceback.title]Traceback[/]",
                    style=background_style,
                    border_style="traceback.border",
                    expand=True,
                    padding=(0, 1),
                )
                stack_renderable = Constrain(stack_renderable, self.width)
                with console.use_theme(traceback_theme):
                    yield stack_renderable
            if stack.syntax_error is not None:
                with console.use_theme(traceback_theme):
                    yield Constrain(
                        Panel(
                            self._render_syntax_error(stack.syntax_error),
                            style=background_style,
                            border_style="traceback.border.syntax_error",
                            expand=True,
                            padding=(0, 1),
                            width=self.width,
                        ),
                        self.width,
                    )
                yield Text.assemble(
                    (f"{stack.exc_type}: ", "traceback.exc_type"),  # NOSONAR
                    highlighter(stack.syntax_error.msg),
                )
            elif stack.exc_value:
                yield Text.assemble(
                    (f"{stack.exc_type}: ", "traceback.exc_type"),
                    highlighter(stack.exc_value),
                )
            else:
                yield Text.assemble((f"{stack.exc_type}", "traceback.exc_type"))

            if not last:
                if stack.is_cause:
                    yield Text.from_markup(
                        "\n[i]The above exception was the direct cause of the following exception:\n",
                    )
                else:
                    yield Text.from_markup(
                        "\n[i]During handling of the above exception, another exception occurred:\n",
                    )
