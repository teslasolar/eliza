# The Tag System — Nervous System of the Factory

## What Is a Tag?

In industrial control, a **tag** is a named data point. Everything is a tag:

- Temperature sensor: `Site1/Area2/Reactor1/TT-301/PV`
- Valve position: `Site1/Area2/Reactor1/XV-101/Position`
- Batch count: `Site1/Area2/Line3/BatchCount`
- Alarm state: `Site1/Area2/Reactor1/TT-301/HighAlarm/State`

## Tag Anatomy

```javascript
const exampleTag = {
  path: "Site1/Area2/Reactor1/TT-301/PV",
  type: "float32",
  value: 72.4,
  quality: "GOOD",
  timestamp: "2026-03-16T12:34:56Z",
  unit: "°C",
  description: "Reactor 1 Temperature Transmitter Process Value",
  range: { low: 0, high: 150 },
};

console.log("Tag:", exampleTag.path);
console.log("Value:", exampleTag.value, exampleTag.unit);
console.log("Quality:", exampleTag.quality);
```

## The Tag Provider

The TagProvider is the central registry. All systems read and write through it:

```javascript
// Tag provider pattern
const provider = {
  tags: new Map(),

  register(path, type, desc) {
    this.tags.set(path, { path, type, desc, value: null, quality: "UNCERTAIN", ts: 0 });
  },

  read(path) {
    return this.tags.get(path) || null;
  },

  write(path, value) {
    const tag = this.tags.get(path);
    if (tag) {
      tag.value = value;
      tag.quality = "GOOD";
      tag.ts = Date.now();
    }
  },

  get count() { return this.tags.size; }
};

provider.register("Reactor1/TT-301/PV", "float32", "Temperature");
provider.register("Reactor1/XV-101/Pos", "bool", "Valve Position");
provider.write("Reactor1/TT-301/PV", 72.4);
provider.write("Reactor1/XV-101/Pos", true);

console.log("Tags registered:", provider.count);
console.log("Temperature:", provider.read("Reactor1/TT-301/PV").value);
```

## Tag Types in KONOMI

| Type | Use |
|------|-----|
| ProcessTags | Temperatures, pressures, flows |
| EquipmentTags | Motor speeds, valve positions |
| BatchTags | Recipe parameters, phase status |
| AlarmTags | Alarm states, acknowledgments |

## Why Tags Matter

Tags are the universal interface. OPC-UA exposes tags. Sparkplug publishes tags. Modbus maps to tags. The L5X compiler generates tags. The scanner checks tag naming. Everything speaks tags.
