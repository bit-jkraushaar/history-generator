"""
Configuration file containing all hardcoded values and settings for the simulation.
"""

# Person settings
PERSON = {
    "max_base_age": 80,
    "max_age_bonus": 40,
    "initial_health": 100,
    "health_decrease_min": 0,
    "health_decrease_max": 5
}

# Marriage settings
MARRIAGE = {
    "min_age": 18,
    "max_initial_age": 30,
    "marriage_chance_base": 0.1,
    "marriage_chance_increase": 0.05
}

# Childbirth settings
CHILDBIRTH = {
    "min_age": 16,
    "max_age": 45,
    "chance": 0.3
}

# Faction settings
FACTIONS = {
    "Noble Houses": {
        "stability_threshold": 30
    },
    "Mages' Guild": {
        "magical_energy_threshold": 80
    }
}

# Region settings
REGIONS = {
    "Central Valley": {
        "magical_energy_threshold": 80
    },
    "Northern Mountains": {
        "dragon_activity_threshold": 20
    }
}

# Event settings
EVENTS = {
    "max_events_per_year": 5,
    "min_events_per_year": 1
} 