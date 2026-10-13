import json, shutil, sys, datetime
F = sys.argv[1]
RULE = "mcp__a035b92d-1045-42ba-9497-a2a58342f986__apply_design_change"
d = json.load(open(F))                      # fails loudly if the file is not valid JSON
allow = d.setdefault("permissions", {}).setdefault("allow", [])
if RULE in allow:
    print("already there — nothing to do"); sys.exit(0)
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
shutil.copy2(F, F + ".backup-" + stamp)     # back up before touching it
allow.insert(0, RULE)
json.dump(d, open(F, "w"), indent=2)
json.load(open(F))                          # read it back; proves it is still valid
print("added. rules now:", len(allow))
print("backup:", F + ".backup-" + stamp)
