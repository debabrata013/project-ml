import sys
import os
sys.path.append(os.path.dirname(__file__))

from google.adk.agents import LlmAgent
from tools import (
    get_weather_forecast, 
    get_current_weather, 
    get_current_location, 
    search_agricultural_info,
    predict_plant_disease,
    predict_crop_yield,
    analyze_crop_health_with_ai,
    generate_farming_plan,
    pest_disease_advisor,
    soil_analysis_advisor,
    market_price_advisor,
    weather_farming_advisor,
    recommend_suitable_crops
)
from prompt import ROOT_AGENT_PROMPT

MODEL = "gemini-1.5-flash"

root_agent = LlmAgent(
    name="agriculture_assistant_agent",
    model=MODEL,
    description="Advanced AI Assistant for comprehensive agricultural guidance with ML models, weather intelligence, market analysis, and expert AI consultation",
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        get_weather_forecast,
        get_current_weather,
        get_current_location,
        search_agricultural_info,
        predict_plant_disease,
        predict_crop_yield,
        analyze_crop_health_with_ai,
        generate_farming_plan,
        pest_disease_advisor,
        soil_analysis_advisor,
        market_price_advisor,
        weather_farming_advisor,
        recommend_suitable_crops
    ],
)
