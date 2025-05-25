from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        criteria = request.form.getlist("criterion")
        options = request.form.getlist("option_name")
        weights_raw = request.form.getlist("weight")

        num_criteria = len(criteria)
        num_options = len(options)

        try:
            weights = [float(w) for w in weights_raw]
        except ValueError:
            return render_template("index.html", error="Falsches Gewicht", data=request.form)

        weight_sum = sum(weights)
        if abs(weight_sum - 100) > 0.01:
            error = f"Die Summe der Gewichte sollte nun 100 ergeben.: {round(weight_sum, 2)}"
            return render_template("index.html", error=error, data=request.form)

        normalized_weights = [w / 100 for w in weights]

        scores = []
        for i in range(num_criteria):
            row = []
            for j in range(num_options):
                field_name = f"score_{i}_{j}"
                val = request.form.get(field_name, "")
                try:
                    score = float(val)
                    if score > 10:
                        return render_template("index.html", error=f"Wert in Zelle {i+1}×{j+1} mehr als 10", data=request.form)
                    row.append(score)
                except ValueError:
                    return render_template("index.html", error=f"Falscher Wert in der Zelle {i+1}×{j+1}", data=request.form)
            scores.append(row)

        results = []
        for j in range(num_options):
            total = sum(scores[i][j] * normalized_weights[i] for i in range(num_criteria))
            results.append((options[j], round(total, 4)))


        chart_data = {
            "labels": criteria,
            "datasets": []
        }

        for j, option in enumerate(options):
            values = [scores[i][j] for i in range(num_criteria)]
            chart_data["datasets"].append({
                "label": option,
                "data": values
            })
        colors = [
            "rgba(255, 99, 132, 0.6)",
            "rgba(54, 162, 235, 0.6)",
            "rgba(255, 206, 86, 0.6)",
            "rgba(75, 192, 192, 0.6)",
            "rgba(153, 102, 255, 0.6)",
            "rgba(255, 159, 64, 0.6)"
        ]

        bar_data = {
            "labels": ["Bewertung"],
            "datasets": [
                {
                    "label": name,
                    "data": [value],
                    "backgroundColor": colors[i % len(colors)],
                    "borderColor": colors[i % len(colors)].replace("0.6", "1"),
                    "borderWidth": 1
                }
                for i, (name, value) in enumerate(results)
            ]
        }

        return render_template("index.html", results=results, data=request.form, chart_data=json.dumps(chart_data), bar_data=bar_data)

    return render_template("index.html")

# 🚀 Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)