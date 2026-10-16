"""Take the design-save permission rule back out.

It does not work. Added on 12 Oct 2026 because the refusal message said an
explicit rule would override the block; it does not. With auto mode on, the
classifier then refused again with reason "[Auto-Mode Bypass]" — i.e. it reads
the rule itself as an attempt to get around auto mode. So the rule grants
nothing and looks like a workaround. This removes it.
"""
import json, shutil, sys, datetime
F = sys.argv[1]
RULE = "mcp__a035b92d-1045-42ba-9497-a2a58342f986__apply_design_change"
d = json.load(open(F))
allow = d.get("permissions", {}).get("allow", [])
if RULE not in allow:
    print("not there — nothing to do"); sys.exit(0)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(F, F + ".backup-" + stamp)
d["permissions"]["allow"] = [r for r in allow if r != RULE]
json.dump(d, open(F, "w"), indent=2)
json.load(open(F))                      # read back; proves it is still valid
print("removed. rules now:", len(d["permissions"]["allow"]))
print("backup:", F + ".backup-" + stamp)
