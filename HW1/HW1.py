import math
import random

class Solution:
    def __init__(self, cities, route):
        self.cities = cities
        self.route = route

    def distance(self):
        total = 0
        n = len(self.route)

        for i in range(n):
            a = self.cities[self.route[i]]
            b = self.cities[self.route[(i + 1) % n]]

            dx = a[0] - b[0]
            dy = a[1] - b[1]
            total += math.sqrt(dx * dx + dy * dy)

        return total

    def height(self):
        return self.distance() * -1

    def neighbor(self):
        n = len(self.route)
        new_route = self.route[:]

        i, j = sorted(random.sample(range(n), 2))

        if i == 0 and j == n - 1:
            return Solution(self.cities, new_route)

        new_route[i:j + 1] = reversed(new_route[i:j + 1])

        return Solution(self.cities, new_route)


def hill_climbing(cities, max_steps=10000):
    n = len(cities)

    # 初始解：1 => 2 => 3 => ... => n => 1
    current = Solution(cities, list(range(n)))

    for step in range(max_steps):
        next_solution = current.neighbor()

        if next_solution.height() > current.height():
            current = next_solution

    return current


cities = [
    (0, 0),   # 1
    (2, 3),   # 2
    (5, 4),   # 3
    (6, 1),   # 4
    (8, 3),   # 5
    (7, 6),   # 6
    (3, 7),   # 7
    (1, 5)    # 8
]

best = hill_climbing(cities)

print("最佳路線：")
for city in best.route:
    print(city + 1, end=" => ")

print(best.route[0] + 1)

print("總距離：", best.distance())
print("高度：", best.height())