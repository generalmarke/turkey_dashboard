import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import requests

# Function to load data (ensure your file path and sheet name are correct)
@st.cache_data
def load_data():
    return pd.read_excel("turkey_trip.xlsx")

data = load_data()


def get_weather_data(city, api_key):
    """Fetch weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data

def display_weather(data):
    """Display weather information."""
    temp = data['main']['temp']
    weather_description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    st.write(f"**Current Temperature:** {temp}°C")
    st.write(f"**Weather:** {weather_description.capitalize()}")
    st.write(f"**Humidity:** {humidity}%")
    st.write(f"**Wind Speed:** {wind_speed} m/s")

# API Key
api_key = '4ae3d5ad8f93e35dac21c0b2c66f5a54'

# User input for location
city = st.text_input('Enter city name:', 'Istanbul')

if st.button('Get Weather'):
    weather_data = get_weather_data(city, api_key)
    display_weather(weather_data)


def format_data_as_markdown(data):
    markdown = "| Date | Location | Description | Google Maps Link |\n"
    markdown += "|------|----------|-------------|------------------|\n"
    for _, row in data.iterrows():
        google_maps_link = f"[Link]({row['Google Maps Link']})"
        markdown += f"| {row['Date']} | {row['Location']} | {row['Description']} | {google_maps_link} |\n"
    return markdown

# Function to create a map with markers for each location, focusing on specific dates or all data
def create_map(data, selected_date, focus_index=None):
    # Starting coordinates for Istanbul or focused location
    if focus_index is not None:
        start_coords = (data.loc[focus_index, 'Latitude'], data.loc[focus_index, 'Longitude'])
        zoom_start = 16  # Closer zoom when focusing on a location
    else:
        start_coords = (41.0083, 28.9784)  # Central Istanbul coordinates for general view
        zoom_start = 12
    
    travel_map = folium.Map(location=start_coords, zoom_start=zoom_start)

    # Filtering data based on selected date
    if selected_date != 'All Days':
        data = data[data['Date'] == selected_date]

    # Adding markers to the map
    for idx, row in data.iterrows():
        popup = folium.Popup(f"{row['Location']}: {row['Description']}<br><a href='{row['Google Maps Link']}' target='_blank'>Google Maps</a>", max_width=250)
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup,
            tooltip=row['Location']
        ).add_to(travel_map)

    return travel_map

# Streamlit application layout
st.title('Turkey Trip Itinerary Dashboard')

# Selecting a date or 'All Days' to view locations
date_options = ['All Days'] + sorted(data['Date'].unique().tolist())
selected_date = st.selectbox('Select a date to view:', date_options)

# Optional: Selecting a location to focus on
location_to_focus = st.selectbox('Focus on a specific location:', ['None'] + data['Location'].unique().tolist())
focus_index = None
if location_to_focus != 'None':
    focus_index = data[data['Location'] == location_to_focus].index[0]

map_size = st.radio("Select Map Size:", ('Standard', 'Large'))
map_width, map_height = (700, 500) if map_size == 'Standard' else (1050, 750)

# Display the map based on selections
trip_map = create_map(data, selected_date, focus_index=focus_index)
folium_static(trip_map, width=map_width, height=map_height)

# Display itinerary with collapsible sections
st.subheader("Istanbul Itinerary for a Family (January 15 - 19, 2025)")

with st.expander("Day 1: January 15, 2025 - Arrival and Local Exploration"):
    st.write("""
    - **Arrival & Check-in:** Settle into your hotel after arriving at 11:35 AM.
    - **Lunch:** Dine at Sultanahmet Koftecisi for an authentic Turkish meal.
    - **Afternoon:**
        - Hagia Sophia - Grand Mosque: Start your exploration with this iconic site.
        - Blue Mosque: Visit this historic mosque, perfect for afternoon prayers.
    - **Evening:**
        - Dinner at Neolokal in Beyoğlu: Enjoy a family dinner with a variety of Turkish mezze.
        - Istiklal Street: Stroll down this famous street for some light shopping and street food.
    """)

with st.expander("Day 2: January 16, 2025 - Cultural Delights and Bosphorus Views"):
    st.write("""
    - **Morning:**
        - Topkapi Palace: Explore the rich history of the Ottoman sultans.
        - Istanbul Archaeology Museums: A short walk from Topkapi, these museums are great for educational insights.
    - **Lunch:** Humdi Restaurant, ideally by the window for Bosphorus views.
    - **Afternoon:**
        - Bosphorus Cruise: Relax on a cruise, enjoying the city's panorama.
        - Grand Bazaar (Kapalıçarşı): Shop and explore this historic market.
    - **Evening:**
        - Dinner at Karaköy Lokantası: Offers traditional Turkish dishes in a family-friendly atmosphere.
        - Galata Tower at Sunset: Witness stunning views of Istanbul.
    """)

with st.expander("Day 3: January 17, 2025 - A Day of Prayer and Historical Insights"):
    st.write("""
    - **Morning:**
        - Süleymaniye Mosque: Attend Jummah Salah at one of Istanbul’s largest and most majestic mosques.
        - Spice Bazaar (Eminönü): Post-prayer, explore the vibrant colors and scents of the Spice Bazaar.
    - **Lunch:** Enjoy a meal at Pandeli, known for its historical charm and exquisite Turkish dishes.
    - **Afternoon:**
        - Chora Church (Kariye Museum): Discover the stunning mosaics and frescoes.
        - Miniature Park: A fun place for kids to see miniature versions of Turkey’s famous landmarks.
    - **Evening:**
        - Bosphorus Dinner Cruise: Conclude your day with a dinner cruise, offering spectacular views.
        - Explore Moda in Kadiköy: This trendy neighborhood offers a more laid-back atmosphere.
    """)

with st.expander("Day 4: January 18, 2025 - Palaces and Modern Art"):
    st.write("""
    - **Morning:**
        - Dolmabahçe Palace: Tour the opulent interiors.
        - Breakfast at Karabatak: Start your day with a hearty breakfast.
    - **Afternoon:**
        - Istanbul Modern Art Museum: Engage with contemporary art.
        - Lunch at a waterfront restaurant: Enjoy fresh seafood.
        - Ferry to Kadıköy: Experience the local ferry transport.
    - **Evening:**
        - Dinner and leisure time in Beyoğlu: Casual dinner and desserts.
    """)

with st.expander("Day 5: January 19, 2025 - Departure"):
    st.write("""
    - **Morning:**
        - Pack up and check-out: Ensure you leave enough time for the airport.
        - Brief visit to Ortaköy: Explore the charming neighborhood.
    - **Departure:** Leave for Istanbul Airport by at least 11:00 AM for your 2:30 PM flight.
    """)

# Initial call to display data table with links
if st.button('Show Data'):
    st.markdown(format_data_as_markdown(data), unsafe_allow_html=True)
