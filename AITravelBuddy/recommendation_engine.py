import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random

class RecommendationEngine:
    """
    Handles recommendation logic for the travel planner application.
    Uses a hybrid approach combining content-based filtering and rule-based recommendations.
    """
    
    def __init__(self, data_manager):
        """Initialize the recommendation engine with data manager"""
        self.data_manager = data_manager
    
    def create_user_feature_vector(self, user_preferences):
        """
        Create a feature vector from user preferences for content-based recommendation
        
        Args:
            user_preferences: Dictionary of user preferences
            
        Returns:
            numpy array representing user's feature vector
        """
        # Define activity category to feature mapping
        activity_to_feature = {
            "Cultural & Historical": "cultural",
            "Outdoor & Adventure": "outdoor",
            "Food & Culinary": "culinary",
            "Relaxation & Wellness": "relaxation",
            "Shopping": "shopping",
            "Entertainment": "entertainment",
            "Sightseeing": "sightseeing"
        }
        
        # Initialize features with zeros
        features = {
            "cultural": 0.0,
            "outdoor": 0.0,
            "culinary": 0.0,
            "relaxation": 0.0,
            "shopping": 0.0,
            "entertainment": 0.0,
            "sightseeing": 0.0
        }
        
        # Set feature values based on user's activity preferences (normalized)
        for activity in user_preferences["activities"]:
            if activity in activity_to_feature:
                features[activity_to_feature[activity]] = 1.0
        
        # Normalize the feature values if any activities were selected
        if user_preferences["activities"]:
            factor = 1.0 / len(user_preferences["activities"])
            for key in features:
                if features[key] > 0:
                    features[key] = 0.5 + (features[key] * factor * 0.5)  # Scale between 0.5 and 1.0 if selected
        
        # Determine cost level based on budget
        # Assume budget is for the whole trip
        daily_budget = user_preferences["budget"] / user_preferences["duration"]
        
        # Map daily budget to cost level (1-5 scale)
        if daily_budget < 50:
            cost_level = 1
        elif daily_budget < 100:
            cost_level = 2
        elif daily_budget < 200:
            cost_level = 3
        elif daily_budget < 350:
            cost_level = 4
        else:
            cost_level = 5
        
        # Create the feature vector
        user_vector = np.array([
            features["cultural"],
            features["outdoor"],
            features["culinary"],
            features["relaxation"],
            features["shopping"],
            features["entertainment"],
            features["sightseeing"],
            cost_level / 5.0  # Normalize cost level
        ])
        
        return user_vector
    
    def recommend_destination(self, user_preferences):
        """
        Recommend destinations based on user preferences using content-based filtering
        
        Args:
            user_preferences: Dictionary of user preferences
            
        Returns:
            List of recommended destinations sorted by relevance
        """
        # If destination is already specified, return it
        if "destination" in user_preferences and user_preferences["destination"]:
            dest = self.data_manager.get_destination_by_name(user_preferences["destination"])
            return [dest]
        
        # Create user feature vector
        user_vector = self.create_user_feature_vector(user_preferences)
        
        # Compute similarity scores
        destination_features = self.data_manager.destination_features
        similarities = cosine_similarity([user_vector], destination_features)[0]
        
        # Get destination IDs sorted by similarity
        destination_ids = self.data_manager.destinations_df["id"].values
        recommendations = pd.DataFrame({
            "destination_id": destination_ids,
            "similarity": similarities
        }).sort_values(by="similarity", ascending=False)
        
        # Get full destination data for each recommended ID
        recommended_destinations = []
        for dest_id in recommendations["destination_id"]:
            dest = self.data_manager.get_destination_by_id(dest_id)
            recommended_destinations.append(dest)
        
        return recommended_destinations
    
    def recommend_transportation(self, user_preferences):
        """
        Recommend transportation based on user preferences and travel distance
        
        Args:
            user_preferences: Dictionary of user preferences
            
        Returns:
            Dictionary with transportation details
        """
        # If transportation mode is already specified
        preferred_mode = user_preferences.get("transportation", "Any")
        
        # If mode is specified and not "Any", use that mode
        if preferred_mode != "Any":
            transport = self.data_manager.get_transportation_by_mode(preferred_mode)
            
            # Calculate some additional details
            origin = user_preferences["origin"]
            destination = user_preferences["destination"]
            
            # In a real application, we would use a distance API
            # For this mock-up, generate a reasonable distance
            if preferred_mode == "Plane":
                distance_km = random.randint(500, 5000)
            elif preferred_mode in ["Train", "Bus", "Car"]:
                distance_km = random.randint(50, 800)
            else:
                distance_km = random.randint(50, 2000)
            
            # Calculate cost based on distance and mode
            cost = distance_km * transport["typical_cost_per_km"]
            
            # Calculate travel time
            travel_time_hours = distance_km / transport["speed_km_h"]
            
            return {
                "mode": transport["mode"],
                "distance_km": distance_km,
                "cost": cost,
                "travel_time_hours": travel_time_hours,
                "details": f"From {origin} to {destination} via {transport['mode']}"
            }
        
        # Otherwise, recommend based on distance
        # In a real application, we would use a distance API
        # For this mock-up, we'll simulate distance-based recommendation
        
        # Generate a reasonable distance based on continents
        origin = user_preferences["origin"]
        destination = user_preferences["destination"]
        
        # Simulate intercontinental vs domestic travel
        if random.random() < 0.7:  # Assume 70% of trips are long distance
            distance_km = random.randint(1000, 8000)
        else:
            distance_km = random.randint(50, 800)
        
        # Choose transportation mode based on distance
        if distance_km > 1000:
            recommended_mode = "Plane"
        elif distance_km > 300:
            recommended_mode = random.choice(["Plane", "Train", "Car"])
        else:
            recommended_mode = random.choice(["Train", "Bus", "Car"])
        
        transport = self.data_manager.get_transportation_by_mode(recommended_mode)
        
        # Calculate cost based on distance and mode
        cost = distance_km * transport["typical_cost_per_km"]
        
        # Calculate travel time
        travel_time_hours = distance_km / transport["speed_km_h"]
        
        return {
            "mode": transport["mode"],
            "distance_km": distance_km,
            "cost": cost,
            "travel_time_hours": travel_time_hours,
            "details": f"From {origin} to {destination} via {transport['mode']}"
        }
    
    def recommend_accommodation(self, user_preferences, destination_id):
        """
        Recommend accommodation based on user preferences and budget
        
        Args:
            user_preferences: Dictionary of user preferences
            destination_id: ID of the destination
            
        Returns:
            Dictionary with accommodation details
        """
        # Get preferred accommodation type
        preferred_type = user_preferences.get("accommodation", "Any")
        
        # Get suitable accommodations by type
        accommodations = self.data_manager.get_accommodations_by_destination_and_type(
            destination_id, preferred_type
        )
        
        if not accommodations:
            # If no accommodations of the preferred type, get all for the destination
            accommodations = self.data_manager.get_accommodations_by_destination(destination_id)
        
        if not accommodations:
            # If still no accommodations, return a generic one
            return {
                "name": "Local Accommodation",
                "type": preferred_type if preferred_type != "Any" else "Hotel",
                "cost_per_night": 100,
                "total_cost": 100 * user_preferences["duration"],
                "rating": 4.0,
                "amenities": ["WiFi", "Breakfast"]
            }
        
        # Calculate daily accommodation budget
        # Assume accommodation is about 30-40% of daily budget
        daily_budget = user_preferences["budget"] / user_preferences["duration"]
        accommodation_budget = daily_budget * 0.35
        
        # Filter by budget
        affordable_accommodations = [a for a in accommodations if a["cost_per_night"] <= accommodation_budget]
        
        if not affordable_accommodations:
            # If no affordable options, sort by price and take the cheapest
            accommodations.sort(key=lambda x: x["cost_per_night"])
            selected = accommodations[0]
        else:
            # Sort affordable options by rating and take the best
            affordable_accommodations.sort(key=lambda x: (x["rating"], -x["cost_per_night"]), reverse=True)
            selected = affordable_accommodations[0]
        
        # Calculate total cost
        total_cost = selected["cost_per_night"] * user_preferences["duration"]
        
        # Enhance with total cost
        selected["total_cost"] = total_cost
        
        return selected
    
    def recommend_activities(self, user_preferences, destination_id, constraints=None):
        """
        Recommend activities based on user preferences, destination and constraints
        
        Args:
            user_preferences: Dictionary of user preferences
            destination_id: ID of the destination
            constraints: Optional dictionary of constraints (e.g., time of day, max cost)
            
        Returns:
            List of recommended activities
        """
        constraints = constraints or {}
        
        # Get all activities for this destination
        all_activities = self.data_manager.get_activities_by_destination(destination_id)
        
        if not all_activities:
            return []
        
        # Filter by user's activity interests
        preferred_categories = user_preferences["activities"]
        
        if preferred_categories:
            preferred_activities = [a for a in all_activities if a["category"] in preferred_categories]
            
            # If no activities match preferences, fall back to all activities
            if not preferred_activities:
                preferred_activities = all_activities
        else:
            preferred_activities = all_activities
        
        # Filter by time of day if specified
        time_of_day = constraints.get("time_of_day")
        if time_of_day:
            if time_of_day == "morning":
                preferred_activities = [a for a in preferred_activities if a["morning_suitable"]]
            elif time_of_day == "afternoon":
                preferred_activities = [a for a in preferred_activities if a["afternoon_suitable"]]
            elif time_of_day == "evening":
                preferred_activities = [a for a in preferred_activities if a["evening_suitable"]]
        
        # Filter by max cost if specified
        max_cost = constraints.get("max_cost")
        if max_cost is not None:
            preferred_activities = [a for a in preferred_activities if a["cost"] <= max_cost]
        
        # Sort by popularity (descending) and price (ascending)
        preferred_activities.sort(key=lambda x: (x["popularity"], -x["cost"]), reverse=True)
        
        # Return top activities
        max_results = constraints.get("max_results", 10)
        return preferred_activities[:max_results]

    def recommend_daily_plan(self, user_preferences, destination_id, day_number, daily_budget):
        """
        Create a daily plan with morning, afternoon, and evening activities
        
        Args:
            user_preferences: Dictionary of user preferences
            destination_id: ID of the destination
            day_number: Which day of the trip (1-indexed)
            daily_budget: Budget allocated for activities on this day
            
        Returns:
            Dictionary with daily plan details
        """
        # Calculate budget distribution
        morning_budget = daily_budget * 0.3
        afternoon_budget = daily_budget * 0.4
        evening_budget = daily_budget * 0.3
        
        # Get destination details
        destination = self.data_manager.get_destination_by_id(destination_id)
        
        # Get morning activities
        morning_activities = self.recommend_activities(
            user_preferences, 
            destination_id,
            {"time_of_day": "morning", "max_cost": morning_budget, "max_results": 3}
        )
        
        # Get afternoon activities
        afternoon_activities = self.recommend_activities(
            user_preferences, 
            destination_id,
            {"time_of_day": "afternoon", "max_cost": afternoon_budget, "max_results": 3}
        )
        
        # Get evening activities
        evening_activities = self.recommend_activities(
            user_preferences, 
            destination_id,
            {"time_of_day": "evening", "max_cost": evening_budget, "max_results": 3}
        )
        
        # Create morning plan
        if morning_activities:
            # Pick a random activity from top 3
            morning_activity = random.choice(morning_activities[:min(3, len(morning_activities))])
            morning_plan = {
                "description": morning_activity["description"],
                "cost": morning_activity["cost"]
            }
        else:
            morning_plan = {
                "description": f"Explore the area near your accommodation in {destination['name']}.",
                "cost": 0
            }
        
        # Create afternoon plan
        if afternoon_activities:
            # Pick a random activity from top 3
            afternoon_activity = random.choice(afternoon_activities[:min(3, len(afternoon_activities))])
            afternoon_plan = {
                "description": afternoon_activity["description"],
                "cost": afternoon_activity["cost"]
            }
        else:
            afternoon_plan = {
                "description": f"Enjoy local sights and culture in {destination['name']}.",
                "cost": morning_budget / 2
            }
        
        # Create evening plan
        if evening_activities:
            # Pick a random activity from top 3
            evening_activity = random.choice(evening_activities[:min(3, len(evening_activities))])
            evening_plan = {
                "description": evening_activity["description"],
                "cost": evening_activity["cost"]
            }
        else:
            evening_plan = {
                "description": f"Dine at a local restaurant and experience {destination['name']}'s nightlife.",
                "cost": evening_budget / 2
            }
        
        # Calculate total cost for the day
        total_cost = morning_plan["cost"] + afternoon_plan["cost"] + evening_plan["cost"]
        
        # Generate a creative title for the day
        if day_number == 1:
            title = f"Welcome to {destination['name']}"
        elif day_number == user_preferences["duration"]:
            title = f"Final Day in {destination['name']}"
        else:
            # Generate a creative title based on the activities
            activities_keywords = []
            if "cultural" in morning_activity.get("description", "").lower() or "museum" in morning_activity.get("description", "").lower():
                activities_keywords.append("Cultural")
            if "outdoor" in afternoon_activity.get("description", "").lower() or "nature" in afternoon_activity.get("description", "").lower():
                activities_keywords.append("Outdoor")
            if "food" in evening_activity.get("description", "").lower() or "cuisine" in evening_activity.get("description", "").lower():
                activities_keywords.append("Culinary")
            
            if activities_keywords:
                keyword = random.choice(activities_keywords)
                title = f"Day of {keyword} Exploration in {destination['name']}"
            else:
                title = f"Exploring {destination['name']} - Day {day_number}"
        
        return {
            "title": title,
            "morning": morning_plan,
            "afternoon": afternoon_plan,
            "evening": evening_plan,
            "total_cost": total_cost
        }
