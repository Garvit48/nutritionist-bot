import json
import os
from datetime import date
from backend import query
from schemas import routine_schema
CONFIGS_DIR = "configs"
from tools import order_food
# Make sure the configs directory exists
os.makedirs(CONFIGS_DIR, exist_ok=True)

def load_json(file_name, default_data):
    file_path = os.path.join(CONFIGS_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        with open(file_path, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data

def save_json(file_name, data):
    file_path = os.path.join(CONFIGS_DIR, file_name)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
import streamlit as st
def get_today_str():
    """Returns today's date in string format YYYY-MM-DD."""
    return str(date.today())

# Function to add calories (first page)
def add_calories():
    st.title("Add Calories Entry")
    
    # Load existing calories log
    calories_log = load_json("calories_log.json", {})

    selected_date = st.date_input("Select Date", date.today())
    selected_date_str = str(selected_date)

    st.subheader(f"Add Food for {selected_date_str}")

    item_name = st.text_input("Food Item Name")
    calories = st.number_input("Calories", min_value=0)
    protein = st.number_input("Protein (g)", min_value=0)
    carbs = st.number_input("Carbs (g)", min_value=0)
    fat = st.number_input("Fat (g)", min_value=0)
    time_of_consumption = st.time_input("Time of Consumption")

    if st.button("Add Entry"):
        new_entry = {
            "time": str(time_of_consumption),
            "items": [{
                "item_name": item_name,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fat": fat
            }]
        }

        if selected_date_str not in calories_log:
            calories_log[selected_date_str] = []

        calories_log[selected_date_str].append(new_entry)
        save_json("calories_log.json", calories_log)
        st.success("Food entry added successfully!")

        
# Function to view calories (second page)
def show_calories():
    st.title("Calories Tracking")

    # Load existing calories log
    calories_log = load_json("calories_log.json", {})

    selected_date = st.date_input("Select Date", date.today())
    selected_date_str = str(selected_date)

    st.subheader(f"Calories for {selected_date_str}")

    day_data = calories_log.get(selected_date_str, [])

    if day_data:
        for entry in day_data:
            st.write(f"**Time**: {entry['time']}")
            for item in entry['items']:
                st.write(f"  - {item['item_name']} | {item['calories']} kcal | {item['protein']}g protein | {item['carbs']}g carbs | {item['fat']}g fat")
    else:
        st.write("No entries for this day.")

def show_personal_info():
    st.title("Personal Information")

    # Load user preferences
    preferences = load_json("user_preferences.json", {
        "name": "John Doe",
        "age": 28,
        "goal": "cutting",
        "height": 175,
        "weight": 80,
        "monthly_budget": 3000,
        "preferred_foods": [],
        "avoid_foods": [],
        "calories_per_day": 1800,
        "diet_type": "high-protein",
        "activity_level": "moderate",
        "allergies": []
    })

    # Create form
    preferences['name'] = st.text_input("Name", preferences['name'])
    preferences['age'] = st.number_input("Age", value=preferences['age'], min_value=0)
    preferences['goal'] = st.selectbox("Goal", ["cutting", "bulking", "maintenance"], index=["cutting", "bulking", "maintenance"].index(preferences['goal']))
    preferences['height'] = st.number_input("Height (cm)", value=preferences['height'])
    preferences['weight'] = st.number_input("Weight (kg)", value=preferences['weight'])
    preferences['monthly_budget'] = st.number_input("Monthly Budget", value=preferences['monthly_budget'])
    preferences['preferred_foods'] = st.text_area("Preferred Foods (comma-separated)", ",".join(preferences['preferred_foods'])).split(",")
    preferences['avoid_foods'] = st.text_area("Foods to Avoid (comma-separated)", ",".join(preferences['avoid_foods'])).split(",")
    preferences['calories_per_day'] = st.number_input("Target Calories per Day", value=preferences['calories_per_day'])
    preferences['diet_type'] = st.selectbox("Diet Type", ["high-protein", "low-carb", "balanced"], index=["high-protein", "low-carb", "balanced"].index(preferences['diet_type']))
    preferences['activity_level'] = st.selectbox("Activity Level", ["low", "moderate", "high"], index=["low", "moderate", "high"].index(preferences['activity_level']))
    preferences['allergies'] = st.text_area("Allergies (comma-separated)", ",".join(preferences['allergies'])).split(",")

    if st.button("Save Information"):
        save_json("user_preferences.json", preferences)
        st.success("Information updated successfully!")



def show_routine():
    st.title("Today's Routine")

    # Load routine (default fallback if empty)
    default_data = {
        "meals": []
    }
    routine = load_json("daily_routine.json", default_data)

    st.subheader(f"Meal Plan for {date.today().strftime('%B %d, %Y')}")

    if routine["meals"]:
        for meal in routine["meals"]:
            st.markdown(f"### {meal['meal_time']} - {meal['name']}")
            total_meal_calories = 0
            for item in meal["items"]:
                food = item["food"]
                qty = item["quantity"]
                cals = item["calories"]
                macros = item["macros"]
                st.markdown(f"- **{food}** ({qty}): {cals} kcal")
                st.caption(f"  - Protein: {macros['protein']}g, Carbs: {macros['carbs']}g, Fat: {macros['fat']}g")
                total_meal_calories += cals
            st.markdown(f"**Total Calories:** {total_meal_calories} kcal")
            st.markdown("---")
    else:
        st.write("No routine generated yet.")

    # Chat interface
    st.subheader("Chat with Nutritionist")
    user_input = st.text_input("Ask to modify today's plan")

    if st.button("Submit Request") and user_input:
        user_data = load_json("user_preferences.json", {})

        # Send user prompt to LLM agent
        response_text = query(
            user_data=user_data,
            routine_schema=routine_schema,
            current_routine=routine,
            user_prompt=user_input
        )

        st.markdown(f"**Nutritionist**: {response_text}")


routine_data = {
  "meals": [
    {
      "meal_time": "01:00 PM",
      "name": "Lunch",
      "items": [
        {
          "food": "Grilled chicken breast",
          "quantity": "150g",
          "calories": 248,
          "macros": {"protein": 35, "carbs": 0, "fat": 11},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Grilled chicken breast"}
        },
        {
          "food": "Steamed broccoli",
          "quantity": "100g",
          "calories": 35,
          "macros": {"protein": 2.5, "carbs": 7, "fat": 0.4},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Steamed broccoli"}
        },
        {
          "food": "Brown rice",
          "quantity": "100g cooked",
          "calories": 112,
          "macros": {"protein": 2.5, "carbs": 23, "fat": 0.8},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Brown rice"}
        }
      ]
    },
    {
      "meal_time": "04:00 PM",
      "name": "Snack",
      "items": [
        {
          "food": "Low-fat Greek yogurt",
          "quantity": "150g",
          "calories": 90,
          "macros": {"protein": 14, "carbs": 7, "fat": 0.7},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Low-fat Greek yogurt"}
        },
        {
          "food": "Almonds",
          "quantity": "15g",
          "calories": 87,
          "macros": {"protein": 3.2, "carbs": 3.2, "fat": 7.6},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Almonds"}
        },
        {
          "food": "Grilled chicken breast",
          "quantity": "50g",
          "calories": 83,
          "macros": {"protein": 11.5, "carbs": 0, "fat": 3.7},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Grilled chicken breast small portion"}
        }
      ]
    },
    {
      "meal_time": "07:00 PM",
      "name": "Dinner",
      "items": [
        {
          "food": "Baked salmon",
          "quantity": "120g",
          "calories": 206,
          "macros": {"protein": 23, "carbs": 0, "fat": 13},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Baked salmon"}
        },
        {
          "food": "Quinoa",
          "quantity": "100g cooked",
          "calories": 120,
          "macros": {"protein": 4.1, "carbs": 21.3, "fat": 1.9},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Quinoa"}
        },
        {
          "food": "Mixed salad (lettuce, tomato, cucumber)",
          "quantity": "100g",
          "calories": 20,
          "macros": {"protein": 1, "carbs": 4, "fat": 0.2},
          "order_info": {"can_order": True, "platform": "Swiggy", "search_query": "Mixed salad"}
        }
      ]
    }
  ]
}



def order_next_meal():
    """Orders the next available food item from the routine."""
    for meal in routine_data["meals"]:
        for item in meal["items"]:
            if item["order_info"]["can_order"]:
                food_item = item["food"]
                platform = item["order_info"]["platform"]
                search_query = item["order_info"]["search_query"]
                
                # Call LangChain agent to order food
                result = order_food(food_item=food_item, platform=platform)
                
                # Show the result in Streamlit
                st.success(f"Order Success: {result}")
                return  # Order the first available item and exit the loop
    st.warning("No food items available for ordering.")

# Add the function to Streamlit button
if st.button("Order Next Meal"):
    order_next_meal()

def main():
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Select a page", ("Calories Tracking", "Add Calories", "Personal Information", "Routine"))

    if tab == "Calories Tracking":
        show_calories()
    elif tab == "Add Calories":
        add_calories()
    elif tab == "Personal Information":
        show_personal_info()
    elif tab == "Routine":
        show_routine()

if __name__ == "__main__":
    main()
