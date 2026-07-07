from datetime import datetime


def report(results, projects, memory):

    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\n📅 Report - {today}\n")

    if not results:
        print("All matching projects were already shown before.")

    else:

        for p in results:

            original = next(
                project
                for project in projects
                if project["title"] == p["title"]
            )

            star = "⭐ " if original["favorite"] else ""

            print(
                f"- {star}{p['title']} ({p['budget']}) -> {p['score']} match"
            )

    memory["history"].append({
        "date": today,
        "projects": [p["title"] for p in results]
    })