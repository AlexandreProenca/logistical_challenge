from typing import List, Any, Tuple

from geopy.distance import geodesic


class Node:
    def __init__(self, point: Tuple[float, float] = (None, None), name: str = None):
        self.point = point
        self.name = name
        self.left = None
        self.right = None

    @property
    def lat(self):
        return self.point[0]

    @property
    def lng(self):
        return self.point[1]

    @classmethod
    def build(cls, nodes: List[Any], depth: int = 0):
        length = len(nodes)
        if length == 0:
            return None

        half = length // 2
        nodes.sort(key=lambda n: n.point[depth % 2])

        node = nodes[half]
        node.left = cls.build(nodes[:half], depth + 1)
        node.right = cls.build(nodes[half + 1:], depth + 1)

        return node

    @classmethod
    def get_closest(cls, root: Any, target: Any, mapping: dict, depth: int = 0) -> Tuple[dict, Any]:
        path = {}
        cls._closest_node(root, target, depth, path, mapping)  # function load path dict with results

        ranking = sorted(path.keys(), key=lambda key: path[key])
        closest = ranking.pop(0)
        while mapping.get(closest) is not None:
            closest = ranking.pop(0)
        mapping[closest] = target

        return path, closest

    @classmethod
    def _closest_node(cls, root: Any, target: Any, depth: int, path: dict, mapping: dict):
        if root is None:
            return

        axis = depth % 2
        next_node, opposite_node = cls._next_node(root, target, axis) # decide if it goes to left or right

        closest_node = lambda node: cls._closest_node(node, target, depth + 1, path, mapping)

        closest = closest_node(next_node)
        best = cls._closer(target, closest, root) # quem tem a menor distancia ate o target

        if geodesic(target.point, best.point) > abs(target.point[axis] - root.point[axis]):
            closest = closest_node(opposite_node)
            best = cls._closer(target, closest, best)

        if best in mapping.keys(): # vefify if exist in mapping busy trucks
            return

        path[best] = geodesic(target.point, best.point)

        return best

    @staticmethod
    def _next_node(root: Any, target: Any, axis: int):
        if target.point[axis] < root.point[axis]:
            return root.left, root.right

        return root.right, root.left

    @classmethod
    def _closer(cls, target: Any, node_a: Any, node_b: Any):
        if node_a is None:
            return node_b
        elif node_b is None:
            return node_a

        distance_t_a = geodesic(target.point, node_a.point)
        distance_t_b = geodesic(target.point, node_b.point)

        return node_a if distance_t_a < distance_t_b else node_b

    def __repr__(self):
        return f"<name:{self.name}, lat:{self.lat}, lng:{self.lng}>"


class KdTree:
    def __init__(self, nodes: List[Any]):
        self.root = Node.build(nodes)
        self.map = {}

    def get_closest(self, target: Any) -> Tuple[dict, Any]:
        return Node.get_closest(self.root, target, self.map)


class SearchTree:
    def __init__(self, cargos: List[dict], trucks: List[dict]):
        self.cargo_nodes, self.truck_nodes = self.build_nodes(cargos, trucks, Node)
        self.tree = KdTree(self.truck_nodes)
        self.delivery_distance = {
            item['product']: geodesic(
                (item['origin_lat'], item['origin_lng']),
                (item['destination_lat'], item['destination_lng'])
            ) for item in cargos
        }

    @staticmethod
    def build_nodes(cargos: List[dict], trucks: List[dict], node_class: Any) -> Tuple[List[Any], List[Any]]:
        cargo_nodes = [node_class((item['origin_lat'], item['origin_lng']), item['product']) for item in cargos]
        truck_nodes = [node_class((item['lat'], item['lng']), item['truck']) for item in trucks]

        return cargo_nodes, truck_nodes

    def truck_assignment(self) -> List[dict]:
        result = []
        for cargo in self.cargo_nodes:
            path, truck = self.tree.get_closest(cargo)
            result.append({
                "cargo": cargo.name,
                "truck": truck.name,
                "distance": round(path[truck].miles + self.delivery_distance[cargo.name].miles, 2)
            })

        return sorted(result, key=lambda x: x['distance'])
