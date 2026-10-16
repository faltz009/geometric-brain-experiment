# Browser experiments

These pages run the experiments live in JavaScript, in any browser, straight
from disk or from GitHub Pages.

- [index.html](index.html) runs Conway's Game of Life on S³ and the Gray Game,
  with its spectrum, resonance and edge modes.
- [enkidu.html](enkidu.html) runs Enkidu-Alive, the agent whose position lives
  on S³ with home at the identity, so σ, his angle from home, is a geometric
  prediction error.

To serve them from GitHub Pages, publish the `docs/` folder of the `main`
branch; `.nojekyll` is already in place.

## Where the pieces live in the Rust crate

| Area | Source |
|---|---|
| Quaternion composition and distances | [sphere.rs](../src/sphere.rs), [hopf.rs](../src/hopf.rs) |
| Input and comparison | [embed.rs](../src/embed.rs), [verify.rs](../src/verify.rs) |
| Buffer, genome and field reads | [buffer.rs](../src/buffer.rs), [genome.rs](../src/genome.rs), [field.rs](../src/field.rs) |
| The living cycle | [three_cell.rs](../src/three_cell.rs) |
| Hierarchy and consolidation | [hierarchy.rs](../src/hierarchy.rs), [consolidation.rs](../src/consolidation.rs) |
| Computation and learning | [execution.rs](../src/execution.rs), [teach.rs](../src/teach.rs), [examples/](../examples/) |

The full derivation of every piece is in the paper,
[A Geometric Computer](../GeometricComputer.pdf) ([Zenodo](https://zenodo.org/records/19578024)).
