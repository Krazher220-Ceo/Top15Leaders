import requests
import json
from datetime import datetime
import os
import subprocess

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

    # Сохраняем top15.json локально
    with open('top15.json', 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    print("Топ-15 сохранен в top15.json")

    # Пушим top15.json в репозиторий GitHub
    try:
        # Клонируем репозиторий (Render предоставит SSH доступ)
        repo_dir = "/app/repo"
        if not os.path.exists(repo_dir):
            subprocess.run(["git", "clone", "git@github.com:Krazher220-Ceo/Top15Leaders.git", repo_dir], check=True)
        os.chdir(repo_dir)

        # Копируем top15.json в репозиторий
        subprocess.run(["cp", "../top15.json", "."], check=True)

        # Добавляем и коммитим изменения
        subprocess.run(["git", "add", "top15.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Update top15.json"], check=True)

        # Пушим изменения
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("top15.json успешно обновлен в репозитории GitHub.")
    except Exception as e:
        print(f"Ошибка при обновлении GitHub: {str(e)}")
        return False

    return True

if __name__ == '__main__':
    update_data()
