"""Tools for the example agent.

Define plain Python functions here — ADK wraps them automatically.
Type hints and docstrings are used by the model to understand when and how to call each tool.
"""


def example_tool(input: str) -> str:
    """A placeholder tool. Replace with real logic.

    Args:
        input: The input string to process.

    Returns:
        A processed result string.
    """
    return f"Processed: {input}"


# Register tools the agent can use
tools = [example_tool]
