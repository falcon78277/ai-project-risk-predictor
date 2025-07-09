import os
from flask import Flask, request, render_template, send_file
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from flask import jsonify

# ----------------------
# Configuration
# ----------------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'supersecretkey'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ----------------------
# Load API key from .env
# ----------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# ----------------------
# Initialize model and features
# ----------------------
model = RandomForestClassifier()
feature_columns = []

# ----------------------
# Train the model
# ----------------------
def train_model():
    global feature_columns
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'large_project_data.csv')
    if not os.path.exists(csv_path):
        print(f"❌ Training skipped: File not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df['deadline'] = pd.to_datetime(df['deadline'])
    df['days_left'] = (df['deadline'] - pd.Timestamp.today()).dt.days
    df['risk'] = ((df['progress'] < 60) | (df['sentiment_score'] < 0)).astype(int)
    df = pd.get_dummies(df, columns=['workload'])

    feature_columns = ['progress', 'hours_logged', 'sentiment_score', 'days_left'] + \
                      [col for col in df.columns if col.startswith('workload_')]

    X = df[feature_columns]
    y = df['risk']
    model.fit(X, y)
    print("✅ Model trained successfully.")

# ----------------------
# Predict risk
# ----------------------
def predict_risk(df):
    df['deadline'] = pd.to_datetime(df['deadline'])
    df['days_left'] = (df['deadline'] - pd.Timestamp.today()).dt.days
    df = pd.get_dummies(df, columns=['workload'])

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]
    df['risk'] = model.predict(df)
    return df

# ----------------------
# Generate AI recommendation using Gemini
# ----------------------
def get_ai_suggestions(row):
    data = row.to_dict()
    prompt = f"""
    Based on the following employee/project data:
    {data}

    Suggest 2 smart actions a project manager should take to reduce the project risk.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini Error: {e}"
    


# ----------------------
# Routes
# ----------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['csv_file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            df = pd.read_csv(file_path)
            df_result = predict_risk(df)

            df_result['recommendation'] = df_result.apply(
                lambda row: get_ai_suggestions(row) if row['risk'] == 1 else '', axis=1
            )

            # Save result to CSV
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'prediction_output.csv')
            df_result.to_csv(output_path, index=False)

            return render_template('result.html',
                                   tables=[df_result.to_html(classes='data text-white', index=False)],
                                   titles=df_result.columns.values)

    return render_template('index.html')

@app.route('/download')
def download():
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'prediction_output.csv')
    return send_file(output_path, as_attachment=True)



@app.route('/dashboard')
def dashboard():
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'prediction_output.csv')
    if not os.path.exists(output_path):
        return "No predictions available. Please upload a CSV file first.", 400

    df = pd.read_csv(output_path)

    # Risk data
    risk_counts = df['risk'].value_counts().sort_index().to_dict()

    # Workload
    workload_cols = [col for col in df.columns if col.startswith("workload_")]
    workload_counts = {}
    if workload_cols:
        for col in workload_cols:
            workload_label = col.replace("workload_", "")
            workload_counts[workload_label] = int(df[col].sum())
    elif 'workload' in df.columns:
        workload_counts = df['workload'].value_counts().to_dict()

    # Status counts
    status_counts = df['status'].value_counts().to_dict() if 'status' in df.columns else {}

    # Timeline metrics
    timeline_projects = df['project_name'].tolist() if 'project_name' in df.columns else []
    timeline_planned = df['planned_days'].tolist() if 'planned_days' in df.columns else []
    timeline_actual = df['actual_days'].tolist() if 'actual_days' in df.columns else []

    # Confidence scores
    confidence_projects = df['project_name'].tolist() if 'project_name' in df.columns else []
    confidence_scores = df['prediction_confidence'].tolist() if 'prediction_confidence' in df.columns else []

    return render_template('dashboard.html',
                           risk_labels=list(risk_counts.keys()),
                           risk_values=list(risk_counts.values()),
                           workload_labels=list(workload_counts.keys()),
                           workload_values=list(workload_counts.values()),
                           status_labels=list(status_counts.keys()),
                           status_values=list(status_counts.values()),
                           timeline_projects=timeline_projects,
                           timeline_planned=timeline_planned,
                           timeline_actual=timeline_actual,
                           confidence_projects=confidence_projects,
                           confidence_scores=confidence_scores)



# ----------------------
# Run server
# ----------------------
train_model()  # Train the model on startup

if __name__ == '__main__':
    
    app.run(debug=True)
