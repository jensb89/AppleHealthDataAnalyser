import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

def main(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    foods = defaultdict(lambda: {
        "count": 0,
        "calories": 0.0
    })

    for record in root.iter("Record"):
        if "YAZIO" not in record.attrib.get("sourceName", "").upper():
            continue

        metadata = {m.attrib["key"]: m.attrib["value"]
                    for m in record.findall("MetadataEntry")}

        food = metadata.get("HKFoodType")
        if not food:
            continue

        if record.attrib.get("type") != "HKQuantityTypeIdentifierDietaryEnergyConsumed":
            continue

        dt = datetime.strptime(
            record.attrib["startDate"],
            "%Y-%m-%d %H:%M:%S %z"
        )

        year, week, _ = dt.isocalendar()
        key = (year, week, food)

        foods[key]["count"] += 1
        foods[key]["calories"] += float(record.attrib.get("value", 0))

    print("year,week,food,count,calories_kcal")
    for (year, week, food), data in sorted(foods.items()):
        food = food.replace(",", ".")  # Remove commas from food names
        print(f"{year},{week},{food},{data['count']},{data['calories']:.0f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python weekly_food_summary.py export.xml")
        sys.exit(1)

    main(sys.argv[1])
