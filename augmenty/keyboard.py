"""
Function for defining and handling keyboard layouts.
"""
from typing import Dict, List, Set, Tuple

from pydantic import BaseModel

from .util import registry


class Keyboard(BaseModel):
    """A Pydantic dataclass object for constructing Keyboard setup.

    Args:
        keyboard_array (Dict[str, str]): An array corresponding to a keyboard.
            This should include two keys a "default" and a "shift". Each containing
            an array of non-shifted and shifted keys respectively.
        shift_distance (int): The distance given by the shift operator. Defaults to 3.

    Returns:
        Keyboard: a Keyboard object
    """

    keyboard_array: Dict[str, List[List[str]]]
    shift_distance: int = 3

    def coordinate(self, key: str) -> Tuple[int, int]:
        """get coordinate for key

        Args:
            key (str): keyboard key

        Returns:
            Tuple[int, int]: key coordinate on keyboard
        """
        for arr in self.keyboard_array:
            for x, row in enumerate(self.keyboard_array[arr]):
                for y, k in enumerate(row):
                    if key == k:
                        return (x, y)

        raise ValueError(f"key {key} was not found in keyboard array")

    def is_shifted(self, key: str) -> bool:
        """is the key shifted?

        Args:
            key (str): keyboard key

        Returns:
            bool: a boolean indicating whether key is shifted.
        """
        for x in self.keyboard_array["shift"]:
            if key in x:
                return True
        return False

    def euclidian_distance(self, key_a: str, key_b: str) -> int:
        """Returns euclidian distance between two keys

        Args:
            key_a (str): keyboard key
            key_b (str): keyboard key

        Returns:
            int: The euclidian distance between two keyboard keys.
        """
        x1, y1 = self.coordinate(key_a)
        x2, y2 = self.coordinate(key_b)

        shift_cost = (
            0
            if self.is_shifted(key_a) == self.is_shifted(key_b)
            else self.shift_distance
        )

        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 + shift_cost

    def all_keys(self):
        """yields all keys in keyboard.

        Yields:
            all keys in keyboard.
        """
        for arr in self.keyboard_array:
            for x, _ in enumerate(self.keyboard_array[arr]):
                for k in self.keyboard_array[arr][x]:
                    yield k

    def get_neighbours(self, key: str, distance: int = 1) -> Set[int]:
        """gets the neighbours of a key with a specified distance.

        Args:
            key (str): A keyboard key
            distance (int, optional): The euclidian distance of neightbours. Defaults to 1.

        Returns:
            Set[int]: The neighbours of a key with a specified distance.
        """
        l = []
        for k in self.all_keys():
            if k == key:
                continue
            if self.euclidian_distance(key, k) <= distance:
                l.append(k)
        return l

    def create_distance_dict(self, distance: int = 1) -> dict:
        return {k: self.get_neighbours(k, distance=distance) for k in self.all_keys()}

    @staticmethod
    def from_registry(entry: str, shift_distance: int = 3) -> "Keyboard":
        """Creates a keyboard from a registry"""
        array = registry.keyboards.get(entry)()
        return Keyboard(keyboard_array=array, shift_distance=shift_distance)
