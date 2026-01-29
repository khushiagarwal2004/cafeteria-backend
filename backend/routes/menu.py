from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(prefix="/menu")

# ✅ DEFINE PATH HERE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENU_JSON_PATH = os.path.join(BASE_DIR, "data", "menu_data.json")


@router.get("/daily")
def get_daily_menu():
    try:
        with open(MENU_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Menu data file not found")

from fastapi import Body

@router.post("/book")
def book_meal(payload: dict = Body(...)):
    date = payload.get("date")
    section = payload.get("section")
    item = payload.get("item")
    print("BOOK ENDPOINT HIT")
    print(payload)

    if not date or not section or not item:
        raise HTTPException(status_code=400, detail="Invalid booking data")

    with open(MENU_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if date not in data:
        raise HTTPException(status_code=404, detail="Date not found")

    meals = data[date]["meals"]

    portion_key = None
    if item == "VEG COMBO":
        portion_key = "PORTION-VC"
    elif item == "SALAD BAR":
        portion_key = "PORTION-SB"
    elif item == "NON VEG COMBO" and section == "Afternoon":
        portion_key = "PORTION-NVC"
    elif item == "NON VEG COMBO" and section == "Night":
        portion_key = "PORTION-D"

    if portion_key:
        current = int(meals.get(portion_key, 0))

        if current <= 0:
            raise HTTPException(status_code=400, detail="Sold out")

        # 🔻 decrement + store as string
        meals[portion_key] = str(current - 1)

    with open(MENU_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return {
        "status": "success",
        "remaining": int(meals[portion_key]) if portion_key else None,
    }

