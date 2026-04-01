from bs4 import BeautifulSoup

with open("monthly_planner_2026/index.html", "r") as f:
    soup = BeautifulSoup(f, "html.parser")

weekly_section = soup.select_one(".weekly-section")
achievement_section = soup.select_one(".achievement-section")

if weekly_section and achievement_section:
    print("New sections exist.")
    week_boxes = weekly_section.select(".week-box")
    if len(week_boxes) == 5:
        print("5 Week boxes found.")
    else:
        print(f"Incorrect number of week boxes: {len(week_boxes)}")
else:
    print("Sections missing.")
