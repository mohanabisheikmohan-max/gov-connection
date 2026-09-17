import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from services.ai_service import ask_gemini

load_dotenv()
app = Flask(__name__)

DEPARTMENTS = {
    "Education": {
        "icon": "🎓",
        "description": "Education services, scholarships, student support, admissions and education-related government information.",
        "topics": ["Scholarships", "Education Loans", "Student Schemes", "Exams", "Admissions"]
    },
    "Agriculture": {
        "icon": "🌾",
        "description": "Farmer services, agriculture schemes, subsidies, crop support and agriculture-related information.",
        "topics": ["Farmer Schemes", "Subsidies", "Crop Services", "Agriculture Loans", "Insurance"]
    },
    "Health": {
        "icon": "🏥",
        "description": "Public health services, government health schemes, hospitals and citizen health information.",
        "topics": ["Health Schemes", "Hospitals", "Public Health", "Insurance"]
    },
    "Revenue": {
        "icon": "🏛️",
        "description": "Revenue administration, certificates, land-related services and citizen documentation information.",
        "topics": ["Certificates", "Land Services", "Revenue Services"]
    },
    "Transport": {
        "icon": "🚌",
        "description": "Transport services, permits, public transport information and citizen transport services.",
        "topics": ["Bus Services", "Licences", "Transport Services"]
    },
    "Labour & Employment": {
        "icon": "💼",
        "description": "Employment, labour welfare, skill development and worker support information.",
        "topics": ["Jobs", "Employment", "Skill Development", "Labour Welfare"]
    },
    "MSME": {
        "icon": "🏭",
        "description": "Micro, Small and Medium Enterprise support, registrations, schemes and business information.",
        "topics": ["MSME Schemes", "Business Support", "Registration"]
    },
    "Social Welfare": {
        "icon": "🤝",
        "description": "Social welfare schemes and citizen support services.",
        "topics": ["Welfare Schemes", "Women & Child Support", "Social Security"]
    },
    "Tourism": {
        "icon": "🧳",
        "description": "Tourism information, government tourism initiatives and public visitor services.",
        "topics": ["Tourist Places", "Tourism Schemes", "Visitor Services"]
    },
    "Religious Endowments": {
        "icon": "🛕",
        "description": "Temple and religious-endowment information, announcements and public services.",
        "topics": ["Temple Information", "Announcements", "Festivals", "Services"]
    }
}

DEMO_UPDATES = [
    {
        "title": "Government Information Update Center",
        "department": "General",
        "date": datetime.now().strftime("%d %b %Y"),
        "text": "Live-update module is ready to connect with verified official government sources."
    },
    {
        "title": "Student Information Hub",
        "department": "Education",
        "date": datetime.now().strftime("%d %b %Y"),
        "text": "Scholarship, education-loan and student-service information can be organized here."
    },
    {
        "title": "Agriculture Information Hub",
        "department": "Agriculture",
        "date": datetime.now().strftime("%d %b %Y"),
        "text": "Farmer schemes, subsidies and agriculture services can be connected to verified sources."
    }
]

@app.route("/")
def home():
    return render_template(
        "index.html",
        departments=DEPARTMENTS,
        updates=DEMO_UPDATES
    )

@app.route("/api/department/<path:name>")
def department(name):
    data = DEPARTMENTS.get(name)
    if not data:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({
        "name": name,
        **data
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    department = (data.get("department") or "General").strip()

    if not message:
        return jsonify({"answer": "Please enter your question."}), 400

    answer = ask_gemini(message, department, DEPARTMENTS)
    return jsonify({
        "answer": answer,
        "department": department,
        "time": datetime.now().strftime("%I:%M %p")
    })

@app.route("/api/updates")
def updates():
    return jsonify(DEMO_UPDATES)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "GovConnect AI"})

if __name__ == "__main__":
    app.run(debug=True)
