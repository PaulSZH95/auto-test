from typing import Union

from llms.models import ClaudeChat
from prompts.prompts import system_prompt


class BaseConversation:

    def __init__(
        self,
        agent_name: str,
        repo_schema: str,
        llm_name: Union[str, ClaudeChat],
        llm_api_key: str,
        tools: list = None,
    ):
        self.claude_chat = (
            llm_name
            if isinstance(llm_name, ClaudeChat)
            else ClaudeChat(
                model_name="claude-3-5-sonnet-20240620", api_key=llm_api_key
            )
        )
        self.system_prompt = system_prompt.substitute(
            {"name": agent_name, "schema": repo_schema}
        )
        self.messages = []
        self.tools = tools

    def messages_thread(self, msg: dict):
        self.messages.append(msg)

    def chat(self, query):
        """
        makes api call to claude
        """
        self.messages_thread(msg={"role": "user", "content": query})
        response = self.claude_chat.response_handler(
            self.messages, self.system_prompt, self.tools
        )
        assistant_response = response.content[0].text
        self.messages_thread({"role": "assistant", "content": assistant_response})
        self.messages = self.messages[-8:]
        return assistant_response
