import requests
import json
from datetime import datetime

def update_data():
    url = "https://www.gov.kz/api/v1/public/bnu/bnu-projects/903?size=1000&page=0&sort-by=id:desc"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка при запросе API: {response.status_code}")
        return False

    data = response.json()
    all_projects = data.get('bnu_projects', [])
    print(f"Получено проектов: {len(all_projects)}")

    approved_projects = [p for p in all_projects if p['status']['code'] == '2']
    projects_list = []
    for project in approved_projects:
        projects_list.append({
            "id": project.get("id", 0),
            "title": project.get("title", ""),
            "votes_count": project.get("votes_count", 0),
            "location": project.get("location", ""),
            "amount": int(project.get("amount", "0")),
            "create_date": project.get("create_date", ""),
            "status": project['status']['title'],
            "images": project.get("images", "").split(",")[0] if project.get("images") else ""
        })

    projects_sorted = sorted(projects_list, key=lambda x: x['votes_count'], reverse=True)
    projects_filtered = [p for p in projects_sorted if p['votes_count'] > 0]
    top_15 = projects_filtered[:15]
    for project in top_15:
        project['amount'] = f"{project['amount']:,}".replace(',', ' ')
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_to_save = {
        "projects": top_15,
        "update_date": update_date,
        "voting_status": "Голосование активно (с 5 по 24 апреля 2025 года)"
    }
    # Используем путь для Render Disk
    with open('/app/data/top15.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    print("Топ-15 сохранен в top15.json")
    return True

if __name__ == '__main__':
    update_data()
