import taipy as tp
from taipy.gui import Gui

# Define the input values as a state variable
input_values = {
    'cost_product1': 0,
    'cost_product2': 0,
    'cost_product3': 0,
    'labor_cost_per_hour': 0,
    'cost_cbd_per_ounce': 0,
    'wholesale_markup': 0,
    'retail_markup': 0,
    'total_ounces': 0,
    'ounces_per_bottle': 0,
    'bottles': 0,
    'cbd_choice': '1'
}

# Define the Taipy GUI layout using Markdown-like syntax
gui = Gui(page="""
# Cost Calculator

## Input Values
* Cost of Product 1: <|cost_product1|>
* Cost of Product 2: <|cost_product2|>
* Cost of Product 3: <|cost_product3|>
* Labor Cost per Hour: <|labor_cost_per_hour|>
* Cost of CBD per Ounce: <|cost_cbd_per_ounce|>
* Wholesale Markup (%): <|wholesale_markup|>
* Retail Markup (%): <|retail_markup|>
* Total Ounces: <|total_ounces|>
* Ounces per Bottle: <|ounces_per_bottle|>
* Bottles: <|bottles|>
* CBD Options: <|cbd_choice|>

## Actions
<|Calculate|button|on_action=calculate|>
""")

# Define the calculate function
def calculate(state):
    # Get the input values from the state
    input_values['cost_product1'] = state.cost_product1
    input_values['cost_product2'] = state.cost_product2
    input_values['cost_product3'] = state.cost_product3
    input_values['labor_cost_per_hour'] = state.labor_cost_per_hour
    input_values['cost_cbd_per_ounce'] = state.cost_cbd_per_ounce
    input_values['wholesale_markup'] = state.wholesale_markup
    input_values['retail_markup'] = state.retail_markup
    input_values['total_ounces'] = state.total_ounces
    input_values['ounces_per_bottle'] = state.ounces_per_bottle
    input_values['bottles'] = state.bottles
    input_values['cbd_choice'] = state.cbd_choice

    # Calculate the total cost
    calculator = ProductCostCalculator(
        input_values['cost_product1'],
        input_values['cost_product2'],
        input_values['cost_product3'],
        input_values['labor_cost_per_hour'],
        input_values['cost_cbd_per_ounce']
    )
    result = calculator.calculate_cost_per_ounce(
        input_values['cbd_choice'] == '1', input_values['total_ounces'])

    # Calculate the wholesale and retail prices
    wholesale_price, retail_price, profit = calculate_prices_and_profits(
        result, input_values['wholesale_markup'], input_values['retail_markup'], input_values['total_ounces'])

    # Calculate the profit per ounce
    distributor_profit_per_ounce = profit['distributor_profit'] / input_values['total_ounces']
    manufacturer_profit_per_ounce = profit['manufacturer_profit'] / input_values['total_ounces']
    retailer_profit_per_ounce = profit['retailer_profit'] / input_values['total_ounces']

    # Return the results
    return {
        'total_cost': result['total_cost'],
        'cost_per_ounce_manufacturing': result['cost_per_ounce_manufacturing'],
        'cost_per_ounce_distribution': result['cost_per_ounce_distribution'],
        'total_cost_per_ounce': result['total_cost_per_ounce'],
        'wholesale_price': wholesale_price,
        'retail_price': retail_price,
        'total_profit': profit['total_profit'],
        'distributor_profit': profit['distributor_profit'],
        'manufacturer_profit': profit['manufacturer_profit'],
        'retailer_profit': profit['retailer_profit'],
        'distributor_profit_per_ounce': distributor_profit_per_ounce,
        'manufacturer_profit_per_ounce': manufacturer_profit_per_ounce,
        'retailer_profit_per_ounce': retailer_profit_per_ounce
    }

# Define the output fields
gui.add_output_field("total_cost", "Total Cost")
gui.add_output_field("cost_per_ounce_manufacturing", "Cost per Ounce Manufacturing")
gui.add_output_field("cost_per_ounce_distribution", "Cost per Ounce Distribution")
gui.add_output_field("total_cost_per_ounce", "Total Cost per Ounce")
gui.add_output_field("wholesale_price", "Wholesale Price")
gui.add_output_field("retail_price", "Retail Price")
gui.add_output_field("total_profit", "Total Profit")
gui.add_output_field("distributor_profit", "Distributor Profit")
gui.add_output_field("manufacturer_profit", "Manufacturer Profit")
gui.add_output_field("retailer_profit", "Retailer Profit")
gui.add_output_field("distributor_profit_per_ounce", "Distributor Profit per Ounce")
gui.add_output_field("manufacturer_profit_per_ounce", "Manufacturer Profit per Ounce")
gui.add_output_field("retailer_profit_per_ounce", "Retailer Profit per Ounce")

# Run the Taipy GUI
if __name__ == '__main__':
    import threading
    # Start Flask server in a separate thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5001)).start()
    port = int(os.environ.get("PORT", 5000))
    gui.run(host="0.0.0.0", port=port)
