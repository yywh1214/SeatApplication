from typing import List


def generate_names(names: List):
    for i, name in enumerate(names):
        print(f"  - name: {name}")


if __name__ == "__main__":
    generate_names(list(range(37)))
