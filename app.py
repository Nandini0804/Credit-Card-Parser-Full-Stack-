from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re
app = Flask(__name__)
CORS(app)  # allow requests from all origins (for dev)

@app.route("/")
def home():
    return jsonify({"message": "✅ Flask backend is running correctly!"})

@app.route("/upload", methods=["POST"])
def upload():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    # Extract text from PDF
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return jsonify({"error": f"Failed to read PDF: {str(e)}"}), 500

    # Example structured data (replace with real parser logic later)

     # Initialize variables
    card_provider = None
    card_last4 = None
    total_due = None
    due_date = None
    billing_cycle = None

    # Example regex patterns (update based on your PDF format)
    provider_pattern = r"(HDFC|SBI|ICICI|Axis|Citi|Kotak)"  # card provider
    last4_pattern = r"(\d{4})\s*$"  # last 4 digits
    total_due_pattern = r"Total Due\s*[:\s]\s*₹?([\d,\.]+)"  # total amount
    due_date_pattern = r"Due Date\s*[:\s](\d{2}-\d{2}-\d{4})"  # due date
    billing_cycle_pattern = r"Billing Cycle\s*[:\s](.*)"  # billing period

       # Split text into lines for easier parsing
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line.lower().startswith("issuer:"):
            card_provider = line.split(":", 1)[1].strip()
        elif line.lower().startswith("card number") or line.lower().startswith("card number (masked)"):
            match = re.search(r"\d{4}$", line)
            if match:
                card_last4 = match.group(0)
        elif line.lower().startswith("total due"):
            match = re.search(r"₹[\d,\.]+", line)
            if match:
                total_due = match.group(0)
        elif line.lower().startswith("due date"):
            due_date = line.split(":", 1)[1].strip()
        elif line.lower().startswith("billing cycle"):
            billing_cycle = line.split(":", 1)[1].strip()

    # Return structured JSON
    extracted_data = {
        "filename": file.filename,
        "extracted_text": text.splitlines(),  # keeps line breaks
        "card_provider": card_provider,
        "card_last4": card_last4,
        "total_due": total_due,
        "due_date": due_date,
        "billing_cycle": billing_cycle
    }

    return jsonify(extracted_data)

if __name__ == "__main__":
    app.run(debug=True)