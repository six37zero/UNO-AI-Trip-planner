from langchain.tools import tool
from typing import List
import requests
import os

class CurrencyConverterTool:
    def __init__(self):
        self.currency_converter_tool_list = [
            self.convert_currency,
            self.get_exchange_rate
        ]
    
    @tool
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> str:
        """Convert amount from one currency to another"""
        try:
            # This is a placeholder - you would need to integrate with a real currency API
            # For now, returning mock data with common exchange rates
            rates = {
                "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0},
                "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.0},
                "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.0}
            }
            
            if from_currency in rates and to_currency in rates[from_currency]:
                rate = rates[from_currency][to_currency]
                converted = amount * rate
                return f"{amount} {from_currency} = {converted:.2f} {to_currency} (Rate: 1 {from_currency} = {rate} {to_currency})"
            else:
                return f"Exchange rate not available for {from_currency} to {to_currency}"
        except Exception as e:
            return f"Error converting currency: {str(e)}"
    
    @tool
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> str:
        """Get current exchange rate between two currencies"""
        try:
            # This is a placeholder - you would need to integrate with a real currency API
            # For now, returning mock data
            rates = {
                "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0},
                "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129.0},
                "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150.0}
            }
            
            if from_currency in rates and to_currency in rates[from_currency]:
                rate = rates[from_currency][to_currency]
                return f"1 {from_currency} = {rate} {to_currency}"
            else:
                return f"Exchange rate not available for {from_currency} to {to_currency}"
        except Exception as e:
            return f"Error getting exchange rate: {str(e)}"
