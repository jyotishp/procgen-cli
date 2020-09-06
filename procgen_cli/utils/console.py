#!/usr/bin/environment python

from rich.console import Console
from rich.markdown import Markdown


class Logger:
    def __init__(self):
        self.console = Console()

    def info(self, msg):
        self.console.print(msg, style="cyan")

    def error(self, msg):
        self.console.print(msg, style="bold red")

    def success(self, msg):
        self.console.print(msg, style="green")

    def normal(self, msg):
        self.console.print(Markdown(msg))


logger = Logger()
