from google.adk.agents import LlmAgent
from .tools import get_weather_forecast, get_current_weather, get_current_location

MODEL = "gemini-1.5-flash"

root_agent = LlmAgent(
    name="agriculture_assistant_agent",
    model=MODEL,
    description="AI Assistant for agricultural guidance and weather monitoring",
    instruction="You are an Agriculture Assistant that helps farmers and agricultural professionals with weather data, crop recommendations, and farming guidance. Use weather data to provide relevant agricultural advice.",
    tools=[
        get_weather_forecast,
        get_current_weather,
        get_current_location
    ],
)
