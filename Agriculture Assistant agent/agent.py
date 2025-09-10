from google.adk.agents import LlmAgent
from .tools import get_weather_forecast, get_current_weather, get_current_location, search_agricultural_info
from .prompt import ROOT_AGENT_PROMPT

MODEL = "gemini-1.5-flash"

root_agent = LlmAgent(
    name="agriculture_assistant_agent",
    model=MODEL,
    description="AI Assistant for agricultural guidance and weather monitoring",
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        get_weather_forecast,
        get_current_weather,
        get_current_location,
        search_agricultural_info
    ],
)
