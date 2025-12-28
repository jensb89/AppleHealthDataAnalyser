import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from collections import defaultdict

MEAL_GAP_MINUTES = 30

NUTRIENT_MAP = {
    "HKQuantityTypeIdentifierDietaryEnergyConsumed": ("calories_kcal", float),
    "HKQuantityTypeIdentifierDietaryProtein": ("protein_g", float),
    "HKQuantityTypeIdentifierDietaryCarbohydrates": ("carbs_g", float),
    "HKQuantityTypeIdentifierDietaryFatTotal": ("fat_g", float),
}

def parse_day(d):
    return datetime.strptime(d, "%Y-%m-%d")

def main(xml_file, start_date, end_date):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    start_dt = parse_day(start_date)
    end_dt = parse_day(end_date) + timedelta(days=1)

    foods = {}

    for record in root.iter("Record"):
        if "YAZIO" not in record.attrib.get("sourceName", "").upper():
            continue

        record_dt = datetime.strptime(
            record.attrib["startDate"],
            "%Y-%m-%d %H:%M:%S %z"
        ).replace(tzinfo=None)

        if not (start_dt <= record_dt < end_dt):
            continue

        metadata = {m.attrib["key"]: m.attrib["value"]
                    for m in record.findall("MetadataEntry")}

        uuid = metadata.get("HKExternalUUID")
        if not uuid:
            continue

        food_name = metadata.get("HKFoodType")

        entry = foods.setdefault(uuid, {
            "food": food_name,
            "datetime": record_dt,
            "nutrients": defaultdict(float)
        })

        record_type = record.attrib["type"]
        if record_type in NUTRIENT_MAP:
            field, cast = NUTRIENT_MAP[record_type]
            entry["nutrients"][field] += cast(record.attrib["value"])

    # Sort food items by time
    items = sorted(foods.values(), key=lambda x: x["datetime"])

    meals = []
    current_meal = []

    for item in items:
        if not current_meal:
            current_meal = [item]
            continue

        last_time = current_meal[-1]["datetime"]
        if item["datetime"] - last_time <= timedelta(minutes=MEAL_GAP_MINUTES):
            current_meal.append(item)
        else:
            meals.append(current_meal)
            current_meal = [item]

    if current_meal:
        meals.append(current_meal)

    # Output
    for i, meal in enumerate(meals, 1):
        dt = meal[0]["datetime"]
        print(f"\n{dt.date()} — Meal {i} ({dt.time().strftime('%H:%M')})")

        totals = defaultdict(float)
        for food in meal:
            print(f"  • {food['food']}")
            for k, v in food["nutrients"].items():
                totals[k] += v

        print(
            f"  Calories: {totals['calories_kcal']:.0f} kcal | "
            f"Protein: {totals['protein_g']:.1f} g | "
            f"Carbs: {totals['carbs_g']:.1f} g | "
            f"Fat: {totals['fat_g']:.1f} g"
        )

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_meals.py export.xml YYYY-MM-DD YYYY-MM-DD")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
