import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict

NUTRIENT_MAP = {
    "HKQuantityTypeIdentifierDietaryEnergyConsumed": ("calories_kcal", float),
    "HKQuantityTypeIdentifierDietaryProtein": ("protein_g", float),
    "HKQuantityTypeIdentifierDietaryCarbohydrates": ("carbs_g", float),
    "HKQuantityTypeIdentifierDietaryFatTotal": ("fat_g", float),
    "HKQuantityTypeIdentifierDietaryWater": ("water_ml", float),
}

def parse_day(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def main(xml_file, start_date, end_date):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    start_dt = parse_day(start_date)
    end_dt = parse_day(end_date)

    foods = defaultdict(lambda: {
        "food": None,
        "datetime": None,
        "nutrients": defaultdict(float)
    })

    for record in root.iter("Record"):
        source = record.attrib.get("sourceName", "")
        if "YAZIO" not in source.upper():
            continue

        start_time = record.attrib.get("startDate")
        record_dt = datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S %z"
        ).replace(tzinfo=None)

        if not (start_dt <= record_dt <= end_dt):
            #print("skipping record:", record.attrib)
            #print(start_dt)
            #print(end_dt)
            #print(record_dt)
            continue
        #print("found record:", record.attrib)
        record_type = record.attrib.get("type")
        value = float(record.attrib.get("value", 0))

        metadata = {m.attrib["key"]: m.attrib["value"]
                    for m in record.findall("MetadataEntry")}

        uuid = metadata.get("HKExternalUUID")
        if not uuid:
            continue

        food_name = metadata.get("HKFoodType")

        entry = foods[uuid]
        #print(entry)

        if food_name:
            entry["food"] = food_name
        if entry["datetime"] is None:
            entry["datetime"] = record_dt

        if record_type in NUTRIENT_MAP:
            field, cast = NUTRIENT_MAP[record_type]
            entry["nutrients"][field] += cast(value)

    # Output CSV
    headers = [
        "date", "time", "food",
        "calories_kcal", "protein_g", "carbs_g", "fat_g", "water_ml"
    ]
    print(",".join(headers))

    for entry in foods.values():
        dt = entry["datetime"]
        row = [
            dt.date().isoformat(),
            dt.time().strftime("%H:%M:%S"),
            entry["food"] or "UNKNOWN"
        ]
        for h in headers[3:]:
            row.append(f"{entry['nutrients'].get(h, 0):.2f}")
        print(",".join(row))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python extract_food_items.py export.xml YYYY-MM-DD YYYY-MM-DD")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
