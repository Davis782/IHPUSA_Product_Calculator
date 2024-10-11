import taipy as tp
from taipy import Gui

# Define the input values
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

# Define the Taipy GUI
gui = Gui(page="# Cost Calculator")

# Define the input fields
gui.add_input_field("cost_product1", "Cost of Product 1",
                    input_values['cost_product1'])
gui.add_input_field("cost_product2", "Cost of Product 2",
                    input_values['cost_product2'])
gui.add_input_field("cost_product3", "Cost of Product 3",
                    input_values['cost_product3'])
gui.add_input_field("labor_cost_per_hour", "Labor Cost per Hour",
                    input_values['labor_cost_per_hour'])
gui.add_input_field("cost_cbd_per_ounce", "Cost of CBD per Ounce",
                    input_values['cost_cbd_per_ounce'])
gui.add_input_field("wholesale_markup", "Wholesale Markup (%)",
                    input_values['wholesale_markup'])
gui.add_input_field("retail_markup", "Retail Markup (%)",
                    input_values['retail_markup'])
gui.add_input_field("total_ounces", "Total Ounces",
                    input_values['total_ounces'])
gui.add_input_field("ounces_per_bottle", "Ounces per Bottle",
                    input_values['ounces_per_bottle'])
gui.add_input_field("bottles", "Bottles", input_values['bottles'])
gui.add_select("cbd_choice", "CBD Options", [
               "1", "2"], input_values['cbd_choice'])

# Define the calculate button


def calculate(state):
    # Get the input values
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
    distributor_profit_per_ounce = profit['distributor_profit'] / \
        input_values['total_ounces']
    manufacturer_profit_per_ounce = profit['manufacturer_profit'] / \
        input_values['total_ounces']
    retailer_profit_per_ounce = profit['retailer_profit'] / \
        input_values['total_ounces']

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


gui.add_button("Calculate", calculate)

# Define the output fields
gui.add_output_field("total_cost", "Total Cost")
gui.add_output
