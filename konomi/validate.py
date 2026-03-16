#!/usr/bin/env python3
"""
KONOMI — Standards Compliance Validator + Factory Sim
ACG Guild Platform

Usage:
    python -m konomi.validate                    # sim mode (default)
    python -m konomi.validate --scan file.py     # scan a file
    python -m konomi.validate --factory brewery  # sim a factory
    python -m konomi.validate --ticks 50         # run N sim ticks
    python -m konomi.validate --list-tags        # list all tags
    python -m konomi.validate --benchmark        # eVGPU benchmark
"""

import argparse
import sys


def run_sim(factory_type: str, ticks: int, list_tags: bool):
    """Run factory simulation."""
    from konomi.factory.site import Site
    from konomi.factory.sim import SimMode
    from konomi.scanner.engine import Scanner

    factories = {
        "brewery": Site.create_brewery,
        "pharma": Site.create_pharma,
        "food": Site.create_food,
    }

    create_fn = factories.get(factory_type)
    if not create_fn:
        print(f"Unknown factory type: {factory_type}")
        print(f"Available: {', '.join(factories.keys())}")
        return 1

    site = create_fn()
    print(f"[SIM] {site.name} — {site.desc}")
    print(f"[SIM] Mode: {site.sim.mode.value}")
    print(f"[SIM] Areas: {len(site.areas)}, Tags: {site.tag_db.tag_count}")

    if list_tags:
        print(f"\n[TAGS] All {site.tag_db.tag_count} tags:")
        for path in site.tag_db.all_paths():
            print(f"  {path}")
        return 0

    # Run sim ticks
    print(f"\n[SIM] Running {ticks} ticks...")
    site.sim.run_sync(ticks=ticks)
    print(f"[SIM] Complete. {site.sim.total_ticks} ticks executed.")

    # Sample tag readings
    print("\n[SIM] Sample tag readings:")
    all_values = site.tag_db.read_all()
    shown = 0
    for path, value in sorted(all_values.items()):
        if value.v is not None and shown < 20:
            print(f"  {path}: {value}")
            shown += 1
    if len(all_values) > 20:
        print(f"  ... and {len(all_values) - 20} more tags")

    # Run scanner against factory
    print("\n[SCAN] Running standards compliance check...")
    scanner = Scanner()
    result = scanner.scan_factory(site)
    print(result.report())

    # OEE if available
    if site.oee and site.oee.total_units > 0:
        print(f"\n[KPI] {site.oee}")

    return 0


def run_scan(filepath: str):
    """Scan a source file."""
    from konomi.scanner.engine import Scanner

    scanner = Scanner()
    result = scanner.scan_file(filepath)
    print(f"[SCAN] {filepath}")
    print(result.report())
    return 0 if result.is_compliant else 1


def run_benchmark():
    """Run eVGPU benchmark."""
    from konomi.evgpu.engine import eVGPU

    gpu = eVGPU(cores=4)
    print("[BENCHMARK] eVGPU — pure CPU compute")
    for size in [64, 128, 256, 512]:
        result = gpu.benchmark(size=size, iterations=50)
        print(f"  {size}x{size}: {result['gflops']} GFLOPS "
              f"({result['elapsed_s']}s)")
    gpu.shutdown()
    return 0


def run_femto():
    """Test FemtoLLM."""
    from konomi.femto.model import FemtoLLM

    llm = FemtoLLM()
    print(f"[FEMTO] {llm}")
    print(f"[FEMTO] Params: {llm.param_count:,}")
    print(f"[FEMTO] Memory: {llm.memory_bytes / 1024:.0f} KB")

    labels = ["temperature", "pressure", "flow", "level", "alarm"]
    tests = [
        "The reactor jacket temp is too high",
        "Vessel PSI reading abnormal",
        "Flow rate through the pump",
        "Tank level dropping",
        "Emergency shutdown triggered",
    ]
    print("\n[FEMTO] Classification test:")
    for text in tests:
        label = llm.classify(text, labels)
        print(f"  '{text}' → {label}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="KONOMI — ACG Standards Compliance + Factory Sim")
    parser.add_argument("--scan", type=str, help="Scan a source file")
    parser.add_argument("--factory", type=str, default="brewery",
                        help="Factory type: brewery, pharma, food")
    parser.add_argument("--ticks", type=int, default=10,
                        help="Number of sim ticks (default: 10)")
    parser.add_argument("--list-tags", action="store_true",
                        help="List all factory tags")
    parser.add_argument("--benchmark", action="store_true",
                        help="Run eVGPU benchmark")
    parser.add_argument("--femto", action="store_true",
                        help="Test FemtoLLM")

    args = parser.parse_args()

    if args.scan:
        return run_scan(args.scan)
    elif args.benchmark:
        return run_benchmark()
    elif args.femto:
        return run_femto()
    else:
        return run_sim(args.factory, args.ticks, args.list_tags)


if __name__ == "__main__":
    sys.exit(main() or 0)
