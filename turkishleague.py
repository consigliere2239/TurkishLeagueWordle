import requests
import json
import os

API_KEY = os.getenv("API_KEY")  # GitHub Actions'ta secret olarak vereceğiz
BASE_URL = "https://v3.football.api-sports.io"


def get_teams(league=203, season=2025):
    url = f"{BASE_URL}/teams"
    headers = {"x-apisports-key": API_KEY}
    params = {"league": league, "season": season}

    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    teams = []

    for item in data.get("response", []):
        tid = item["team"]["id"]
        name = item["team"]["name"]
        teams.append((tid, name))

    return teams


def get_squad(team_id):
    url = f"{BASE_URL}/players/squads"
    headers = {"x-apisports-key": API_KEY}
    params = {"team": team_id}

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    if not data.get("response"):
        return []

    return data["response"][0]["players"]


def main():
    print("Fetching Süper Lig teams...")
    teams = get_teams()

    all_players = []

    for tid, name in teams:
        print("→", name)
        squad = get_squad(tid)
        for p in squad:
            all_players.append({
                "id": p["id"],
                "name": p["name"],
                "age": p["age"],
                "position": p["position"],
                "number": p["number"],
                "team": name
            })

    # ensure output folder exists
    os.makedirs("data", exist_ok=True)

    with open("data/players.json", "w", encoding="utf-8") as f:
        json.dump(all_players, f, ensure_ascii=False, indent=2)

    print("players.json created successfully!")


if __name__ == "__main__":
    main()
