from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RunConfig:
    alpha: float = 0.99
    window: int = 500

    def validate(self) -> None:
        if not (0.90 <= self.alpha < 1.0):
            raise ValueError("alpha must be in [0.90, 1.0)")
        if self.window < 50:
            raise ValueError("window must be >= 50 (need enough history)")
