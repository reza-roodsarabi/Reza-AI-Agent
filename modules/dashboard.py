from project_manager import (
    project_statistics,
    favorite_count,
)


def dashboard(projects):

    data = project_statistics(projects)

    print("\n========== Dashboard ==========\n")

    print(f"Total Projects    : {len(projects)}")
    print(f"Favorite Projects : {favorite_count(projects)}")

    print()

    print(f"Highest Budget    : ${data['highest']}")
    print(f"Lowest Budget     : ${data['lowest']}")
    print(f"Average Budget    : ${data['average']:.2f}")

    print("\n===============================\n")