import random
from datetime import datetime, timedelta

class ItineraryGenerator:
    """
    Generates complete travel itineraries based on recommendations and user preferences.
    """
    
    def __init__(self, data_manager, recommendation_engine):
        """Initialize the itinerary generator"""
        self.data_manager = data_manager
        self.recommendation_engine = recommendation_engine
    
    def generate_itinerary(self, user_preferences):
        """
        Generate a complete travel itinerary based on user preferences
        
        Args:
            user_preferences: Dictionary of user preferences
            
        Returns:
            Dictionary with complete itinerary details
        """
        # Get destination data
        destination = self.data_manager.get_destination_by_name(user_preferences["destination"])
        destination_id = destination["id"]
        
        # Get recommended transportation
        transportation = self.recommendation_engine.recommend_transportation(user_preferences)
        
        # Get recommended accommodation
        accommodation = self.recommendation_engine.recommend_accommodation(user_preferences, destination_id)
        
        # Calculate remaining budget after transportation and accommodation
        transportation_cost = transportation["cost"]
        accommodation_cost = accommodation["total_cost"]
        remaining_budget = user_preferences["budget"] - transportation_cost - accommodation_cost
        
        # Ensure we have at least some budget for activities
        if remaining_budget < 0:
            remaining_budget = user_preferences["budget"] * 0.2  # Allocate 20% for activities
        
        # Calculate daily activity budget
        daily_activity_budget = remaining_budget / user_preferences["duration"]
        
        # Generate daily plans
        daily_plans = []
        for day in range(1, user_preferences["duration"] + 1):
            daily_plan = self.recommendation_engine.recommend_daily_plan(
                user_preferences, destination_id, day, daily_activity_budget
            )
            daily_plans.append(daily_plan)
        
        # Calculate total activities cost
        activities_cost = sum(plan["total_cost"] for plan in daily_plans)
        
        # Allocate budget for food and miscellaneous
        food_budget = remaining_budget * 0.4
        misc_budget = remaining_budget * 0.1
        
        # Generate overview text
        overview = self._generate_overview_text(
            user_preferences, destination, transportation, accommodation, daily_plans
        )
        
        # Construct the complete itinerary
        itinerary = {
            "destination": destination,
            "transportation": transportation,
            "accommodation": accommodation,
            "daily_plan": daily_plans,
            "overview": overview,
            "budget_breakdown": {
                "transportation": transportation_cost,
                "accommodation": accommodation_cost,
                "activities": activities_cost,
                "food": food_budget,
                "miscellaneous": misc_budget
            }
        }
        
        return itinerary
    
    def _generate_overview_text(self, user_preferences, destination, transportation, accommodation, daily_plans):
        """Generate a textual overview of the trip"""
        total_days = user_preferences["duration"]
        destination_name = destination["name"]
        transport_mode = transportation["mode"]
        accommodation_type = accommodation["type"]
        
        # Format dates
        start_date = user_preferences["start_date"].strftime("%B %d, %Y")
        end_date = user_preferences["end_date"].strftime("%B %d, %Y")
        
        # Create an engaging introduction
        intros = [
            f"Get ready for an amazing {total_days}-day adventure in {destination_name}!",
            f"Your {total_days}-day journey to beautiful {destination_name} awaits!",
            f"Prepare for an unforgettable {total_days}-day experience in {destination_name}!"
        ]
        intro = random.choice(intros)
        
        # Transportation description
        transport_desc = f"You'll travel from {user_preferences['origin']} to {destination_name} by {transport_mode.lower()}."
        
        # Accommodation description
        accommodation_desc = f"During your stay, you'll be enjoying the comfort of a {accommodation_type.lower()} accommodation at {accommodation['name']}."
        
        # Activities highlight
        activities = []
        for plan in daily_plans:
            if "description" in plan["morning"]:
                activities.append(plan["morning"]["description"])
            if "description" in plan["afternoon"]:
                activities.append(plan["afternoon"]["description"])
            if "description" in plan["evening"]:
                activities.append(plan["evening"]["description"])
        
        # Pick 3 random activities to highlight
        if activities:
            sample_size = min(3, len(activities))
            highlighted_activities = random.sample(activities, sample_size)
            activities_desc = "Some highlights of your trip include: " + "; ".join(highlighted_activities)
        else:
            activities_desc = f"You'll have plenty of time to explore the best of {destination_name}."
        
        # Destination specific note
        destination_notes = f"{destination_name} is known for {destination['description']}"
        
        # Put it all together
        overview = f"{intro}\n\n"
        overview += f"From {start_date} to {end_date}, you'll be exploring {destination_name}. "
        overview += f"{transport_desc} {accommodation_desc}\n\n"
        overview += f"{activities_desc}\n\n"
        overview += f"{destination_notes}"
        
        return overview
