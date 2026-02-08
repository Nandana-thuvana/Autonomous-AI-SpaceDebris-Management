from flask import Flask, render_template, request, jsonify
from predict_debris import predict_with_cleanup
from rag_gemini import ask_gemini

app = Flask(__name__)

# Mapping HTML input names to model column names
FIELD_MAP = {
    "sma": "semi_major_axis",
    "ecc": "eccentricity",
    "inc": "inclination",
    "raan": "raan",
    "argp": "arg_perigee",
    "ma": "mean_anomaly"
}


# ================= HOME PAGE =================
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    plan = None
    explanation = None
    error = None

    if request.method == "POST":
        try:
            orbital_params_dict = {}

            for short_name, long_name in FIELD_MAP.items():
                value = request.form.get(short_name, "").strip()
                if value == "":
                    raise ValueError(f"{short_name} is required")
                orbital_params_dict[long_name] = float(value)

            # ML Prediction + Cleanup plan
            result, plan = predict_with_cleanup(orbital_params_dict)

            # Gemini scientific explanation
            explanation = ask_gemini(
                f"""
                These are the orbital parameters:
                {orbital_params_dict}

                The ML model classified this object as: {result}

                Explain scientifically why this object is classified this way
                and describe its orbit behavior.
                """
            )

        except ValueError as ve:
            error = f"Input Error: {ve}"
        except Exception as e:
            error = f"Unexpected Error: {e}"

    return render_template(
        "index.html",
        result=result,
        plan=plan,
        explanation=explanation,
        error=error
    )


# ================= AI QUESTION ROUTE (FOR script.js) =================
@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"answer": "No question provided."})

        answer = ask_gemini(question)
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {e}"})


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
