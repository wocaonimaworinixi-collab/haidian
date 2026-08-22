#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Z1-Z3 一期试点可实施性验收门槛核验器。

读取 metrics.json 中 z1_* / z2_* / z3_* 条目，逐项断言是否达到 v4.20 设定的
试点验收门槛。评审可本地复算：

    python assets/verification/z1_z3_pilot_gate.py

退出码 0 = 全部达标；1 = 存在未达标项。
"""
import json
import os
import sys

THRESHOLDS = {
    "z1_barrier_free_continuity_pct": (">=", 95.0, "连续无障碍路径贯通率 ≥ 95%"),
    "z1_lowspeed_separation_pct":     ("==", 100.0, "低速带与人行带物理分隔到位率 = 100%"),
    "z2_false_positive_cap_ratio":    ("<=", 1.2, "月均误报率不超过 X15 基线 1.2 倍"),
    "z3_safeguard_coverage_count":    (">=", 4, "公共利益六类保障至少覆盖四类"),
}


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    pkg = os.path.dirname(os.path.dirname(here))
    with open(os.path.join(pkg, "metrics.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    metrics = data.get("metrics", {})
    results = []
    for key, (op, thr, desc) in THRESHOLDS.items():
        m = metrics.get(key)
        if not m or "value" not in m:
            results.append((key, "MISSING", desc, None, thr))
            continue
        val = m["value"]
        ok = (
            (op == ">=" and val >= thr)
            or (op == "<=" and val <= thr)
            or (op == "==" and abs(val - thr) < 1e-9)
        )
        results.append((key, "PASS" if ok else "FAIL", desc, val, thr))
    all_ok = all(r[1] == "PASS" for r in results)
    for key, st, desc, val, thr in results:
        print(f"[{st}] {key}: {desc} (value={val}, threshold={thr})")
    print("Z1-Z3 pilot gate:", "ALL PASS" if all_ok else "NOT MET")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
