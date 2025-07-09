# 🤖 AI Project Risk Predictor

A visually engaging, AI-powered web application that predicts the risk level of projects using machine learning. It includes a sleek dashboard, interactive visualizations, and CSV upload support, built with **Flask**, **Chart.js**, and **TailwindCSS**.

---

## 🚀 Features

* 📂 Upload project datasets (CSV)
* 📊 Predict risk category (Low / High)
* 📈 Interactive dashboards for:

  * Risk Level Distribution
  * Workload Balance
  * Delay Trends
* 🎨 Glassmorphism UI with dark mode theme
* 💬 Integrated with Gemini AI for mitigation suggestions *(optional)*

---

## 📁 Folder Structure

```
├── app.py                   # Main Flask server
├── generate_data.py         # Generate dummy/sample project data
├── uploads/                 # Uploaded CSVs (gitignored)
├── static/
│   ├── bg.jpg               # Background image
│   └── ...
├── templates/
│   ├── index.html           # Landing & upload
│   ├── dashboard.html       # Dashboard page
│   └── result.html          # Prediction results
├── .env                     # Environment config (gitignored)
├── .gitignore               # Git ignore rules
└── README.md                # You're here!
```

---

## 🧠 How It Works

1. User uploads a CSV of project metrics.
2. The backend processes the data using a **trained ML model** (e.g. Random Forest).
3. The predicted risk levels are visualized in charts.
4. Gemini (optional) generates insights/recommendations.

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **ML**: scikit-learn (RandomForestClassifier)
* **Frontend**: TailwindCSS, HTML, Chart.js
* **Visualization**: Bar Charts, Metrics
* **AI Recommendations** *(optional)*: Gemini API

---

## 🧪 Sample Test Data

Upload sample CSVs like `sample_ai_project_data.csv` to test risk classification. File format:

| project\_name | complexity | duration | team\_size | cost | ... |
| ------------- | ---------- | -------- | ---------- | ---- | --- |
| AI App Dev    | High       | 120      | 5          | 150K | ... |

---

## 📦 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/falcon78277/ai-project-risk-predictor.git
cd ai-project-risk-predictor

# 2. Create a virtual environment (optional but recommended)
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# Visit http://127.0.0.1:5000 in your browser
```

---

## 📸 Screenshots

| Upload CSV                      | Risk Dashboard                     |
| ------------------------------- | ---------------------------------- |
| ![](static/image/upload_ui.png) | ![](static/image/dashboard_ui.png) |

---

## 🌐 Live Demo *(Optional)*

> Host your app on platforms like **Render**, **Railway**, or **Replit**.

---

## 🤝 Contributing

Pull requests and suggestions are welcome! If you’d like to add new charts, enhance the UI, or improve model accuracy, feel free to fork and contribute.

---

## 📫 Contact

* GitHub: [falcon78277](https://github.com/falcon78277)
* LinkedIn: *Your LinkedIn URL here*
* Email: *Your email if you'd like recruiters to contact you*

---

## 🏁 License

This project is licensed under the [MIT License](LICENSE).

---

**Made with 💡 by Aakash Gupta**
