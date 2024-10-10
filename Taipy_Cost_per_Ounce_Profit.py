import os
from taipy import Gui
from flask import Flask, send_file
from flask_cors import CORS
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer

# Create a Taipy GUI
gui = Gui("<|This Page is meant to give access to the COA of the CBD offered, and subject to change without notice depending on the harvest season.|>")

nav_menu = """
# Navigation Menu
* [COA Page](/pdf)
* [Warning/Directions Page](/warning)
* [Cost Calculator](/calculator)
* [Survey](https://docs.google.com/forms/d/e/1FAIpQLSeFQwgFouHuj6qauAXjab5po0jKMM030eiOLi0gKuxtTtGUHw/viewform)
"""

# Add the navigation menu to the GUI
gui.add_page("nav", nav_menu)

# Define the Markdown content of the COA page
pdf_page = """
# COA Page can be gotten at link below
You can view the COA at the following link and download: [here](http://ai-claude-opensource.onrender.com/pdf/IHPUSA_COA.pdf).
"""

# Add the COA page to the GUI
gui.add_page("pdf", pdf_page)

# Create a Flask app to serve the PDF
app = Flask(__name__)
CORS(app)


@app.route("/pdf")
def serve_pdf():
    return send_file(r'C:\Users\Solid\OneDrive\Documents\GitHub\AI_Claude_OpenSource\pdf\IHPUSA_COA.pdf', as_attachment=False)


@app.route("/warning")
def serve_warning():
    return gui.get_page("warning")


# Create a warning page
warning_page = """
# IHPUSA Product Warning QR Code
Scan this QR code to view the product warning information.
## Product Warning
* **WARNING:** KEEP OUT OF REACH OF CHILDREN AND PETS and don't use on FINISHED FLOOR SURFACES ex. CERAMIC TILE.
* **EYE IRRITANTS:** Avoid contact with eyes. If eye contact occurs, rinse with water. If irritation persists, contact a physician.
## Instructions
* Do not spray on or permit contact with fabrics, painted surfaces, or finished surfaces.
* Do not spray in automobiles or in confined areas.
* Shake well before using.
* Keep in a cool, dry space.
* Avoid long exposure to sun.
* Shake well before using.
## Ingredients
* All Natural Products - Proprietary Information
## Cautions and Warnings
* For external use only.
* Do not spray on or permit contact with fabrics, painted surfaces, or finished surfaces which may cause slippery surfaces.
* The product is flammable.
* May irritate skin. Discontinue use if irritation or rash occurs.
* Avoid contact with eyes, ears, mouth, and open cuts or wounds, even when diluted.
* Keep out of children’s reach to avoid accidental ingestion or inhalation, which can cause serious injury.
* Consult a doctor immediately if breathing problems occur.
* Consult a physician before use if pregnant, nursing, taking medication, or suffering from a medical condition.
* This product may stain due to its strong pigment.
## Contact Information
* K&L Manufacturing
* IHPUSA Distribution: 757-271-1576
* Organic CBD Grown in VA, USA
"""

# Add the warning page to the GUI
gui.add_page("warning", warning_page)

# Generate a QR code with the warning information
try:
    qr = qrcode.QRCode(
        version=7,  # Set a specific version that you know will fit the data
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(warning_page)
    qr.make(fit=True)
    # Create an image from the QR Code instance
    img = qr.make_image(image_factory=StyledPilImage,
                        module_drawer=GappedSquareModuleDrawer())
    # Save the image
    img.save("ihpusa_qrcode.png")
except ValueError as e:
    print(f"Error creating QR code: {e}")


@app.route("/")
def index():
    return redirect(url_for("serve_nav"))

# Serve the navigation menu


@app.route("/nav")
def serve_nav():
    return gui.get_page("nav")

# Define the ProductCostCalculator class


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
            'total_cost_manufacturing': total_cost_manufacturing,
            'total_cost_distribution': total_cost_distribution,
            'total_cost': total_cost_manufacturing + total_cost_distribution
        }


# Create a page for the cost calculator
calculator_page = """
# Product Cost Calculator
## Input Values
* Cost of Product 1: <|cost_product1|>
* Cost of Product 2: <|cost_product2|>
* Cost of Product 3: <|cost_product3|>
* Labor Cost per Hour: <|labor_cost_per_hour|>
* Cost of CBD per Ounce: <|cost_cbd_per_ounce|>

## Total Gallons: <|gallons|>
## Total Ounces: <|total_ounces|>

## Results
* Total Cost per Ounce: <|total_cost_per_ounce|>
* Total Cost of Manufacturing: <|total_cost_manufacturing|>
* Total Cost of Distribution: <|total_cost_distribution|>
* Total Cost: <|total_cost|>

## Actions
* [Calculate](calculate_cost)
"""

# Add the calculator page to the GUI
gui.add_page("calculator", calculator_page)

# Function to calculate cost and update the GUI


def calculate_cost(gallons, cost_product1, cost_product2, cost_product3, labor_cost_per_hour, cost_cbd_per_ounce):
    total_ounces = gallons * 128  # 1 gallon = 128 ounces
    calculator = ProductCostCalculator(
        cost_product1, cost_product2, cost_product3, labor_cost_per_hour, cost_cbd_per_ounce)
    result = calculator.calculate_cost_per_ounce(
        True, total_ounces)  # Assuming CBD calculation is true

    # Update the GUI with results
    return {
        'total_cost_per_ounce': result['total_cost_per_ounce'],
        'total_cost_manufacturing': result['total_cost_manufacturing'],
        'total_cost_distribution': result['total_cost_distribution'],
        'total_cost': result['total_cost']
    }


# Run the Taipy GUI
if __name__ == '__main__':
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5001)).start()
    gui.run(host="0.0.0.0", port=5000)
