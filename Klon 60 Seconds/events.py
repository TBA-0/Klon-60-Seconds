import random
import json
import os
from settings import *

class Event:
    def __init__(self, event_id, title, description, choices, condition=None, priority=0):
        self.id = event_id
        self.title = title
        self.description = description
        self.choices = choices
        self.condition = condition  
        self.priority = priority  
        
    def get_outcome(self, choice_index):
        """Get the outcome for the selected choice"""
        if choice_index < 0 or choice_index >= len(self.choices):
            return None
        return self.choices[choice_index]["outcome"]
    
    def meets_condition(self, day, people_alive, food, water, weapons, tools):
        """Check if event meets conditions to occur"""
        if not self.condition:
            return True
            
        condition = self.condition
        if "min_day" in condition and day < condition["min_day"]:
            return False
        if "max_day" in condition and day > condition["max_day"]:
            return False
        if "min_people" in condition and people_alive < condition["min_people"]:
            return False

        if "min_food" in condition and food < condition["min_food"]:
            return False
        if "min_water" in condition and water < condition["min_water"]:
            return False
        if "min_weapons" in condition and weapons < condition["min_weapons"]:
            return False
        if "min_tools" in condition and tools < condition["min_tools"]:
            return False
        if "max_food" in condition and food > condition["max_food"]:
            return False
        if "max_water" in condition and water > condition["max_water"]:
            return False
            
        return True


class EventManager:
    def __init__(self):
        self.events = []
        self.load_events()
    
    def load_events(self):
        """Load events from JSON file or create default events"""
        try:
            if os.path.exists(EVENTS_FILE):
                with open(EVENTS_FILE, 'r') as f:
                    events_data = json.load(f)
                    
                    for event_data in events_data:
                        event = Event(
                            event_data["id"],
                            event_data["title"],
                            event_data["description"],
                            event_data["choices"],
                            event_data.get("condition", None),
                            event_data.get("priority", 1)
                        )
                        self.events.append(event)
            else:
                self.create_default_events()
                
        except Exception as e:
            print(f"Error loading events: {e}")
            self.create_default_events()
    
    def create_default_events(self):
        """Create and save default events"""
        default_events = [
            {
                "id": 1,
                "title": "Radiation Storm",
                "description": "A radiation storm is approaching. You should prepare your shelter.",
                "choices": [
                    {
                        "text": "Close all ventilation",
                        "outcome": {
                            "message": "You closed all ventilation. The air gets stale, but you're safe from radiation.",
                            "effects": [
                                {"type": "sanity", "value": -5, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Keep ventilation open",
                        "outcome": {
                            "message": "You kept ventilation open. The air is fresh, but some radiation got in.",
                            "effects": [
                                {"type": "health", "value": -10, "target": "all"}
                            ]
                        }
                    }
                ],
                "priority": 2
            },
            {
                "id": 2,
                "title": "Strange Noises",
                "description": "You hear strange noises outside your shelter. It could be survivors, animals, or worse.",
                "choices": [
                    {
                        "text": "Investigate (Send Dad)",
                        "outcome": {
                            "message": "Dad investigated the noise. It was just the wind, but he found some supplies!",
                            "effects": [
                                {"type": "food", "value": 1},
                                {"type": "health", "value": -5, "target": "dad"}
                            ]
                        }
                    },
                    {
                        "text": "Ignore it",
                        "outcome": {
                            "message": "You decided to ignore the noise. Better safe than sorry.",
                            "effects": [
                                {"type": "sanity", "value": -3, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Make loud noises to scare it away",
                        "outcome": {
                            "message": "You made noise to scare away whatever was outside. It worked!",
                            "effects": []
                        }
                    }
                ]
            },
            {
                "id": 3,
                "title": "Water Leak",
                "description": "There's a leak in your water supply!",
                "choices": [
                    {
                        "text": "Fix it with tools",
                        "outcome": {
                            "message": "You successfully fixed the leak with your tools.",
                            "effects": [
                                {"type": "tools", "value": -1}
                            ]
                        }
                    },
                    {
                        "text": "Ignore it",
                        "outcome": {
                            "message": "You ignored the leak. Your water supply is contaminated.",
                            "effects": [
                                {"type": "water", "value": -2}
                            ]
                        }
                    }
                ],
                "condition": {
                    "min_tools": 1
                }
            },
            {
                "id": 4,
                "title": "Food Shortage",
                "description": "Your food supplies are running dangerously low.",
                "choices": [
                    {
                        "text": "Ration food",
                        "outcome": {
                            "message": "You decided to ration food. Everyone is hungry but will survive longer.",
                            "effects": [
                                {"type": "sanity", "value": -5, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Send someone to scavenge (Mom)",
                        "outcome": {
                            "message": "Mom went scavenging and found some canned food, but got injured.",
                            "effects": [
                                {"type": "food", "value": 2},
                                {"type": "health", "value": -15, "target": "mom"}
                            ]
                        }
                    }
                ],
                "condition": {
                    "max_food": 2
                },
                "priority": 3
            },
            {
                "id": 5,
                "title": "Radio Broadcast",
                "description": "You picked up a radio broadcast mentioning a supply drop nearby.",
                "choices": [
                    {
                        "text": "Send someone to investigate (Son)",
                        "outcome": {
                            "message": "Son found the supply drop and brought back valuable resources!",
                            "effects": [
                                {"type": "food", "value": 3},
                                {"type": "water", "value": 2},
                                {"type": "medical", "value": 1}
                            ]
                        }
                    },
                    {
                        "text": "Ignore it, could be a trap",
                        "outcome": {
                            "message": "You ignored the broadcast. It might have been a trap, or maybe not...",
                            "effects": []
                        }
                    }
                ],
                "condition": {
                    "min_day": 5
                }
            },
            {
                "id": 6,
                "title": "Illness",
                "description": "Daughter is showing signs of illness. She needs medical attention.",
                "choices": [
                    {
                        "text": "Use medical supplies",
                        "outcome": {
                            "message": "You used medical supplies to treat Daughter. She's recovering now.",
                            "effects": [
                                {"type": "medical", "value": -1},
                                {"type": "health", "value": 15, "target": "daughter"}
                            ]
                        }
                    },
                    {
                        "text": "Wait and see if it passes",
                        "outcome": {
                            "message": "You decided to wait. Daughter's condition is getting worse.",
                            "effects": [
                                {"type": "health", "value": -20, "target": "daughter"}
                            ]
                        }
                    }
                ],
                "condition": {
                    "min_medical": 1
                }
            },
            {
                "id": 7,
                "title": "Raiders",
                "description": "A group of raiders is trying to break into your shelter!",
                "choices": [
                    {
                        "text": "Fight them off with weapons",
                        "outcome": {
                            "message": "You fought off the raiders, but used some weapons and Dad got injured.",
                            "effects": [
                                {"type": "weapons", "value": -1},
                                {"type": "health", "value": -10, "target": "dad"}
                            ]
                        }
                    },
                    {
                        "text": "Hide and stay quiet",
                        "outcome": {
                            "message": "You hid quietly until the raiders left, but they stole some supplies.",
                            "effects": [
                                {"type": "food", "value": -1},
                                {"type": "water", "value": -1}
                            ]
                        }
                    },
                    {
                        "text": "Try to negotiate",
                        "outcome": {
                            "message": "You tried to negotiate with the raiders. They took some food but left peacefully.",
                            "effects": [
                                {"type": "food", "value": -2}
                            ]
                        }
                    }
                ],
                "condition": {
                    "min_day": 10
                },
                "priority": 2
            },
            {
                "id": 8,
                "title": "Nightmare",
                "description": "Son had a terrible nightmare and is having trouble sleeping.",
                "choices": [
                    {
                        "text": "Comfort him",
                        "outcome": {
                            "message": "You comforted Son. He feels better now, and everyone's morale improved.",
                            "effects": [
                                {"type": "sanity", "value": 5, "target": "son"},
                                {"type": "sanity", "value": 3, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Ignore it",
                        "outcome": {
                            "message": "You ignored Son's nightmare. His mental state is deteriorating.",
                            "effects": [
                                {"type": "sanity", "value": -10, "target": "son"}
                            ]
                        }
                    }
                ]
            },
            {
                "id": 9,
                "title": "Water Filter Broken",
                "description": "Your water filter is broken. You need to fix it or find another source of clean water.",
                "choices": [
                    {
                        "text": "Try to fix it with tools",
                        "outcome": {
                            "message": "You managed to fix the water filter with your tools!",
                            "effects": [
                                {"type": "tools", "value": -1}
                            ]
                        }
                    },
                    {
                        "text": "Drink unfiltered water",
                        "outcome": {
                            "message": "You drank unfiltered water. Everyone got sick.",
                            "effects": [
                                {"type": "health", "value": -15, "target": "all"}
                            ]
                        }
                    }
                ],
                "condition": {
                    "min_tools": 1
                }
            },
            {
                "id": 10,
                "title": "Government Rescue",
                "description": "You hear an official-sounding broadcast about government evacuation.",
                "choices": [
                    {
                        "text": "Leave shelter for evacuation point",
                        "outcome": {
                            "message": "You arrived at the evacuation point, but it was abandoned long ago. You lost supplies returning home.",
                            "effects": [
                                {"type": "food", "value": -1},
                                {"type": "water", "value": -1},
                                {"type": "health", "value": -5, "target": "all"}
                            ]
                        }
                    },
                    {
                        "text": "Stay in shelter",
                        "outcome": {
                            "message": "You decided to stay in your shelter. It's safer not to trust random broadcasts.",
                            "effects": []
                        }
                    }
                ],
                "condition": {
                    "min_day": 15
                }
            }
        ]
        
        for event_data in default_events:
            event = Event(
                event_data["id"],
                event_data["title"],
                event_data["description"],
                event_data["choices"],
                event_data.get("condition", None),
                event_data.get("priority", 1)
            )
            self.events.append(event)
            
        os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
        with open(EVENTS_FILE, 'w') as f:
            json.dump(default_events, f, indent=4)
    
    def get_random_events(self, day, people_alive, food, water, weapons, tools, max_events=3):
        """Get random events that can occur on the current day"""
        eligible_events = []
        
        for event in self.events:
            if event.meets_condition(day, people_alive, food, water, weapons, tools):
                for _ in range(event.priority):
                    eligible_events.append(event)
        max_events = min(max_events, len(set(eligible_events)))
        
        if not eligible_events:
            return []

        selected_events = []
        unique_events = list(set(eligible_events))
        
        if len(unique_events) <= max_events:
            return unique_events

        while len(selected_events) < max_events and eligible_events:
            event = random.choice(eligible_events)
            if event not in selected_events:
                selected_events.append(event)
                eligible_events = [e for e in eligible_events if e.id != event.id]
                
        return selected_events
