#!/usr/bin/env python3
"""
National & Enterprise AI Dependency Audit CLI
Companion diagnostic tool for "The Sovereign Illusion: AI, Geopolitics, and Power in an Interdependent World"
by Victor Brooks (Digbijoy Labs, 2026).

Evaluates a computing stack across the 4 Operational Sovereignty Invariants:
1. Interruption Authority (Who holds the kill switch?)
2. Autonomous Runway (How long can critical workloads run disconnected?)
3. Switching Friction (What is the time/capital cost to migrate providers?)
4. Governance Jurisdiction (Who controls keys, telemetry, and legal jurisdiction?)
"""

import json
import argparse
from pathlib import Path


LAYERS = [
    ("silicon_accelerators", "Silicon Accelerators & Packaging Reserve"),
    ("energy_baseload", "Firm Baseload Power & Substation Redundancy"),
    ("cloud_control_plane", "Cloud Control Plane & Cryptographic Key Custody"),
    ("model_weights_runtime", "Foundation Model Weights & Inference Portability"),
    ("data_public_rails", "Data Residency, Data Embassies & Open Protocol Rails"),
]


SAMPLE_PROFILES = {
    "single_vendor_cloud": {
        "name": "Unhedged Single-Vendor Foreign Cloud API Dependency",
        "scores": {
            "silicon_accelerators": {"interruption": 20, "runway": 10, "switching": 25, "governance": 15},
            "energy_baseload": {"interruption": 50, "runway": 40, "switching": 30, "governance": 50},
            "cloud_control_plane": {"interruption": 10, "runway": 0, "switching": 20, "governance": 10},
            "model_weights_runtime": {"interruption": 10, "runway": 0, "switching": 30, "governance": 15},
            "data_public_rails": {"interruption": 20, "runway": 15, "switching": 20, "governance": 20},
        },
    },
    "diversified_sovereign_leverage": {
        "name": "Multi-Aligned Interdependent Architecture (Book Blueprint)",
        "scores": {
            "silicon_accelerators": {"interruption": 70, "runway": 80, "switching": 65, "governance": 75},
            "energy_baseload": {"interruption": 85, "runway": 80, "switching": 70, "governance": 90},
            "cloud_control_plane": {"interruption": 85, "runway": 85, "switching": 80, "governance": 90},
            "model_weights_runtime": {"interruption": 95, "runway": 90, "switching": 90, "governance": 90},
            "data_public_rails": {"interruption": 90, "runway": 85, "switching": 85, "governance": 95},
        },
    },
}


def evaluate_profile(profile_key: str) -> str:
    prof = SAMPLE_PROFILES[profile_key]
    lines = [
        "=" * 78,
        f" SOVEREIGN AI DEPENDENCY AUDIT REPORT: {prof['name']}",
        " Framework: The Sovereign Illusion (Victor Brooks | Digbijoy Labs)",
        "=" * 78,
        f"{'Stack Layer':<44} | {'Int':>4} | {'Run':>4} | {'Swi':>4} | {'Gov':>4} | {'Composite':>9}",
        "-" * 78,
    ]
    total = 0.0
    for key, label in LAYERS:
        s = prof["scores"][key]
        comp = (s["interruption"] + s["runway"] + s["switching"] + s["governance"]) / 4.0
        total += comp
        lines.append(
            f"{label[:44]:<44} | {s['interruption']:>4} | {s['runway']:>4} | {s['switching']:>4} | {s['governance']:>4} | {comp:>8.1f}%"
        )
    overall = total / len(LAYERS)
    lines.append("-" * 78)
    tier = (
        "CRITICAL COERCION VULNERABILITY (<40%)"
        if overall < 40
        else ("MODERATE STRATEGIC EXPOSURE (40-75%)" if overall < 75 else "RESILIENT INTERDEPENDENT LEVERAGE (>75%)")
    )
    lines.append(f" OVERALL SOVEREIGNTY RESILIENCE INDEX: {overall:.1f}/100.0  -->  [{tier}]")
    lines.append("=" * 78)
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run National AI Dependency Audit Scorecard")
    parser.add_argument(
        "--profile",
        choices=list(SAMPLE_PROFILES.keys()),
        default="diversified_sovereign_leverage",
        help="Diagnostic profile to evaluate",
    )
    args = parser.parse_args()
    print(evaluate_profile("single_vendor_cloud"))
    print()
    print(evaluate_profile("diversified_sovereign_leverage"))
