"""The stream classifier Enkidu: a Python port of the Closure SDK's `Enkidu`.

A shared counter closes observations. An occurrence that arrives on one side
holds its slot open for one full cycle; a counterpart inside that grace period
resolves it with no incident. When the grace cycle closes with the slot still
empty, the empty counterpart is zero presence in that frame and the occurrence
is missing. A counterpart that arrives later reclassifies the same occurrence
as a reorder, and `absent_at` keeps the cycle where its slot closed empty.

Here each drive is one stream: a drive that leaves identity opens a source
record, and resolving the drive closes it with a target record.
"""

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class Incident:
    """One incident: `kind` is "missing" or "reorder"."""

    kind: str
    source_index: int | None
    target_index: int | None
    record: bytes


@dataclass
class Observation:
    """One occurrence and the evidence that classifies it."""

    record: bytes
    source: int | None = None  # position of the source arrival
    target: int | None = None  # position of the target arrival
    absent_at: int | None = None  # cycle where the slot closed empty

    def incident(self) -> Incident | None:
        """The current incident: decided by the closed zero alone."""
        if self.absent_at is None:
            return None
        kind = "reorder" if self.source is not None and self.target is not None else "missing"
        return Incident(kind, self.source, self.target, self.record)


@dataclass
class Enkidu:
    """Counter-based classifier of presence and position over two streams."""

    observations: list = field(default_factory=list)
    cycle: int = 0
    reclassified_count: int = 0
    _unmatched: dict = field(default_factory=lambda: {"source": defaultdict(deque), "target": defaultdict(deque)})
    _waiting: list = field(default_factory=list)  # arrived in this cycle
    _grace: list = field(default_factory=list)  # in their grace cycle

    def ingest(self, record: bytes, position: int, side: str) -> Incident | None:
        """Observe one arrival; returns a reorder when it resolves a missing occurrence."""
        other = "target" if side == "source" else "source"
        queue = self._unmatched[other].get(record)
        if queue:
            obs = self.observations[queue.popleft()]
            setattr(obs, side, position)
            if obs.absent_at is not None:
                self.reclassified_count += 1
            return obs.incident()
        self._unmatched[side][record].append(len(self.observations))
        self._waiting.append(len(self.observations))
        self.observations.append(Observation(record, **{side: position}))
        return None

    def advance_cycle(self) -> list:
        """Close a cycle: slots still empty after their grace cycle become missing."""
        self.cycle += 1
        closing, self._grace, self._waiting = self._grace, self._waiting, []
        return self._close(closing)

    def finish(self) -> list:
        """Both inputs ended: close the last cycle and every slot still open."""
        self.cycle += 1
        closing, self._grace, self._waiting = self._grace + self._waiting, [], []
        return self._close(closing)

    def _close(self, ids) -> list:
        promoted = []
        for i in ids:
            obs = self.observations[i]
            if obs.source is None or obs.target is None:
                obs.absent_at = self.cycle
                promoted.append(obs.incident())
        return promoted

    @property
    def unresolved_source(self) -> int:
        return sum(len(q) for q in self._unmatched["source"].values())

    @property
    def unresolved_target(self) -> int:
        return sum(len(q) for q in self._unmatched["target"].values())
