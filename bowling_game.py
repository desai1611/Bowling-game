"""
Bowling Game Implementation

A module for calculating ten-pin bowling scores.
Includes handling of strikes, spares, and 10th-frame bonus rules.
"""

from typing import List


class BowlingGame:
    """Class to represent a single bowling game."""

    def __init__(self) -> None:
        """Initialize a new BowlingGame instance with an empty rolls list."""
        self.rolls: List[int] = []

    def roll(self, pins: int) -> None:
        """
        Record a roll in the game.

        Args:
            pins (int): Number of pins knocked down in this roll.

        Raises:
            ValueError: If pins < 0, pins > 10, or game is already finished.
        """
        if pins < 0 or pins > 10:
            raise ValueError("Pins must be between 0 and 10")
        if self.is_finished():
            raise ValueError("Game already finished")
        self.rolls.append(pins)

    def score(self) -> int:
        """
        Calculate the total score for the game.

        Returns:
            int: The total score after applying bowling scoring rules.
        """
        result = 0
        roll_index = 0

        for frame in range(10):  # 10 frames in a game
            if self._is_strike(roll_index):
                result += 10 + self._strike_bonus(roll_index)
                roll_index += 1
            elif self._is_spare(roll_index):
                result += 10 + self._spare_bonus(roll_index)
                roll_index += 2
            else:
                result += self.rolls[roll_index] + self.rolls[roll_index + 1]
                roll_index += 2

        return result

    # -------------------------------
    # Internal helper methods
    # -------------------------------

    def _is_strike(self, roll_index: int) -> bool:
        """Check if the roll at roll_index is a strike."""
        return roll_index < len(self.rolls) and self.rolls[roll_index] == 10

    def _is_spare(self, roll_index: int) -> bool:
        """Check if the two rolls at roll_index form a spare."""
        return (
            roll_index + 1 < len(self.rolls)
            and self.rolls[roll_index] + self.rolls[roll_index + 1] == 10
        )

    def _strike_bonus(self, roll_index: int) -> int:
        """Calculate the bonus for a strike (next two rolls)."""
        return sum(self.rolls[roll_index + 1 : roll_index + 3])

    def _spare_bonus(self, roll_index: int) -> int:
        """Calculate the bonus for a spare (next one roll)."""
        return self.rolls[roll_index + 2] if roll_index + 2 < len(self.rolls) else 0

    # -------------------------------
    # Game status
    # -------------------------------

    def is_finished(self) -> bool:
        """
        Check if the game has finished.

        Returns:
            bool: True if the game is finished, False otherwise.
        """
        roll_index = 0

        # First 9 frames
        for _ in range(9):
            if roll_index >= len(self.rolls):
                return False
            if self.rolls[roll_index] == 10:  # strike
                roll_index += 1
            else:
                roll_index += 2

        # 10th frame
        if len(self.rolls) <= roll_index:
            return False

        first = self.rolls[roll_index]
        second = (
            self.rolls[roll_index + 1] if len(self.rolls) > roll_index + 1 else None
        )

        # Strike in 10th frame
        if first == 10:
            return len(self.rolls) >= roll_index + 3
        # Spare in 10th frame
        if second is not None and first + second == 10:
            return len(self.rolls) >= roll_index + 3
        # Open 10th frame
        return second is not None
