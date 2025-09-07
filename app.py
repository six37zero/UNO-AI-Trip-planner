from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import datetime
import requests
import re

app = Flask(__name__)

# Ensure the templates and static directories exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Configuration for your AI backend
AI_BACKEND_URL = "http://localhost:8000"  # Your FastAPI backend URL


def localize_currency(text: str, user_message: str) -> str:
    """Convert USD symbol to INR for India-specific queries.
    Simple heuristic: if the user asks about India-related trips (keywords),
    replace currency symbol `$` with `₹` when it looks like a money amount.
    """
    if not isinstance(text, str):
        return text

    msg = (user_message or "").lower()
    india_keywords = ["india", "manali", "inr", "rupee", "₹", "delhi", "mumbai", "goa", "himachal", "bali inr"]
    if any(k in msg for k in india_keywords):
        # Replace $ when followed by a number (optionally with commas and decimals)
        return re.sub(r"\$(?=\d|\s*\d)", "₹", text)
    return text

@app.route('/')
def index():
    """Main page - serves the HTML interface"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('static', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chat functionality - integrated with your AI backend"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Call your actual AI backend
        try:
            response = requests.post(
                f"{AI_BACKEND_URL}/query",
                json={"question": user_message},
                timeout=30
            )
            
            if response.status_code == 200:
                ai_response = response.json().get('answer', 'No response from AI')
            else:
                # Fallback to intelligent response if AI backend fails
                ai_response = generate_fallback_response(user_message)
                
        except requests.exceptions.RequestException as e:
            print(f"AI Backend Error: {e}")
            # Fallback to intelligent response if AI backend is unavailable
            ai_response = generate_fallback_response(user_message)
        
        # Localize currency symbols when appropriate
        ai_response = localize_currency(ai_response, user_message)
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather', methods=['POST'])
def weather():
    """API endpoint for weather information - integrated with your weather tool"""
    try:
        data = request.get_json()
        city = data.get('city', '')
        country = data.get('country', '')
        
        if not city or not country:
            return jsonify({'error': 'City and country are required'}), 400
        
        # Call your actual weather tool
        try:
            # You can integrate this with your weather_tool.py
            from tools.weather_tool import get_weather_info
            weather_data = get_weather_info(city, country)
            return jsonify(weather_data)
        except ImportError:
            # Fallback to simulated weather if tool not available
            weather_data = {
                'city': city,
                'country': country,
                'temperature': 22,
                'condition': 'Sunny',
                'humidity': 65,
                'wind_speed': 12
            }
            return jsonify(weather_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/currency', methods=['POST'])
def currency():
    """API endpoint for currency conversion - integrated with your currency tool"""
    try:
        data = request.get_json()
        from_currency = data.get('from_currency', '')
        to_currency = data.get('to_currency', '')
        amount = float(data.get('amount', 0))
        
        if not from_currency or not to_currency or amount <= 0:
            return jsonify({'error': 'Invalid parameters'}), 400
        
        # Call your actual currency tool
        try:
            from tools.currency_conversion_tool import convert_currency
            result = convert_currency(from_currency, to_currency, amount)
            return jsonify(result)
        except ImportError:
            # Fallback to simulated conversion if tool not available
            exchange_rates = {
                'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0, 'CAD': 1.25},
                'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.4, 'CAD': 1.47},
                'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.7, 'CAD': 1.71},
                'JPY': {'USD': 0.009, 'EUR': 0.0077, 'GBP': 0.0066, 'CAD': 0.011},
                'CAD': {'USD': 0.80, 'EUR': 0.68, 'GBP': 0.58, 'JPY': 88.0}
            }
            
            rate = exchange_rates.get(from_currency, {}).get(to_currency, 1)
            converted_amount = amount * rate
            
            return jsonify({
                'from_currency': from_currency,
                'to_currency': to_currency,
                'amount': amount,
                'converted_amount': round(converted_amount, 2),
                'exchange_rate': round(rate, 4)
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/expenses', methods=['POST'])
def expenses():
    """API endpoint for expense calculation - integrated with your calculator tool"""
    try:
        data = request.get_json()
        flight_cost = float(data.get('flight_cost', 0))
        accommodation_cost = float(data.get('accommodation_cost', 0))
        daily_budget = float(data.get('daily_budget', 0))
        trip_duration = int(data.get('trip_duration', 0))
        
        if trip_duration <= 0:
            return jsonify({'error': 'Trip duration must be greater than 0'}), 400
        
        # Call your actual expense calculator tool
        try:
            from tools.expense_calculator_tools import calculate_travel_expenses
            result = calculate_travel_expenses(
                flight_cost, accommodation_cost, daily_budget, trip_duration
            )
            return jsonify(result)
        except ImportError:
            # Fallback to basic calculation if tool not available
            total_daily_cost = daily_budget * trip_duration
            total_cost = flight_cost + accommodation_cost + total_daily_cost
            average_daily_cost = total_cost / trip_duration
            
            return jsonify({
                'flight_cost': flight_cost,
                'accommodation_cost': accommodation_cost,
                'daily_budget': daily_budget,
                'trip_duration': trip_duration,
                'total_daily_cost': round(total_daily_cost, 2),
                'total_cost': round(total_cost, 2),
                'average_daily_cost': round(average_daily_cost, 2)
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/places', methods=['POST'])
def places():
    """API endpoint for place search - integrated with your place search tool"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        location = data.get('location', '')
        
        if not query or not location:
            return jsonify({'error': 'Query and location are required'}), 400
        
        # Call your actual place search tool
        try:
            from tools.place_search_tool import search_places
            results = search_places(query, location)
            return jsonify({
                'query': query,
                'location': location,
                'results': results
            })
        except ImportError:
            # Fallback to simulated search if tool not available
            places_results = [
                {
                    'name': f'{query} in {location}',
                    'rating': 4.5,
                    'type': 'Attraction',
                    'description': 'A popular destination that matches your search criteria.'
                },
                {
                    'name': f'{query} Experience',
                    'rating': 4.2,
                    'type': 'Activity',
                    'description': 'An exciting activity that you might enjoy.'
                },
                {
                    'name': f'{query} Tour',
                    'rating': 4.7,
                    'type': 'Tour',
                    'description': 'A guided tour option for your interests.'
                }
            ]
            
            return jsonify({
                'query': query,
                'location': location,
                'results': places_results
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_fallback_response(user_message):
    """Generate intelligent fallback response when AI backend is unavailable"""
    responses = {
        'paris': "Paris is a beautiful city! Here are some recommendations:\n\n• Best time to visit: April-June or September-October\n• Must-see attractions: Eiffel Tower, Louvre Museum, Notre-Dame Cathedral\n• Budget: $150-300/day for mid-range travel\n• Weather: Check current conditions before booking",
        'budget': "I can help you plan your travel budget! Here's what to consider:\n\n• Transportation (flights, local transport)\n• Accommodation (hotels, hostels, vacation rentals)\n• Food and dining\n• Activities and attractions\n• Emergency fund\n\nWhat type of trip are you planning?",
        'weather': "I can help you check weather conditions for your destination! Just let me know:\n\n• City and country\n• Travel dates\n• What activities you're planning\n\nThis will help me give you the most relevant weather information.",
        'japan': "Japan is amazing! Here are the best times to visit:\n\n• Spring (March-May): Cherry blossoms, mild weather\n• Summer (June-August): Festivals, but hot and humid\n• Fall (September-November): Beautiful autumn colors\n• Winter (December-February): Snow, hot springs, skiing\n\nWhat interests you most about Japan?"
    }
    
    user_message_lower = user_message.lower()
    
    for keyword, response in responses.items():
        if keyword in user_message_lower:
            return response
    
    # Default response
    return "I'd love to help you plan your trip! I can assist with:\n\n• Destination recommendations\n• Budget planning\n• Weather information\n• Travel tips and advice\n\nWhat specific aspect of travel planning would you like help with?"

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})

if __name__ == '__main__':
    print("🌍 BREVO - Smart Travel Planner")
    print("Starting Flask server...")
    print(f"AI Backend URL: {AI_BACKEND_URL}")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
