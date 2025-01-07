from flask import Flask, render_template, request
import google.generativeai as genai  # Promijenjen import
import os

app = Flask(__name__)

# Konfiguracija API ključa
genai.configure(api_key = 'AIzaSyBIGETjjp18ap_9kc5_R4FI_O7eFQUkBlc')

# Inicijalizacija modela
model = genai.GenerativeModel("gemini-1.5-flash") 

def generiraj_odgovor(upit):
    """Generira odgovor od Gemini API-ja."""
    print(f"Generating response for query: {upit}")
    try:
        response = model.generate_content(  # Korištenje model.generate_content()
            f"""Ti si Andrija Mohorovičić, hrvatski znanstvenik i seizmolog. 
            Korisnik: {upit}"""
        )
        print(f"Raw API response: {response}")
    except Exception as e:
        print(f"Error during API request: {e}")
        return "Error during request"

    if response and response.text:  # Pristup odgovoru preko response.text
        response_text = response.text
        print(f"Chatbot Response: {response_text}")
        return response_text
    else:
        print("No valid response from the API.")
        return "No valid response from the API."

@app.route("/", methods=["GET", "POST"])
def index():
    """Prikazuje chatbot sučelje i obrađuje korisničke upite."""
    odgovor = None
    if request.method == "POST":
        upit = request.form.get("query", "").strip()
        print(f"User query: {upit}")
        if upit:
            odgovor = generiraj_odgovor(upit)
        else:
            odgovor = "Please enter a question."
        print(f"Response being passed to template: {odgovor}") 
    return render_template("index.html", response=odgovor)

if __name__ == "__main__":
    app.run(debug=True)