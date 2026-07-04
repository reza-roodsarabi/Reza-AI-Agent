import json
from datetime import datetime

from memory_manager import load_memory, save_memory
from scoring import calculate_score
from project_manager import (
    load_projects,
    add_project,
    delete_project,
    edit_project,
    search_projects,
    sort_by_budget,
    project_statistics,
    export_to_csv,
    import_from_csv,
    toggle_favorite,
)
# ------------------ Load Memory ------------------

memory = load_memory()

if "name" not in memory:
    memory["name"] = ""

if "skills" not in memory:
    memory["skills"] = []

if "history" not in memory:
    memory["history"] = []
    # ------------------ Load Projects ------------------

projects = load_projects()
# ------------------ User ------------------

if not memory["name"]:
    memory["name"] = input("What is your name? ")

if not memory["skills"]:
    skills_input = input("What are your skills? (comma separated): ")
    memory["skills"] = [
        s.strip().lower()
        for s in skills_input.split(",")
    ]

skills_list = memory["skills"]

print(f"\n👋 Welcome {memory['name']}!\n")
# ------------------ Find Projects ------------------

def find_projects():

    seen_projects = []

    for item in memory["history"]:
        seen_projects.extend(item["projects"])

    scored = []

    for p in projects:

        if p["title"] in seen_projects:
            continue

        score = calculate_score(p, skills_list)

        if score > 0:
            scored.append({
                "title": p["title"],
                "budget": p["budget"],
                "score": score
            })

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored
# ------------------ Report ------------------

def report():

    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\n📅 Report - {today}\n")

    results = find_projects()

    if not results:
        print("All matching projects were already shown before.")

    else:

        for p in results:

            original = next(
                project for project in projects
                if project["title"] == p["title"]
            )

            star = "⭐ " if original["favorite"] else ""

            print(f"- {star}{p['title']} ({p['budget']}) -> {p['score']} match")

   
    memory["history"].append({
        "date": today,
        "projects": [p["title"] for p in results]
    })
    # ------------------ Menu ------------------

print("======== AI Agent ========")
print("1. Show projects")
print("2. Update skills")
print("3. Add new project")
print("4. Delete project")
print("5. Search project")
print("6. Sort by budget")
print("7. Project statistics")
print("8. Export to CSV")
print("9. Edit project")
print("10. Import from CSV")
print("11. Toggle Favorite")
print("12. Exit")

choice = input("\nChoose: ")

if choice == "1":
    report()

elif choice == "2":

    skills_input = input("Enter your new skills: ")

    memory["skills"] = [
        s.strip().lower()
        for s in skills_input.split(",")
    ]

    skills_list = memory["skills"]

    print("\n✅ Skills updated!")

    report()

elif choice == "3":

    title = input("Project title: ")
    budget = input("Budget: ")
    tags = input("Tags (comma separated): ")

    add_project(projects, title, budget, tags)

    print("\n✅ Project added successfully!")
elif choice == "4":

    print("\nProjects:")

    for i, p in enumerate(projects):
        print(f"{i+1}. {p['title']}")

    number = int(input("\nEnter project number to delete: "))

    deleted = delete_project(projects, number - 1)

    if deleted:
        print(f"\n✅ '{deleted['title']}' deleted.")
    else:
        print("Invalid number.")
elif choice == "5":

    keyword = input("Keyword: ")

    results = search_projects(projects, keyword)

    if results:
        print("\nFound projects:\n")

        for p in results:
            print(f"- {p['title']} ({p['budget']})")

    else:
        print("\nNo projects found.")
elif choice == "6":

    sorted_projects = sort_by_budget(projects)

    print("\nProjects sorted by budget:\n")

    for p in sorted_projects:
        print(f"- {p['title']} ({p['budget']})")
elif choice == "7":

    stats = project_statistics(projects)

    print("\n===== Project Statistics =====\n")

    print(f"Total projects : {stats['total']}")
    print(f"Highest budget : ${stats['highest']}")
    print(f"Lowest budget  : ${stats['lowest']}")
    print(f"Average budget : ${stats['average']:.2f}")  
elif choice == "8":

    export_to_csv(projects)

    print("\n✅ Projects exported to projects.csv")   
elif choice == "9":

    print("\nProjects:")

    for i, p in enumerate(projects):
        print(f"{i+1}. {p['title']}")

    number = int(input("\nChoose project: "))

    title = input("New title: ")
    budget = input("New budget: ")
    tags = input("New tags (comma separated): ")

    updated = edit_project(
        projects,
        number - 1,
        title,
        budget,
        tags
    )

    if updated:
        print("\n✅ Project updated successfully!")
    else:
        print("\n❌ Invalid project number.")
elif choice == "10":

    projects = import_from_csv()

    print("\n✅ Projects imported from CSV successfully!")      
elif choice == "11":

    print("\nProjects:")

    for i, p in enumerate(projects):

        star = "⭐" if p["favorite"] else ""

        print(f"{i+1}. {star} {p['title']}")

    number = int(input("\nChoose project: "))

    project = toggle_favorite(projects, number - 1)

    if project:

        if project["favorite"]:
            print(f"\n⭐ '{project['title']}' added to favorites!")

        else:
            print(f"\n❌ '{project['title']}' removed from favorites!")

    else:

        print("\nInvalid project number.")      
elif choice == "12":

    print("Goodbye!")  
save_memory(memory)
