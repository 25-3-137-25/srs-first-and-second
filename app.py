from flask import Flask, render_template, request, url_for

app = Flask(__name__)


ducks = [
    {
        "id": 1,
        "name": "Классическая Жёлтая Утка",
        "category": "Классика",
        "current_bid": 500,
        "image": "duck1.jpg",
        "description": "Та самая утка из детства. Идеальна для ванной и коллекционирования.",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Утка-Пират",
        "category": "Тематические",
        "current_bid": 1200,
        "image": "duck2.jpg",
        "description": "Резиновая утка в повязке пирата. Для тех, кто ищет приключений.",
        "status": "active"
    },
    {
        "id": 3,
        "name": "Золотая Утка",
        "category": "Премиум",
        "current_bid": 5000,
        "image": "duck3.jpg",
        "description": "Позолоченная резиновая утка. Символ роскоши и хорошего вкуса.",
        "status": "ended"
    },
    {
        "id": 4,
        "name": "Утка-Программист",
        "category": "Тематические",
        "current_bid": 999,
        "image": "duck4.jpg",
        "description": "Помогает отлаживать код. Обязательный атрибут рабочего места разработчика.",
        "status": "active"
    }
]

@app.route("/")
def index():
    active_ducks = [d for d in ducks if d["status"] == "active"]
    return render_template("index.html", ducks=active_ducks)

@app.route("/catalog")
def catalog():
    
    category = request.args.get("category")
    if category:
        filtered_ducks = [d for d in ducks if d["category"] == category]
    else:
        filtered_ducks = ducks
    return render_template("catalog.html", ducks=filtered_ducks, current_category=category)

@app.route("/duck/<int:duck_id>")
def duck_detail(duck_id):
   
    duck = next((d for d in ducks if d["id"] == duck_id), None)
    return render_template("duck.html", duck=duck)

@app.route("/bid/<int:duck_id>", methods=["GET", "POST"])
def bid(duck_id):
    duck = next((d for d in ducks if d["id"] == duck_id), None)
    if not duck:
        return render_template("bid.html", error="Утка не найдена", result=None, duck=None)
    
    error = ""
    result = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        bid_amount_str = request.form.get("bid_amount", "").strip()

        
        if not name or not email:
            error = "Пожалуйста, заполните имя и email."
        elif "@" not in email:
            error = "Пожалуйста, введите корректный email."
        else:
            try:
                bid_amount = int(bid_amount_str)
                if bid_amount <= duck["current_bid"]:
                    error = f"Ставка должна быть строго больше текущей ({duck['current_bid']} ₽)."
                else:
                    
                    result = {
                        "name": name,
                        "email": email,
                        "bid_amount": bid_amount,
                        "duck_name": duck["name"]
                    }
                   
                    duck["current_bid"] = bid_amount
            except ValueError:
                error = "Ставка должна быть целым числом."

  
    return render_template("bid.html", duck=duck, error=error, result=result)

if __name__ == "__main__":
    app.run(debug=True)