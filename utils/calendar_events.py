# def build_calendar_events():
#     entries = load_entries()
#     vars_by_name = {v["name"]: v for v in load_variables()}

#     events=[]
#     for e in entries:
#         v = vars_by_name.get(e["variable"])
#         if not v: continue
#         events.append({
#             "title": f"{e['variable']}: {e['wert']}",
#             "start": e["datum"],
#             "end":   e["datum"],
#             "color": v.get("color","#999"),
#         })
#     return events, list(vars_by_name.values())