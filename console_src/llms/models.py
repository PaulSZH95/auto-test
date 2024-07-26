import os
import random
import time
from os import getenv

from anthropic import Anthropic


class ClaudeChat:

    def __init__(
        self, model_name: str = "claude-3-5-sonnet-20240620", api_key: str = None
    ):
        if not api_key:
            api_key = getenv("ANTHROPIC_API_KEY")
        self.claude_instance = Anthropic(api_key)
        self.model_name = model_name

    def response_handler(self, messages: str, system_prompt: str, tools: list):
        if tools:
            claude_response = self.claude_instance.messages.create(
                model=self.model_name,
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                tools=tools,
            )
        else:
            claude_response = self.claude_instance.create(
                model=self.model_name,
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
            )
        return claude_response
