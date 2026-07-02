skills = {
    "python": 3,
    "ai": 5,
    "design": 2,
    "javascript": 2
}


def calculate_score(project, skills_list):
    score = 0

    for skill in skills_list:
        if skill in project["tags"]:
            score += skills.get(skill, 1)

    return score