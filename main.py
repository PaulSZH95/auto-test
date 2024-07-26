import json
import os
import random
import time

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from console_src.ast_parsers.naive_parser import AstVanillaParse as avp
from console_src.console_agent.agentic_starter import AutoTestConsole

load_dotenv("secrets/secrets.env")
console = Console()
random.seed(0)
project_path = "./"  # Change this to your actual project directory
# formatted_output = print_tree(project_path)


def main():
    console.print(
        Panel(
            "Hi! auto-test assistant, let me help you with your llm evals",
            title="Welcome",
            style="bold green",
        )
    )
    console.print("Type 'exit' to end the conversation.")

    auto_test_handler = AutoTestConsole(
        agent_name="auto-test",
        repo_schema=json.dumps(avp.build_tree(project_path), indent=2),
        llm_name="claude-3-5-sonnet-20240620",
        llm_api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    while True:
        user_input = console.input("[bold cyan]You:[/bold cyan] ")

        if user_input.lower() == "exit":
            console.print(
                Panel(
                    "Thank you for chatting. Goodbye!",
                    title_align="left",
                    title="Goodbye",
                    style="bold green",
                )
            )
            break

        # Use TinyChat to process the user's input and get a response
        response = auto_test_handler.chat(user_input)

        # Display Retrieved Conversations
        if auto_test_handler.retrieved_conversations:
            console.print(
                Panel(
                    "[bold green]Retrieved Conversations:[/bold green]", style="green"
                )
            )
            conversations = auto_test_handler.retrieved_conversations.split("\n")
            for i, conv in enumerate(
                conversations[1:], 1
            ):  # Skip the first line as it's the header
                if conv.strip():  # Check if the line is not empty
                    color = f"color({i % 5 + 1})"  # Cycle through 5 different colors
                    console.print(
                        Panel(Markdown(conv), border_style=color, expand=False)
                    )
                    time.sleep(
                        random.uniform(0.1, 0.3)
                    )  # Random delay between 0.1 and 0.3 seconds

        # Display the assistant's response
        console.print(Panel.fit("[bold green]RAG-Agent:[/bold green]", style="green"))
        response_with_newlines = response.replace(
            "\n", "  \n"
        )  # Fix newlines for Markdown
        console.print(
            Panel(Markdown(response_with_newlines), style="green", expand=False)
        )
