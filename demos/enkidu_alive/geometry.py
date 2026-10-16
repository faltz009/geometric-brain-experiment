"""Quaternion geometry for Enkidu Alive.

The S³ algebra the agent uses: Hamilton product, inverse, σ, the Hopf
decomposition, and grid positions on the Clifford torus T² ⊂ S³, where the
two directions of movement commute, so a position's quaternion is exact
whatever path reached it.
"""

import numpy as np


# --- Quaternion operations ---

def qmul(q1, q2):
    """Hamilton product of two quaternions [w, x, y, z]."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return normalize(np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    ]))


def normalize(q):
    """Project back to unit sphere."""
    n = np.linalg.norm(q)
    if n < 1e-12:
        return IDENTITY.copy()
    return q / n


def invert(q):
    """Quaternion conjugate = inverse on S³. Three sign flips."""
    return np.array([q[0], -q[1], -q[2], -q[3]])


def sigma(q):
    """Geodesic distance from identity, σ = arccos(w) ∈ [0, π].

    Signed: −q is the mirror of q, a full turn short of home, at σ = π.
    """
    return float(np.arctan2(np.linalg.norm(q[1:]), q[0]))


def gap(a, b):
    """The quaternion that takes a to b: invert(a) · b."""
    return qmul(invert(a), b)


def distance(a, b):
    """Geodesic distance between two quaternions."""
    return sigma(gap(a, b))


# --- Hopf decomposition ---

def hopf_decompose(q):
    """Hopf decomposition of q into σ, its base point on S² and its fibre phase.

    The same convention as the Rust crate's `hopf::decompose`: q is read as the
    complex pair a = w + z·i, b = y + x·i, and the Hopf map
    h(a, b) = (|a|² − |b|², 2ab̄) sends it to the base point (R, G, B) on S².
    W is the phase on the S¹ fibre over that point, in [0, 4π): twice the
    common phase of a and b, so a carrier and its mirror differ by 2π.

    Returns dict with sigma, R, G, B, W.
    """
    w, x, y, z = q
    R = 2.0 * (x * z + w * y)
    G = 2.0 * (y * z - w * x)
    B = w * w + z * z - x * x - y * y
    norm = np.sqrt(R * R + G * G + B * B) or 1.0
    # The fibre phase is twice the fibre angle, so a full fibre is 4π and
    # q and −q sit 2π apart: the same convention as Rust's decompose.
    alpha, beta, delta = np.arctan2(z, w), np.arctan2(x, y), np.arctan2(G, R)
    phase = 2 * alpha - delta if w * w + z * z >= x * x + y * y else 2 * beta + delta
    W = float(np.mod(phase, 4 * np.pi))
    return {"sigma": sigma(q), "R": R / norm, "G": G / norm, "B": B / norm, "W": W}


# --- Constants ---

IDENTITY = np.array([1.0, 0.0, 0.0, 0.0])

# Grid positions on the Clifford torus T² ⊂ S³.
#
# Position (x, y) becomes the quaternion
#   q(α, β) = (cos α · cos β,  sin α · cos β,  cos α · sin β,  sin α · sin β)
# with α = y·θ and β = x·θ. Steps in α and in β commute, so q depends only on
# where Enkidu is, whatever path brought him there.
#
# q(α + π, β + π) = q(α, β), so the map is one-to-one while the grid spans
# less than half a turn in each direction. With θ = π/32 the 31 cells of a
# ±15 grid span 30θ < π, and along each axis σ = |steps|·θ grows all the way
# to the edge.

_THETA = np.pi / 32  # one grid cell


def _clifford(alpha, beta):
    """Clifford torus parametrization: (α, β) → unit quaternion."""
    return np.array([
        np.cos(alpha) * np.cos(beta),
        np.sin(alpha) * np.cos(beta),
        np.cos(alpha) * np.sin(beta),
        np.sin(alpha) * np.sin(beta),
    ])


def position_to_quaternion(x, y):
    """Grid position (x, y) → quaternion on the Clifford torus."""
    alpha = y * _THETA  # up/down = α
    beta = x * _THETA   # left/right = β
    return _clifford(alpha, beta)


def quaternion_to_position(q):
    """Quaternion on the Clifford torus → grid position (x, y).

    On the grid both |α| and |β| stay below π/2, so cos α and cos β are
    positive and w = cos α·cos β, x = sin α·cos β, y = cos α·sin β give
    α = atan2(x, w) and β = atan2(y, w) exactly.
    """
    w, x, y, _ = q
    alpha = np.arctan2(x, w)
    beta = np.arctan2(y, w)
    return (round(float(beta / _THETA), 1), round(float(alpha / _THETA), 1))


# Movement: add/subtract _THETA to α or β, recompute quaternion.
# This is equivalent to composing on the torus, but exact.

MOVE_DELTAS = {
    "up":    (0, 1),     # +1 in y (α)
    "down":  (0, -1),    # -1 in y
    "right": (1, 0),     # +1 in x (β)
    "left":  (-1, 0),    # -1 in x
}

MOVE_NAMES = list(MOVE_DELTAS.keys())


class EnkiduState:
    """Enkidu's position on the Clifford torus.

    Tracks grid position (x, y) as integers and computes the
    corresponding quaternion. Movement is exact — no floating
    point drift.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def quaternion(self):
        return position_to_quaternion(self.x, self.y)

    @property
    def position(self):
        return (self.x, self.y)

    def move(self, direction):
        """Take one step. Returns the new quaternion."""
        dx, dy = MOVE_DELTAS[direction]
        self.x += dx
        self.y += dy
        return self.quaternion

    def sigma_from(self, target_q):
        """Distance from current position to a target quaternion."""
        return distance(self.quaternion, target_q)

    def sigma_home(self):
        """Distance from home (identity)."""
        return sigma(self.quaternion)

    def hopf(self):
        """Hopf decomposition of current state."""
        return hopf_decompose(self.quaternion)

    def best_step_toward(self, target_x, target_y):
        """Which direction reduces Manhattan distance to target?

        Uses grid coordinates directly — no ambiguity from S³ wrapping.
        Returns (move_name, manhattan_distance_after_move).
        """
        best_name = None
        best_dist = float("inf")

        for name, (dx, dy) in MOVE_DELTAS.items():
            nx, ny = self.x + dx, self.y + dy
            d = abs(nx - target_x) + abs(ny - target_y)
            if d < best_dist:
                best_dist = d
                best_name = name

        return best_name, best_dist

    def copy(self):
        return EnkiduState(self.x, self.y)
