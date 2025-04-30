# schemas.py

routine_schema = {
    "type": "object",
    "properties": {
        "meals": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "meal_time": {"type": "string", "example": "08:00 AM"},
                    "name": {"type": "string", "example": "Breakfast"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "food": {"type": "string", "example": "Boiled eggs"},
                                "quantity": {"type": "string", "example": "2 eggs"},
                                "calories": {"type": "number"},
                                "macros": {
                                    "type": "object",
                                    "properties": {
                                        "protein": {"type": "number"},
                                        "carbs": {"type": "number"},
                                        "fat": {"type": "number"}
                                    }
                                },
                                "order_info": {
                                    "type": "object",
                                    "properties": {
                                        "can_order": {"type": "boolean"},
                                        "platform": {"type": "string", "example": "Swiggy"},
                                        "search_query": {"type": "string", "example": "Boiled eggs protein meal"}
                                    }
                                }
                            },
                            "required": ["food", "quantity", "calories", "macros", "order_info"]
                        }
                    }
                },
                "required": ["meal_time", "name", "items"]
            }
        }
    },
    "required": ["meals"]
}
