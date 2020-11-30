import argparse
import os
from datetime import datetime
from typing import List

import typer

from .binary_search import SearchTree
from .controllers import read_csv, truck_assignment, write_csv


def _cargo_validation(header: List[str]) -> bool:
    if header != ["product", "origin_city", "origin_state", "origin_lat", "origin_lng", "destination_city",
                  "destination_state", "destination_lat", "destination_lng"]:
        typer.echo(f"{typer.style('Wrong CSV header for cargo csv file!!!', fg=typer.colors.RED, bold=True)}")
        message = ("product, origin_city, origin_state, origin_lat, origin_lng, destination_city, destination_state, "
                   "destination_lat, destination_lng")
        typer.echo(f"Allowed values {typer.style(message, fg=typer.colors.GREEN, bold=True)}")
        typer.echo(f"You gave       {typer.style(', '.join(header), fg=typer.colors.BRIGHT_RED, bold=True)}")
        return False

    return True


def _truck_validation(header: List[str]) -> bool:
    if header != ["truck", "city", "state", "lat", "lng"]:
        typer.echo(f"{typer.style('Wrong CSV header for truck csv file!!!', fg=typer.colors.RED, bold=True)}")
        typer.echo(f"Allowed values {typer.style('truck, city, state, lat, lng', fg=typer.colors.GREEN, bold=True)}")
        typer.echo(f"You gave       {typer.style(', '.join(header), fg=typer.colors.BRIGHT_RED, bold=True)}")
        return False

    return True


def _save(assignments: List[dict], file_name: str) -> None:
    write_csv(path=file_name, data=assignments, header=["cargo", "truck", "distance"])
    typer.echo(f"Everything was {typer.style('good', fg=typer.colors.GREEN, bold=True)}!")
    typer.echo(f"The file {typer.style(file_name, fg=typer.colors.GREEN, bold=True)} was generated successful!! 🍰 ")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cargo_file_path", action="store", help="File path to cargo.csv, use relative path")
    parser.add_argument("truck_file_path", action="store", help="File path to truck.csv, use relative path")
    parser.add_argument("--huge", type=bool, default=False, help="Option to handle huge data")

    args = parser.parse_args()
    cargo_file_path = os.path.join(os.getcwd(), args.cargo_file_path)
    truck_file_path = os.path.join(os.getcwd(), args.truck_file_path)

    start = datetime.now()

    cargos, cargo_header = read_csv(file_path=cargo_file_path)
    if not _cargo_validation(cargo_header):
        typer.Exit(1)

    trucks, truck_header = read_csv(file_path=truck_file_path)
    if not _truck_validation(truck_header):
        typer.Exit(1)

    if args.huge:
        binary_tree = SearchTree(cargos, trucks)
        results = binary_tree.truck_assignment()
    else:
        results = truck_assignment(cargos, trucks)

    _save(results, os.path.join(os.getcwd(), "results.csv"))
    typer.echo(f"Time spended ✨ {datetime.now() - start} ✨ ")


if __name__ == "__main__":
    typer.run(main)
