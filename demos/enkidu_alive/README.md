# Enkidu Alive

A grid agent whose position lives on S³ and whose home is the identity element,
so his distance from home is a geometric prediction error: σ, the angle that
separates his current state from the state he returns to.

## What this is

Enkidu lives on a grid with home at the origin. Two drives pull on him, hunger
and cold, and at every tick he compares them, attends to the larger one, and
steps toward what resolves it: food for hunger, shelter for cold. Applied tick
after tick, that comparison produces foraging trips, direct paths home,
hesitation when the drives are close, and rest at home once both are resolved.
When taught to build shelter, he creates new camps along his routes, which is
niche construction, and extends the range he can survive in.

The agent combines two kinds of machinery, and the table separates them.

| On S³: the geometry | Ordinary game rules |
|---|---|
| Each grid position (x, y) becomes a unit quaternion on the Clifford torus inside S³, at an angle θ of π/32 per cell (π/64 on the browser's larger grid). | Movement is a greedy step: of the four neighbours, he takes the one with the smallest grid (Manhattan) distance to his target. |
| Home is the identity element [1, 0, 0, 0], and σ(position) is the geodesic angle from it, the geometric prediction error. | Hunger is a timer: it rises by a fixed amount each tick and resets to zero when he eats. |
| In the Python version, cold **is** σ(position): the farther his state has turned from identity, the colder he is. | In the browser version, cold is a second timer: it rises each tick he is away from shelter and resets when he reaches one. The browser shows σ as a readout and a glow near home. |
| In the Python version, each tick reports the Hopf decomposition of his position (σ, R, G, B, W). | The larger drive picks the target, with cold multiplied by the temperament weight (Cautious 1.5, Balanced 1.0, Bold 0.5). |
| Each drive runs through the Enkidu stream classifier, ported from the Closure SDK (`stream.py`, and the same rule in the page): a drive that leaves identity opens a record, a record still open after its grace cycle is missing at that cycle, and a later resolution makes it a reorder that keeps that zero. The agent reads it as an open/closed flag per drive. | Shelter building is a threshold rule: when the nearest shelter is more than 24 grid steps away, he spends 3 ticks building a camp where he stands. Food appears at random. |

Because the position is computed from (x, y) on the torus, where the two
directions of movement commute, the quaternion depends only on where he is,
whatever path brought him there.

The torus point repeats only after half a turn in both directions, and each
grid stays inside that range: the Python grid spans 30 cells at π/32 and the
browser's spans 50 cells at π/64. Every cell therefore has its own quaternion,
which converts back to the same cell, and along each axis σ is exactly the
number of cells from home times θ.

**The Free Energy Principle reading.** Home, the identity element, plays the
prior and expected state; σ from identity plays the prediction error that the
agent acts to reduce; the temperament weight plays precision weighting, deciding
which drive becomes the active channel; and each new camp is niche construction,
a new place where cold resets. The greedy grid step carries out the action, and
the geometry supplies the measure of how far he is from home.

## Running the demo

Open [`docs/enkidu.html`](../../docs/enkidu.html) in any browser; the page is
self-contained.

**Controls:**
- **Click** the grid to drop food
- **Shift+click** to place a shelter
- **Thriving / Scarce** toggle the environment
- **Cautious / Balanced / Bold** change his temperament
- **Teach him to build shelter** enables the camp-building rule

**Suggested demo flow:**
1. Start in Thriving and watch the foraging rhythm emerge
2. Switch to Scarce, where he dies of cold or hunger in about half the runs
3. Click "Teach him to build shelter" and watch him build camps along his
   foraging routes, which lifts a Balanced Enkidu to about 97% survival
4. Try Bold, where he roams wider, builds further out, and dies more often,
   the cost of risk-taking

## Survival statistics

Measured with the browser's own simulation code, 2,000 runs of 600 ticks per
setting, in the scarce environment:

| Temperament | No shelter | With shelter | Main cause of death, no shelter |
|---|---:|---:|---|
| Cautious | 47.1% | 86.0% | hunger (71%) |
| Balanced | 47.8% | 97.0% | cold (80%) |
| Bold | 31.1% | 73.8% | cold (100%) |

The thriving environment gives about 99% survival with every temperament, with
or without shelter. `node docs/survival.mjs`, run from the repository root,
prints this table exactly: its random numbers come from a seeded generator.

## Running the Python version

The Python `World` is the version where cold is σ. It has hunger, cold, food and
home, and the browser adds the temperaments, the scarce environment and shelter
building. It needs only NumPy. From the repository root, with Python 3.10 or
newer (on Windows the interpreter is `.venv\Scripts\python`):

```bash
python -m venv .venv
.venv/bin/python -m pip install -r demos/enkidu_alive/requirements.txt pytest
.venv/bin/python -m pytest demos/enkidu_alive
```

| File | What it holds |
|---|---|
| `geometry.py` | The quaternion algebra, σ, the Hopf decomposition, and grid positions on the Clifford torus |
| `homeostasis.py` | The `World`: drives, the stream classifier per drive, target choice and the tick loop |
| `stream.py` | The Enkidu stream classifier, ported from the Closure SDK |
| `test_*.py` | Checks of the geometry, the drives, the paths and the classifier |

## What comes next

**Cold from σ in the browser.** Driving the browser's cold from σ, as the
Python version does, puts the geometric prediction error in charge of the drive
the page shows. σ on the browser's grid reaches about 1.2 at the edge, below the
lethal cold of π, so the death rule needs re-deriving on σ's range first.

**Food storage.** Enkidu carries food back to shelter and eats it later,
reducing hunger from his store between foraging trips, which defers hunger
closure.

**Fire.** Camps with fire reset cold faster or provide a warmth radius, an
amplified cold closure that builds on shelter, since a fire needs a place
to burn.

**Extreme mode.** Very scarce food and harsh cold make both storage and fire
necessary to survive, so compound tool use builds on the same rules.
