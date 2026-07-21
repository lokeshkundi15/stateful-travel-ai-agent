import os
import requests
from typing import Dict, Any, Literal
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults

# Real-Time Web Search Tool via Tavily API
web_search_tool = TavilySearchResults(
    max_results=3,
    description="Use this tool to search the live web for recent travel information, flight details, events, or news."
)


# Weather Fetching Tool via OpenWeatherMap API
@tool
def get_weather(city: str) -> str:
    """Get current weather for a specified city using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return f"Weather API key missing. Simulated Weather for {city}: 25°C, Sunny."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("cod") == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"The current weather in {city} is {temp}°C with {desc}."
        return f"Could not fetch weather for {city}. City might be invalid."
    except Exception as e:
        return f"Error fetching weather: {e}"


# Mock Local Attractions Tool
POIS = [
    {"name": "Central Park", "category": "park"},
    {"name": "Times Square", "category": "landmark"},
    {"name": "The Met", "category": "museum"},
    {"name": "MoMA", "category": "museum"},
]

@tool
def attractionsNear(category: Literal["museum", "park", "landmark", "any"] = "any", limit: int = 2) -> Dict[str, Any]:
    """Return a few NYC attractions by category from local database."""
    items = [p for p in POIS if category == "any" or p["category"] == category][:limit]
    return {"category": category, "results": items}


# Master Tools Export
TOOLS = [get_weather, attractionsNear, web_search_tool]