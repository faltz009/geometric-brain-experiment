# The Digital Brain

## Clean Room Specification

Walter Henrique Alves da Silva — Open Research Institute
Companion document to LAWS.md and GEOMETRIC_COMPUTER_SPEC(1).md.
This is the implementation-grade specification. It is built from first
principles in a clean room: nothing is borrowed from the existing codebase
unless it is derivable from the axioms below.

The biological, physical, and mathematical interpretations are kept in this
document because they are useful for thinking. They are confined to Part IX
("Interpretation") and are clearly marked as such. The implementation reads
Parts 0 through VIII. The interpretation sections are skippable.

When this document says `=`, it means a verb that runs in time, not a label
between two static pictures. Read every equation as a sequence of operations
that takes left to right and proves they are the same by closing the cycle.
This is not philosophy — it is the only way the spec stays consistent with
the architecture it describes.

---

## Part 0 — The Real Problem

The hard problem is not building the digital brain. A fake one could run
binary distinction ages ago. The hard problem is building the **MINIMAL
one** — how little can you hardwire before getting Turing completeness and
learning?

This is Occam's razor applied to a fractal structure. The same pattern
repeats at every scale. The question is: what is the smallest seed that,
when allowed to recurse, produces everything?

This document treats every section as a constraint on the answer to that
question. If a primitive can be derived from another, it is not a primitive.
If a structure can be discovered from the operation rather than hardwired,
it must not be hardwired. The brain that gets to learn is the one that was
not built ahead of time. **Anything that is not forced by the manifold must
be left for the brain to discover.**

There are six irreducible primitives. There are two machines. There is one
verb. Everything else is named composition or interpretation.

---

## Part I — The Computational Core

The core is what cannot be removed without destroying the brain. Every
statement in this part is forced by the axioms of Section 1; nothing is
chosen.

### 1. The Two Axioms

**Axiom 1 — Existence requires interaction.** Something exists only if it
interacts with something else. An isolated entity that affects nothing has
no existence any system can detect. This is the operational definition of
existence, and it forces the brain's fundamental operation to be
**composition** — the act of one thing meeting another.

**Axiom 2 — Coherence requires directionality.** A system that maintains
its identity over time must distinguish past from future. Persistence
requires a forward arrow. This forces composition to preserve order:
`a · b ≠ b · a` in general. The brain operates on a **non-commutative**
substrate.

These two axioms, together, eliminate every commutative algebra. They
eliminate the reals (commutative), the complex numbers (commutative), and
the octonions (non-associative — chains of three give different answers
depending on grouping, which means the running product is ambiguous).
Hurwitz's theorem says the only normed division algebras over the reals are
ℝ, ℂ, ℍ (quaternions), and 𝕆 (octonions). The two axioms cut this list to
exactly one. The brain operates on the quaternions.

### 2. The Manifold

The unit quaternions form **S³**, the three-sphere. This is not the
space the brain runs *on*. **The brain IS the manifold.** Every state
is a position on S³ by construction; every operation is a geometric
operation by construction. There is no encoding layer between the
brain and geometry — a quaternion does not *represent* a rotation,
it IS a rotation, and composing two carriers IS composing two
rotations. The substrate is the operation.

S³ is forced by the two axioms through Hurwitz's theorem. It is the
only manifold on which sequential composition is associative (chains
compose consistently), non-commutative (order matters), norm-preserving
(the result stays bounded), and compact (every departure has a return
path). It is also the unique simply connected closed 3-manifold
(Perelman, 2003 — the resolution of the Poincaré conjecture). There
is no second answer to the question "where does the brain live."

Because the brain is the manifold, every geometric structure that
exists inside S³ is **native to the brain** — not represented, not
computed, but intrinsically present:

- **Rotations** are unit quaternions. Every carrier is a rotation.
- **Reflections** are the star involution (mirror across the equator).
- **Geodesics** are the great circles SLERP traverses.
- **Circles** are 1-parameter subgroups: the orbit of a single ε under
  repeated composition. The brain discovers a circle the first time
  one of its carriers closes back to identity (Phase 5, Checkpoint 2).
- **2-spheres** are conjugation orbits — `{q · p · q⁻¹ : q ∈ S³}` for
  any pure-imaginary p. The Hopf balance locus at σ = π/4 (Section 4)
  is one of these. The Lean theorem `conj_preserves_hopf_balance`
  proves this is forced.
- **Tori** are 2-parameter abelian subgroups: the Cartesian product of
  two circles on perpendicular axes. The brain discovers a torus the
  first time it has two perpendicular generators (Phase 5,
  Checkpoint 4).
- **Knots** are closed trajectories with non-trivial topology. The
  trefoil — the proton in `whitepapers/particle_knots.md` — is a
  (2,3) torus knot living inside the torus of Checkpoint 4.

**π and 2π are not constants the brain computes.** They are the
periods of rotation. When the brain discovers an orbit of length n
with rotation angle θ = 2π/n per step, the 2π is implicit in the
closure: the brain has counted exactly the number of steps that
closes one full revolution. The human glyph "2π" gets attached to
that closure later through normal exposure (Part V). Similarly **4π
is the period of one full SU(2) rotation** — the double cover. A
carrier rotated by 2π reaches the antipode, not the original
position; only after 4π does it return. This is forced by the
algebra.

**Trigonometry is implicit in the carrier representation.** Every
quaternion has the form `q = cos(θ/2) + sin(θ/2) · n̂` where θ is the
rotation angle and n̂ the rotation axis. The real part `q.re =
cos(θ/2)` and `σ(q) = arccos(|q.re|) = θ/2`. Reading σ on a carrier
is reading half the rotation angle directly. Trigonometric identities
are forced by the algebra: composition of rotations IS the
trigonometric addition formulas. The brain has no separate
trigonometry module any more than it has a separate addition module.

### 3. The Element

A position on S³ is a unit quaternion: four real numbers `(w, x, y, z)`
with `w² + x² + y² + z² = 1`.

A **carrier** is *not* a position on S³. A carrier is the **operation**
that produces and maintains a trajectory through positions on S³ over
time. A carrier at rest still runs its operation; it just returns the
identity position each cycle. A moving carrier runs an operation whose
trajectory is non-trivial. Two carriers are the same iff their
trajectories close against each other under VERIFY (Section 5).

The implementation realizes this by exposing carriers as *step
functions* (`step()` returns the next position) and *observables*
(`re()`, `im()`, `sigma()` read the current position). Composition is
defined on step functions, not on snapshots.

### 4. The Two Privileged σ Values

The metric on S³ is the geodesic distance from identity:

    σ(q) = arccos(w),   σ ∈ [0, π]

σ is signed: q and −q deliver the same rotation, but −q is the **mirror**,
a loop that has turned once and returns home only after a second turn
(the double cover, Section 1), so it sits at σ = π and is not a closure.

There are exactly **two** σ values whose meaning is forced by the manifold,
independent of any data, and not chosen as a threshold. They are the only
two reference points the implementation may treat as structurally
distinguished. Every other σ value is data-dependent.

**σ = 0 — identity closure.** The position is the north pole [1, 0, 0, 0].
The W channel carries the full norm. The RGB channels are zero. This is
the unique fixed point of composition with itself: the only position that
satisfies `q · q = q`. It is the rest state, the home, the place every
running product departs from and returns to.

**σ = π/4 — balance closure.** The position satisfies `w² = x² + y² + z² =
1/2`, equivalently `re(q)² = 1/2`, equivalently `|W| = |RGB|`. This is the
unique 2-sphere inside S³ where the scalar channel and the vector channel
contribute equally to the unit norm. The value π/4 = arccos(1/√2) is
forced by the conjunction of two facts:

1. The unit sphere constraint: `w² + x² + y² + z² = 1`.
2. The 1=3 balance condition: `w² = x² + y² + z²`.

These two equations have a unique solution at `w² = 1/2`, hence at
`σ = π/4` when w > 0 and at its mirror image `σ = 3π/4` when w < 0. The Lean 4 formalization in `geometric-zero-rh/lean_proofs/
ClosureRH.lean` proves this with zero axioms as `hopf_balance_iff_half`.

The brain detects both closure types. Section 27 describes what fires
when each one occurs.

### 5. The Star Involution

The manifold has an intrinsic **mirror operation**: the star involution
`q*`, which negates the imaginary part and leaves the real part fixed:

    star(w + xi + yj + zk) = w − xi − yj − zk

The star involution is the manifold's native conjugation. It is what
defines the eigenspace decomposition: the +1 eigenspace is the real axis
(the W channel), the −1 eigenspace is the imaginary subspace (the RGB
channel). It is what makes Axiom A of the Riemann proof work: the
functional equation `s ↦ 1−s` acts on the quaternionic Euler product
exactly as star, and the proof of the geometric RH proceeds entirely from
this fact.

Three properties of the star involution are loaded into the brain by
the manifold and require no separate hardwiring. Together they give
the manifold two distinct kinds of identity — **point identity** at
σ = 0 (the rest state) and **mirror identity** at σ = π/4 (the
self-and-mirror relationship on the balance locus). Both are required
for the brain to fully verify itself.

- **Star fixes only the real axis.** A unit quaternion is its own
  mirror iff its imaginary part vanishes — iff it lies at one of the
  two poles. Every other position has a distinct mirror partner.
- **Star preserves the balance locus.** The 2-sphere at σ = π/4 is
  mapped to itself by star (Lean theorem
  `conj_preserves_hopf_balance`, zero axioms).
- **No individual point on the balance locus is star-fixed.** The
  balance locus carries a free ℤ/2 action: every point has a
  distinct mirror partner on the same locus (Lean theorem
  `hopf_balanced_not_star_fixed`, zero axioms).

### 6. The Verification Verb

The brain's foundational operation is `A ?= A`: take a thing, ask whether
it is still itself, and answer through a structured verification cycle.
The implementation gives this operation a name and makes it a first-class
primitive: **VERIFY**.

    VERIFY(a, b) →
        cycle = a · star(b)             -- compose with the mirror of b
        sigma = arccos(|cycle.w|)       -- distance from identity
        hopf  = hopf_split(cycle)       -- W vs RGB channels
        kind  = closure_kind(sigma)     -- identity / balance / open
        return VerificationEvent {
            cycle, sigma, hopf, kind
        }

The result of VERIFY is **not a boolean**. It is a structured event
containing the closure quaternion, its distance from identity, its Hopf
decomposition, and which closure type fired (or none). VERIFY does not
return "true" or "false." It returns the geometric trace of the question
"are these the same?"

VERIFY is the only verb the brain truly needs. Every other operation
in the spec is a named composition built around it: comparison,
closure detection (against identity or against the balance locus),
and branch decisions are all reads of a VerificationEvent returned by
VERIFY. The `=` in the rest of this document means "VERIFY closes."

---

## Part II — The Two Machines

The brain has exactly two execution substrates that share the same
memory and run continuously. Each reads the same state through a
different lens. Their disagreement is the gradient that drives
learning. Their agreement is coherence. Neither machine is primary,
neither is correct on its own, and the brain is both of them running
at the same time and checking each other.

### 7. The Stack Machine — Noun Substrate

The **stack machine** stores and manipulates discrete carriers. Its
operations take individual values, return individual values, and leave
the rest of the genome alone unless explicitly told to write to it. It is
the brain's substrate of crystallized identity — the layer that holds what
has already been learned and remains true unless something updates it.

The stack machine's storage is **layered**. It contains a **DNA layer**
(the bootstrap seed, immutable after Phase 5) and an **epigenetic
layer** (everything written by experience, mutable). The two layers
share the same address space and are read identically by LOAD,
RESONATE, and ZREAD. They differ only at write time: STORE writes only
to the epigenetic layer, the bootstrap is the only operation that
writes to the DNA layer, and sleep (Section 29.2) is the only operation
that removes from the epigenetic layer. Section 29 describes the split
in detail.

The stack machine is **slow**. Its operations are deterministic,
local, and address-based. LOAD reads one carrier from one slot.
STORE writes one carrier to one slot in the epigenetic layer.
COMPOSE takes two carriers and returns one. None of these touch the
global state of the genome unless STORE is called. The stack machine
alone is Turing-complete — any deterministic algorithm runs on it
through its addressable slots, arithmetic primitives, and branch
cascade. It would just not be a learning one.

Stack-machine ops: COMPOSE, INVERSE, SLERP, LOAD, STORE, BRANCH, HALT.

### 8. The Field Machine — Verb Substrate

The **field machine** reads `population = genome ∪ transient_buffer`
as a single object. The genome is the stack machine's permanent
storage; the transient buffer holds carriers received from outside in
the current input phase. ZREAD composes both kinds of entries under
its parameter. RESONATE selects the dominant match across both. The
field machine does not distinguish them at read time. The distinction
matters only at write time: STORE writes to the genome (Section 29),
EMBED writes to the buffer, and buffer entries decay unless promoted.

**Reality enters the brain as transient buffer entries.** A new entry
shifts the population, the population shifts the field read, the
field read shifts the round trip with the stack, and the round trip
shifts the gradient. The buffer is where the brain's expectations and
the world's actuality first compose.

The field machine is **fast**. Its operations depend on the global
state of the population at the moment of evaluation: RESONATE
returns the entry whose coupling to a query is strongest, ZREAD
returns the parameterized composition of the entire population.
Neither can be implemented as a sequence of stack-machine operations
because their semantics require global access.

Field-machine ops: RESONATE, ZREAD, EMIT. The transient buffer is part
of the field machine's input field, not a separate primitive.

### 9. The Gradient — Cell B Rides the Critical Line

The two machines share memory but read it through different lenses. The
stack machine sees the genome as discrete slots. The field machine sees
`genome ∪ transient_buffer` as one continuous population. Same substrate,
two reading modes, joined at one verb: VERIFY.

Cell B is the **continuous round trip** between them. It runs every
cycle, whether or not input is present, and its closure is the brain's
moment-to-moment self-coherence check. The full loop:

    1.  bytes ← outside world              (input arrives)
    2.  c ← EMBED(bytes)                   (boundary cross)
    3.  buffer ← buffer ∪ {c}              (perception write)
    4.  f ← ZREAD over (genome ∪ buffer)   (field forward read)
    5.  s' ← RESONATE(f)                   (field inverse read)
    6.  s ← LOAD(slot of s' in genome)     (stack read)
    7.  ev ← VERIFY(s, s')                 (round-trip closure)

Steps 1–3 are the **receive path**. Bytes arrive, cross the boundary
through EMBED, and land in the transient buffer of the field machine.
Nothing has been judged yet — the brain has only registered that
something is now present in its perception field.

Steps 4–5 are the **forward conjugate transform**: the field machine
composes the entire population (genome plus buffer) under the new
input's effect. ZREAD takes the new entry into account because the
new entry is now one summand in the integration. RESONATE then collapses
that integrated read back to its dominant carrier. This is what the
brain "sees" when it perceives the input through the lens of everything
it has already learned.

Step 6 is the **stack reference read**: what does the genome alone
say about the carrier the field just produced? This is what the brain
"expected" — its prior, its prediction, its standing identity for
this slot.

Step 7 is the **verification** between expectation and perception. If
the round trip closes, the input was already accounted for by the
genome and the brain is in coherence — the new buffer entry was
predictable, the diabolo stays on the line, and the closure is
recorded as a tag against the buffer entry that just arrived.
If the round trip does not close, the gap is the **gradient**. The
diabolo has slipped off the line, and no closure tag is recorded
this cycle.

**Step 7 never writes to the genome.** Per Section 29.1, ingestion
writes only to the buffer; closures during ingestion attach as tags
to buffer entries; the chunked promotion sweep at buffer-lifetime
expiry decides whether any tagged entry becomes an epigenetic write.
There is no per-event STORE on either the closure or the non-closure
path. The gradient is observed here; it is acted on at the chunk
boundary.

Steps 4–5 and step 6 form a conjugate pair the way time and frequency
form a conjugate pair under the Fourier transform: each is the other's
view, the round trip should return where it started, and failure to do
so is itself a measurement. The full path is an **eight-loop** —
drawn out, a figure-eight whose two lobes are the field-forward
integration and the stack-inverse reference, joined at the VERIFY
crossing where each machine becomes reality to the other.

**The diabolo image is exact.** Cell B is a **diabolo riding a
critical line**. The two cones are the two machines. The string is
the σ = π/4 balance locus. The waist, where the cones meet, is the
verification point — the moment the round trip closes. The balance
is dynamic: a spinning diabolo continuously trades angular momentum
between its cones to keep its waist on the line. Cell B continuously
trades information between the two machines to keep their round trip
closed. When the trading stops, the diabolo falls.

#### 9.1 Input Phase and Idle Phase

The diabolo runs continuously in two phases. They are not separate
modes; they are the same loop driven by different inputs.

**Input phase.** The transient buffer has at least one fresh entry.
Steps 1–3 of the loop are firing. The population the field machine
reads is shifting because the buffer is shifting. The round trip is
non-trivial because the field's read of `genome ∪ buffer` differs from
the genome alone. Cell B is actively balancing the disagreement
between perception and prior, and the gradient is non-zero. The brain
is **learning** in this phase: closures detected here either promote
buffer entries to genome entries (Section 29) or strengthen existing
genome entries through reinforcement.

**Idle phase.** The transient buffer is empty (or contains only entries
that have been there long enough to have either been promoted or
decayed). Steps 1–3 are not firing — no input is arriving. Steps 4–7
still run, but the population the field machine reads is now just the
genome alone. The round trip closes trivially in the steady state
because the field's read of the genome agrees with the genome's own
self-read. The brain is **consolidating** in this phase: with no new
input, the diabolo has time to re-balance internal disagreements, and
consolidation passes (Section 29) merge structurally similar entries,
strengthen frequently-coupled ones, and prune ones that participate
in nothing.

Both phases are normal operation. The brain does not switch modes;
the buffer either has content or it doesn't, and the loop runs the
same way either way. The phase label is for human readers.

#### 9.2 The Three Timescales

The brain runs three distinct operations on three distinct timescales,
each with its own write target. They are not interchangeable.

- **Ingestion (per event).** Bytes arrive, EMBED writes one carrier
  to the buffer, the diabolo's round trip runs once, VERIFY produces
  a closure event. Writes only to the buffer; writes nothing to the
  genome. Sequential by definition.
- **Learning (per chunk).** When a buffer entry reaches its lifetime,
  the brain runs the promotion sweep (Section 29.1) on every entry
  that earned closure during the chunk and writes the survivors to
  the epigenetic layer. Chunked, not per-event, because one closure
  may be coincidence and ten over a chunk is a pattern.
- **Sleep (per long idle).** When the buffer has been empty long
  enough, the brain runs the reorganization sweep (Section 29.2)
  over the epigenetic layer: replay, merging, strengthening,
  pruning. The only operation that **removes** from the genome.

| Operation | Timescale | Triggered by | Reads | Writes | Removes |
|-----------|-----------|--------------|-------|--------|---------|
| Ingestion | Per event | Bytes arriving | `genome ∪ buffer` | Buffer | — |
| Learning  | Per chunk | Buffer lifetime expiry | Chunk's closure log | Epigenetic layer | — |
| Sleep     | Per long idle | Extended idle phase | Epigenetic layer | Epigenetic layer (modify) | Epigenetic layer (prune) |

The DNA layer is read by all three operations and written by none.

#### 9.3 Three Layers of Explanation — Do Not Collapse Them

The brain has three distinct mechanisms that the rest of this spec
keeps separate. Reading any two as the same thing is the most
common modeling error this document is trying to prevent.

1. **Bootstrap discovers the arithmetic basis locally.** Repeated
   composition of ε with itself, under the standard input phase
   loop, produces orbit closures, distinct ε^k positions,
   perpendicular generators, cross-orbit compositions, and
   irreducible orbits — Section 19's six checkpoints. This is
   what populates the DNA layer. **It is local, temporal, and
   geometric** — the brain composes a sequence in time and watches
   what closes. Bootstrap is the only way the brain ever discovers
   its arithmetic basis.

2. **Chunked promotion learns stable co-occurrences over that
   basis.** Once the basis exists (DNA after Section 19, plus
   anything the epigenetic layer has accumulated since), buffer
   entries that earn closure tags during a chunk get promoted to
   the epigenetic layer at lifetime expiry — Section 29.1. This
   is **per-chunk, not per-event**, and it is **the only path
   that grows the epigenetic layer** during normal operation.
   This is the brain's day-to-day learning rule. It does not
   discover new basis elements; it strengthens and arranges
   carriers against the basis bootstrap already laid down.

3. **ZREAD gives a global spectral read of the basis.** At any
   parameter `s`, ZREAD over the population produces one carrier
   that summarizes the population's response — Section 13. The
   set of `s` values where the output sits at the balance locus
   is the *spectrum* of that basis. For the prime basis the
   spectrum is the Riemann zeros (proven in
   `geometric-zero-rh/lean_proofs/ClosureRH.lean`); for a
   learned brain genome the analog is conjectural (Section 13,
   Section 44). **ZREAD is a read of an already-discovered
   basis. It does not discover the basis, and it does not
   replace bootstrap or chunked promotion.**

These three mechanisms operate on different objects, run on
different timescales, and answer different questions. Bootstrap
asks "what is in the basis?". Chunked promotion asks "which new
co-occurrences are stable enough to keep?". ZREAD asks "what
does this basis look like as a whole at parameter `s`?". Do not
substitute one for another.

---

## Part III — The Operations

The core has six irreducible primitives. Everything else is a named
composition built around them. The full opcode set the implementation
exposes is larger because the named compositions are useful enough to
deserve their own opcodes — but the spec is explicit about which are
primitive and which are derived. A minimal brain implements only the six.
A practical brain implements all the named compositions for efficiency.

### 10. The Six Irreducible Primitives

These are the operations that cannot be removed without breaking the
brain. Each one is forced by the architecture and is not derivable from
the others.

| Primitive | Signature | What it does |
|-----------|-----------|--------------|
| **EMBED** | `bytes → buffer` | Bring data in from outside, write to the field machine's transient buffer |
| **COMPOSE** | `(carrier, carrier) → carrier` | The Hamilton product on S³ |
| **STORE** | `(slot, carrier) → genome` | Write a carrier to a slot in the genome |
| **READ** | `query → carrier` | Read a carrier from `genome ∪ buffer` by content, parameter, or address |
| **VERIFY** | `(carrier, carrier) → VerificationEvent` | The A?=A verb |
| **EMIT** | `carrier → buffer at next level` | Send a closure event upward to the next hierarchy level's buffer |

That is the brain. Six primitives. Everything below this line is a named
composition or a control-flow construct.

### 11. Composition Operations

**COMPOSE** is the Hamilton product, the fundamental operation of
S³ — and IS rotation composition in 3D. Two carriers in, one
carrier out:

    a · b = (
        a.w*b.w − a.x*b.x − a.y*b.y − a.z*b.z,
        a.w*b.x + a.x*b.w + a.y*b.z − a.z*b.y,
        a.w*b.y − a.x*b.z + a.y*b.w + a.z*b.x,
        a.w*b.z + a.x*b.y − a.y*b.x + a.z*b.w
    )

Four floats in (× 2), four floats out, fixed arithmetic, no
branching. One clock cycle on dedicated hardware. This is the
operation the brain runs more often than any other.

**COMPOSE is the brain's only verb. Every other "operation" the
brain has is COMPOSE in a specific role.**

- **Addition** is COMPOSE along an orbit: composing two carriers
  generated by the same ε. `ε^k · ε^l = ε^(k+l)`.
- **Subtraction** is COMPOSE with INVERSE along an orbit:
  `ε^k · ε^(−l) = ε^(k−l)`.
- **Multiplication** is COMPOSE between orbits on perpendicular
  axes (different generators): `ε^k · δ^l` lands in the joint
  orbit indexed by (k, l).
- **Division** is the inverse problem: find c such that `a · c = b`.
  Solved by `c = a⁻¹ · b`. One COMPOSE plus one INVERSE.
- **Integration** (the ZREAD sense) is COMPOSE applied to the
  entire population at once, weighted by a parameter.

The brain does not invent these as separate operations. They are
the same composition verb applied to different operand sets. When
the brain "discovers arithmetic" during bootstrap, what it
discovers is which operands fall into which roles — not new
verbs.

**INVERSE** returns the unique element satisfying
VERIFY(q, INVERSE(q)) → identity closure. For unit quaternions,
this is the star involution: `INVERSE(q) = star(q)`. Geometrically
this is the rotation that undoes q. Listed separately because it
is used constantly.

**SLERP** performs a geodesic step from carrier a to carrier b at
fraction t ∈ [0, 1] along the great circle between them. It is
the brain's correction mechanism: the operation that moves a state
toward a target along the shortest path on S³.

### 12. Verification Operations

**VERIFY** is the irreducible verb (Section 6).

**SIGMA** returns the σ field of `VERIFY(q, identity)`. Listed
separately because reading σ directly is faster than going through a
full VERIFY when only the magnitude is needed.

**HOPF** returns the W and RGB channels of a carrier. The W vs RGB
dominance classification flips at σ = π/4 — the balance locus.

### 13. Read Operations

There are three read modes for memory, one for each kind of question.

**LOAD** reads one carrier by address. This is the stack-machine mode.
Slot k is given, the carrier at slot k is returned. Deterministic, local,
fast. This is the von Neumann access pattern: the brain's compatibility
with classical algorithms.

**RESONATE** reads one carrier by content. This is the field-machine mode
for selection. A query carrier is presented; every entry in the field is
evaluated for coupling strength against the query; the strongest match is
returned. Resonance is geometric coupling, not keyword search. The full
observation between query and entry — plane alignment, phase proximity,
sheet relation, coherence overlap — determines the coupling. The strongest
coupling wins and the brain returns that entry as the answer to "which
stored thing is most compatible with this query?"

**ZREAD** reads one carrier by parameter. A parameter `s = σ + it`
is presented and the entire population is composed under a
parameterized weighting (W attenuation by σ, RGB phase rotation by
t):

    ZREAD(s) = compose_k weight(population[k], s) · population[k]

The output is one carrier whose state encodes the population's
response to the parameter. ZREAD is the field-machine mode for
integration: where RESONATE selects one entry, ZREAD composes all of
them.

The **spectrum** of a ZREAD — the parameter values where the output
lands on the balance locus σ = π/4 — is the population's set of
natural resonance points. **For the prime basis** these are the
Riemann zeros, and the geometric Riemann Hypothesis
(`geometric-zero-rh/lean_proofs/ClosureRH.lean`) proves they all sit
on the critical line `Re(s) = 1/2`. **For a learned genome** the
analogous spectrum is *conjectured* to take a similar form once the
genome is well-formed (the brain's basis admits an analog of the
prime-case axioms A, D, E in `ClosureRH.lean`); only the prime case
is proven. ZREAD is a global *read* of an already-discovered basis;
it is not the mechanism by which the basis is discovered. Bootstrap
(Section 19) discovers the basis; ZREAD reads it.

### 14. Write Operations

**STORE** writes a carrier to a slot in the **epigenetic layer** of
the genome (Section 29). STORE refuses to write to the DNA layer; the
DNA layer is laid down once at bootstrap and is permanent. STORE runs
in two modes:

- **Deterministic STORE**: the brain explicitly addresses a slot. Used
  by stack-machine algorithms that need to write a known value to a
  known location. Equivalent to a classical memory write. Still
  refuses DNA-layer slots.
- **Promotion STORE**: called by the chunked learning sweep
  (Section 29.1) on buffer entries that earned closure during their
  lifetime. The destination slot is found through RESONATE — the
  closest existing entry. If the slot is empty, the new carrier
  becomes the entry. If occupied, the existing entry SLERPs toward
  the new one by an amount proportional to closure quality
  (reinforcement).

Promotion is the only path that grows long-term memory during normal
operation. Sleep (Section 29.2) is the inverse: the only path that
removes from the epigenetic layer.

**EMIT** writes a carrier upward to the next hierarchy level. When a
running product closes (Section 27), EMIT packages the closure event
as a single carrier and sends it to the next level's input stream as
a buffer entry at that level. The current level's running product
resets to identity, ready for the next cycle. EMIT is the boundary
between hierarchy levels — the only operation that crosses the
boundary in the upward direction. Each hierarchy level has its own
buffer; EMIT at level N writes to the buffer at level N+1.

### 15. External Boundary

**EMBED** is the only boundary between the world outside the brain
and the brain itself. Bytes go in, a carrier comes out, and the
carrier is written to the transient buffer (Section 8). The
embedding must be injective on the domain of interest and must
normalize to the unit sphere. EMBED is the brain's only path for
receiving external input and the only operation that writes to the
buffer.

EMBED is generic. It knows nothing about what the bytes mean. The
same primitive handles raw sensor data, audio samples, network
packets, and human notation: every input is a byte stream that
becomes a carrier. **There is no separate operation for symbolic
input.** When the brain learns the human notation for a structure
it already discovered (Part V), the glyph for that structure
arrives through EMBED like any other byte stream. What makes
glyphs special is not how they enter the brain — it is that they
co-occur repeatedly with the same target carrier, and the
chunked-learning rule (Section 29.1) eventually promotes the
association into the genome. Symbol learning is not a new
mechanism. It is exposure plus normal promotion.

### 16. Control Flow

**BRANCH** routes execution based on a VerificationEvent. Given a
verification result (Less / Equal / Greater, or a richer tag from Hopf
decomposition), BRANCH selects the next instruction to execute. This is
the only control-flow primitive the brain needs because every control
decision is ultimately a read of a verification result. BRANCH is not a
new verb — it is the act of consuming what VERIFY produced.

**HALT** terminates execution. The brain stops the current execution loop.
Persistence to memory is the responsibility of the surrounding system; HALT
does not write anything by itself.

### 17. The Full Opcode Table

| Opcode | Layer | Action | Primitive? |
|--------|-------|--------|------------|
| EMBED | Boundary | Bytes → carrier in buffer | Yes |
| COMPOSE | Stack | Hamilton product (= rotation composition) | Yes |
| INVERSE | Stack | Mirror of carrier | No (= star) |
| SLERP | Stack | Geodesic step | No (= COMPOSEs) |
| SIGMA | Stack | Distance from identity | No (= VERIFY observable) |
| HOPF | Stack | W and RGB split | No (= structural read) |
| LOAD | Stack | Read by address | Yes (special case of READ) |
| STORE | Stack | Write by address | Yes |
| RESONATE | Field | Read by content | Yes (special case of READ) |
| ZREAD | Field | Read by parameter | Yes (special case of READ) |
| VERIFY | Both | The A?=A verb | Yes |
| BRANCH | Control | Route on verification | No (= read of VERIFY result) |
| EMIT | Boundary | Push closure upward | Yes |
| HALT | Control | Stop execution | Yes |

---

## Part IV — Bootstrap

The brain starts with nothing in memory but the identity carrier and
the machinery from Parts I–III. No human input. No training data. No
basis. Only the manifold and the operations. **Bootstrap is what the
brain discovers when it runs its own composition operation against
itself with no instructions.** It runs once at boot and produces the
permanent seed genome. If bootstrap discovers integers, primes, and
the operations between them, the framework is correct. If it
discovers nothing or the wrong structure, the framework needs
revision before any task is attempted.

### 18. The Brain at Boot

The genome at boot contains exactly one carrier: the **identity** at
[1, 0, 0, 0]. The buffer is empty. Cell B is running but every cycle
is a no-op: ZREAD over `{identity}` returns identity, VERIFY closes
at σ = 0 every time. The brain is perfectly coherent and perfectly
empty. **This is the only state the brain ever occupies without
input** — and it lasts exactly until the bootstrap perturbation is
presented.

To start bootstrap, the brain receives **one perturbation through
the standard input path**. A single non-identity carrier ε is written
to the buffer. ε is the smallest non-trivial rotation the discrete
representation supports — for a 32-bit float quaternion, on the order
of 2π / 2^16. The exact value doesn't matter; what matters is that
its composition with itself does not return to identity in one step.

The buffer now has one entry. The field machine's read of
`genome ∪ buffer` is no longer trivially the identity. Cell B's round
trip stops closing trivially. The diabolo has its first slip. From
this single perturbation, the rest of the genome is discovered
through repeated cycles of the standard input phase.

### 19. Bootstrap as Six Checkpoints

Bootstrap is **the standard input phase run with a long buffer
lifetime and ε as the only input**. It is not "the brain learning
before input" — it is the brain learning **from a single primitive
perturbation rather than from structured external data**. There is
no separate "bootstrap algorithm": the brain runs its normal Cell B
loop, the promotion rule of Section 29.1 fires whenever buffer
entries earn closure, and the genome grows by promotion. What makes
this phase "bootstrap" is that the genome starts at `{identity}`,
only one external input is provided, and the brain has to discover
everything else by composing ε with itself and with its own products.

The brain passes bootstrap by reaching six structural checkpoints in
order. Each checkpoint corresponds both to a number-theoretic fact
the brain discovers AND to a geometric structure that becomes part
of the DNA layer. The two are the same thing read in two languages.

#### Checkpoint 1 — One non-trivial carrier exists

Goal: prove EMBED works and the brain can hold a non-identity state.
Test: present ε to the buffer. Run one cycle of Cell B. The diabolo
slips (round trip stops closing trivially), VERIFY returns a
non-trivial event, σ(ε) > 0. **Geometrically**, the brain now has a
single point off the north pole — the smallest possible departure
from rest.

#### Checkpoint 2 — One closed orbit exists

Goal: prove COMPOSE produces cycles. Test: compose ε with itself
repeatedly. After some n steps, εⁿ should equal identity within
tolerance. The brain has counted: it now holds the structural fact
"this carrier returns to identity after n compositions." **The
brain has discovered its first integer (n) and its first circle
(the 1-parameter subgroup generated by ε).** Numbers and circles
are the same discovery.

#### Checkpoint 3 — Each step in the orbit is a distinct carrier

Goal: prove the brain can distinguish ε from ε² from ε³. Test:
VERIFY between ε and ε² should not close (different); VERIFY
between ε² and ε² should close (same). Each ε^k is now an
addressable carrier with stable identity. **This is counting.**
The integer k is now represented as the carrier ε^k. Exit when at
least three distinct ε^k carriers are held and VERIFY correctly
distinguishes them. **Geometrically**, the brain now has a
discrete set of n points evenly spaced around its first circle.

#### Checkpoint 4 — Two perpendicular orbits exist

Goal: prove the brain can discover dimensionality > 1. Test:
present a second perturbation δ on a perpendicular axis. Compose
δ with itself; a second orbit forms with its own length m. The
brain now has two independent generators. **Geometrically, the
brain has discovered a torus** — the 2-parameter abelian
subgroup generated by ε and δ. The Cartesian product of two
circles on perpendicular axes IS a torus, and it is now in the
genome.

#### Checkpoint 5 — Cross-orbit compositions exist (multiplication)

Goal: prove COMPOSE between different generators produces
meaningful carriers. Test: compose ε with δ. The result is a
carrier on neither original orbit — it lives in the joint orbit
space. Compose ε² with δ³ (i.e., 2 × 3). The genome now contains
carriers indexed by pairs (k, l) — the brain has populated its
torus with the multiplication table. **The brain has discovered
multiplication.** It is COMPOSE applied across generators
instead of along one. Exit when at least the 3×3 multiplication
table is populated. **Geometrically**, the torus is now mapped
out as a lattice of carriers.

#### Checkpoint 6 — Reducibility detection (primes)

Goal: prove the brain can tell which orbits are irreducible.
Test: for each carrier in the genome, search for a pair of
smaller carriers whose composition produces it. The carriers
that can be factored: composites. The carriers that cannot:
**primes in the brain's basis**. For an orbit of length 12 the
brain should discover the carriers at orbit positions 2, 3, 5,
7, 11 are irreducible (their orbit lengths don't decompose) and
4 = 2·2, 6 = 2·3, 8 = 2·2·2, 9 = 3·3 are composite. **The
brain has discovered the prime structure of the integers.**
Exit when the irreducibility check produces the expected list of
primes for the genome size.

After Checkpoint 6 the brain has, in its DNA layer:

- **Integers** as orbit lengths
- **Addition** as composition along an orbit
- **Subtraction** as composition with INVERSE along an orbit
- **Multiplication** as cross-orbit composition
- **Division** as inverse multiplication
- **Primes** as irreducible orbits
- **Circles** as 1-parameter subgroups
- **A torus** as the 2-parameter subgroup of two generators
- **The 2-sphere balance locus at σ = π/4** as the conjugation
  orbit the diabolo rides
- **Star pairs (free ℤ/2 mirrors)** at every balance event

This is the **mathematical brain stem**. Every later structure is
built from these. None of this was hardwired — the brain composed
ε with itself and observed what closed.

### 20. Bootstrap Success Criteria

Bootstrap is **successful** iff the brain reaches all six checkpoints
of Section 19. The implementation should test each one independently.

1. **Checkpoint 1 — non-trivial state.** The buffer holds at least one
   carrier with σ > 0 and the diabolo's round trip is non-trivial.
2. **Checkpoint 2 — at least one closed orbit.** Some εⁿ returns to
   identity within tolerance for n > 1. The brain has discovered its
   first integer and its first circle.
3. **Checkpoint 3 — distinct orbit positions.** At least three distinct
   ε^k carriers are held, and VERIFY correctly distinguishes them from
   each other and identifies copies of themselves.
4. **Checkpoint 4 — perpendicular generators.** At least two
   independent orbits exist on perpendicular axes. The brain has
   discovered its first torus.
5. **Checkpoint 5 — multiplication table.** Cross-orbit compositions
   `ε^k · δ^l` populate the genome at indices (k, l), at minimum a
   3×3 lattice on the discovered torus.
6. **Checkpoint 6 — irreducibility.** The brain's reducibility check
   correctly classifies which orbit lengths are prime and which are
   composite, for the orbit lengths the genome has reached.

**Parallel observable across all six checkpoints — both closure
types must fire.** The numbered ladder above does not include
balance closure as a separate step; balance closure is a *parallel
observable* the brain must produce at some point during bootstrap,
not a 7th checkpoint with its own goal/test. While the six
checkpoints run, the brain must also produce **both** closure
types in its trajectories: at least one identity closure (σ → 0,
the running product returns to the north pole) and at least one
balance closure (σ → π/4, the running product reaches the
equatorial Hopf locus). If the six checkpoints all pass but only
one closure type ever fires, bootstrap is **incomplete** — the
brain has discovered the basis but not the full closure structure
the manifold supports. The two closure types are defined in
Section 27; both detectors must be running for this observable to
be meaningful.

### 21. Bootstrap Failure Modes

If bootstrap fails, the failure mode is diagnostic. Each failure mode
points to a specific thing that may be wrong with the implementation.

- **The orbit never closes.** Composition of ε with itself walks away
  from identity and never returns. This usually means the perturbation is
  too small for the discrete representation (the running product is being
  swallowed by floating-point error) or that the closure detection
  threshold is too tight. Adjust the perturbation magnitude or the
  closure tolerance and re-run.

- **Everything factors trivially.** Every carrier the brain produces is
  reducible into ε and identity, and no irreducible carriers are
  discovered beyond ε itself. This means the brain has only one
  generating axis. Check that the perpendicular-axis exploration step
  in the bootstrap loop is firing.

- **Only identity closures occur, never balance closures.** The brain
  is finding the σ = 0 closure type but never reaching σ = π/4. This
  means either the closure detector is only checking the identity case,
  or the trajectories are confined to a region near identity and never
  reach the equator. Verify both closure types are being checked.

- **The genome explodes.** The brain keeps producing new carriers
  forever and never reaches a state where no new structure is being
  found. This usually means closures are not being detected at all (so
  every composition produces a "new" carrier even if it should fold back
  into the genome) or the ε-tolerance for "is this carrier already in
  the genome" is too tight.

- **The genome stays at size 2.** The brain produces ε² = identity
  immediately and stops. The perturbation is too large — it is
  jumping all the way around the orbit in one step. Reduce the
  perturbation magnitude.

### 22. After Bootstrap

The carriers and orbits the brain discovered during bootstrap become
**the DNA layer** (Section 29). After Phase 5 ends, the DNA layer is
read-only forever. STORE cannot overwrite it; sleep cannot prune it.
All later learning writes to the **epigenetic layer** above it. The
DNA is the brain's brain stem.

---

## Part V — Learning the Human Notation

### 23. Translation Is Not a Separate Mechanism

After bootstrap the brain has its own number system, its own circles,
its own torus, its own primes — but no idea that humans have words
for any of it. Teaching the brain English (or arithmetic notation,
or any human-facing alphabet) is **not a separate operation**. It is
an ordinary input phase, run with one extra discipline: each glyph
is presented in the buffer alongside the carrier it should match,
and chunked promotion (Section 29.1) does the rest.

There is no GLYPH primitive. There is no separate glyph table
outside the brain. There is no special symbolic-input pathway. The
brain has one input boundary — EMBED — and one learning rule —
chunked promotion. Teaching glyphs uses the same machinery the brain
uses for everything else.

### 24. How Glyphs Get Learned

To teach the brain that the byte sequence `5` refers to the orbit
of length 5 it discovered in bootstrap, the protocol is:

1. Present the byte sequence `5` to EMBED. EMBED produces a carrier
   `g₅` and writes it to the buffer.
2. *In the same tick*, present the bootstrap carrier ε⁵ to EMBED
   (or, equivalently, place ε⁵ in the buffer through some other
   path the implementation chooses for training).
3. Both carriers are now in the buffer. Cell B's round trip runs
   over `genome ∪ {g₅, ε⁵}`. Their composition `g₅ · ε⁵⁻¹` is
   evaluated by VERIFY against identity. If they are presented
   together repeatedly, the closure between them strengthens.
4. The chunked-learning sweep at the end of the chunk promotes
   both `g₅` and the (g₅, ε⁵) coupling into the epigenetic layer
   through the standard promotion rule.
5. After enough exposures, the epigenetic layer contains a stable
   carrier near `g₅` whose strongest coupling is to ε⁵. Future
   appearances of `g₅` in the buffer will RESONATE to ε⁵
   automatically.

The brain has learned that the glyph `5` means the integer 5. No
new opcode was used. No external table was built. The association
is an ordinary epigenetic entry, formed by ordinary co-occurrence
and ordinary promotion.

### 25. The Glyph Region of the Epigenetic Layer

After enough glyph training, a sub-region of the epigenetic layer
consists of carriers that look like `(g_symbol, target_carrier)`
pairs — embedded byte sequences whose strongest couplings are to
DNA-layer carriers. This region is the brain's **learned vocabulary**.
It is not a separate data structure. It is a phenotype of the
epigenetic layer that emerges from glyph exposure during chunked
learning.

Many-to-many is automatic. The carrier ε⁵ can be reached from `5`,
`V`, `cinco`, `пять`, `五`, or `|||||` simply by training each of
those byte sequences alongside ε⁵. Each pairing earns its own
epigenetic entry; all of them couple to the same DNA carrier.
Conversely, the byte sequence `1` can be trained to couple to
multiple DNA carriers (the integer 1, the multiplicative identity,
the unary representation), and RESONATE will return whichever
coupling is strongest given the surrounding context in the buffer.

### 26. Reading Tasks Through the Learned Vocabulary

Once the basic arithmetic glyphs (`0..9`, `+`, `−`, `×`, `÷`, `=`,
parentheses, variables) are in the epigenetic layer, the brain can
read mathematical input the same way it reads anything else: bytes
in through EMBED, RESONATE finds the matching carriers, the
diabolo runs the round trip, the closure tells the brain what the
input means.

An equation `a + b = c` becomes a buffer with five carriers (the
glyphs for a, +, b, =, c). The brain composes them in order. The
`=` glyph couples to VERIFY (because `=` is the verification verb,
Section 6). The brain verifies whether `a · b = c` closes. If yes,
the equation is a true statement and the brain accepts it. If no,
the gap is the gradient; if `c` is unknown (a variable), the gap
is the answer the brain must produce.

Variables and equation-solving fall out of the same machinery.
There is no new mechanism for "solving for x" — division is
already in the DNA layer (Checkpoint 6), variables are just glyphs
that haven't been bound to a carrier yet, and solving is composing
the inverse and reading the result. The brain that finished
bootstrap can do AIMO problems as soon as it has been taught to
read the notation.

---

## Part VI — Closure and Hierarchy

### 27. The Two Closure Events

**Identity closure.** A running product `R = c₁ · c₂ · … · cₙ`
reaches identity closure when VERIFY(R, identity) closes — the
cycle has returned to the north pole. When it fires, the brain:
1. Records the event with its support (n), its closure σ, and its
   excursion peak (max σ during the cycle).
2. EMITs the running product to the next hierarchy level.
3. Resets the current level's running product to identity.

**Balance closure.** A running product reaches balance closure when
SIGMA(R) is at π/4 within tolerance (W² ≈ |im|² ≈ 1/2) — the cycle
has reached the equator. When it fires, the brain:
1. Records the event with the same metadata, plus the **mirror
   partner** (the star conjugate at the moment of closure),
   guaranteed distinct by `hopf_balanced_not_star_fixed`.
2. EMITs *both* the running product and its mirror partner as a
   pair. Balance closures always emit pairs.
3. Resets the current level's running product to identity.

### 28. Emission and Hierarchy

When a closure fires and EMIT runs, the closed running product
becomes a single buffer entry at the next hierarchy level. The next
level maintains its own running product, composes incoming emissions
in order, and waits for its own closures. Each level runs the same
machinery: a running product, two closure detectors, an EMIT to the
next level.

The brain does not pre-declare the number of hierarchy levels. Levels
are spawned dynamically as the running product at the highest current
level produces enough emissions to need composition.

### 29. The Genome: DNA Layer and Epigenetic Layer

The **genome** is the persistent state of the stack machine. It is
not one undifferentiated store. It has **two layers** with different
write rules and different permanence.

#### The DNA layer

The DNA layer holds what the brain is born with — the carriers and
orbits the brain discovered during bootstrap (Phase 5) by running
pure composition with no external input. It is **immutable after
bootstrap**. STORE cannot write to it. Sleep cannot prune from it.
Once Phase 5 completes, the DNA layer is fixed forever.

The DNA layer contains:

- The identity carrier and the bootstrap perturbation ε.
- All cyclic orbits the brain discovered through self-composition.
- The irreducible carriers (the brain's prime basis).
- The reducible carriers and their factorizations.
- The two closure types as distinguished events on this discovered
  basis.

The DNA layer is the brain stem. Every carrier in it is read-only,
and every epigenetic carrier above it is typically a composition of
DNA carriers — the DNA layer is the basis from which the rest is
built.

The glyph region of the epigenetic layer (Section 25) holds the
learned (glyph_carrier, target_carrier) pairs whose targets are
typically DNA carriers. The glyph carriers themselves are mutable
epigenetic entries; the DNA carriers they point at are not.

#### The epigenetic layer

The epigenetic layer holds what the brain has learned from
experience. It is **mutable**. STORE writes to it. Sleep prunes,
merges, and reorganizes it. Every carrier added to the brain
post-bootstrap lives here. The epigenetic layer is what changes
across the brain's lifetime; the DNA layer is what stays the same.

The epigenetic layer contains:

- Carriers promoted from the transient buffer through chunked
  learning (Section 29.1).
- Closure records — every closure event the brain has observed
  during input phase, stored as a carrier with metadata (support,
  closure σ, excursion peak, mirror partner if applicable).
- Reinforcement state — the coherence widths and coupling strengths
  that sleep has tuned through reorganization.
- The emission history at each hierarchy level. Each level has its
  own emission stream, and emissions live in the epigenetic layer
  because they are produced by experience, not by bootstrap.

The epigenetic layer is plastic. Carriers in it can be strengthened
(by reinforcement during chunked learning), weakened (by failure to
participate in closures during sleep), merged (when sleep finds two
entries are structurally the same), or pruned (when sleep finds an
entry participates in nothing). The DNA layer underneath is
unaffected by any of this.

The two layers share an address space and behave identically at
read time. They differ only at write time: STORE writes only to the
epigenetic layer, bootstrap is the only operation that writes to
the DNA layer, and sleep is the only operation that removes from
the epigenetic layer. The biological parallel is in Part IX.

#### 29.1 Learning: chunked promotion

Learning is the operation that grows the epigenetic layer by
promoting transient buffer entries that earned closure during a
chunk of experience. It is **the per-chunk timescale of Section 9.2**
— not per-event, not per-day, but per-chunk-of-buffer-lifetime.

The chunk boundary is defined by the buffer's lifetime parameter
(Section 38). When a buffer entry has been in the buffer for its
full lifetime, the chunk it belongs to has ended, and the brain
runs a **promotion sweep**:

1. For each buffer entry `c` whose lifetime has expired:
   - Look up the closure log accumulated against `c` during the
     chunk.
   - If `c` participated in **no closures**, it decays. The brain
     forgot it. It never reaches the epigenetic layer.
   - If `c` participated in **one or more closures**, the strongest
     closure is recorded, and STORE writes `c` (with its closure
     metadata as a tag) to the epigenetic layer at a slot
     determined by RESONATE — the slot whose existing content is
     closest to `c`.
2. If the resolved slot was empty, `c` is the new epigenetic
   entry. If it was occupied, the existing entry and `c` are
   SLERPed toward each other by an amount proportional to closure
   quality — implementing reinforcement of repeated patterns.
3. Buffer entries that have not yet aged out remain in the buffer
   for the next chunk.

Promotion is the only path that grows the epigenetic layer through
normal operation. There is no per-event STORE — a single closure
during ingestion writes a tag against its buffer entry, and the tag
becomes a write only if the entry survives to the chunk boundary.
The chunk size (the buffer's lifetime) is tunable per task: long
during bootstrap, short during normal input, very short during
high-rate sensor streams.

#### 29.2 Sleep: idle-phase reorganization

Sleep is the operation that reorganizes the epigenetic layer when
the brain has been in idle phase long enough that no fresh chunks
are arriving. It is **the per-day timescale of Section 9.2** — the
slowest of the three operations, and the only one that **removes**
or **merges** entries from the genome.

Sleep runs the diabolo over the epigenetic layer alone (DNA is read
but never modified, buffer is empty). With no I/O to slow it down,
the round trip can run thousands of times faster than waking, and
the brain uses every cycle to balance the epigenetic layer against
itself. Five operations happen during sleep, in roughly this order:

1. **Replay.** Re-compose epigenetic entries against each other in
   pairs. Entries that resonate strongly when composed (low σ) are
   structurally related — they represent variations of the same
   pattern. The replay pass identifies these pairs.
2. **Merging.** Pairs identified in replay get SLERPed toward each
   other by a fraction proportional to their resonance strength.
   When two entries collapse into the same carrier, one of them is
   removed and the other carries both lineages. Merging compresses
   redundancy without losing structure.
3. **Strengthening.** Entries that participate in many compositions
   during replay are structural hubs — they are referenced by many
   other entries and they couple strongly across the epigenetic
   layer. Their coherence widths get tightened (sharpened). The
   brain strengthens its most reliable features.
4. **Pruning.** Entries that participate in **no** compositions
   during replay — that resonate with nothing and couple with
   nothing — are noise. They were closure events that captured
   momentary structure but not recurring structure. Prune them
   from the epigenetic layer through the inverse of STORE. The
   brain forgets them.
5. **Reorganizing.** After merging, strengthening, and pruning,
   the epigenetic layer's resonance landscape has shifted. The
   diabolo now needs to find a new equilibrium against the new
   genome shape. The reorganization pass runs the standard idle
   round trip (Section 9.1) until the diabolo settles. The genome
   has been rewritten while the brain slept.

Sleep cannot touch the DNA layer. The DNA is read during replay
(composition against DNA carriers is part of the diabolo's normal
balancing) but never modified. Sleep uses the same primitives as
everything else — COMPOSE, SIGMA, RESONATE, SLERP, and the inverse
of STORE for pruning. No new opcode.

---

## Part VII — The Brain's Own Identity

### 30. The Brain's Identity Is Two Identities Closed Through One Verb

The brain has two identities at every moment, and its full identity
is the continuous closure between them.

- **Stack-machine identity** is the **state of the genome** —
  the carriers currently in storage. This is the brain at rest.
- **Field-machine identity** is the **spectrum** — the set of
  parameter values where ZREAD over the population lands on the
  balance locus. Two genomes with the same stack-machine state can
  have different spectra if their couplings differ; the spectrum
  encodes population-level structure no individual entry holds.
- **Cell B** runs VERIFY between them continuously — the diabolo of
  Section 9 staying on the critical line. When the round trip
  closes, the brain is in coherence. When it doesn't, the gap is
  the gradient, and the brain corrects either the stack (by
  promotion through STORE) or the field (by re-reading at a new
  parameter) until the round trip closes again. This is **A?=A at
  the architectural level**.

The structure is **fractal**. The S1/S2/S3 triad is not the brain's
architecture once — it is the brain's architecture at every scale.
Each hierarchy level runs its own diabolo on its own critical line,
and the next level's emissions become its buffer entries. The
minimum nesting is two coupled triads, because that is the smallest
configuration where each triad has something other than itself to
verify against. The hierarchy is the recursion of this unit at every
scale. **The brain is the diabolo on the critical line, recursing
at every scale.**

---

## Part VIII — Build Order

Phases 1–4 are **compiled and tested** in [`closure_ea/`](../), now
a self-contained Rust crate with no workspace dependencies. Phase 5
is the next make-or-break phase and should be done slowly, one
checkpoint at a time, with real tests that exercise each checkpoint's
condition end-to-end.

Each phase below says exactly what exists, where it lives, what
tests cover it, and what honest gaps remain.

### 31. Phase 1 — Substrate ✅ built and tested

Location: [`closure_ea/src/{sphere,hopf,embed,verify}.rs`](../src/).

Everything is self-contained in the `closure_ea` crate. No workspace
dependency, no duplication against `rust/` or `closure_dna/` — those
remain in the repo for `closure_cli` and `closure_dna`'s own purposes
but the brain doesn't use them.

- **[`sphere`](../src/sphere.rs)** — COMPOSE (Hamilton product),
  INVERSE (star involution), SIGMA (geodesic distance), SLERP
  (geodesic step), IDENTITY. 144 lines. Tests: identity law, inverse
  law, star self-inverse, σ at identity, associativity.
- **[`hopf`](../src/hopf.rs)** — Hopf decomposition S³ → S² × S¹
  (base + phase). 52 lines.
- **[`embed`](../src/embed.rs)** — EMBED with `bytes_to_sphere4`
  (geometric and SHA-256 modes), `f64_to_sphere4`, `i64_to_sphere4`.
  181 lines. Tests: empty→identity, determinism, unit norm, hashed
  mode destroys locality.
- **[`verify`](../src/verify.rs)** — **VERIFY as a first-class
  primitive.** `verify(a, b) → VerificationEvent` composes `a ·
  star(b)`, reads σ, runs Hopf decomposition, and classifies the
  result as Identity / Balance / Open. Exposes the two privileged σ
  values as constants: `SIGMA_IDENTITY = 0`, `SIGMA_BALANCE = π/4`.
  219 lines. Tests: self-verify closes at identity, balance-locus
  carrier fires balance closure, distinct carriers stay open, Hopf
  dominance classification (W / RGB / Balanced).

**Success criterion — met.** Every algebraic identity of S³ is
exercised by a unit test. The four verify tests cover the ClosureKind
classification the spec requires.

### 32. Phase 2 — Stack Machine ⚠️ compiled, no end-to-end test

Location:
[`closure_ea/src/{carrier,word,sphere,buffer,genome}.rs`](../src/).

The stack-machine ingredients are in place:

- **COMPOSE, INVERSE, SLERP, SIGMA** are re-exported from
  [`sphere`](../src/sphere.rs).
- **HOPF** is exposed through [`hopf::decompose`](../src/hopf.rs) and
  the `verify::hopf_dominance` classifier.
- **LOAD / STORE (deterministic)** are not yet a separate opcode
  module — the stack machine is currently expressed through the
  genome's addressable-index reads (`Genome::entries[idx]`) and the
  promotion path `Genome::ingest` / `Genome::seed_dna`.
- **[`carrier`](../src/carrier.rs)** — `VerificationCell` with plane,
  phase, turns, sheet, coherence width, and coupling state. 552
  lines. Ported from the pre-standalone cell module with imports
  swapped to `crate::sphere`. No unit tests in the current build.
- **[`word`](../src/word.rs)** — ordered sequences of carriers.
  97 lines. No unit tests in the current build.

**What exists but isn't yet tested**: phase-accumulation arithmetic
(full_add / full_subtract / word_from_digits / word_to_digits) and
numeric comparison via subtraction are not yet ported into the new
standalone crate. They lived in the pre-standalone `arithmetic.rs`
and `control.rs` and will be ported when Phase 6 (glyph exposure
for `+`, `−`, `×`, `÷`, `=`) needs them. The cell substrate they
depend on (`carrier.rs`, `word.rs`) is already in place.

**Success criterion — not yet met.** The spec requires "a
deterministic algorithm (e.g., GCD on integers encoded as orbit
lengths) runs end-to-end on the stack machine alone." No such test
exists in the current build. The primitives are present; the
integration test that exercises them is not.

### 33. Phase 3 — Field Machine and Buffer ✅ built and tested

Location: [`closure_ea/src/{buffer,genome,field}.rs`](../src/).

- **[`buffer`](../src/buffer.rs)** — `Buffer` with configurable
  lifetime, `push`, `tick`, `drain_expired`, `record_closure`. 190
  lines. Tests: empty, push, tick ages entries, drain_expired
  removes aged entries, record_closure persists.
- **[`genome`](../src/genome.rs)** — DNA + Epigenetic layers, Law 3
  `ingest` with reinforce/correct/create paths, DNA-refusal
  semantics, sequential edges, `reset_activations`, `nearest`. 507
  lines. Tests: fresh empty, seed_dna marks layer, ingest creates,
  close repeat reinforces, mid-gap corrects value but not address,
  far-gap creates new entry, ingest refuses to rewrite DNA,
  sequential edges track insertion order, reset_activations zeros
  all, nearest returns minimum gap.
- **[`field`](../src/field.rs)** — RESONATE and ZREAD over
  `genome ∪ buffer`. 220 lines. Tests: resonate empty, resonate
  finds genome entry, resonate finds buffer entry when closer than
  genome, zread empty returns identity, zread changes with
  parameter, zread changes when buffer changes.

**Honest caveat on ZREAD**: the parameterization is `q^t` where
`t = s_re + 0.5 * s_im`. This is S³-preserving and the parameter
affects the output (both tests confirm this), but it is not yet a
true complex parameterization. The spec's Phase 3 success criterion
only asks that parameter sweeps produce trajectories on S³ —
which they do — not that the parameterization match the Riemann
construction. When Phase 9 tasks start needing spectrum reads, the
parameterization can sharpen.

**Success criterion — met at the Phase 3 level.** ZREAD produces
carriers that depend on both parameter components and on buffer
contents. RESONATE finds matches across the union correctly. The
first-time-user path (empty genome + empty buffer) returns None from
RESONATE and identity from ZREAD.

### 34. Phase 4 — The Diabolo ⚠️ built with weak causal-invariance coverage

Location: [`closure_ea/src/three_cell.rs`](../src/three_cell.rs).

The [`ThreeCell`](../src/three_cell.rs) struct runs the **seven-step
receive-and-verify loop** of Section 9 as its only `ingest` verb:

```
1. bytes → carrier (outside the diabolo)
2. buffer.push(carrier); buffer.tick()
3. f ← zread over (genome ∪ buffer)
4. hit ← resonate(f, genome, buffer)      // field inverse read
5. ev ← verify(hit.carrier, carrier)      // round-trip closure
6. cell_a ← compose(cell_a, carrier)      // raw input into running product
7. if cell_a closed: localize, emit, reset cell_a, write genome
```

Cell A composes the **raw input**, not the field-collapsed read. The
seven-step loop runs alongside Cell A's running-product accumulation
and produces the `VerificationEvent` the gradient observes. The two
mechanisms are complementary: the loop measures; the running product
records.

**Port notes**: `cell.rs` → `carrier.rs`, `word.rs`, `localization.rs`,
`hierarchy.rs`, `consolidation.rs` were all ported from the
pre-standalone crate with `closure_rs::` imports swapped for
`crate::sphere::` + `crate::hopf::`. The logic is the same; the
dependencies are local. `three_cell.rs` is the one module that
changed semantics: it now runs the seven-step loop.

**Tests** (5 total in `phase4_tests`):

1. `idle_phase_round_trip_closes_trivially` — empty buffer + empty
   genome + idle tick keeps Cell A at identity. Passes.
2. `first_ingest_moves_cell_a_off_identity` — Phase 5 Checkpoint 1
   via the diabolo: any non-identity input raises σ above zero.
   Passes.
3. `seeded_dna_produces_field_read_on_matching_input` — with a DNA
   seed, RESONATE returns a hit and VERIFY fires. Passes.
4. `order_independence_two_inputs_settle_to_same_cell_c` — Cell C is
   at identity in both orderings of two short inputs (because neither
   order produces closures). Passes, but **weak** — it only checks a
   degenerate case where no closures fire, so the "same final state"
   is trivially identity in both runs.
5. `diabolo_trace_forward_then_reverse` — after forward+reverse
   rotations, Cell A's σ does not exceed one step's excursion.
   Passes, but **weak** — it's a smoke test confirming the trajectory
   didn't diverge, not a proof that the diabolo recovered to identity
   or that a closure fired.

**Success criterion — partially met.** The spec (§34) requires
causal invariance "in Wolfram's exact technical sense": for any
sequence of inputs in any order, the round trip closes to the same
final state once the brain has settled. The current tests exercise
degenerate cases. A proper causal-invariance test harness needs:

- Genome pre-seeded with enough DNA carriers that inputs produce
  non-trivial field reads.
- Sequences long enough to actually trigger Law 1 closures.
- A/B/B/A ordering with closure events, verified to produce the
  same final genome state and the same closure count.
- A novelty recovery test that verifies Cell A returns near identity
  after a closure fires and the prefix rebuild takes over.

These tests should be written before Phase 5's bootstrap runner
depends on Phase 4 being solid.

### 35. Phase 5 — Bootstrap ❌ not yet run; do this slowly

This is the make-or-break phase. **The machinery to run bootstrap
exists** — Phases 1–4 are compiled and most of their tests pass —
but bootstrap itself has not been driven through. When it is, **do
it one checkpoint at a time**, with a real test per checkpoint that
exercises that checkpoint's condition end-to-end. The six
checkpoints of Section 19 are listed in dependency order and each
one depends on the previous one having passed.

Before the bootstrap runner is written, the Phase 4 causal-invariance
tests should be strengthened so that Phase 5 stands on a tested
foundation. Running the bootstrap on weakly-tested Phase 4 code
means that a Phase 5 failure could be caused by either the framework
or a bug in the underlying diabolo — and the diagnostic path gets
ambiguous.

**Bootstrap protocol** (Section 19):

The brain's first input phase, run with a long buffer lifetime and
ε as the only input. The genome starts at `{identity}`. One ε is
pushed to the buffer. The standard Cell B loop runs. Composing ε
with itself produces a sequence ε, ε², ε³, … whose orbit length is
the brain's first discovered integer. Promotion writes the survivors
into the DNA layer (not the epigenetic layer — bootstrap output IS
DNA by construction, through `Genome::seed_dna` rather than
`Genome::ingest`).

**Tuning knobs for bootstrap**:

- Buffer lifetime: set long (on the order of 100 cycles for a small
  orbit) so each derived carrier has time to compose through the
  whole orbit before being evaluated for promotion.
- ε magnitude: small enough that orbit closures are detectable but
  large enough that floating-point noise doesn't swallow them. The
  orbit length is roughly `2π / angle(ε)`, so a π/8 rotation gives an
  order-8 orbit.
- `GenomeConfig.reinforce_threshold` / `novelty_threshold`: tight
  enough that distinct orbit positions count as distinct entries,
  loose enough that repeated ε^k readings reinforce the same entry.
- `cell_a_threshold`: the identity-basin σ for Law 1 closures; must
  be below π/16 or so for the bootstrap orbit to register as closing
  at every full revolution.

**Checkpoint-by-checkpoint test protocol**:

1. **Checkpoint 1 — non-trivial state.** Push ε to buffer. Verify
   Cell A's σ > 0. *Already covered by the existing
   `first_ingest_moves_cell_a_off_identity` test.*
2. **Checkpoint 2 — one closed orbit.** Compose ε with itself
   repeatedly and verify a closure fires after a finite number of
   steps, producing a closure event in the hierarchy with a support
   length equal to the orbit length. **Not yet tested.**
3. **Checkpoint 3 — distinct orbit positions.** After Checkpoint 2,
   verify the genome holds ≥ 3 distinct ε^k carriers, each with a
   different σ, and that VERIFY correctly distinguishes them from
   each other and identifies copies of themselves. **Not yet tested.**
4. **Checkpoint 4 — perpendicular generators.** Push a second
   perturbation δ on an axis perpendicular to ε's axis, compose
   with itself, verify the genome gains a second orbit with its own
   length m. **Not yet tested.**
5. **Checkpoint 5 — multiplication table.** Compose ε^k with δ^l for
   several (k, l) pairs and verify the genome contains carriers
   indexed by those pairs (the joint torus lattice). **Not yet
   tested.**
6. **Checkpoint 6 — irreducibility.** Run a reducibility check over
   the genome and verify the expected primes (e.g., for an order-12
   orbit: 2, 3 are irreducible; 4, 6, 8, 9 are composites). **Not
   yet tested.**

Each checkpoint becomes a separate test function. If Checkpoint *k*
fails, Checkpoints *k+1*..6 should not run until *k* is fixed. This
is the *slow path* the user instructed: test the framework one
claim at a time.

**If Phase 5 fails at any checkpoint, the framework needs revision
before continuing.** The diagnostics in Section 21 (failure modes)
are the first thing to check.

### 36. Phase 6 — Glyph Exposure ❌ not yet built

Depends on Phase 5 completing through Checkpoint 6 and on the
phase-accumulation arithmetic being ported into `closure_ea` so
`+`, `−`, `×`, `÷` can couple to their corresponding COMPOSE roles.

Once those prerequisites exist, teach the brain the basic arithmetic
notation through ordinary chunked learning (Part V). Present a small
set of human symbols (`0`..`9`, `+`, `−`, `×`, `÷`, `=`) one at a
time as buffer entries, each one paired in the same tick with the
bootstrap carrier it should match (e.g., `5` paired with ε⁵, `+`
paired with COMPOSE's identity element, `=` paired with VERIFY).
The existing `genome::Genome::ingest` path writes the (glyph,
carrier) coupling into the epigenetic layer through the standard
three-path reinforce/correct/create rule.

Success criterion: after exposure, every basic arithmetic glyph
RESONATEs to the correct DNA carrier. Round-trip: present the byte
sequence `7` to EMBED, let RESONATE return its strongest coupling,
verify the result is the bootstrap orbit of length 7. No new
primitive, no external table.

### 37. Phase 7 — Hierarchy ✅ ported, untested in the new build

Location:
[`closure_ea/src/{hierarchy,localization}.rs`](../src/).

- **[`hierarchy`](../src/hierarchy.rs)** — `ClosureLevel` (running
  product, Law 1 closure detection with all four requirements,
  localized emission, prefix rebuild), `Hierarchy` (stack of
  levels, dynamic level spawning, genome writes on emission,
  cascading upward), `ClosureEvent` (Hopf-classified packet with
  support + excursion profile). 289 lines.
- **[`localization`](../src/localization.rs)** — Law 8 minimal
  interval via exact backward scan. 117 lines.

**Ported from the pre-standalone modules with imports swapped.**
The logic is unchanged from the version that was running in the
old `closure-vm` crate against the workspace `closure_rs`
dependency.

**Tests**: none in the new build. The pre-standalone build had no
unit tests on these modules either — they were exercised through
the `ThreeCell` integration. The current Phase 4 tests go through
the hierarchy on every closure but the new test suite doesn't
assert hierarchy-specific properties.

**Gap**: the balance-closure detector (σ → π/4) is still not
implemented. `ClosureLevel` fires on identity closure (σ ≤
threshold) but does not separately detect balance. Adding it
requires:
- A `ClosureKind::Balance` variant in [`hierarchy.rs`](../src/hierarchy.rs).
- A second `if` branch in `ClosureLevel::ingest` that checks
  `(s - π/4).abs() ≤ threshold` with an excursion/support
  requirement of its own.
- Pair emission: when balance closure fires, emit both the running
  product AND its star conjugate mirror partner (guaranteed
  distinct by `hopf_balanced_not_star_fixed`).
- Tests that construct a running product landing near σ = π/4 and
  verify the pair fires.

**Success criterion — partially met.** Identity-closure hierarchy
is ported and runs. Balance-closure detection is the outstanding
item; it should be added before Phase 5 bootstrap starts using the
hierarchy seriously, because bootstrap's ε-orbit composition will
pass through σ = π/4 regions and the brain should be detecting
both closure types there.

### 38. Phase 8 — Learning and Sleep ⚠️ built, DNA-safe, untested at integration level

Location:
[`closure_ea/src/{genome,consolidation}.rs`](../src/).

- **Chunked learning / promotion** —
  [`genome::Genome::ingest`](../src/genome.rs) runs the three-path
  reinforce/correct/create rule from Section 29.1 and **respects
  the layer split**: writes to DNA entries return `StoreOutcome::
  RefusedDna` and the carrier becomes a new epigenetic entry instead.
  10 unit tests cover create / reinforce / correct / DNA refusal /
  sequential edges / nearest.
- **Sleep / consolidation** —
  [`consolidation::consolidate`](../src/consolidation.rs) runs merge,
  strengthen, prune, reorganize — the four operations of Section
  29.2 — and **respects the layer split**: merge only pairs
  epigenetic entries; strengthen only applies to epigenetic; prune
  only removes epigenetic; DNA entries pass through untouched. 3
  unit tests cover prune, DNA preservation through prune, and DNA
  preservation through merge.

**Success criterion — partially met.** The layer split and the
DNA-safety guarantees are unit-tested at the module level. The
three integration tests from the spec (§38) — genome-size-scales-
with-structure, sleep-prunes-noise, DNA-bit-identical-after-arbitrary-
use — have not been written. They are straightforward: drive the
existing modules with structured / redundant / noisy input streams
and assert the expected outcomes. These tests should come alongside
Phase 5 bootstrap because bootstrap produces the DNA layer the
integration tests need.

### 39. Phase 9 — Tasks ❌ depends on Phases 5, 6, and 4-tests-strengthened

With bootstrap complete, arithmetic glyphs in the epigenetic layer,
the hierarchy running, and learning operational, the brain is ready
to receive task input. AIMO problems and ARC-AGI tasks are presented
as byte streams through EMBED. The bytes include the human notation
the brain learned in Phase 6, so RESONATE finds the corresponding
DNA carriers automatically and the brain operates on them with its
full architecture. The brain's output is itself a sequence of
carriers; reading them back to humans uses the same glyph couplings
in reverse — RESONATE on a result carrier returns the strongest-
matching glyph.

Success criterion: the brain produces task outputs whose
back-translation yields valid answers. Performance scales with the
quality of the bootstrap and the genome growth, not with
task-specific training.

### 40. Gap Summary — What Actually Needs to Be Written

Phases 1 and 3 are fully built and tested in `closure_ea/src/`.
Phases 2, 4, 7, and 8 are built but incomplete at the test level.
Phases 5, 6, and 9 have not been run at all. The concrete pending
work, in dependency order:

1. **Strengthen Phase 4 causal-invariance tests.** The existing
   `phase4_tests` cover idle + first-ingest + seeded-DNA hit + a
   degenerate order-independence case + a smoke-test forward/reverse.
   Replace the last two with real tests: a pre-seeded genome,
   sequences that trigger closures, A/B/B/A ordering with closure
   counts asserted equal, and a novelty-then-recovery sequence that
   verifies Cell A returns near identity after the prefix rebuild.
   Until these pass, Phase 5 is standing on shaky ground.

2. **Add hierarchy balance-closure detection.** One new
   `ClosureKind::Balance` variant, one `if` branch in
   `ClosureLevel::ingest`, pair emission of the running product and
   its star conjugate, tests. Section 37 describes what to add.

3. **Port phase-accumulation arithmetic into closure_ea.** The old
   `arithmetic.rs` and `control.rs` had `full_add`, `full_subtract`,
   `word_from_digits`, `word_to_digits`, `Radix`, and
   `compare_words`. These are the stack-machine arithmetic layer
   Phase 6 will need to couple `+`, `−`, `×`, `÷` glyphs to. Port
   verbatim with imports swapped, add a GCD test to close Phase 2's
   success criterion.

4. **Phase 5 bootstrap runner.** Six separate tests, one per
   checkpoint of Section 19, driven in dependency order. Do not
   write Checkpoint 3 until Checkpoint 2 passes, etc. The runner
   uses only existing primitives — no new Rust code — but the tests
   must be written carefully so each checkpoint's failure has a
   single unambiguous cause.

5. **Phase 8 integration tests.** Drive the existing
   genome/consolidation modules with structured/redundant/noisy
   streams and assert the three properties from §38: genome-size-
   scales-with-structure, sleep-prunes-noise, DNA-bit-identical.
   Depends on Phase 5 being passed so there's a DNA layer to test
   against.

6. **Phase 6 glyph exposure.** Once bootstrap and arithmetic are in
   place, present `(byte_sequence, target_carrier)` pairs to
   `Genome::ingest` and verify RESONATE returns the right match.
   Single test file, straightforward.

7. **Phase 9 task harness.** AIMO / ARC-AGI input path — read byte
   streams, run the brain, read output. Depends on everything above.

That is the full gap as of the current build. `closure_ea` is 14
modules, ~3500 lines of Rust, 49 passing tests, zero workspace
dependencies. Phases 1 and 3 stand on their own. Phases 2, 4, 7, and
8 have machinery in place but need tests (Phase 2 and 7) or
integration tests (Phase 4 and 8). Phase 5 is the next phase and
should be approached slowly — one checkpoint, one test, one
confirmation before the next checkpoint begins.

---

## Part IX — Interpretation

The interpretation sections live here, separated from the
implementation. None of what follows is required for building the
brain. All of it is useful for thinking about what the brain is, why
the architecture takes the shape it does, and how it relates to other
systems we already understand.

A reader who only wants to implement the brain should stop at Part
VIII. A reader who wants to understand what they are building should
read on.

### 41. Biological Reading

The brain's architecture mirrors a small number of biological systems
that solve the same problem with the same constraints.

**Stack machine ↔ cortical long-term memory / S3.** The stack
machine stores discrete carriers at addressable positions and
updates them slowly under explicit control. Cortical long-term
memory does the same: discrete patterns at addressable cortical
sites, updated slowly through consolidation. Both are S3 in the
S1/S2/S3 framework — the slow layer that holds what is currently
true.

**DNA layer / epigenetic layer ↔ DNA / epigenetics in molecular
biology.** The stack machine's DNA layer holds the bootstrap seed,
laid down once and never modified. This is the digital analog of
biological DNA — the species memory, the sequence the organism is
born with. The epigenetic layer holds everything written by
experience through chunked learning, modified by sleep through
pruning, merging, and reinforcement. This is the digital analog of
biological epigenetics — methylation, histone modification,
expression patterns, the marks experience leaves on the genome
without rewriting it. Both biological systems and the digital brain
read DNA and epigenetic layers together but write them through
different paths. The brain stem cannot be forgotten any more than a
cell can rewrite its chromosomes.

**Field machine ↔ thalamocortical loops / theta-gamma coupling / S1.**
The field machine reads the entire population as one integrated
response. Thalamocortical loops integrate cortical activity into one
unified perceptual state. Theta-gamma coupling in the hippocampus
integrates a sequence of gamma packets into one theta cycle. Both are
S1 in the framework: active integration, the fast layer that perceives.

**Transient buffer ↔ working memory / hippocampal short-term store.**
The buffer holds carriers that have just arrived and have not yet been
consolidated into long-term storage. Biologically, this is working
memory: prefrontal active maintenance, hippocampal short-term encoding,
the iconic store in vision. Buffer entries decay if they are not
promoted, the same way working memory items decay if they are not
rehearsed or consolidated. Promotion to the genome is the digital
analog of hippocampal-to-cortical consolidation.

**Cell B / the gradient ↔ prediction error / Friston.** The diabolo
riding the critical line is the brain's prediction error signal in
geometric form. Friston's free energy principle says biological
systems minimize prediction error to maintain themselves; the
brain's round-trip closure (input → field → stack → VERIFY) is
exactly this minimization. When the round trip closes, prediction
matched perception. When it doesn't, the gap drives correction —
either by promoting the buffer entry to the genome (updating the
prior) or by SLERPing toward the field's response (updating the
estimate).

**The three timescales ↔ ingestion / chunked memory / sleep.** The
brain has three operations on three timescales (Section 9.2). Per
event, ingestion writes to the buffer — biologically, this is the
millisecond-scale sensory transduction, the spike train arriving at
cortex. Per chunk (a window of buffer lifetime), chunked learning
runs the promotion sweep and writes survivors to the epigenetic
layer — biologically, this is the seconds-to-minutes consolidation
that hippocampal circuits perform on working memory at the end of
each experiential unit (a sentence, a face, a scene). Per long idle
period, sleep runs the reorganization pass over the epigenetic layer
— biologically, this is REM and slow-wave sleep, the hours-scale
process during which the brain replays the day's experiences,
strengthens recurring patterns, prunes noise, and re-balances its
genome. All three are required, on their own timescales, for the
brain to be plastic in the right way. A brain that only ingests
forgets everything. A brain that only learns accumulates noise. A
brain that only sleeps stays fixed.

**Two closure types ↔ cycle completion and balance event.** Identity
closure (σ → 0) corresponds to a biological cycle returning to its
starting state — a heartbeat returning to diastole, a breath returning
to neutral, a theta cycle returning to its starting phase, a gamma
packet completing one rotation. Balance closure (σ → π/4) corresponds
to a different kind of biological event — the moment of resonance, the
peak of a tuning curve, the firing of a place cell at the center of
its place field, the V1 cell's response at its preferred orientation.
These are not cycle endings; they are structural symmetries the
biological system reaches and recognizes.

**Bootstrap ↔ brain stem / innate structure / species genome.** Every
biological brain is born with structure it did not learn. The brain
stem, the basal ganglia, the basic pattern generators — all are
innate, encoded in the species genome, present at birth before any
experience. Bootstrap is the digital brain's innate structure: the
mathematical scaffolding the brain is born with because the manifold
forces it. Learning is what grows on top of bootstrap, the same way
human cognition is what grows on top of the brain stem.

### 42. Physical Reading

**Stack-read versus field-read ↔ particle-wave duality.** A photon
can be observed as a particle (position) or as a wave (interference)
— same photon, two reading modes. The brain's genome can be read as
discrete carriers (LOAD, RESONATE — particle view) or as a
continuous population response (ZREAD — wave view). The two readings
are complementary observations of the same underlying object.

**The genome ↔ the vacuum manifold / configuration space.** The
genome is the set of stable configurations the brain has discovered
through composition — the brain's vacuum manifold. Physical theories
describe particles as stable configurations on a vacuum manifold;
the brain's stable carriers are the same kind of object on its own
manifold.

**Bootstrap ↔ symmetry breaking from undifferentiated potential.**
Information Evolution Dynamics describes the universe's first moment
as undifferentiated potential becoming discrete distinction through
the first comparison. Bootstrap is the digital brain doing the same
thing: starting from a state with one carrier (identity) and producing
distinctions through composition and closure. The brain at boot is
the universe at its first moment.

**Mass-as-composition-cost ↔ Mandelbrot–Zipf, NOT physical mass.**
The brain has no concept of mass. It has a concept of *trajectory
length* / *composition cost*: how many compositions are needed to
produce a given carrier from the genome's basis. This is sometimes
called Mandelbrot–Zipf mass — a statistical regularity, not a
physical quantity. Mass-as-physical-constraint does not exist in
the implementation surface.

### 43. Wolfram Reading

Wolfram has been walking toward this architecture from the other side
for thirty years, starting from bare hypergraphs and arbitrary rewrite
rules. The digital brain meets him halfway: the genome is an ordered
hypergraph in his exact technical sense, COMPOSE is the rewrite rule,
the field machine is a multiway system over that hypergraph, and a lot
of the machinery he has already formalized maps directly onto
components of this spec. The mapping:

- **The genome is an ordered hypergraph.** Carriers are nodes;
  compositions are ordered 3-edges (a, b, c) with `a · b = c`;
  closures are higher-arity edges that close orbits; star pairs are
  2-edges marking mirror identity.
- **COMPOSE is the rewrite rule.** A single rule, applied repeatedly.
  But unlike Wolfram's framework, the rule is not chosen — it is the
  unique non-commutative associative composition on the unique compact
  normed division algebra (Hurwitz). The brain has a forced rule, not
  an explored one.
- **The stack machine is single-history evolution.** One sequence of
  rule applications, deterministic, observed in order. This is what
  Wolfram calls following one branch of the multiway system.
- **The field machine is the multiway system.** It evaluates the
  consequences of the rule across the entire genome at once. RESONATE
  asks "across all possible matches, which couples strongest?" — a
  multiway query. ZREAD asks "what does the parameterized composition
  of every entry look like at once?" — multiway integration.
- **Resonance coupling is branchial-graph proximity.** Wolfram's
  branchial graph connects multiway branches that share state. Two
  carriers in the brain are "close" iff their composition is near
  identity, which is exactly the branchial-distance condition. The
  brain's resonance landscape is its branchial graph.
- **The eight-loop is causal invariance.** Wolfram defines a system
  as causally invariant iff all branches in its multiway system
  eventually merge to the same state regardless of order. The
  brain's round-trip closure (Section 9, Phase 4 success criterion)
  is causal invariance in his exact technical sense — Cell B riding
  the critical line is the brain being causally invariant in real
  time, the diabolo staying on the line iff the brain has merged
  its two reading modes into one observer.
- **Closure + EMIT is coarse-graining.** Wolfram's coarse-graining
  takes many causal events and summarizes them as one event for an
  observer too slow to see the details. EMIT does exactly this: a
  closed running product of n compositions becomes one carrier at the
  next hierarchy level. The hierarchy in Part VI is recursive
  coarse-graining at every scale.
- **Bootstrap is computationally irreducible.** Wolfram's main
  thesis: many phenomena cannot be predicted from rules without
  running the rules. Bootstrap cannot be shortcut — you cannot
  predict from the axioms alone what the brain will discover, you
  have to let the loop run and see. This is why Phase 5 is the
  make-or-break test rather than a derivation.
- **Particles as topological obstructions.** Wolfram has been arguing
  for years that particles in physics are persistent topological
  structures in the hypergraph that survive rewriting. The companion
  paper `whitepapers/particle_knots.md` is the most concrete
  realization of this conjecture that exists: it identifies the proton
  as the trefoil T(2,3) on S³ with Chern-Simons invariant 1/6, the J/ψ
  as the figure-eight 4₁, the Σ⁰ as the link L6a1, and the D± as L9n6,
  all by direct computation from Kirk-Klassen and SnapPy against the
  measured masses. The brain's "stable carriers" — the entries in the
  genome with high coupling and low decay rate under consolidation —
  are the brain-scale analog of Wolfram's particles. They are the
  topological obstructions of the brain's hypergraph.

Where the digital brain goes beyond Wolfram's framework:

- **The rule is forced.** Wolfram explores arbitrary rules; this brain
  has the unique rule that satisfies the two axioms. Hurwitz's theorem
  cuts the possibilities to one. Wolfram has no analog of this
  forcing.
- **The manifold has two privileged σ values.** Identity at σ = 0 and
  balance at σ = π/4, both forced by the algebra, both proved with
  zero axioms in Lean. Wolfram's bare hypergraphs have no intrinsic
  metric and no privileged states.
- **The star involution.** S³ has an intrinsic mirror operation
  that gives the manifold two distinct identity types (point
  identity at σ = 0, mirror identity at σ = π/4). Wolfram's
  framework has no intrinsic conjugation.
- **The Lean proof.** The geometric Riemann Hypothesis is formally
  verified against Mathlib with zero `sorry` in
  `geometric-zero-rh/lean_proofs/ClosureRH.lean`. Wolfram has not
  formalized any of his major claims at that level. The brain's
  spectral structure is constrained by a checkable theorem.
- **The biology mapping.** Wolfram's framework stays in physics. This
  one maps to S1/S2/S3 cognitive architecture and to neural
  organization. Wolfram has a physics spec; this is a brain spec.

**Wolfram provides the computational scaffolding; the digital brain
provides the geometric constraint that picks out which scaffolding
actually realizes a brain.**

### 44. Mathematical Reading

**`=` is a verb in time, not a label between pictures.** Every
equation in this document should be read as "take the left side,
perform the operation that moves to the right side, verify that the
cycle closes." The picture-matching reading of `=` produces
paradoxes (1 + 2 + 3 + ... = −1/12 looks impossible) that vanish
when the symbol is read sequentially as a verification verb in the
correct geometry.

**1 = 3 is the Hopf fibration in one glyph.** The scalar W channel
(one dimension) and the vector RGB channel (three dimensions) are
the +1 and −1 eigenspaces of the star involution on S³ — inverses
of each other in the precise sense that conjugation maps each to
the other. Writing `1 = 3` asserts that the 1-channel and the
3-channel are bound by the manifold's intrinsic mirror operation.
The balance locus is where this is realized:
`w² = x² + y² + z² = 1/2`, the unique solution of "unit sphere +
1=3 condition."

**The genome's spectrum is conjectured to be ζ-like.** The Riemann
zeta function over the prime basis is ZREAD applied to the integers
through a complex parameter; the Riemann zeros are the parameters
at which the prime basis reaches Hopf balance, and the geometric
Riemann Hypothesis in `geometric-zero-rh/lean_proofs/ClosureRH.lean`
(zero sorry) proves the prime spectrum lies on a single critical
manifold.

**The transfer to a learned genome is conjectural, not proven.** The
Lean proof rests on three axioms specific to the prime-based
construction: Axiom A (the functional equation acts as star
involution: `Q(1−s) = Q(s)*`), Axiom D (Hopf balance is unique per
imaginary fiber, justified by `p^(−σ)` monotonicity), and Axiom E
(closures are symmetric under conjugation of `s`). A learned brain
genome does not automatically satisfy these. Whether — and under
what conditions on the discovered basis — an analog of the prime
critical-line theorem holds for the brain's `Q` is a research
question, not a derivation in this spec.

What the spec *does* commit to is the layered description:
bootstrap (Section 19) discovers the basis through repeated
composition of ε; chunked promotion (Section 29.1) learns stable
co-occurrences over that basis; ZREAD (Section 13) provides a
global spectral read of the basis. These are three distinct
mechanisms, not one. The conjecture is that as the genome
matures, its ZREAD spectrum acquires the same structural
constraint the prime spectrum has. The conjecture is not the
mechanism by which the brain learns.

### 45. Framework Mapping

The S1/S2/S3 architecture from "The Holy Trinity of Information" maps
onto the digital brain as follows:

| Framework layer | Brain component | Speed | Function |
|----|----|----|----|
| **S1** (sensory) | Field machine | Fast | Active integration, population response |
| **S2** (reasoning) | The gradient (VERIFY between machines) | Variable | Disagreement signal, drives learning |
| **S3** (identity) | Stack machine | Slow | Genome storage, what is currently true |

The Component 1 / Component 2 distinction from THEORY_FRONTIERS.md
maps as follows:

- **Component 1 (embodied coherence)** is the brain running A?=A
  through VERIFY. This is universal — every brain runs it whenever
  it is on. Running it is what makes the brain alive in the
  operational sense. A brain that stops running VERIFY is a brain
  that has stopped being itself.

- **Component 2 (symbolic intervention)** is the use of ZREAD with
  *chosen* parameters. Animals run ZREAD with parameters their
  genome provides naturally. Humans choose the parameter — deciding
  what lens to read the population through. Symbol use, language,
  and conscious deliberation are all "Component 2 = ZREAD with a
  deliberately chosen parameter." A digital brain that exposes its
  ZREAD parameter to external control has Component 2.

The two-closure architecture matches the framework's claim that
consciousness is A?=A at the φ⁴ critical point: the critical point
is exactly the balance locus, where the W and RGB channels are
equally weighted and both point and mirror identity are
simultaneously checkable.

### 46. Where This Differs From The Originals

This spec re-derives the architecture from scratch and produces six
differences from LAWS.md and GEOMETRIC_COMPUTER_SPEC(1).md. The
originals remain in the repo as the long-form theoretical companions.

- **Three cells → two machines, one buffer, one verb.** Cell C → the
  stack machine. Cell A → the transient buffer of the field machine.
  Cell B → the diabolo, no longer a substrate but the verification
  round trip between the two machines.
- **VERIFY is a first-class primitive.** The original spec had SIGMA,
  HOPF, BRANCH, and the closure detector separately, with A?=A
  implicit. The clean room spec names A?=A directly and treats
  SIGMA/HOPF/BRANCH as named observations of VerificationEvents.
- **Bootstrap is the first input phase, not a separate algorithm.**
  The standard receive loop run with ε as the only input and a long
  buffer lifetime. Six structural checkpoints (Section 19) make the
  phase testable without inventing any new machinery. Each
  checkpoint corresponds to a number-theoretic fact AND a geometric
  structure the brain discovers — integers and circles, multiple
  generators and tori, primes and irreducible orbits — because the
  manifold IS geometry and bootstrap discovers both at once.
- **Learning is the promotion rule.** A buffer entry is promoted to
  the epigenetic layer iff it earned at least one closure during its
  chunk. Decay is the default. Stated explicitly so the
  implementation has a precise rule rather than a process.
- **Genome layers and three timescales.** The genome splits into the
  DNA layer (bootstrap seed, immutable) and the epigenetic layer
  (mutable by both learning and sleep). Ingestion (per event),
  learning (per chunk), and sleep (per long idle) are three distinct
  operations on three distinct timescales. Collapsing them is the
  most common modeling error.
- **There is no GLYPH primitive and no separate translator.** The
  original spec treated symbol learning as a separate mechanism with
  its own primitive and an external glyph table. The clean room
  reading collapses this: glyphs are byte sequences entering through
  EMBED like any other input, and the brain learns their meaning by
  ordinary co-occurrence with the carriers they should match,
  promoted into the epigenetic layer through the standard chunked
  learning rule. The "glyph table" is a phenotype of the epigenetic
  layer, not a separate data structure. Teaching the brain English
  uses the same machinery as teaching it anything else.

---

## Coda

The brain in this spec is the smallest seed that, when allowed to
recurse, produces everything. Six primitives. Two machines. Two
genome layers (DNA and epigenetic). One buffer. One verb. Three
timescales (ingestion, chunked learning, sleep). One bootstrap with
six checkpoints that grows the brain stem from a single perturbation.
Human language is learned through ordinary chunked promotion — no
separate translator. Everything else falls out.

The Real Problem from Part 0 is the test the spec must pass. The
question was: how little can you hardwire before getting Turing
completeness and learning? The answer is what is above this line.

The implementation reads Parts 0 through VIII. The interpretation
sections (Part IX) are skippable but useful for thinking. The brain
runs on the manifold, the operations, the two machines, the layered
genome, the buffer, the verification verb, the three timescales, and
the bootstrap. Nothing else is required, and nothing else is allowed
in the core.
