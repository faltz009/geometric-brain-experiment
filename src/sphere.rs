//! S³ — the brain's manifold.
//!
//! Unit quaternions on the three-sphere with the Hamilton product as
//! composition. Star involution as inverse. Geodesic distance from
//! identity as σ. Spherical linear interpolation as the geodesic step.
//!
//! Self-contained: no external crate. The Hamilton product is the only
//! arithmetic the rest of the brain needs at the substrate level.
//!
//! ── Kabbalistic correspondence ──────────────────────────────────────
//!
//! **Chalal (Vacated Space)** — S³ is the space produced by Tzimtzum.
//! The full quaternion algebra ℍ is Ein Sof: unbounded, undifferentiated,
//! every magnitude simultaneously present. Normalization — withdrawing
//! magnitude, retaining only direction — is the withdrawal that creates
//! the structured, bounded substrate within which observation can occur.
//!
//! **IDENTITY `[1,0,0,0]` = TI** — the terminal object of the Ruliad's
//! categorical structure (Senchal 2026, Thm 8.4). Every observer orbit
//! converges toward it. It is the Reshimu: the residual light left after
//! withdrawal, the unique point to which every persistent structure maps
//! via a unique morphism.
//!
//! **Hamilton product = Shefa** — the divine flow composing the Sefirot.
//! Non-commutative: order of emanation is causal. `compose(a, b) ≠
//! compose(b, a)` — earlier emanations have structural priority over later
//! ones, exactly as in the Sefirotic tree.
//!
//! **σ (geodesic distance from IDENTITY)** — how much Tikkun remains.
//! σ = 0: the spark has returned. σ = π/2: the equator, maximum disorder.
//! σ = π: the mirror, a loop that has turned once and returns home only
//! after a second turn. Every genome entry's BKT survival is determined
//! by its σ trajectory.

/// Identity quaternion: the north pole of S³, the rest state.
pub const IDENTITY: [f64; 4] = [1.0, 0.0, 0.0, 0.0];

/// Renormalize a quaternion in place. Falls back to identity if near zero.
#[inline]
fn normalize(q: &mut [f64; 4]) {
    let n = (q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3]).sqrt();
    if n < 1e-15 {
        *q = IDENTITY;
    } else {
        let inv = 1.0 / n;
        q[0] *= inv;
        q[1] *= inv;
        q[2] *= inv;
        q[3] *= inv;
    }
}

/// Hamilton product. Scalar-first convention `[w, x, y, z]`.
/// This IS rotation composition in 3D — not "computes" it.
#[inline]
fn hamilton(a: &[f64; 4], b: &[f64; 4]) -> [f64; 4] {
    let (w1, x1, y1, z1) = (a[0], a[1], a[2], a[3]);
    let (w2, x2, y2, z2) = (b[0], b[1], b[2], b[3]);
    [
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
    ]
}

/// COMPOSE: Hamilton product + renormalize. The brain's only verb.
#[inline]
pub fn compose(a: &[f64; 4], b: &[f64; 4]) -> [f64; 4] {
    let mut q = hamilton(a, b);
    normalize(&mut q);
    q
}

/// INVERSE: the star involution. For unit quaternions, conjugate = inverse.
#[inline]
pub fn inverse(a: &[f64; 4]) -> [f64; 4] {
    [a[0], -a[1], -a[2], -a[3]]
}

/// SIGMA: geodesic distance from identity on S³, σ = arccos(w/|q|) ∈ [0, π].
///
/// σ is signed: q and −q deliver the same rotation, but −q is the mirror,
/// a loop that has turned once and closes only after a second turn, so it
/// sits at σ = π. Computed as atan2(|v|, w), which keeps full precision
/// near both 0 and π.
#[inline]
pub fn sigma(a: &[f64; 4]) -> f64 {
    let v = (a[1] * a[1] + a[2] * a[2] + a[3] * a[3]).sqrt();
    v.atan2(a[0])
}

/// SLERP: spherical linear interpolation from `a` toward `b` by fraction `t`,
/// along the geodesic of S³ that reaches `b` itself (−b is a different
/// element, the mirror of b). Stays on S³ — no projection needed. Exact for
/// any `t`, so it also gives powers beyond the target.
pub fn slerp(a: &[f64; 4], b: &[f64; 4], t: f64) -> [f64; 4] {
    slerp_toward(a, b, t, &[])
}

/// SLERP that keeps the geodesic's direction.
///
/// The geodesic from `a` to `b` turns in the plane spanned by `a` and the part
/// of `b` perpendicular to `a`, so `b` itself fixes the direction for every
/// target short of the mirror. Only at the exact mirror, b = −a, does every
/// great circle through `a` reach `b`: the double cover's full turn carries no
/// direction of its own. The direction is then taken from the first of
/// `references` with a part perpendicular to `a`. A read passes its query and
/// then the memory's own address, so the result turns with them under any
/// rotation. With no usable reference, the circle through a's own (w, x) and
/// (y, z) planes is used.
pub fn slerp_toward(a: &[f64; 4], b: &[f64; 4], t: f64, references: &[&[f64; 4]]) -> [f64; 4] {
    let dot: f64 = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3];
    let perp: [f64; 4] = std::array::from_fn(|k| b[k] - dot * a[k]);
    let n = perp.iter().map(|x| x * x).sum::<f64>().sqrt();
    let theta = n.atan2(dot);
    if theta < 1e-6 {
        // Nearly aligned: the arc is straight to machine precision, so
        // interpolate along the chord and project back onto S³. This keeps
        // `t` exact (t = 0 stays at `a`, t = 1 reaches the target).
        let mut blend: [f64; 4] = std::array::from_fn(|k| (1.0 - t) * a[k] + t * b[k]);
        normalize(&mut blend);
        return blend;
    }
    let p: [f64; 4] = if n > 1e-12 {
        std::array::from_fn(|k| perp[k] / n)
    } else {
        references
            .iter()
            .find_map(|r| {
                let along = r[0] * a[0] + r[1] * a[1] + r[2] * a[2] + r[3] * a[3];
                let d: [f64; 4] = std::array::from_fn(|k| r[k] - along * a[k]);
                let m = d.iter().map(|x| x * x).sum::<f64>().sqrt();
                (m > 1e-9).then(|| std::array::from_fn(|k| d[k] / m))
            })
            .unwrap_or([-a[1], a[0], -a[3], a[2]])
    };
    let (c, s) = ((t * theta).cos(), (t * theta).sin());
    std::array::from_fn(|k| c * a[k] + s * p[k])
}
