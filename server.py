from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def top_15():
    try:
        with open('/app/data/top15.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        projects = data['projects']
        update_date = data['update_date']
        voting_status = data['voting_status']
    except FileNotFoundError:
        return "Данные не найдены. Запустите update_data.py для получения данных."
    return render_template('index.html', projects=projects, update_date=update_date, voting_status=voting_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
