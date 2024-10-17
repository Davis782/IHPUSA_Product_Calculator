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

## Results
* Total Cost: <|total_cost|>
* Cost per Ounce Manufacturing: <|cost_per_ounce_manufacturing|>
* Cost per Ounce Distribution: <|cost_per_ounce_distribution|>
* Total Cost per Ounce: <|total_cost_per_ounce|>
* Wholesale Price: <|wholesale_price|>
* Retail Price: <|retail_price|>
* Total Profit: <|total_profit|>
* Distributor Profit: <|distributor_profit|>
* Manufacturer Profit: <|manufacturer_profit|>
* Retailer Profit: <|retailer_profit|>
* Distributor Profit per Ounce: <|distributor_profit_per_ounce|>
* Manufacturer Profit per Ounce: <|manufacturer_profit_per_ounce|>
* Retailer Profit per Ounce: <|retailer_profit_per_ounce|>
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

    # Update the state with the results
    state.total_cost = result['total_cost']
    state.cost_per_ounce_manufacturing = result['cost_per_ounce_manufacturing']
    state.cost_per_ounce_distribution = result['cost_per_ounce_distribution']
    state.total_cost_per_ounce = result['total_cost_per_ounce']
    state.wholesale_price = wholesale_price
    state.retail_price = retail_price
    state.total_profit = profit['total_profit']
    state.distributor_profit = profit['distributor_profit']
    state.manufacturer_profit = profit['manufacturer_profit']
    state.retailer_profit = profit['retailer_profit']
    state.distributor_profit_per_ounce = distributor_profit_per_ounce
    state.manufacturer_profit_per_ounce = manufacturer_profit_per_ounce
    state.retailer_profit_per_ounce = retailer_profit_per_ounce

# Run the Taipy GUI
if __name__ == '__main__':
    import threading
    # Start Flask server in a separate thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5001)).start()
    port = int(os.environ.get("PORT", 5000))
    gui.run(host="0.0.0.0", port=port)
