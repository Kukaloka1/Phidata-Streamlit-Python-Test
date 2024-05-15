from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo

print("Bittech Network will rules the world")

assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
assistant.print_response("What's happening in Bitcoin today?", markdown=True)
