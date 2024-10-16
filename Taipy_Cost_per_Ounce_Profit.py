import streamlit as st

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

        total_cost_manufacturing = total_cost_product1 + \
            total_cost_product2 + total_cost_product3 + total_labor_cost
        total_cost_distribution = total_labor_cost + total_cost_cbd

        total_cost_per_ounce = (
            total_cost_manufacturing + total_cost_distribution) / total_ounces

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

def calculate_prices_and_profits(result, wholesale_markup, retail_markup, total_ounces, ounces_per_bottle):
    # Calculate total cost per bottle
    total_cost_per_bottle = result['total_cost'] / (total_ounces / ounces_per_bottle)

    # Calculate wholesale and retail prices per bottle
    wholesale_price_per_bottle = total_cost_per_bottle * (1 + wholesale_markup / 100)
    retail_price_per_bottle = wholesale_price_per_bottle * (1 + retail_markup / 100)

    total_profit = (retail_price_per_bottle * (total_ounces / ounces_per_bottle)) - result['total_cost']  # Total bottles = total ounces / ounces per bottle
    distributor_profit = total_profit / 2
    manufacturer_profit = total_profit / 2
    retailer_profit = (retail_price_per_bottle - wholesale_price_per_bottle) * (total_ounces / ounces_per_bottle)

    return {
        'total_cost_per_bottle': total_cost_per_bottle,
        'wholesale_price_per_bottle': wholesale_price_per_bottle,
        'retail_price_per_bottle': retail_price_per_bottle,
        'distributor_profit': distributor_profit,
        'manufacturer_profit': manufacturer_profit,
        'retailer_profit': retailer_profit,
        'total_profit': total_profit,
    }

# Streamlit app
def main():
    st.title("Product Cost Calculator")

    # Input values
    cost_product1 = st.number_input("Cost of Product 1 ($)", value=5.0, key="cost_product1")
    cost_product2 = st.number_input("Cost of Product 2 ($)", value=6.0, key="cost_product2")
    cost_product3 = st.number_input("Cost of Product 3 ($)", value=9.0, key="cost_product3")
    labor_cost_per_hour = st.number_input("Labor Cost per Hour ($)", value=15.0, key="labor_cost_per_hour")
    cost_cbd_per_ounce = st.number_input("Cost of CBD per Ounce ($)", value=0.326, key="cost_cbd_per_ounce")

    # Toggle for selecting calculation method
    calculation_method = st.radio("Select Calculation Method:", ["Calculate based on Gallons", "Calculate based on Total Bottles"], key="calculation_method")

    if calculation_method == "Calculate based on Gallons":
        gallons = st.number_input("Enter the number of gallons:", value=1.0, key="gallons")
        total_ounces = gallons * 128  # 1 gallon = 128 ounces
    else:
        total_bottles = st.number_input("Enter the total number of bottles:", value=1, key="total_bottles")
        ounces_per_bottle = st.number_input("Enter the number of ounces per bottle:", value=2, key="ounces_per_bottle")
        total_ounces = total_bottles * ounces_per_bottle

    # CBD Options
    cbd_choice = st.radio("Calculate cost per ounce with CBD?", ("Yes", "No"), key="cbd_choice")

    # Initialize session state for calculations
    if 'result' not in st.session_state:
        st.session_state.result = None
        st.session_state.wholesale_markup = 20.0
        st.session_state.retail_markup = 30.0

    # Calculate button
    if st.button("Calculate", key="calculate_button"):
        calculator = ProductCostCalculator(
            cost_product1,
            cost_product2,
            cost_product3,
            labor_cost_per_hour,
            cost_cbd_per_ounce
        )

        st.session_state.result = calculator.calculate_cost_per_ounce(
            cbd_choice == "Yes", total_ounces)

    # Display results if available
    if st.session_state.result is not None:
        result = st.session_state.result

        # Display results
        st.subheader("Calculation Results")
        st.write(f"Total cost to produce {total_ounces:.1f} ounces: ${result['total_cost']:.2f}")
        st.write(f"Cost per ounce: ${result['total_cost_per_ounce']:.2f}")

        # Calculate cost per bottle dynamically
        ounces_per_bottle = st.number_input("Enter the number of ounces per bottle:", value=2, key="dynamic_ounces_per_bottle")
        total_cost_per_bottle = result['total_cost'] / (total_ounces / ounces_per_bottle)
        st.write(f"Cost per bottle ({ounces_per_bottle} ounces): ${total_cost_per_bottle:.2f}")

        st.write(f"Total Manufacturing Dept cost for {total_ounces:.1f} ounces: ${result['total_cost_manufacturing']:.2f}")
        st.write(f"Total Distribution Dept cost for {total_ounces:.1f} ounces: ${result['total_cost_distribution']:.2f}")

        # Markup inputs
        wholesale_markup = st.number_input("Wholesale Markup (%)", value=st.session_state.wholesale_markup, key="wholesale_markup")
        retail_markup = st.number_input("Retail Markup (%)", value=st.session_state.retail_markup, key="retail_markup")

        # Calculate prices and profits
        profit = calculate_prices_and_profits(
            result, wholesale_markup, retail_markup, total_ounces, ounces_per_bottle)

        # Display profit report
        st.subheader("Profit Report")
        st.write(f"Total cost per bottle: ${profit['total_cost_per_bottle']:.2f}")  # Added total cost per bottle
        st.write(f"Wholesale price per bottle: ${profit['wholesale_price_per_bottle']:.2f}")
        st.write(f"Retail price per bottle: ${profit['retail_price_per_bottle']:.2f}")
        st.write(f"Total profit: ${profit['total_profit']:.2f}")
        st.write(f"Distributor profit: ${profit['distributor_profit']:.2f}")
        st.write(f"Manufacturer profit: ${profit['manufacturer_profit']:.2f}")
        st.write(f"Retailer profit: ${profit['retailer_profit']:.2f}")

if __name__ == "__main__":
    main()
