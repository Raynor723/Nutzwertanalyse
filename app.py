from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        option_names = request.form.getlist("option_name")
        criteria_names = request.form.getlist("criterion_name")
        weights_raw = request.form.getlist("weight")

        try:
            weights = [float(w) for w in weights_raw]
        except ValueError:
            return render_template("index.html", error="Некорректный вес (не число)")

        num_criteria = len(criteria_names)
        num_options = len(option_names)

        scores = []
        for i in range(num_criteria):
            row = []
            for j in range(num_options):
                field_name = f"score_{i}_{j}"
                val = request.form.get(field_name, "")
                try:
                    row.append(float(val))
                except ValueError:
                    row.append(0.0)
            scores.append(row)

        results = []
        for j in range(num_options):
            total = 0
            for i in range(num_criteria):
                total += scores[i][j] * weights[i]
            results.append({
                "name": option_names[j],
                "score": total
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        return render_template("index.html", results=results)

    return render_template("index.html")

# 🚀 Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
