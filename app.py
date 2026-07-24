from flask import Flask, render_template, request, jsonify
import joblib
import requests

app = Flask(__name__)

# Load trained model
model = joblib.load("crop_model.pkl")

# OpenWeather API Key
API_KEY = "YOUR_OPENWEATHER_API_KEY"


# ---------------------------------
# Weather Function
# ---------------------------------
def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            rainfall = 0
            if "rain" in data:
                rainfall = data["rain"].get("1h", data["rain"].get("3h", 0))

            city = data["name"]

            return city, temperature, humidity, rainfall

    except Exception as e:
        print(e)

    return "", "", "", ""


# ---------------------------------
# Crop Information
# ---------------------------------

crop_info = {

    "rice": {
        "image": "rice.jpg",
        "fertilizer": "Urea",
        "season": "Kharif",
        "water": "High",
        "yield": "4-6 Tons/Hectare",
        "description": "Rice is one of the most important food crops."
    },

    "maize": {
        "image": "maize.jpg",
        "fertilizer": "NPK Fertilizer",
        "season": "Kharif",
        "water": "Medium",
        "yield": "5-7 Tons/Hectare",
        "description": "Maize is widely used for food and animal feed."
    },

    "chickpea": {
        "image": "chickpea.jpg",
        "fertilizer": "DAP",
        "season": "Rabi",
        "water": "Low",
        "yield": "2-3 Tons/Hectare",
        "description": "Chickpea is a protein-rich pulse crop."
    },

    "kidneybeans": {
        "image": "kidneybeans.jpg",
        "fertilizer": "Organic Compost",
        "season": "Kharif",
        "water": "Medium",
        "yield": "2 Tons/Hectare",
        "description": "Kidney beans are rich in protein."
    },

    "pigeonpeas": {
        "image": "pigeonpeas.jpg",
        "fertilizer": "DAP",
        "season": "Kharif",
        "water": "Medium",
        "yield": "2 Tons/Hectare",
        "description": "Pigeon pea is an important pulse crop."
    },

    "mothbeans": {
        "image": "mothbeans.jpg",
        "fertilizer": "Organic",
        "season": "Kharif",
        "water": "Low",
        "yield": "1.5 Tons/Hectare",
        "description": "Moth beans grow well in dry regions."
    },

    "mungbean": {
        "image": "mungbean.jpg",
        "fertilizer": "Compost",
        "season": "Summer",
        "water": "Low",
        "yield": "1.5 Tons/Hectare",
        "description": "Green gram is rich in protein."
    },

    "blackgram": {
        "image": "blackgram.jpg",
        "fertilizer": "Organic",
        "season": "Kharif",
        "water": "Medium",
        "yield": "1.5 Tons/Hectare",
        "description": "Black gram is widely cultivated in India."
    },

    "lentil": {
        "image": "lentil.jpg",
        "fertilizer": "Organic",
        "season": "Rabi",
        "water": "Low",
        "yield": "1.2 Tons/Hectare",
        "description": "Lentil is a nutritious pulse crop."
    },

    "pomegranate": {
        "image": "pomegranate.jpg",
        "fertilizer": "Farm Yard Manure",
        "season": "Summer",
        "water": "Medium",
        "yield": "15 Tons/Hectare",
        "description": "Pomegranate is rich in antioxidants."
    },

    "banana": {
        "image": "banana.jpg",
        "fertilizer": "Organic Compost",
        "season": "All Season",
        "water": "High",
        "yield": "35 Tons/Hectare",
        "description": "Banana is a tropical fruit crop."
    },

    "mango": {
        "image": "mango.jpg",
        "fertilizer": "Farm Yard Manure",
        "season": "Summer",
        "water": "Medium",
        "yield": "10 Tons/Hectare",
        "description": "Mango is the king of fruits."
    },

    "grapes": {
        "image": "grapes.jpg",
        "fertilizer": "NPK",
        "season": "Winter",
        "water": "Medium",
        "yield": "20 Tons/Hectare",
        "description": "Grapes are grown in vineyards."
    },

    "watermelon": {
        "image": "watermelon.jpg",
        "fertilizer": "NPK",
        "season": "Summer",
        "water": "Medium",
        "yield": "30 Tons/Hectare",
        "description": "Watermelon is a refreshing summer fruit."
    },

    "muskmelon": {
        "image": "muskmelon.jpg",
        "fertilizer": "NPK",
        "season": "Summer",
        "water": "Moderate",
        "yield": "25 Tons/Hectare",
        "description": "Muskmelon grows well in warm climates."
    },

    "apple": {
        "image": "apple.jpg",
        "fertilizer": "NPK + Compost",
        "season": "Winter",
        "water": "Medium",
        "yield": "12 Tons/Hectare",
        "description": "Apple is a temperate fruit crop."
    },

    "orange": {
        "image": "orange.jpg",
        "fertilizer": "Organic Compost",
        "season": "Winter",
        "water": "Medium",
        "yield": "15 Tons/Hectare",
        "description": "Orange is rich in Vitamin C."
    },

    "papaya": {
        "image": "papaya.jpg",
        "fertilizer": "Organic",
        "season": "All Season",
        "water": "Medium",
        "yield": "35 Tons/Hectare",
        "description": "Papaya grows throughout the year."
    },

    "coconut": {
        "image": "coconut.jpg",
        "fertilizer": "Farm Yard Manure",
        "season": "All Season",
        "water": "High",
        "yield": "100 Nuts/Tree",
        "description": "Coconut is an important plantation crop."
    },

    "cotton": {
        "image": "cotton.jpg",
        "fertilizer": "DAP",
        "season": "Kharif",
        "water": "Medium",
        "yield": "3 Tons/Hectare",
        "description": "Cotton is used in textile industries."
    },

    "jute": {
        "image": "jute.jpg",
        "fertilizer": "Nitrogen",
        "season": "Kharif",
        "water": "High",
        "yield": "2 Tons/Hectare",
        "description": "Jute is a natural fibre crop."
    },

    "coffee": {
        "image": "coffee.jpg",
        "fertilizer": "Nitrogen Rich",
        "season": "Monsoon",
        "water": "Medium",
        "yield": "2 Tons/Hectare",
        "description": "Coffee is a plantation crop."
    }

}


# ---------------------------------
# Routes
# ---------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/weather")
def weather():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    city, temperature, humidity, rainfall = get_weather(lat, lon)

    return jsonify({
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall
    })


@app.route("/predict", methods=["POST"])
def predict():

    N = float(request.form["N"])
    P = float(request.form["P"])
    K = float(request.form["K"])
    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    ph = float(request.form["ph"])
    rainfall = float(request.form["rainfall"])

    location = request.form["location"]
    soil = request.form["soil"]

    prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

    crop = prediction[0].lower()

    info = crop_info.get(crop, {
        "image": "default.jpg",
        "fertilizer": "N/A",
        "season": "N/A",
        "water": "N/A",
        "yield": "N/A",
        "description": "No description available."
    })

    return render_template(
        "result.html",
        crop=crop,
        info=info,
        temperature=temperature,
        humidity=humidity,
        rainfall=rainfall,
        location=location,
        soil=soil
    )


if __name__ == "__main__":
    app.run(debug=True)