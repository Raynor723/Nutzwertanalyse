from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получаем значения из формы
        option_names = request.form.getlist("option_name")
        criteria_names = request.form.getlist("criterion_name")
        weights_raw = request.form.getlist("weight")

        try:
            weights = [float(w) for w in weights_raw]
        except ValueError:
            return render_template("index.html", error="Некорректный вес", data=request.form)

        # Нормализация весов: перевод в доли
        try:
            weights = [float(w) for w in weights_raw]
        except ValueError:
            return render_template("index.html", error="Некорректный вес", data=request.form)

        weight_sum = sum(weights)
        if abs(weight_sum - 100) > 0.01:
            return render_template("index.html", error="Сумма всех весов должна быть ровно 100", data=request.form)

        normalized_weights = [w / 100 for w in weights]

        num_criteria = len(criteria_names)
        num_options = len(option_names)

        # Чтение оценок
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

        # Расчёт результата
        results = []
        for j in range(num_options):
            total = 0
            for i in range(num_criteria):
                total += scores[i][j] * normalized_weights[i]
            results.append({
                "name": option_names[j],
                "score": total
            })

        results.sort(key=lambda x: x["score"], reverse=True)

        # Передаём обратно данные + результат
        return render_template("index.html", results=results, data=request.form)

    return render_template("index.html")


# 🚀 Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
