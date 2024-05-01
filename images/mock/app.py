from flask import Flask, jsonify, request

app = Flask(__name__)

templates = [
    {
        "id": "1",
        "title": "Template 1",
        "description": "This is the first template",
        "tags": ["tag1", "tag2"],
        "owner": "Owner 1",
    },
    {
        "id": "2",
        "title": "Template 2",
        "description": "This is the second template",
        "tags": ["tag2", "tag3"],
        "owner": "Owner 2",
    },
    {
        "id": "3",
        "title": "Template 3",
        "description": "This is the third template",
        "tags": ["tag1", "tag3"],
        "owner": "Owner 3",
    },
]

@app.route("/recommendations", methods=["GET"])
def get_recommendations():
    return jsonify(templates)

@app.route("/feedback", methods=["POST"])
def post_feedback():
    feedback_data = request.get_json()
    template_id = feedback_data["templateId"]
    feedback = feedback_data["feedback"]

    print(f"Received feedback for template {template_id}: {feedback}")

    return jsonify({"message": "Feedback received"})

if __name__ == "__main__":
    app.run(port=5000)