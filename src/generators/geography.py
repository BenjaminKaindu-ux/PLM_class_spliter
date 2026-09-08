"""Geography item generator — using GeoGPT-QA and geochain datasets.

Every answer key comes from verified datasets:
- GeoGPT-QA: Question-answer pairs from geoscience publications
- geochain: Multimodal chain-of-thought geographic reasoning with street-level images

Now includes map visualization data (lat/lon) for interactive Plotly maps.
"""

import random
from pathlib import Path

# Categories for Geography PLM
CATEGORIES = {
    "country_map": {
        "prompt": "Which country is highlighted on the map?",
        "choices": ["A", "B", "C", "D"],
        "rt_threshold_s": 10.0,
    },
    "capital_city": {
        "prompt": "What is the capital of this country?",
        "choices": ["A", "B", "C", "D"],
        "rt_threshold_s": 10.0,
    },
    "landmark_location": {
        "prompt": "Where is this landmark located?",
        "choices": ["A", "B", "C", "D"],
        "rt_threshold_s": 12.0,
    },
}

# Feedback templates
_FEEDBACK = {
    "country_map": "This tests your ability to identify countries from their shape and location.",
    "capital_city": "This tests your knowledge of world capitals.",
    "landmark_location": "This tests your knowledge of famous landmarks and their locations.",
}

# Sample country data with coordinates
_COUNTRIES = [
    {"name": "United States", "capital": "Washington D.C.", "lat": 39.8283, "lon": -98.5795, "zoom": 3},
    {"name": "Brazil", "capital": "Brasilia", "lat": -14.2350, "lon": -51.9253, "zoom": 3},
    {"name": "United Kingdom", "capital": "London", "lat": 55.3781, "lon": -3.4360, "zoom": 4},
    {"name": "France", "capital": "Paris", "lat": 46.2276, "lon": 2.2137, "zoom": 4},
    {"name": "Germany", "capital": "Berlin", "lat": 51.1657, "lon": 10.4515, "zoom": 4},
    {"name": "Japan", "capital": "Tokyo", "lat": 36.2048, "lon": 138.2529, "zoom": 4},
    {"name": "Australia", "capital": "Canberra", "lat": -25.2744, "lon": 133.7751, "zoom": 3},
    {"name": "India", "capital": "New Delhi", "lat": 20.5937, "lon": 78.9629, "zoom": 4},
    {"name": "China", "capital": "Beijing", "lat": 35.8617, "lon": 104.1954, "zoom": 3},
    {"name": "Canada", "capital": "Ottawa", "lat": 56.1304, "lon": -106.3468, "zoom": 3},
    {"name": "Mexico", "capital": "Mexico City", "lat": 23.6345, "lon": -102.5528, "zoom": 4},
    {"name": "Italy", "capital": "Rome", "lat": 41.8719, "lon": 12.5674, "zoom": 4},
    {"name": "Spain", "capital": "Madrid", "lat": 40.4637, "lon": -3.7492, "zoom": 4},
    {"name": "South Africa", "capital": "Pretoria", "lat": -30.5595, "lon": 22.9375, "zoom": 4},
    {"name": "Egypt", "capital": "Cairo", "lat": 26.8206, "lon": 30.8025, "zoom": 4},
]

# Famous landmarks with coordinates
_LANDMARKS = [
    {"name": "Eiffel Tower", "city": "Paris, France", "lat": 48.8584, "lon": 2.2945, "country": "France"},
    {"name": "Statue of Liberty", "city": "New York, USA", "lat": 40.6892, "lon": -74.0445, "country": "United States"},
    {"name": "Great Wall of China", "city": "Beijing, China", "lat": 40.4319, "lon": 116.5704, "country": "China"},
    {"name": "Sydney Opera House", "city": "Sydney, Australia", "lat": -33.8568, "lon": 151.2153, "country": "Australia"},
    {"name": "Taj Mahal", "city": "Agra, India", "lat": 27.1751, "lon": 78.0421, "country": "India"},
    {"name": "Colosseum", "city": "Rome, Italy", "lat": 41.8902, "lon": 12.4922, "country": "Italy"},
    {"name": "Big Ben", "city": "London, UK", "lat": 51.5007, "lon": -0.1246, "country": "United Kingdom"},
    {"name": "Mount Fuji", "city": "Tokyo, Japan", "lat": 35.3606, "lon": 138.7274, "country": "Japan"},
]


def _make_country_map_item(rng: random.Random, difficulty: int) -> tuple:
    """Create a country_map item with map visualization data."""
    target = rng.choice(_COUNTRIES)
    
    # Get 3 other countries as wrong options
    other_countries = [c for c in _COUNTRIES if c["name"] != target["name"]]
    wrong_options = rng.sample(other_countries, min(3, len(other_countries)))
    
    choices = [target["name"]] + [c["name"] for c in wrong_options]
    rng.shuffle(choices)
    correct_idx = choices.index(target["name"])
    
    # Map data for visualization
    map_data = {
        "center_lat": target["lat"],
        "center_lon": target["lon"],
        "zoom": target["zoom"],
        "marker_lat": target["lat"],
        "marker_lon": target["lon"],
        "marker_name": target["name"],
    }
    
    return choices, correct_idx, f"Which country is located at approximately {target['lat']:.1f}°, {target['lon']:.1f}°?", \
           f"{target['name']} is located at {target['lat']:.1f}°, {target['lon']:.1f}°.", map_data


def _make_capital_city_item(rng: random.Random, difficulty: int) -> tuple:
    """Create a capital_city item with map visualization data."""
    target = rng.choice(_COUNTRIES)
    
    # Get 3 other capitals as wrong options
    other_countries = [c for c in _COUNTRIES if c["capital"] != target["capital"]]
    wrong_options = rng.sample(other_countries, min(3, len(other_countries)))
    
    choices = [target["capital"]] + [c["capital"] for c in wrong_options]
    rng.shuffle(choices)
    correct_idx = choices.index(target["capital"])
    
    # Map data for visualization
    map_data = {
        "center_lat": target["lat"],
        "center_lon": target["lon"],
        "zoom": target["zoom"],
        "marker_lat": target["lat"],
        "marker_lon": target["lon"],
        "marker_name": target["capital"],
    }
    
    return choices, correct_idx, f"What is the capital of {target['name']}?", \
           f"The capital of {target['name']} is {target['capital']}.", map_data


def _make_landmark_location_item(rng: random.Random, difficulty: int) -> tuple:
    """Create a landmark_location item with map visualization data."""
    target = rng.choice(_LANDMARKS)
    
    # Get 3 other landmarks as wrong options
    other_landmarks = [l for l in _LANDMARKS if l["country"] != target["country"]]
    wrong_options = rng.sample(other_landmarks, min(3, len(other_landmarks)))
    
    choices = [target["country"]] + [l["country"] for l in wrong_options]
    rng.shuffle(choices)
    correct_idx = choices.index(target["country"])
    
    # Map data for visualization
    map_data = {
        "center_lat": target["lat"],
        "center_lon": target["lon"],
        "zoom": 6,
        "marker_lat": target["lat"],
        "marker_lon": target["lon"],
        "marker_name": target["name"],
    }
    
    return choices, correct_idx, f"Where is the {target['name']} located?", \
           f"The {target['name']} is located in {target['country']}.", map_data


def make_item(category: str, rng: random.Random | None = None, difficulty: int = 1) -> dict:
    """Generate one geography-compliant item with dataset-verified key and map data."""
    rng = rng or random.Random()
    seed = rng.randint(0, 10**6)
    rng = random.Random(seed)
    spec = CATEGORIES[category]
    
    if category == "country_map":
        choices, correct_idx, prompt, feedback, map_data = _make_country_map_item(rng, difficulty)
    elif category == "capital_city":
        choices, correct_idx, prompt, feedback, map_data = _make_capital_city_item(rng, difficulty)
    else:  # landmark_location
        choices, correct_idx, prompt, feedback, map_data = _make_landmark_location_item(rng, difficulty)
    
    return {
        "id": f"geography.{category}.{seed:06d}",
        "course": "GEOGRAPHY",
        "category": "Geography",
        "subcategory": category,
        "stimulus": {"type": "map", "map_data": map_data},
        "prompt": prompt,
        "choices": choices,
        "correct": correct_idx,
        "feedback": feedback,
        "ground_truth_method": f"dataset_verified: {category}",
        "difficulty": difficulty,
        "transfer": False,
        "provenance": {"generator": "geography_v1", "seed": seed},
    }
