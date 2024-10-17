from taipy.gui import Gui

class ProductCostCalculator:
    def __init__(self, cost_product1, cost_product2, cost_product3, labor_cost_per_hour, cost_cbd_per_ounce):
        self.cost_product1 = cost_product1
        self.cost_product2 = cost_product2
        self.cost_product3 = cost_product3
        self.labor_cost_per_hour = labor_cost_per_hour
        self.cost_cbd_per_ounce = cost_cbd_per_ounce

    def calculate_cost_per_ounce(self, cbd_calculation, total_ounces):
        gallons = total_ounces / 128  # Calculate the number of gallons
        total_cost_product1 = gallons * (30 / 32) * self.cost_product1
        total_cost_product2 = gallons * (30 / 32) * self.cost_product2
        total_cost_product3 = gallons * (2 / 4) * self.cost_product3

        time_to_produce = total_ounces / 60  # Assuming 60 ounces per hour
        total_labor_cost = time_to_produce * self.labor_cost_per_hour

        total_cost_cbd = total_ounces * self.cost_cbd_per_ounce if cbd_calculation else 0

        total_cost_manufacturing = total_cost_product1 + total_cost_product2 + total_cost_product3 + total_labor_cost
        total_cost_distribution = total_labor_cost + total_cost_cbd

        total_cost_per_ounce = (total_cost_manufacturing + total_cost_distribution) / total_ounces

        return {
            'total_cost_per_ounce': total_cost_per_ounce,
            'total_cost': total_cost_manufacturing + total_cost_distribution,
            'total_cost_product1': total_cost_product1,
            'total_cost_product2': total_cost_product2,
            'total_cost_product3': total_cost_product3,
            'total_labor_cost': total_labor_cost,
            'total_cost_cbd': total_cost_cbd,
            'total_cost_manufacturing': total_cost_manufacturing,
            'total_cost_distribution': total_cost_distribution,
        }

def calculate_prices_and_profits(result, wholesale_markup, retail_markup, total_ounces):
    wholesale_price = result['total_cost_per_ounce'] * (1 + wholesale_markup / 100)
    retail_price = wholesale_price * (1 + retail_markup / 100)
    total_profit = (retail_price * total_ounces) - result['total_cost']

    distributor_profit = total_profit / 2
    manufacturer_profit = total_profit / 2
    retailer_profit = (retail_price - wholesale_price) * total_ounces

    return wholesale_price, retail_price, {
        'distributor_profit': distributor_profit,
        'manufacturer_profit': manufacturer_profit,
        'retailer_profit': retailer_profit,
        'total_profit': total_profit,
    }

# Taipy GUI setup
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

## Actions
<|Calculate|button|on_action=calculate|>

## Results
* Total Cost: <|total_cost|>
* Cost per Ounce: <|total_cost_per_ounce|>
* Wholesale Price: <|wholesale_price|>
* Retail Price: <|retail_price|>
* Total Profit: <|total_profit|>
* Distributor Profit: <|distributor_profit|>
* Manufacturer Profit: <|manufacturer_profit|>
* Retailer Profit: <|retailer_profit|>
""")

def calculate(state):
    # Extract input values from the state
    input_values = {
        'cost_product1': state.cost_product1,
        'cost_product2': state.cost_product2,
        'cost_product3': state.cost_product3,
        'labor_cost_per_hour': state.labor_cost_per_hour,
        'cost_cbd_per_ounce': state.cost_cbd_per_ounce,
        'wholesale_markup': state.wholesale_markup,
        'retail_markup': state.retail_markup,
        'total_ounces': state.total_ounces,
    }

    # Calculate costs and profits
    calculator = ProductCostCalculator(**input_values)
    result = calculator.calculate_cost_per_ounce(cbd_calculation=True, total_ounces=input_values['total_ounces'])

    wholesale_price, retail_price, profit = calculate_prices_and_profits(result, input_values['wholesale_markup'], input_values['retail_markup'], input_values['total_ounces'])

    # Update state with results
    state.total_cost = result['total_cost']
    state.total_cost_per_ounce = result['total_cost_per_ounce']
    state.wholesale_price = wholesale_price
    state.retail_price = retail_price
    state.total_profit = profit['total_profit']
    state.distributor_profit = profit['distributor_profit']
    state.manufacturer_profit = profit['manufacturer_profit']
    state.retailer_profit = profit['retailer_profit']

if __name__ == "__main__":
    gui.run(host="0.0.0.0", port=5000)
