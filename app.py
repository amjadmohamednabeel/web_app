from flask import Flask, render_template, jsonify
import pandas as pd
import os
from glob import glob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    folder_path = 'excel_data'  # Update with your actual path
    file_pattern = os.path.join(folder_path, 'tag_log_*.xlsx')

    all_files = glob(file_pattern)
    if not all_files:
        return jsonify({"error": "No log files found."}), 404

    df_list = [pd.read_excel(file) for file in all_files]
    df = pd.concat(df_list, ignore_index=True)

    # Handle mixed Timestamp formats
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')  # Coerce invalid formats to NaT
        df.dropna(subset=['Timestamp'], inplace=True)  # Drop rows where Timestamp is NaT
    except Exception as e:
        return jsonify({"error": f"Error processing timestamps: {str(e)}"}), 500

    # Add a 'Date' column
    df['Date'] = df['Timestamp'].dt.date.astype(str)  # Ensure 'Date' is a string

    # Convert DataFrame to JSON
    records = df.to_dict(orient='records')
    
    return jsonify(records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
