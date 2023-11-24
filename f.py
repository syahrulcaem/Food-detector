import requests
import tkinter as tk

def get_nutrition_info():
    # Clear previous results
    for widget in result_label.winfo_children():
        widget.destroy()

    food_name = entry.get()  # Get the food name from the entry field
    api_endpoint = f"https://world.openfoodfacts.org/api/v0/product/{food_name}.json"
    
    response = requests.get(api_endpoint)
    
    if response.status_code == 200:
        data = response.json()
        display_nutrition_info(data)
    else:
        result_label.config(text="Could not fetch nutrition information")

def display_nutrition_info(data):
    # Check if the product exists
    if data['status'] == 1:
        product = data['product']
        # Display product name
        product_name = product.get('product_name', 'Product name not available')
        tk.Label(result_label, text=f"Product Name: {product_name}", font=("Arial", 14, "bold")).pack(pady=5)

        # Display important nutrition information
        nutrients = {
            'Energy': product['nutriments'].get('energy-kcal_100g', 'Not available'),
            'Fat': product['nutriments'].get('fat_100g', 'Not available'),
            'Saturated Fat': product['nutriments'].get('saturated-fat_100g', 'Not available'),
            'Trans Fat': product['nutriments'].get('trans-fat_100g', 'Not available'),
            'Cholesterol': product['nutriments'].get('cholesterol_100g', 'Not available'),
            'Carbohydrates': product['nutriments'].get('carbohydrates_100g', 'Not available'),
            'Sugars': product['nutriments'].get('sugars_100g', 'Not available'),
            'Fiber': product['nutriments'].get('fiber_100g', 'Not available'),
            'Proteins': product['nutriments'].get('proteins_100g', 'Not available'),
            'Salt': product['nutriments'].get('salt_100g', 'Not available'),
            # Add more nutrients as needed
        }
        # Display fetched nutrition information
        for nutrient, value in nutrients.items():
            tk.Label(result_label, text=f"{nutrient}: {value}", font=("Arial", 12)).pack(pady=2)
    else:
        result_label.config(text="Product not found")

# Create the main Tkinter window
root = tk.Tk()
root.title("Nutrition Tracker")

# Create GUI elements
label = tk.Label(root, text="Enter a food item:", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=get_nutrition_info, font=("Arial", 12))
search_button.pack(pady=10)

result_label = tk.Label(root, font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()
