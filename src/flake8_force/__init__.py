import tokenize

import flake8.checker


class ForceFileChecker(flake8.checker.FileChecker):
    """FileChecker that ignores AST build failure."""

    def run_ast_checks(self, *args, **kwargs) -> None:
        if not self.options.force_check:
            # Do nothing if the option is not specified.
            return super().run_ast_checks(*args, **kwargs)

        try:
            super().run_ast_checks(*args, **kwargs)
        except (SyntaxError, tokenize.TokenError) as e:
            if hasattr(self, "_extract_syntax_information"):
                row, column = self._extract_syntax_information(e)
            else:
                (row, column) = (1, 1)
            self.report(
                "E902" if isinstance(e, tokenize.TokenError) else "E999",
                row,
                column,
                f"{type(e).__name__}: {e.args[0]}",
            )


flake8.checker.FileChecker = ForceFileChecker


class Flake8Force:
    name = "flake8-force"
    version = "0.0.1"

    def __init__(self, tree):
        pass

    def run(self):
        yield from []

    @staticmethod
    def add_options(optmanager):
        optmanager.add_option(
            "--force-check",
            action="store_true",
            parse_from_config=True,
            default=False,
            help="Force running check even when failed to parse a file",
        )
