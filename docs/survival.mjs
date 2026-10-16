// Survival rates of Enkidu-Alive, measured with the simulation code of enkidu.html itself.
//
//     node docs/survival.mjs            # 2,000 runs of 600 ticks per setting
//     node docs/survival.mjs 500        # fewer runs, faster
//
// The page's script runs headless with its drawing and controls stubbed out; every
// tick, drive and death follows the same code the browser runs. Its random numbers
// come from a seeded generator, so every run of this script prints the same table.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const page = readFileSync(fileURLToPath(new URL("enkidu.html", import.meta.url)), "utf8");
const src = page.slice(page.lastIndexOf("<script>") + 8, page.lastIndexOf("</script>"));
const element = () => new Proxy(
  { style: {}, classList: { add() {}, remove() {} }, children: [], value: "",
    appendChild() {}, removeChild() {}, addEventListener() {},
    getBoundingClientRect: () => ({ left: 0, top: 0 }),
    getContext: () => new Proxy({}, { get: () => () => ({ addColorStop() {} }) }) },
  { get: (t, k) => t[k], set: (t, k, v) => ((t[k] = v), true) });
// mulberry32: a small seeded generator standing in for Math.random.
let seed = 2026;
const random = () => {
  seed = (seed + 0x6d2b79f5) >>> 0;
  let t = seed;
  t = Math.imul(t ^ (t >>> 15), t | 1);
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const seededMath = Object.create(Math, { random: { value: random } });
const elements = new Map();
const context = {
  document: { getElementById: id => elements.get(id) ?? elements.set(id, element()).get(id), createElement: element },
  setInterval: () => 0, clearInterval: () => {}, requestAnimationFrame: () => 0, Math: seededMath, console,
};
vm.createContext(context);
vm.runInContext(src + `
globalThis.sim = { tick, setMode, setTemperament, teachShelter,
  get alive() { return alive; }, get cause() { return deathCause; } };`, context);

const sim = context.sim, runs = Number(process.argv[2] ?? 2000), ticks = 600;
console.log(`${runs} runs of ${ticks} ticks per setting\n`);
for (const mode of ["thriving", "scarce"]) for (const shelter of [false, true]) {
  for (const temperament of ["cautious", "balanced", "bold"]) {
    let survived = 0; const causes = {};
    for (let r = 0; r < runs; r++) {
      sim.setMode(mode); sim.setTemperament(temperament); if (shelter) sim.teachShelter();
      for (let k = 0; k < ticks && sim.alive; k++) sim.tick();
      if (sim.alive) survived++; else causes[sim.cause] = (causes[sim.cause] ?? 0) + 1;
    }
    const [cause, count] = Object.entries(causes).sort((a, b) => b[1] - a[1])[0] ?? [];
    console.log(`${mode.padEnd(9)} ${shelter ? "with shelter" : "no shelter  "}  ${temperament.padEnd(9)}` +
      `${(100 * survived / runs).toFixed(1).padStart(5)}% survive` +
      (cause ? `   main cause of death: ${cause} (${Math.round(100 * count / (runs - survived))}%)` : ""));
  }
}
