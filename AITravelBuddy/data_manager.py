import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataManager:
    """
    Manages all data operations for the travel planner application.
    Creates and maintains in-memory datasets for destinations, activities,
    transportation, and accommodations.
    """
    
    def __init__(self):
        """Initialize the data manager and load all datasets"""
        # Generate sample datasets
        self._create_destination_data()
        self._create_activity_data()
        self._create_transportation_data()
        self._create_accommodation_data()
    
    def _create_destination_data(self):
        """Create destination dataset with features for recommendation"""
        # List of destinations with their features and attributes
        destinations = [
            {
                "id": 1,
                "name": "Paris, France",
                "region": "Europe",
                "cost_level": 3,  # 1-5 scale (1=budget, 5=luxury)
                "features": {
                    "cultural": 0.9,
                    "outdoor": 0.4,
                    "culinary": 0.8,
                    "relaxation": 0.5,
                    "shopping": 0.9,
                    "entertainment": 0.8,
                    "sightseeing": 0.9
                },
                "climate": "temperate",
                "best_seasons": ["spring", "fall"],
                "avg_daily_cost": 150,
                "languages": ["French", "English"],
                "currency": "EUR",
                "description": "The City of Light, known for its art, fashion, gastronomy, and culture.",
                "local_transportation": ["Metro", "Bus", "Taxi", "Bicycle"],
                "popular_attractions": [
                    "Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", 
                    "Arc de Triomphe", "Montmartre", "Seine River"
                ]
            },
            {
                "id": 2,
                "name": "Tokyo, Japan",
                "region": "Asia",
                "cost_level": 4,
                "features": {
                    "cultural": 0.8,
                    "outdoor": 0.3,
                    "culinary": 0.9,
                    "relaxation": 0.4,
                    "shopping": 0.8,
                    "entertainment": 0.9,
                    "sightseeing": 0.8
                },
                "climate": "temperate",
                "best_seasons": ["spring", "fall"],
                "avg_daily_cost": 120,
                "languages": ["Japanese", "English (limited)"],
                "currency": "JPY",
                "description": "A vibrant mix of traditional and ultramodern culture.",
                "local_transportation": ["Metro", "JR Lines", "Bus", "Taxi"],
                "popular_attractions": [
                    "Tokyo Tower", "Shibuya Crossing", "Meiji Shrine", 
                    "Senso-ji Temple", "Imperial Palace", "Akihabara"
                ]
            },
            {
                "id": 3,
                "name": "New York, USA",
                "region": "North America",
                "cost_level": 4,
                "features": {
                    "cultural": 0.9,
                    "outdoor": 0.5,
                    "culinary": 0.9,
                    "relaxation": 0.3,
                    "shopping": 0.9,
                    "entertainment": 0.9,
                    "sightseeing": 0.8
                },
                "climate": "temperate",
                "best_seasons": ["spring", "fall"],
                "avg_daily_cost": 200,
                "languages": ["English"],
                "currency": "USD",
                "description": "The city that never sleeps, a global center for finance, culture, and entertainment.",
                "local_transportation": ["Subway", "Bus", "Taxi", "Uber/Lyft"],
                "popular_attractions": [
                    "Times Square", "Statue of Liberty", "Central Park", 
                    "Empire State Building", "Broadway", "Brooklyn Bridge"
                ]
            },
            {
                "id": 4,
                "name": "Rome, Italy",
                "region": "Europe",
                "cost_level": 3,
                "features": {
                    "cultural": 1.0,
                    "outdoor": 0.6,
                    "culinary": 0.9,
                    "relaxation": 0.5,
                    "shopping": 0.7,
                    "entertainment": 0.6,
                    "sightseeing": 0.9
                },
                "climate": "mediterranean",
                "best_seasons": ["spring", "fall"],
                "avg_daily_cost": 120,
                "languages": ["Italian", "English (limited)"],
                "currency": "EUR",
                "description": "The Eternal City with ancient ruins, art, and cuisine.",
                "local_transportation": ["Metro", "Bus", "Taxi", "Tram"],
                "popular_attractions": [
                    "Colosseum", "Roman Forum", "Vatican City", 
                    "Trevi Fountain", "Pantheon", "Spanish Steps"
                ]
            },
            {
                "id": 5,
                "name": "Bali, Indonesia",
                "region": "Asia",
                "cost_level": 2,
                "features": {
                    "cultural": 0.7,
                    "outdoor": 0.9,
                    "culinary": 0.7,
                    "relaxation": 1.0,
                    "shopping": 0.5,
                    "entertainment": 0.6,
                    "sightseeing": 0.7
                },
                "climate": "tropical",
                "best_seasons": ["dry season (Apr-Oct)"],
                "avg_daily_cost": 60,
                "languages": ["Indonesian", "English"],
                "currency": "IDR",
                "description": "Island paradise with beaches, temples, and lush landscapes.",
                "local_transportation": ["Scooter rental", "Taxi", "Private driver"],
                "popular_attractions": [
                    "Ubud Monkey Forest", "Tanah Lot Temple", "Uluwatu Temple", 
                    "Kuta Beach", "Rice Terraces", "Mount Batur"
                ]
            },
            {
                "id": 6,
                "name": "Barcelona, Spain",
                "region": "Europe",
                "cost_level": 3,
                "features": {
                    "cultural": 0.8,
                    "outdoor": 0.7,
                    "culinary": 0.9,
                    "relaxation": 0.7,
                    "shopping": 0.8,
                    "entertainment": 0.7,
                    "sightseeing": 0.8
                },
                "climate": "mediterranean",
                "best_seasons": ["spring", "early summer", "fall"],
                "avg_daily_cost": 110,
                "languages": ["Spanish", "Catalan", "English"],
                "currency": "EUR",
                "description": "Vibrant city with stunning architecture, beaches, and cuisine.",
                "local_transportation": ["Metro", "Bus", "Taxi", "Bicycle"],
                "popular_attractions": [
                    "Sagrada Familia", "Park Güell", "La Rambla", 
                    "Gothic Quarter", "Casa Batlló", "Barceloneta Beach"
                ]
            },
            {
                "id": 7,
                "name": "Bangkok, Thailand",
                "region": "Asia",
                "cost_level": 2,
                "features": {
                    "cultural": 0.8,
                    "outdoor": 0.5,
                    "culinary": 0.9,
                    "relaxation": 0.5,
                    "shopping": 0.8,
                    "entertainment": 0.7,
                    "sightseeing": 0.7
                },
                "climate": "tropical",
                "best_seasons": ["cool season (Nov-Feb)"],
                "avg_daily_cost": 50,
                "languages": ["Thai", "English (limited)"],
                "currency": "THB",
                "description": "Bustling city with temples, markets, and vibrant street life.",
                "local_transportation": ["BTS Skytrain", "MRT Subway", "Taxi", "Tuk-tuk", "Boat"],
                "popular_attractions": [
                    "Grand Palace", "Wat Arun", "Chatuchak Market", 
                    "Khao San Road", "Jim Thompson House", "Chao Phraya River"
                ]
            },
            {
                "id": 8,
                "name": "Cape Town, South Africa",
                "region": "Africa",
                "cost_level": 2,
                "features": {
                    "cultural": 0.7,
                    "outdoor": 0.9,
                    "culinary": 0.7,
                    "relaxation": 0.6,
                    "shopping": 0.6,
                    "entertainment": 0.6,
                    "sightseeing": 0.8
                },
                "climate": "mediterranean",
                "best_seasons": ["spring", "summer (Oct-Apr)"],
                "avg_daily_cost": 80,
                "languages": ["English", "Afrikaans", "Xhosa"],
                "currency": "ZAR",
                "description": "Stunning coastal city with mountains, beaches, and wildlife.",
                "local_transportation": ["MyCiti Bus", "Taxi", "Uber", "Car rental"],
                "popular_attractions": [
                    "Table Mountain", "Robben Island", "Cape of Good Hope", 
                    "V&A Waterfront", "Kirstenbosch Gardens", "Boulders Beach"
                ]
            },
            {
                "id": 9,
                "name": "Sydney, Australia",
                "region": "Oceania",
                "cost_level": 4,
                "features": {
                    "cultural": 0.7,
                    "outdoor": 0.9,
                    "culinary": 0.8,
                    "relaxation": 0.7,
                    "shopping": 0.7,
                    "entertainment": 0.7,
                    "sightseeing": 0.8
                },
                "climate": "temperate",
                "best_seasons": ["spring", "fall"],
                "avg_daily_cost": 150,
                "languages": ["English"],
                "currency": "AUD",
                "description": "Harbor city with iconic landmarks, beaches, and outdoor lifestyle.",
                "local_transportation": ["Train", "Bus", "Ferry", "Light Rail", "Taxi"],
                "popular_attractions": [
                    "Sydney Opera House", "Sydney Harbour Bridge", "Bondi Beach", 
                    "Darling Harbour", "Royal Botanic Garden", "Taronga Zoo"
                ]
            },
            {
                "id": 10,
                "name": "Rio de Janeiro, Brazil",
                "region": "South America",
                "cost_level": 2,
                "features": {
                    "cultural": 0.7,
                    "outdoor": 0.9,
                    "culinary": 0.7,
                    "relaxation": 0.8,
                    "shopping": 0.6,
                    "entertainment": 0.8,
                    "sightseeing": 0.8
                },
                "climate": "tropical",
                "best_seasons": ["winter (May-Oct)"],
                "avg_daily_cost": 70,
                "languages": ["Portuguese", "English (limited)"],
                "currency": "BRL",
                "description": "Vibrant city with stunning beaches, mountains, and culture.",
                "local_transportation": ["Metro", "Bus", "Taxi", "Uber"],
                "popular_attractions": [
                    "Christ the Redeemer", "Sugarloaf Mountain", "Copacabana Beach", 
                    "Ipanema Beach", "Tijuca Forest", "Lapa Steps"
                ]
            }
        ]
        
        # Convert to DataFrame
        self.destinations_df = pd.DataFrame(destinations)
        
        # Create feature vectors for recommendations
        self.destination_features = np.array([
            [
                d["features"]["cultural"], 
                d["features"]["outdoor"], 
                d["features"]["culinary"],
                d["features"]["relaxation"],
                d["features"]["shopping"],
                d["features"]["entertainment"],
                d["features"]["sightseeing"],
                d["cost_level"] / 5.0  # Normalize cost level
            ] 
            for d in destinations
        ])
    
    def _create_activity_data(self):
        """Create activity dataset for each destination"""
        activities = []
        activity_id = 1
        
        for dest in self.destinations_df.to_dict(orient='records'):
            # Cultural & Historical
            cultural_activities = [
                {
                    "id": activity_id + i,
                    "destination_id": dest["id"],
                    "name": f"Museum/Cultural Site Visit in {dest['name']}",
                    "category": "Cultural & Historical",
                    "description": f"Visit a prominent museum or cultural landmark in {dest['name']}.",
                    "duration_hours": random.choice([2, 3, 4]),
                    "cost": random.randint(10, 40) * dest["cost_level"],
                    "morning_suitable": True,
                    "afternoon_suitable": True,
                    "evening_suitable": False,
                    "popularity": random.uniform(0.7, 0.95)
                } for i in range(3)
            ]
            activities.extend(cultural_activities)
            activity_id += 3
            
            # Outdoor & Adventure
            outdoor_activities = [
                {
                    "id": activity_id + i,
                    "destination_id": dest["id"],
                    "name": f"Outdoor Adventure in {dest['name']}",
                    "category": "Outdoor & Adventure",
                    "description": f"Enjoy the natural surroundings in {dest['name']} with hiking, walking tours, or outdoor sports.",
                    "duration_hours": random.choice([3, 4, 5]),
                    "cost": random.randint(20, 100) * dest["cost_level"] / 2,
                    "morning_suitable": True,
                    "afternoon_suitable": True,
                    "evening_suitable": False,
                    "popularity": random.uniform(0.6, 0.9)
                } for i in range(3)
            ]
            activities.extend(outdoor_activities)
            activity_id += 3
            
            # Food & Culinary
            food_activities = [
                {
                    "id": activity_id + i,
                    "destination_id": dest["id"],
                    "name": f"Culinary Experience in {dest['name']}",
                    "category": "Food & Culinary",
                    "description": f"Taste the local cuisine or join a food tour in {dest['name']}.",
                    "duration_hours": random.choice([2, 3]),
                    "cost": random.randint(30, 80) * dest["cost_level"] / 2,
                    "morning_suitable": False,
                    "afternoon_suitable": True,
                    "evening_suitable": True,
                    "popularity": random.uniform(0.8, 0.95)
                } for i in range(2)
            ]
            activities.extend(food_activities)
            activity_id += 2
            
            # Relaxation & Wellness
            relaxation_activities = [
                {
                    "id": activity_id + i,
                    "destination_id": dest["id"],
                    "name": f"Relaxation Activity in {dest['name']}",
                    "category": "Relaxation & Wellness",
                    "description": f"Unwind with spa treatments, beach time, or wellness activities in {dest['name']}.",
                    "duration_hours": random.choice([2, 3, 4]),
                    "cost": random.randint(40, 120) * dest["cost_level"] / 2,
                    "morning_suitable": True,
                    "afternoon_suitable": True,
                    "evening_suitable": True,
                    "popularity": random.uniform(0.7, 0.9)
                } for i in range(2)
            ]
            activities.extend(relaxation_activities)
            activity_id += 2
            
            # Shopping
            shopping_activities = [
                {
                    "id": activity_id,
                    "destination_id": dest["id"],
                    "name": f"Shopping Experience in {dest['name']}",
                    "category": "Shopping",
                    "description": f"Explore local markets, boutiques, or shopping districts in {dest['name']}.",
                    "duration_hours": random.choice([2, 3, 4]),
                    "cost": random.randint(0, 50) * dest["cost_level"],  # Base cost - actual shopping varies
                    "morning_suitable": False,
                    "afternoon_suitable": True,
                    "evening_suitable": True,
                    "popularity": random.uniform(0.6, 0.85)
                }
            ]
            activities.extend(shopping_activities)
            activity_id += 1
            
            # Entertainment
            entertainment_activities = [
                {
                    "id": activity_id + i,
                    "destination_id": dest["id"],
                    "name": f"Entertainment in {dest['name']}",
                    "category": "Entertainment",
                    "description": f"Enjoy shows, performances, or nightlife in {dest['name']}.",
                    "duration_hours": random.choice([2, 3, 4]),
                    "cost": random.randint(30, 100) * dest["cost_level"] / 2,
                    "morning_suitable": False,
                    "afternoon_suitable": False,
                    "evening_suitable": True,
                    "popularity": random.uniform(0.7, 0.9)
                } for i in range(2)
            ]
            activities.extend(entertainment_activities)
            activity_id += 2
            
            # Sightseeing
            sightseeing_activities = [
                {
                    "id": activity_id + i,
                    "destination_id": dest["id"],
                    "name": f"Sightseeing in {dest['name']}",
                    "category": "Sightseeing",
                    "description": f"Visit popular landmarks and attractions in {dest['name']}.",
                    "duration_hours": random.choice([2, 3, 4, 5]),
                    "cost": random.randint(10, 50) * dest["cost_level"] / 2,
                    "morning_suitable": True,
                    "afternoon_suitable": True,
                    "evening_suitable": random.choice([True, False]),
                    "popularity": random.uniform(0.8, 0.95)
                } for i in range(3)
            ]
            activities.extend(sightseeing_activities)
            activity_id += 3
        
        # Convert to DataFrame
        self.activities_df = pd.DataFrame(activities)
        
        # Add specific activities for destinations
        self._add_destination_specific_activities()
    
    def _add_destination_specific_activities(self):
        """Add some specific activities for each destination"""
        specific_activities = []
        activity_id = len(self.activities_df) + 1
        
        # Paris
        paris_activities = [
            {
                "id": activity_id,
                "destination_id": 1,
                "name": "Eiffel Tower Visit",
                "category": "Sightseeing",
                "description": "Visit the iconic symbol of Paris with options to go to the top for panoramic views.",
                "duration_hours": 3,
                "cost": 25,
                "morning_suitable": True,
                "afternoon_suitable": True,
                "evening_suitable": True,
                "popularity": 0.95
            },
            {
                "id": activity_id + 1,
                "destination_id": 1,
                "name": "Louvre Museum Tour",
                "category": "Cultural & Historical",
                "description": "Explore one of the world's largest art museums, home to the Mona Lisa.",
                "duration_hours": 4,
                "cost": 15,
                "morning_suitable": True,
                "afternoon_suitable": True,
                "evening_suitable": False,
                "popularity": 0.9
            },
            {
                "id": activity_id + 2,
                "destination_id": 1,
                "name": "Seine River Cruise",
                "category": "Sightseeing",
                "description": "See Paris from the water on a scenic boat tour along the Seine River.",
                "duration_hours": 1.5,
                "cost": 15,
                "morning_suitable": True,
                "afternoon_suitable": True,
                "evening_suitable": True,
                "popularity": 0.85
            }
        ]
        specific_activities.extend(paris_activities)
        activity_id += 3
        
        # Tokyo
        tokyo_activities = [
            {
                "id": activity_id,
                "destination_id": 2,
                "name": "Tsukiji Outer Market Tour",
                "category": "Food & Culinary",
                "description": "Explore the famous seafood market and enjoy fresh sushi for breakfast.",
                "duration_hours": 3,
                "cost": 40,
                "morning_suitable": True,
                "afternoon_suitable": False,
                "evening_suitable": False,
                "popularity": 0.85
            },
            {
                "id": activity_id + 1,
                "destination_id": 2,
                "name": "Shibuya Crossing Experience",
                "category": "Sightseeing",
                "description": "Witness the busiest pedestrian crossing in the world and explore the Shibuya district.",
                "duration_hours": 2,
                "cost": 0,
                "morning_suitable": True,
                "afternoon_suitable": True,
                "evening_suitable": True,
                "popularity": 0.9
            },
            {
                "id": activity_id + 2,
                "destination_id": 2,
                "name": "Robot Restaurant Show",
                "category": "Entertainment",
                "description": "Experience a uniquely Japanese spectacle of lights, music, and robots in Shinjuku.",
                "duration_hours": 2,
                "cost": 80,
                "morning_suitable": False,
                "afternoon_suitable": False,
                "evening_suitable": True,
                "popularity": 0.8
            }
        ]
        specific_activities.extend(tokyo_activities)
        activity_id += 3
        
        # More activities for other destinations...
        # (Would add more, but keeping it concise for this example)
        
        # Add to the activities DataFrame
        new_activities_df = pd.DataFrame(specific_activities)
        self.activities_df = pd.concat([self.activities_df, new_activities_df], ignore_index=True)
    
    def _create_transportation_data(self):
        """Create transportation options dataset"""
        self.transportation_df = pd.DataFrame([
            {
                "mode": "Plane",
                "typical_cost_per_km": 0.15,
                "speed_km_h": 900,
                "comfort_level": 3,
                "eco_friendliness": 1,
                "suitable_distance_min_km": 300,
                "suitable_distance_max_km": 20000
            },
            {
                "mode": "Train",
                "typical_cost_per_km": 0.10,
                "speed_km_h": 200,
                "comfort_level": 4,
                "eco_friendliness": 4,
                "suitable_distance_min_km": 50,
                "suitable_distance_max_km": 1000
            },
            {
                "mode": "Bus",
                "typical_cost_per_km": 0.05,
                "speed_km_h": 80,
                "comfort_level": 2,
                "eco_friendliness": 3,
                "suitable_distance_min_km": 10,
                "suitable_distance_max_km": 800
            },
            {
                "mode": "Car",
                "typical_cost_per_km": 0.20,
                "speed_km_h": 100,
                "comfort_level": 4,
                "eco_friendliness": 2,
                "suitable_distance_min_km": 5,
                "suitable_distance_max_km": 1000
            },
            {
                "mode": "Ferry",
                "typical_cost_per_km": 0.08,
                "speed_km_h": 40,
                "comfort_level": 3,
                "eco_friendliness": 3,
                "suitable_distance_min_km": 10,
                "suitable_distance_max_km": 500
            }
        ])
    
    def _create_accommodation_data(self):
        """Create accommodation options dataset for each destination"""
        accommodations = []
        
        for dest in self.destinations_df.to_dict(orient='records'):
            # Budget options
            budget_options = [
                {
                    "destination_id": dest["id"],
                    "name": f"Budget Hotel in {dest['name']}",
                    "type": "Hotel",
                    "cost_per_night": int(30 * dest["cost_level"]),
                    "rating": random.uniform(3.0, 4.0),
                    "amenities": ["WiFi", "Air Conditioning"],
                    "suitable_for": ["Solo", "Couple", "Friends"],
                    "location_quality": random.uniform(3.0, 4.0)
                },
                {
                    "destination_id": dest["id"],
                    "name": f"Hostel in {dest['name']}",
                    "type": "Hostel",
                    "cost_per_night": int(20 * dest["cost_level"]),
                    "rating": random.uniform(3.0, 4.0),
                    "amenities": ["WiFi", "Shared Kitchen", "Lounge"],
                    "suitable_for": ["Solo", "Friends"],
                    "location_quality": random.uniform(3.5, 4.5)
                }
            ]
            accommodations.extend(budget_options)
            
            # Mid-range options
            midrange_options = [
                {
                    "destination_id": dest["id"],
                    "name": f"Mid-range Hotel in {dest['name']}",
                    "type": "Hotel",
                    "cost_per_night": int(60 * dest["cost_level"]),
                    "rating": random.uniform(3.5, 4.5),
                    "amenities": ["WiFi", "Air Conditioning", "Restaurant", "Room Service"],
                    "suitable_for": ["Solo", "Couple", "Family", "Friends"],
                    "location_quality": random.uniform(3.5, 4.5)
                },
                {
                    "destination_id": dest["id"],
                    "name": f"Airbnb Apartment in {dest['name']}",
                    "type": "Airbnb",
                    "cost_per_night": int(50 * dest["cost_level"]),
                    "rating": random.uniform(3.8, 4.8),
                    "amenities": ["WiFi", "Kitchen", "Washer", "Air Conditioning"],
                    "suitable_for": ["Solo", "Couple", "Family", "Friends"],
                    "location_quality": random.uniform(3.5, 4.5)
                }
            ]
            accommodations.extend(midrange_options)
            
            # Luxury options
            luxury_options = [
                {
                    "destination_id": dest["id"],
                    "name": f"Luxury Hotel in {dest['name']}",
                    "type": "Hotel",
                    "cost_per_night": int(150 * dest["cost_level"]),
                    "rating": random.uniform(4.0, 4.9),
                    "amenities": ["WiFi", "Air Conditioning", "Pool", "Spa", "Gym", "Restaurant", "Room Service"],
                    "suitable_for": ["Solo", "Couple", "Family"],
                    "location_quality": random.uniform(4.0, 5.0)
                },
                {
                    "destination_id": dest["id"],
                    "name": f"Resort in {dest['name']}",
                    "type": "Resort",
                    "cost_per_night": int(200 * dest["cost_level"]),
                    "rating": random.uniform(4.2, 5.0),
                    "amenities": ["WiFi", "Air Conditioning", "Pool", "Spa", "Gym", "Multiple Restaurants", "Private Beach/Garden"],
                    "suitable_for": ["Couple", "Family"],
                    "location_quality": random.uniform(4.5, 5.0)
                }
            ]
            accommodations.extend(luxury_options)
        
        # Convert to DataFrame
        self.accommodations_df = pd.DataFrame(accommodations)
    
    def get_destination_list(self):
        """Return a list of all destination names"""
        return self.destinations_df["name"].tolist()
    
    def get_destination_by_name(self, name):
        """Return destination data by name"""
        return self.destinations_df[self.destinations_df["name"] == name].iloc[0].to_dict()
    
    def get_destination_by_id(self, destination_id):
        """Return destination data by ID"""
        return self.destinations_df[self.destinations_df["id"] == destination_id].iloc[0].to_dict()
    
    def get_activities_by_destination(self, destination_id):
        """Return activities for a specific destination"""
        return self.activities_df[self.activities_df["destination_id"] == destination_id].to_dict(orient='records')
    
    def get_activities_by_destination_and_category(self, destination_id, category):
        """Return activities for a specific destination and category"""
        mask = (self.activities_df["destination_id"] == destination_id) & (self.activities_df["category"] == category)
        return self.activities_df[mask].to_dict(orient='records')
    
    def get_accommodations_by_destination(self, destination_id):
        """Return accommodations for a specific destination"""
        return self.accommodations_df[self.accommodations_df["destination_id"] == destination_id].to_dict(orient='records')
    
    def get_accommodations_by_destination_and_type(self, destination_id, accommodation_type):
        """Return accommodations for a specific destination and type"""
        if accommodation_type == "Any":
            return self.get_accommodations_by_destination(destination_id)
        
        mask = (self.accommodations_df["destination_id"] == destination_id) & (self.accommodations_df["type"] == accommodation_type)
        return self.accommodations_df[mask].to_dict(orient='records')
    
    def get_transportation_options(self):
        """Return all transportation options"""
        return self.transportation_df.to_dict(orient='records')
    
    def get_transportation_by_mode(self, mode):
        """Return transportation data by mode"""
        if mode == "Any":
            # Choose a random transportation mode
            return self.transportation_df.sample(1).iloc[0].to_dict()
        return self.transportation_df[self.transportation_df["mode"] == mode].iloc[0].to_dict()
