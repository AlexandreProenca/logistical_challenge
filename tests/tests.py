from app.main import _truck_validation, _cargo_validation, _save
from app.binary_search import SearchTree

import os


def test_truck_assignment(cargos, trucks):
    expected = [
        {'cargo': 'Oranges', 'truck': 'Fish-Bones Towingew York', 'distance': 299.74},
        {'cargo': 'Wood', 'truck': 'Wisebuys Stores Incouverneur', 'distance': 467.77},
        {'cargo': 'Wood', 'truck': 'Gary Lee Wilcoxpencer', 'distance': 520.24},
        {'cargo': 'Light bulbs', 'truck': 'Viking Products Of Austin Incustin', 'distance': 622.51},
        {'cargo': 'Recyclables', 'truck': 'Ricardo Juradoacramento', 'distance': 692.32},
        {'cargo': 'Apples', 'truck': "Kjellberg'S Carpet Oneuffalo", 'distance': 2103.46},
        {'cargo': 'Cell phones', 'truck': 'Paul J Krez Companyorton Grove', 'distance': 2226.39}
    ]

    binary_tree = SearchTree(cargos, trucks)

    assert binary_tree.truck_assignment() == expected


def test_truck_validation():
    header = ["product", "origin_city", "origin_state", "origin_lat", "origin_lng", "destination_city",
              "destination_state", "destination_lat", "destination_lng"]

    assert _cargo_validation(header)


def test_cargo_validation():
    header = ["truck", "city", "state", "lat", "lng"]

    assert _truck_validation(header)


def test_save_file(cargos, trucks, tmpdir):
    file_name = os.path.join(tmpdir, 'results.csv')
    binary_tree = SearchTree(cargos, trucks)
    _save(binary_tree.truck_assignment(), file_name)

    assert os.path.isfile(file_name)
