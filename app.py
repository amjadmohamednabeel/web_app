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

    # Convert 'Timestamp' to datetime without specifying a format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date.astype(str)  # Convert date to string

    # Convert DataFrame to JSON
    records = df.to_dict(orient='records')
    
    return jsonify(records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
