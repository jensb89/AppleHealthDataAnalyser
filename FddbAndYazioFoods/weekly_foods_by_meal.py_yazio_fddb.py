import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

def main(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # week -> meal -> {event_key: food_name}
    events = defaultdict(lambda: defaultdict(dict))

    for record in root.iter("Record"):
        source = record.attrib.get("sourceName", "")
        if not ("YAZIO" in source.upper() or "FDDB" in source.upper()):
            continue

        metadata = {m.attrib["key"]: m.attrib["value"]
                    for m in record.findall("MetadataEntry")}

        food = metadata.get("HKFoodType")
        if not food:
            continue

        meal = metadata.get("Mahlzeit", "UNKNOWN")
        uuid = metadata.get("HKExternalUUID")

        dt = datetime.strptime(
            record.attrib["startDate"],
            "%Y-%m-%d %H:%M:%S %z"
        )

        year, week, _ = dt.isocalendar()

        # Build food-event identity
        if uuid:
            event_key = ("UUID", uuid)
        else:
            # FDDB fallback
            event_key = (
                "FDDB",
                food,
                meal,
                dt.replace(second=0, microsecond=0)
            )

        # Store event (deduplicated automatically by key)
        events[(year, week)][meal][event_key] = food

    # Output
    for (year, week), meals in sorted(events.items()):
        print(f"\nWeek {year}-{week:02d}")

        for meal, meal_events in meals.items():
            food_counts = defaultdict(int)

            for food_name in meal_events.values():
                food_counts[food_name] += 1

            print(f"  {meal}:")
            for food, count in sorted(food_counts.items(), key=lambda x: -x[1]):
                food = food.replace(",", ".")  # Remove commas from food names
                print(f"    • {food} ({count}×)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python weekly_foods_by_meal_fixed.py export.xml")
        sys.exit(1)

    main(sys.argv[1])
