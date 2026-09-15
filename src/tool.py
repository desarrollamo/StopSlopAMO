#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path
from collections import Counter
MODE="stopslop"
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def uiux(d):
    domain=(d.get("domain") or d.get("rubro") or "general").lower()
    ps={"medical":["#F7FBFC","#0B6E75","#3AAFA9","#123B4A"],"legal":["#FAF8F4","#18212F","#8A6A3F","#D8D1C4"],"food":["#FFF9F2","#9D3C1E","#E2A14A","#2D4B36"],"plants":["#F7FAF3","#315B3A","#789B5A","#D8E6C9"]}
    colors=next((v for k,v in ps.items() if k in domain),["#FAFAF9","#1F2937","#2563EB","#E5E7EB"])
    return {"principle":"No templates. Derive direction from the client.","domain":domain,"palette":colors,"layout":["one dominant idea per section","purposeful imagery","clear CTA hierarchy"],"avoid":["generic purple gradients","repeated card grids without need","decorative badges","copy that fits any company"],"quality_gates":["mobile check","WCAG AA contrast","project-specific identity"]}
def taste(t):
    low=t.lower(); pats={"gradient":["linear-gradient","radial-gradient"],"rounding":["rounded-3xl","rounded-2xl","border-radius:24"],"glass":["backdrop-filter","backdrop-blur"],"generic copy":["innovative solution","seamless experience"]}
    hits={k:sum(low.count(x) for x in xs) for k,xs in pats.items()}
    return {"score":max(0,100-sum(min(v,3) for v in hits.values())*5),"signals":{k:v for k,v in hits.items() if v}}
def impec(h):
    low=h.lower(); issues=[]
    if "<title" not in low: issues.append("missing title")
    if 'name="viewport"' not in low and "name='viewport'" not in low: issues.append("missing viewport meta")
    for i,x in enumerate(re.findall(r"<img\\b[^>]*>",h,re.I),1):
        if not re.search(r"\\balt\\s*=",x,re.I): issues.append(f"image {i} missing alt")
    if "<h1" not in low: issues.append("missing h1")
    if "outline:none" in low or "outline: none" in low: issues.append("focus outline removed")
    return {"pass":not issues,"score":max(0,100-len(issues)*12),"issues":issues}
def slides(d):
    rows=[f"# {d.get('title','Untitled')}",f"Audience: {d.get('audience','audience')}","","## Deck plan","1. Hook - why this matters","2. Objectives - what people should leave with"]
    n=3
    for s in d.get("sections",[]): rows.append(f"{n}. {s} - one idea, one visual proof"); n+=1
    rows += [f"{n}. Case / example",f"{n+1}. Takeaways",f"{n+2}. Questions / next action"]
    return "\n".join(rows)+"\n"
def design(d):
    c=d.get("colors",{}); name=d.get("name","Project Design")
    return f"""---
name: {name}
colors:
  primary: "{c.get('primary','#0B6E75')}"
  secondary: "{c.get('secondary','#3AAFA9')}"
  neutral: "{c.get('neutral','#F7FBFC')}"
  ink: "{c.get('ink','#123B4A')}"
---
# Visual direction
{d.get('tone','clear, distinctive, useful')}
# Typography
Define display, heading, body and label roles.
# Layout
Derive composition from content. Do not start from another client's layout.
# Components
Components inherit this project's identity.
# Imagery
Prefer real assets or intentional custom illustration.
# Accessibility
Maintain WCAG AA contrast and visible keyboard focus.
# Do
- Build project-specific hierarchy.
# Don't
- Reuse another client's visual identity.
"""
def library(root,q=""):
    items=[]
    for p in Path(root).rglob("DESIGN.md"):
        t=p.read_text(encoding="utf-8",errors="ignore"); title=next((x[2:] for x in t.splitlines() if x.startswith("# ")),p.parent.name)
        if not q or q.lower() in (title+" "+t[:2000]).lower(): items.append({"title":title,"path":str(p)})
    return {"count":len(items),"items":items[:100]}
AI=["in today's fast-paced","game-changer","revolutionary","cutting-edge","seamless","unlock the power","elevate your","delve into","it's important to note","in conclusion","innovative solution"]
def humanize(t):
    low=t.lower(); hits=[p for p in AI if p in low]; long=sum(1 for s in re.split(r"[.!?]+",t) if len(s.split())>28)
    return {"score":max(0,100-len(hits)*9-long*4),"phrases":hits,"long_sentences":long,"guidance":["replace claims with specifics","prefer verbs over stacked adjectives","keep client vocabulary"]}
def understand(root):
    root=Path(root); fs=[p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]; ex=Counter((p.suffix.lower() or "[no-ext]") for p in fs)
    return {"root":str(root),"files":len(fs),"extensions":dict(ex.most_common(12)),"entry_candidates":[str(p.relative_to(root)) for p in fs if p.name.lower() in {"readme.md","package.json","pyproject.toml","index.html","main.py","app.py"}][:20]}
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def diagram(d):
    ns=d.get("nodes",[]); es=d.get("edges",[]); pos={n["id"]:(110+i*200,170) for i,n in enumerate(ns)}; lines=[]; boxes=[]
    for e in es:
        if e["from"] in pos and e["to"] in pos:
            x1,y1=pos[e["from"]]; x2,y2=pos[e["to"]]; lines.append(f'<line x1="{x1+70}" y1="{y1}" x2="{x2-70}" y2="{y2}" stroke="#6B8795" stroke-width="2"/>')
    for n in ns:
        x,y=pos[n["id"]]; boxes.append(f'<rect x="{x-70}" y="{y-38}" width="140" height="76" rx="12" fill="#F7FBFC" stroke="#0B6E75" stroke-width="2"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="Arial" font-size="15">{esc(n.get("label",n["id"]))}</text>')
    return f'<!doctype html><meta charset="utf-8"><svg viewBox="0 0 {max(800,220*max(1,len(ns)))} 360" width="100%" xmlns="http://www.w3.org/2000/svg">{"".join(lines)}{"".join(boxes)}</svg>'
SLOP=["let's dive in","in the ever-evolving","at the end of the day","it is worth noting","not just","but also","whether you're","paradigm shift","leverage","synergy","holistic"]
def stopslop(t):
    low=t.lower(); hits={p:low.count(p) for p in SLOP if p in low}
    return {"score":max(0,100-sum(hits.values())*8),"cliches":hits,"action":"Cut filler; keep concrete claims and varied rhythm."}
def main():
    p=argparse.ArgumentParser(); p.add_argument("input",nargs="?"); p.add_argument("-o","--output"); p.add_argument("--query",default=""); a=p.parse_args()
    if MODE=="uiux": out=json.dumps(uiux(load(a.input)),ensure_ascii=False,indent=2)
    elif MODE=="taste": out=json.dumps(taste(Path(a.input).read_text(encoding="utf-8",errors="ignore")),ensure_ascii=False,indent=2)
    elif MODE=="impec": out=json.dumps(impec(Path(a.input).read_text(encoding="utf-8",errors="ignore")),ensure_ascii=False,indent=2)
    elif MODE=="slides": out=slides(load(a.input))
    elif MODE=="design": out=design(load(a.input))
    elif MODE=="library": out=json.dumps(library(a.input or ".",a.query),ensure_ascii=False,indent=2)
    elif MODE=="humanize": out=json.dumps(humanize(Path(a.input).read_text(encoding="utf-8",errors="ignore")),ensure_ascii=False,indent=2)
    elif MODE=="understand": out=json.dumps(understand(a.input or "."),ensure_ascii=False,indent=2)
    elif MODE=="diagram": out=diagram(load(a.input))
    elif MODE=="stopslop": out=json.dumps(stopslop(Path(a.input).read_text(encoding="utf-8",errors="ignore")),ensure_ascii=False,indent=2)
    else: raise SystemExit("unknown mode")
    if a.output: Path(a.output).write_text(out,encoding="utf-8")
    else: print(out)
if __name__=="__main__": main()
