from flask import Flask, jsonify, request

app = Flask(__name__)

templates = [
    {
        "id": "1",
        "title": "Order Fries",
        "description": "Create an order for fries with customizable size and sauces.",
        "tags": ["side"],
        "owner": "kitchen-team",
    },
    {
        "id": "2",
        "title": "Order Milkshake",
        "description": "Create an order for milkshake with customizable flavors and size.",
        "tags": ["drink"],
        "owner": "customer-service-team",
    },
    {
        "id": "3",
        "title": "Order Cheeseburger",
        "description": "Create an order for cheeseburger with customizable size, sauces, and toppings.",
        "tags": ["main"],
        "owner": "kitchen-team",
    },
]

@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    response = jsonify(templates)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    
    return response, 200

@app.route("/feedback", methods=["POST"])
def post_feedback():
    feedback_data = request.get_json()
    template_id = feedback_data["templateId"]
    feedback = feedback_data["feedback"]

    print(f"Received feedback for template {template_id}: {feedback}")

    return jsonify({"message": "Feedback received"})

if __name__ == "__main__":
    app.run(port=5000)