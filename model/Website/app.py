from flask import Flask, render_template, request
import pickle
import numpy as np
import os


app = Flask(__name__)

# Load the pre-trained model (make sure the model file path is correct)
def prediction(features):
    filename =  'Mmodel/predictor.pickle'  # Adjust the path if needed
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([features])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    pred_value = 0
    car_name = None  # Initialize car_name as None
    if request.method == 'POST':
        try:
            # Extract data from the form
            car_name = request.form['car_name'] 
            year = int(request.form['year'])
            km = int(request.form['km'])
            seller_type = request.form['seller_type']
            transmission = request.form['transmission']
            owner = request.form['owner']
            fuel = request.form['fuel']
            mileage = request.form['mileage']
            engine = request.form['engine']
            max_power = request.form['max_power']
            seats = request.form['seats']

            # Print the form data for debugging
            print(year, km, seller_type, transmission, owner, fuel, mileage, engine, max_power, seats)

            # Prepare the feature list
            feature_list = [] # Year and Kilometers driven
            feature_list.append(int(year))
            feature_list.append(int(km))

            # Categorical features
            seller_type_list = ['individual', 'dealer', 'trust']
            transmission_list = ['manual', 'automatic']
            owner_list = ['first', 'second', 'third', 'fourth', 'test']
            fuel_list = ['petrol', 'diesel', 'cng', 'lpg']

            # Encode categorical variables
            feature_list.extend([1 if item == seller_type else 0 for item in seller_type_list])
            feature_list.extend([1 if item == transmission else 0 for item in transmission_list])
            feature_list.extend([1 if item == owner else 0 for item in owner_list])
            feature_list.extend([1 if item == fuel else 0 for item in fuel_list])

            # Continuous features
            feature_list.append(float(mileage))  # Mileage
            feature_list.append(int(engine))  # Engine capacity
            feature_list.append(float(max_power))  # Max Power
            feature_list.append(int(seats))  # Number of seats

            # Print the feature list for debugging
            print("Feature List: ", feature_list)

            # Get the prediction
            pred_value = prediction(feature_list)
            pred_value = np.round(pred_value[0], 2)  # Round the prediction for better presentation

        except Exception as e:
            print(f"Error processing input: {e}")
            pred_value = "Error: Invalid Input"

    return render_template("index.html", pred_value=pred_value, car_name=car_name)

if __name__ == '__main__':
    app.run(debug=True)
