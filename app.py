from flask import Flask, render_template, request, jsonify
import joblib
import requests

app = Flask(__name__)

# Load trained model
model = joblib.load("crop_model.pkl")

# OpenWeather API Key
API_KEY = "58368b5fe6fb29858a451ba96c248fea"


# Weather Function
# Weather Function using GPS Coordinates
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


# Crop Information
crop_info = {

    "rice": {
        "fertilizer": "Urea",
        "season": "Kharif",
        "water": "High",
        "yield": "4-6 Tons/Hectare",
        "description": "Rice is one of the most important food crops grown mainly in water-rich areas."
    },

    "maize": {
        "fertilizer": "NPK Fertilizer",
        "season": "Kharif",
        "water": "Medium",
        "yield": "5-7 Tons/Hectare",
        "description": "Maize is a cereal crop widely used for food and animal feed."
    },

    "cotton": {
        "fertilizer": "DAP",
        "season": "Kharif",
        "water": "Medium",
        "yield": "2-3 Tons/Hectare",
        "description": "Cotton is a major fiber crop used in the textile industry."
    },

    "banana": {
        "fertilizer": "Organic Compost",
        "season": "All Season",
        "water": "High",
        "yield": "30-40 Tons/Hectare",
        "description": "Banana is a tropical fruit crop rich in potassium."
    },

    "mango": {
        "fertilizer": "Farm Yard Manure",
        "season": "Summer",
        "water": "Medium",
        "yield": "8-10 Tons/Hectare",
        "description": "Mango is known as the king of fruits."
    },

    "apple": {
        "fertilizer": "NPK + Compost",
        "season": "Winter",
        "water": "Medium",
        "yield": "10-15 Tons/Hectare",
        "description": "Apple is a temperate fruit crop."
    },

    "coffee": {
        "fertilizer": "Nitrogen Rich Fertilizer",
        "season": "Monsoon",
        "water": "Medium",
        "yield": "1-2 Tons/Hectare",
        "description": "Coffee is a commercial plantation crop."
    }
    crop_info = {

    "Muskmelon": {
        "image": "muskmelon.jpg",
        "fertilizer": "NPK Fertilizer",
        "season": "Summer",
        "water": "Moderate",
        "yield": "20-30 tons/hectare",
        "description": "Muskmelon grows well in warm climate."
    },

    ...
}
  

}


@app.route("/")
def home():
    return render_template("index.html")


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


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


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