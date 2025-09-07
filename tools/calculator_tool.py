from langchain.tools import tool
from typing import List
import math

class CalculatorTool:
    def __init__(self):
        self.calculator_tool_list = [
            self.calculate_expense,
            self.calculate_budget
        ]
    
    @tool
    def calculate_expense(self, amount: float, currency: str = "USD") -> str:
        """Calculate basic expenses and provide cost breakdown"""
        try:
            # Basic expense calculation
            tax_rate = 0.08  # 8% tax rate
            tax_amount = amount * tax_rate
            total = amount + tax_amount
            
            return f"Expense breakdown for {currency} {amount:.2f}:\n" \
                   f"Base amount: {currency} {amount:.2f}\n" \
                   f"Tax (8%): {currency} {tax_amount:.2f}\n" \
                   f"Total: {currency} {total:.2f}"
        except Exception as e:
            return f"Error calculating expense: {str(e)}"
    
    @tool
    def calculate_budget(self, total_budget: float, expenses: str) -> str:
        """Calculate remaining budget after listing expenses"""
        try:
            # This is a simplified version - you could enhance it to parse actual expense lists
            estimated_expenses = total_budget * 0.7  # Assume 70% for expenses
            remaining = total_budget - estimated_expenses
            
            return f"Budget analysis:\n" \
                   f"Total budget: ${total_budget:.2f}\n" \
                   f"Estimated expenses: ${estimated_expenses:.2f}\n" \
                   f"Remaining budget: ${remaining:.2f}"
        except Exception as e:
            return f"Error calculating budget: {str(e)}"
