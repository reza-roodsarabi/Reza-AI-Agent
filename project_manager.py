import json
import csv

def load_projects():
    with open("projects.json", "r") as f:
        return json.load(f)


def save_projects(projects):
    with open("projects.json", "w") as f:
        json.dump(projects, f, indent=4)


def add_project(projects, title, budget, tags):
    new_project = {
        "title": title,
        "budget": budget,
        "tags": [t.strip().lower() for t in tags.split(",")]
    }

    projects.append(new_project)
    save_projects(projects)


def delete_project(projects, index):
    if 0 <= index < len(projects):
        deleted = projects.pop(index)
        save_projects(projects)
        return deleted

    return None

def search_projects(projects, keyword):

    results = []

    keyword = keyword.lower()

    for p in projects:

        if keyword in p["title"].lower():
            results.append(p)

        elif keyword in p["tags"]:
            results.append(p)

    return results
def sort_by_budget(projects):

    def get_budget(project):
        return int(project["budget"].replace("$", ""))

    return sorted(
        projects,
        key=get_budget,
        reverse=True
    )
def project_statistics(projects):

    budgets = []

    for p in projects:
        budgets.append(
            int(p["budget"].replace("$", ""))
        )

    stats = {
        "total": len(projects),
        "highest": max(budgets),
        "lowest": min(budgets),
        "average": sum(budgets) / len(budgets)
    }

    return stats
def export_to_csv(projects):

    with open("exports/projects.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Title", "Budget", "Tags"])

        for p in projects:

            writer.writerow([
                p["title"],
                p["budget"],
                ", ".join(p["tags"])
            ])
def edit_project(projects, index, title, budget, tags):

    if 0 <= index < len(projects):

        projects[index]["title"] = title
        projects[index]["budget"] = budget
        projects[index]["tags"] = [
            t.strip().lower()
            for t in tags.split(",")
        ]

        save_projects(projects)

        return True

    return False
def import_from_csv():

    projects = []

    with open("exports/projects.csv", "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            projects.append({
                "title": row["Title"],
                "budget": row["Budget"],
                "tags": [
                    t.strip().lower()
                    for t in row["Tags"].split(",")
                ],
                "favorite": False
            })

    save_projects(projects)

    return projects

def toggle_favorite(projects, index):

    if 0 <= index < len(projects):

        projects[index]["favorite"] = not projects[index]["favorite"]

        save_projects(projects)

        return projects[index]

    return None