# tools.py

from langchain.tools import tool
from playwright.sync_api import sync_playwright
import time

def order_food(food_item: str, platform: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch browser
        page = browser.new_page()  # Create new page
        page.goto(f"https://www.{platform}.com")  # Example: Navigate to Swiggy
        
        # Add food item search or ordering logic here
        page.fill('input[name="search"]', food_item)  # Search for the food item
        page.press('input[name="search"]', 'Enter')  # Press 'Enter' to search

        # You can add further steps here based on your platform's order flow

        browser.close()  # Close browser

    return f"Successfully searched for {food_item} on {platform}"

# Example of calling the function
print(order_food("Grilled chicken breast", "swiggy"))
@tool
def order_food_p():
        """
    Automates ordering food using Playwright.           
    
    Args:
        food_item: The name of the food item to order.
        quantity: The number of items to order.
        platform: 'zomato' or 'swiggy' (default is 'zomato').

    Returns:
        A message confirming the action.
    """
        pass