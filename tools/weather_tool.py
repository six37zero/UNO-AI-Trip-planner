from langchain.tools import tool
from typing import List
import requests
import os

class WeatherInfoTool:
    def __init__(self):
        self.weather_tool_list = [
            self.get_current_weather,
            self.get_weather_forecast
        ]
    
    @tool
    def get_current_weather(self, city: str) -> str:
        """Get current weather information for a specific city"""
        try:
            # This is a placeholder - you would need to integrate with a real weather API
            # For now, returning mock data
            return f"Current weather in {city}: Sunny, 25°C, Humidity: 60%"
        except Exception as e:
            return f"Error getting weather for {city}: {str(e)}"
    
    @tool
    def get_weather_forecast(self, city: str, days: int = 5) -> str:
        """Get weather forecast for a specific city for the next few days"""
        try:
            # This is a placeholder - you would need to integrate with a real weather API
            # For now, returning mock data
            return f"Weather forecast for {city} for the next {days} days: Mostly sunny with occasional clouds, temperatures ranging from 20-28°C"
        except Exception as e:
            return f"Error getting forecast for {city}: {str(e)}"
