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
            return render_template("index.html", error="Некорректный вес", data=request.form)

        weight_sum = sum(weights)
        if abs(weight_sum - 100) > 0.01:
            error = f"Сумма весов должна быть равна 100, сейчас: {round(weight_sum, 2)}"
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
                        return render_template("index.html", error=f"Значение в ячейке {i+1}×{j+1} больше 10", data=request.form)
                    row.append(score)
                except ValueError:
                    return render_template("index.html", error=f"Некорректное значение в ячейке {i+1}×{j+1}", data=request.form)
            scores.append(row)

        results = []
        for j in range(num_options):
            total = sum(scores[i][j] * normalized_weights[i] for i in range(num_criteria))
            results.append((options[j], round(total, 4)))

        # Подготовка данных для радарных графиков
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

        return render_template("index.html", results=results, data=request.form, chart_data=json.dumps(chart_data))

    return render_template("index.html")

# 🚀 Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)