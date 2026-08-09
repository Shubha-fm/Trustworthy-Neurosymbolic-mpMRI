from dataclasses import dataclass
import numpy as np

@dataclass
class IntervalBounds:
    lower: np.ndarray
    upper: np.ndarray

    def validate(self):
        if self.lower.shape != self.upper.shape:
            raise ValueError("Shape mismatch.")
        if np.any(self.lower > self.upper):
            raise ValueError("Lower bound exceeds upper bound.")
        return self

def interval_from_samples(latents, radius):
    """
    Convenience baseline for creating conservative per-coordinate bounds
    around a latent point. For the paper's actual verifier, replace this
    with bounds emitted by a sound encoder abstraction.
    """
    z = np.asarray(latents, dtype=float)
    return IntervalBounds(z-radius, z+radius).validate()
