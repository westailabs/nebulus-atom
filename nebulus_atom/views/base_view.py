from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any


class BaseView(ABC):
    @abstractmethod
    async def print_welcome(self):
        """Displays the welcome message."""
        pass

    @abstractmethod
    async def prompt_user(self) -> str:
        """Prompts the user for input."""
        pass

    @abstractmethod
    async def ask_user_input(self, question: str) -> str:
        """Prompts the user for specific input requested by the agent."""
        pass

    @abstractmethod
    async def print_agent_response(self, text: str):
        """Displays the agent s text response."""
        pass

    @abstractmethod
    async def print_telemetry(self, metrics: dict[str, Any]):
        """Displays performance telemetry."""
        pass

    @abstractmethod
    async def print_tool_output(self, output: str, tool_name: str = ""):
        """Displays the output of a tool execution."""
        pass

    @abstractmethod
    async def print_plan(self, plan_data: dict[str, Any]):
        """Displays the plan status."""
        pass

    @abstractmethod
    async def print_error(self, message: str):
        """Displays an error message."""
        pass

    @abstractmethod
    async def print_goodbye(self):
        """Displays a goodbye message."""
        pass

    @abstractmethod
    def create_spinner(self, text: str) -> AbstractContextManager:
        """Creates a context manager for a loading spinner."""
        pass

    # Optional streaming hooks. They are deliberately concrete no-ops, not
    # abstract: views that do not stream (e.g. HeadlessView) inherit them, so
    # B027 ("empty method in ABC without @abstractmethod") is suppressed here.
    def print_stream_start(self):  # noqa: B027 - optional hook, no-op default
        """Called before streaming response begins."""
        pass

    def print_stream_chunk(self, text: str):  # noqa: B027 - optional hook, no-op default
        """Called for each chunk of streamed text."""
        pass

    def print_stream_end(self):  # noqa: B027 - optional hook, no-op default
        """Called when streaming response is complete."""
        pass
