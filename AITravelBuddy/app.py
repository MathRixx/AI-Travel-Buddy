import streamlit as st
import datetime
import pandas as pd

from data_manager import DataManager
from recommendation_engine import RecommendationEngine
from itinerary_generator import ItineraryGenerator
from utils import format_currency, calculate_date_range

# Set page title and configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'generated_itinerary' not in st.session_state:
    st.session_state.generated_itinerary = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = None
if 'destinations' not in st.session_state:
    st.session_state.destinations = None

# Initialize the data manager to load datasets
data_manager = DataManager()
recommendation_engine = RecommendationEngine(data_manager)
itinerary_generator = ItineraryGenerator(data_manager, recommendation_engine)

# Application title and description
st.title("AI Travel Planner")
st.write("Generate personalized travel itineraries based on your preferences")

# Main app layout with sidebar for inputs
with st.sidebar:
    st.header("Trip Preferences")
    
    # Origin location
    origin = st.text_input("Origin City/Country", "New York")
    
    # Get the list of available destinations
    destination_options = data_manager.get_destination_list()
    destination = st.selectbox("Destination", destination_options)
    
    # Travel dates
    col1, col2 = st.columns(2)
    with col1:
        today = datetime.date.today()
        start_date = st.date_input("Start Date", today + datetime.timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", today + datetime.timedelta(days=14))
    
    # Calculate trip duration
    trip_duration = (end_date - start_date).days
    if trip_duration < 1:
        st.error("End date must be after start date")
    else:
        st.info(f"Trip duration: {trip_duration} days")
    
    # Budget
    budget = st.slider("Budget (USD)", 500, 10000, 2000, step=100)
    st.write(f"Budget: {format_currency(budget)}")
    
    # Transportation preference
    transportation_options = ["Plane", "Train", "Bus", "Car", "Any"]
    transportation = st.selectbox("Preferred Transportation", transportation_options)
    
    # Accommodation preference
    accommodation_options = ["Hotel", "Hostel", "Airbnb", "Resort", "Any"]
    accommodation = st.selectbox("Preferred Accommodation", accommodation_options)
    
    # Activity interests - multiselect
    activity_options = ["Cultural & Historical", "Outdoor & Adventure", "Food & Culinary", 
                       "Relaxation & Wellness", "Shopping", "Entertainment", "Sightseeing"]
    activities = st.multiselect("Activity Interests", activity_options,
                               default=["Cultural & Historical", "Food & Culinary"])
    
    # Special requirements or notes
    special_requests = st.text_area("Special Requests/Notes", "")
    
    # Generate button
    generate_button = st.button("Generate Travel Plan", type="primary")

# Generate travel plan when the button is clicked
if generate_button:
    if trip_duration < 1:
        st.session_state.error_message = "Please select valid travel dates."
        st.session_state.generated_itinerary = None
    elif not activities:
        st.session_state.error_message = "Please select at least one activity interest."
        st.session_state.generated_itinerary = None
    else:
        with st.spinner("Generating your personalized travel plan..."):
            # Create user preferences dictionary
            user_preferences = {
                "origin": origin,
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date, 
                "duration": trip_duration,
                "budget": budget,
                "transportation": transportation,
                "accommodation": accommodation,
                "activities": activities,
                "special_requests": special_requests
            }
            
            try:
                # Generate the itinerary
                itinerary = itinerary_generator.generate_itinerary(user_preferences)
                
                # Save to session state
                st.session_state.generated_itinerary = itinerary
                st.session_state.user_preferences = user_preferences
                st.session_state.error_message = None
            except Exception as e:
                st.session_state.error_message = f"Error generating itinerary: {str(e)}"
                st.session_state.generated_itinerary = None

# Display error message if exists
if st.session_state.error_message:
    st.error(st.session_state.error_message)

# Display the generated itinerary if it exists
if st.session_state.generated_itinerary:
    itinerary = st.session_state.generated_itinerary
    preferences = st.session_state.user_preferences
    
    # Create tabs for different sections of the itinerary
    tab1, tab2, tab3 = st.tabs(["Overview", "Day-by-Day Itinerary", "Budget Breakdown"])
    
    with tab1:
        st.header(f"Your Trip to {preferences['destination']}")
        
        # Display trip summary in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Trip Details")
            st.write(f"**From:** {preferences['origin']}")
            st.write(f"**To:** {preferences['destination']}")
            st.write(f"**Dates:** {preferences['start_date'].strftime('%b %d')} - {preferences['end_date'].strftime('%b %d, %Y')}")
            st.write(f"**Duration:** {preferences['duration']} days")
        
        with col2:
            st.subheader("Transportation")
            st.write(f"**Mode:** {itinerary['transportation']['mode']}")
            if 'details' in itinerary['transportation']:
                st.write(f"**Details:** {itinerary['transportation']['details']}")
            st.write(f"**Cost:** {format_currency(itinerary['transportation']['cost'])}")
        
        with col3:
            st.subheader("Accommodation")
            st.write(f"**Type:** {itinerary['accommodation']['type']}")
            st.write(f"**Name:** {itinerary['accommodation']['name']}")
            st.write(f"**Cost:** {format_currency(itinerary['accommodation']['total_cost'])}")
            st.write(f"**Per Night:** {format_currency(itinerary['accommodation']['cost_per_night'])}")
        
        st.subheader("Trip Overview")
        st.write(itinerary['overview'])
    
    with tab2:
        st.header("Day-by-Day Itinerary")
        
        for day_num, day_plan in enumerate(itinerary['daily_plan'], 1):
            date = preferences['start_date'] + datetime.timedelta(days=day_num-1)
            
            with st.expander(f"Day {day_num}: {date.strftime('%A, %b %d, %Y')}", expanded=True if day_num == 1 else False):
                st.subheader(day_plan['title'])
                
                # Morning activities
                st.write("🌅 **Morning**")
                st.write(day_plan['morning']['description'])
                if 'cost' in day_plan['morning']:
                    st.write(f"Estimated cost: {format_currency(day_plan['morning']['cost'])}")
                
                # Afternoon activities
                st.write("☀️ **Afternoon**")
                st.write(day_plan['afternoon']['description'])
                if 'cost' in day_plan['afternoon']:
                    st.write(f"Estimated cost: {format_currency(day_plan['afternoon']['cost'])}")
                
                # Evening activities
                st.write("🌆 **Evening**")
                st.write(day_plan['evening']['description'])
                if 'cost' in day_plan['evening']:
                    st.write(f"Estimated cost: {format_currency(day_plan['evening']['cost'])}")
                
                st.write(f"**Daily Budget:** {format_currency(day_plan['total_cost'])}")
    
    with tab3:
        st.header("Budget Breakdown")
        
        # Create a pie chart for budget allocation
        budget_data = {
            'Category': ['Transportation', 'Accommodation', 'Activities', 'Food', 'Miscellaneous'],
            'Amount': [
                itinerary['transportation']['cost'],
                itinerary['accommodation']['total_cost'],
                itinerary['budget_breakdown']['activities'],
                itinerary['budget_breakdown']['food'],
                itinerary['budget_breakdown']['miscellaneous']
            ]
        }
        
        budget_df = pd.DataFrame(budget_data)
        
        total_cost = sum(budget_df['Amount'])
        remaining_budget = preferences['budget'] - total_cost
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Budget Allocation")
            st.bar_chart(budget_df.set_index('Category'))
        
        with col2:
            st.subheader("Budget Summary")
            st.write(f"**Total Budget:** {format_currency(preferences['budget'])}")
            st.write(f"**Estimated Expenses:** {format_currency(total_cost)}")
            
            if remaining_budget >= 0:
                st.write(f"**Remaining Budget:** {format_currency(remaining_budget)}")
            else:
                st.error(f"**Budget Exceeded by:** {format_currency(abs(remaining_budget))}")
        
        # Detailed budget breakdown
        st.subheader("Detailed Expenses")
        
        expense_details = []
        
        # Transportation
        expense_details.append({
            "Category": "Transportation",
            "Description": f"{itinerary['transportation']['mode']} ({preferences['origin']} to {preferences['destination']})",
            "Amount": itinerary['transportation']['cost']
        })
        
        # Accommodation
        expense_details.append({
            "Category": "Accommodation",
            "Description": f"{itinerary['accommodation']['type']} - {itinerary['accommodation']['name']} ({preferences['duration']} nights)",
            "Amount": itinerary['accommodation']['total_cost']
        })
        
        # Daily activities, food, etc.
        for day_num, day_plan in enumerate(itinerary['daily_plan'], 1):
            date = preferences['start_date'] + datetime.timedelta(days=day_num-1)
            
            # Activities for the day
            if 'cost' in day_plan['morning']:
                expense_details.append({
                    "Category": "Activities",
                    "Description": f"Day {day_num} - Morning: {day_plan['morning']['description'][:50]}...",
                    "Amount": day_plan['morning']['cost']
                })
                
            if 'cost' in day_plan['afternoon']:
                expense_details.append({
                    "Category": "Activities",
                    "Description": f"Day {day_num} - Afternoon: {day_plan['afternoon']['description'][:50]}...",
                    "Amount": day_plan['afternoon']['cost']
                })
                
            if 'cost' in day_plan['evening']:
                expense_details.append({
                    "Category": "Activities",
                    "Description": f"Day {day_num} - Evening: {day_plan['evening']['description'][:50]}...",
                    "Amount": day_plan['evening']['cost']
                })
        
        # Miscellaneous expenses
        expense_details.append({
            "Category": "Miscellaneous",
            "Description": "Souvenirs, tips, unexpected expenses, etc.",
            "Amount": itinerary['budget_breakdown']['miscellaneous']
        })
        
        # Convert to dataframe and display
        expenses_df = pd.DataFrame(expense_details)
        st.dataframe(expenses_df, use_container_width=True)

# If no itinerary is generated yet, show some sample destinations or tips
if not st.session_state.generated_itinerary and not st.session_state.error_message:
    st.info("👈 Complete your travel preferences in the sidebar and click 'Generate Travel Plan' to create your personalized itinerary.")
    
    st.subheader("Popular Destinations")
    
    # Display some featured destinations in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### Paris, France")
        st.write("Known for its art, culture, cuisine, and the iconic Eiffel Tower.")
        
    with col2:
        st.write("### Kyoto, Japan")
        st.write("Experience traditional Japanese culture, temples, and gardens.")
        
    with col3:
        st.write("### New York City, USA")
        st.write("The bustling metropolis with world-class museums, theaters, and dining.")
    
    st.subheader("Travel Planning Tips")
    st.write("""
    - **Book in advance** for better deals on flights and accommodation
    - **Pack light** to avoid extra baggage fees and easier mobility
    - **Research local customs** and basic phrases if traveling internationally
    - **Make copies** of important documents
    - **Check visa requirements** well before your planned travel dates
    """)
