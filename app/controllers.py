import csv
import sys
from typing import List, Tuple

from geopy.distance import geodesic


def read_csv(file_path: str) -> Tuple[List[dict], List[str]]:
    try:
        with open(file_path, "r") as file:
            headers = [item.replace("\n", "") for item in [line.split(",") for line in file.readlines()][0]]
    except FileNotFoundError as e:
        print(e.strerror)
        raise sys.exit(1)

    records: List[dict] = []
    with open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, value in row.items():
                if key in [
                    "lat",
                    "lng",
                    "origin_lat",
                    "origin_lng",
                    "destination_lat",
                    "destination_lng",
                ]:
                    row[key] = float(value)
            records.append(row)

    return records, headers


def write_csv(path: str, data: List[dict], header: List[str]):
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def truck_assignment(cargos: List[dict], trucks: List[dict]) -> List[dict]:
    busy_trucks: List[dict] = []
    result: List[dict] = []

    for cargo in cargos:
        shortest_distance = float('inf')
        current_cargo, current_truck, total_distance = None, None, 0.0
        cargo_p1 = (cargo["origin_lat"], cargo["origin_lng"])
        cargo_p2 = (cargo["destination_lat"], cargo["destination_lng"])
        cargo_distance = geodesic(cargo_p1, cargo_p2)

        for truck in trucks:
            if truck in busy_trucks:
                continue

            p2 = (truck["lat"], truck["lng"])
            if geodesic(cargo_p1, p2) < shortest_distance:
                shortest_distance = geodesic(cargo_p1, p2)
                current_cargo = cargo["product"]
                current_truck = truck["truck"]
                busy_trucks.append(truck)
                total_distance = shortest_distance + cargo_distance

        result.append({
            "cargo": current_cargo,
            "truck": current_truck,
            "distance": round(total_distance.miles, 2)
        })

    return sorted(result, key=lambda x: x['distance'])
