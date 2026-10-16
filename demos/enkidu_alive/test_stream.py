"""The stream classifier keeps the meaning of a closed zero."""

from .stream import Enkidu


def test_counterpart_inside_the_grace_cycle_is_coherent():
    e = Enkidu()
    e.ingest(b"hunger", 0, "source")
    assert e.advance_cycle() == []  # the grace cycle begins
    assert e.ingest(b"hunger", 1, "target") is None
    assert e.finish() == []
    assert e.unresolved_source == 0


def test_closed_zero_survives_a_late_counterpart():
    e = Enkidu()
    e.ingest(b"cold", 0, "source")
    e.advance_cycle()
    missing = e.advance_cycle()
    assert [m.kind for m in missing] == ["missing"]
    late = e.ingest(b"cold", 5, "target")
    assert late.kind == "reorder"
    assert e.observations[0].absent_at == 2  # the zero stays on record
    assert e.reclassified_count == 1


def test_a_world_tick_is_one_observation_cycle():
    from .homeostasis import World

    w = World(grid_size=15, hunger_rate=0.15, food_spawn_rate=0.0)
    w.spawn_food(3, 0)
    for _ in range(12):
        w.tick()
        # An extra observation inside the same tick must not add a cycle.
        w._hunger_channel.observe(w._hunger_channel._active, w.tick_count)
    assert w._hunger_channel.detector.cycle == w.tick_count
    assert w._cold_channel.detector.cycle == w.tick_count
