from flask import Flask, render_template, request
import pandas as pd
from joblib import load
import os

app = Flask(__name__)

# Enhanced model loading with debugging
def load_model():
    """Load the ML model with detailed error reporting"""
    model_path = os.path.join('model', 'random_forest_flood_model.joblib')
    
    # Debug: Print current directory and contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    # Debug: Check if model directory exists
    if os.path.exists('model'):
        print(f"Model directory exists. Contents: {os.listdir('model')}")
    else:
        print("ERROR: Model directory does not exist!")
        return None
    
    # Debug: Check if model file exists
    if os.path.exists(model_path):
        print(f"Model file found at: {model_path}")
        print(f"Model file size: {os.path.getsize(model_path)} bytes")
    else:
        print(f"ERROR: Model file not found at: {model_path}")
        return None
    
    # Try to load the model
    try:
        model = load(model_path)
        print("✅ Model loaded successfully!")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None

# Load model at startup
flood_model = load_model()

# Flood prediction route (main page)
@app.route('/', methods=['GET', 'POST'])
def flood():
    flood_prediction = None
    
    if request.method == 'POST':
        # Check if model is loaded
        if flood_model is None:
            flood_prediction = "❌ Error: Model not loaded. Please check server logs."
            return render_template('flood.html', flood_prediction=flood_prediction)
        
        try:
            # Retrieve input data from form
            monsoon_intensity = float(request.form['monsoon_intensity'])
            population_score = float(request.form['population_score'])
            river_management = float(request.form['river_management'])
            deforestation = float(request.form['deforestation'])
            urbanization = float(request.form['urbanization'])
            climate_change = float(request.form['climate_change'])
            dams_quality = float(request.form['dams_quality'])
            drainage_systems = float(request.form['drainage_systems'])
            agricultural_practices = float(request.form['agricultural_practices'])

            # Create DataFrame for model input
            input_data = pd.DataFrame([[
                monsoon_intensity, population_score, river_management, deforestation,
                urbanization, climate_change, dams_quality, drainage_systems,
                agricultural_practices
            ]], columns=[
                'MonsoonIntensity', 'PopulationScore', 'RiverManagement',
                'Deforestation', 'Urbanization', 'ClimateChange',
                'DamsQuality', 'DrainageSystems', 'AgriculturalPractices'
            ])

            # Make prediction
            prediction = flood_model.predict(input_data)[0]
            flood_prediction = '🌊 Flood Risk Detected' if prediction == 1 else '✅ No Flood Risk Detected'

        except ValueError:
            flood_prediction = "❌ Invalid input: Please enter valid numbers"
        except KeyError as ke:
            flood_prediction = f"❌ Missing field: {str(ke)}"
        except Exception as e:
            flood_prediction = f"❌ Error: {str(e)}"

    return render_template('flood.html', flood_prediction=flood_prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
