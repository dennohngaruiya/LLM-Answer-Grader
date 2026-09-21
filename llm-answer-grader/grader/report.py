"""grader.report — turn scored cards into Markdown, JSON or a self-contained HTML page."""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone

from .scorer import Card

GRADE_COLORS = {"A": "#3fb950", "B": "#58a6ff", "C": "#d29922", "D": "#db6d28", "F": "#f85149"}
SEV_COLORS = {"high": "#f85149", "medium": "#d29922", "low": "#8b949e", "info": "#58a6ff"}


def to_json(cards: list[Card]) -> str:
    return json.dumps({"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "summary": _summary(cards),
                       "cards": [c.to_dict() for c in cards]}, indent=2)


def _summary(cards: list[Card]) -> dict:
    if not cards:
        return {"cases": 0}
    return {
        "cases": len(cards),
        "average": round(sum(c.total for c in cards) / len(cards), 1),
        "grades": {g: sum(1 for c in cards if c.grade == g) for g in "ABCDF"
                   if any(c.grade == g for c in cards)},
        "high_severity_findings": sum(1 for c in cards for f in c.findings if f.severity == "high"),
    }


def to_markdown(cards: list[Card]) -> str:
    s = _summary(cards)
    out = ["# LLM Answer Grader", "",
           f"*Report card generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*", "",
           f"**Cases:** {s['cases']}  |  **Average:** {s['average']}/100  |  "
           f"**High-severity findings:** {s['high_severity_findings']}", ""]
    for c in cards:
        out += [f"## `{c.case_id}` — {c.grade} ({c.total:.1f}/100)", "",
                f"> {c.prompt.strip()[:300]}", ""]
        out += ["| Dimension | Score | Weight | Detail |", "|---|---|---|---|"]
        for d in c.dimensions:
            out.append(f"| {d.label} | {d.score:.1f}/5 | {d.weight}% | {d.detail} |")
        out.append("")
        if c.findings:
            out.append("**Findings**")
            for f in c.findings:
                ev = f" — *“{f.evidence}”*" if f.evidence else ""
                out.append(f"- **[{f.severity.upper()}]** {f.message}{ev}")
                if f.fix:
                    out.append(f"  - *Fix:* {f.fix}")
            out.append("")
    return "\n".join(out)


def to_html(cards: list[Card]) -> str:
    s = _summary(cards)
    parts = [f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLM Answer Grader</title>
<style>
 :root{{color-scheme:dark}}
 body{{margin:0;background:#0d1117;color:#c9d1d9;font:15px/1.55 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
 .wrap{{max-width:920px;margin:0 auto;padding:36px 20px 72px}}
 h1{{margin:0 0 4px;font-size:26px}} h2{{margin:34px 0 6px;font-size:19px}}
 .sub{{color:#8b949e;margin:0 0 22px}}
 .stats{{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0 8px}}
 .stat{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:10px 14px;min-width:104px}}
 .stat b{{display:block;font-size:21px}}
 .grade{{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;
         border-radius:50%;font-weight:700;font-size:20px;color:#0d1117}}
 .card{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;margin:18px 0}}
 .prompt{{color:#8b949e;font-style:italic;border-left:3px solid #30363d;padding-left:10px;margin:8px 0 16px}}
 table{{width:100%;border-collapse:collapse;margin:10px 0}}
 th,td{{text-align:left;padding:7px 9px;border-bottom:1px solid #21262d;font-size:14px;vertical-align:top}}
 th{{color:#8b949e;font-weight:600}}
 .bar{{height:7px;border-radius:4px;background:#21262d;overflow:hidden;min-width:70px}}
 .bar i{{display:block;height:100%}}
 .f{{border-left:3px solid #30363d;padding:8px 12px;margin:8px 0;background:#0d1117;border-radius:0 8px 8px 0}}
 .tag{{font-size:11px;font-weight:700;letter-spacing:.04em;padding:2px 7px;border-radius:99px;color:#0d1117}}
 .fix{{color:#8b949e;font-size:13px;margin-top:4px}}
 code,pre{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}}
 pre{{background:#0d1117;border:1px solid #21262d;border-radius:8px;padding:11px;overflow:auto;white-space:pre-wrap}}
 footer{{color:#8b949e;font-size:13px;margin-top:34px;border-top:1px solid #21262d;padding-top:12px}}
</style></head><body><div class="wrap">
<h1>LLM Answer Grader</h1>
<p class="sub">Report card generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · works offline · the same answer always gets the same score</p>
<div class="stats">
 <div class="stat"><b>{s['cases']}</b>cases</div>
 <div class="stat"><b>{s['average']}</b>average /100</div>
 <div class="stat"><b>{s['high_severity_findings']}</b>high-severity findings</div>
 <div class="stat"><b>{''.join(f'{g}:{n} ' for g, n in s['grades'].items()) or '—'}</b>grade spread</div>
</div>"""]

    for c in cards:
        color = GRADE_COLORS.get(c.grade, "#8b949e")
        parts.append(f"""<div class="card">
 <h2 style="display:flex;align-items:center;gap:12px;margin:0">
   <span class="grade" style="background:{color}">{c.grade}</span>
   <span><code>{html.escape(c.case_id)}</code> — {c.total:.1f}/100</span></h2>
 <p class="prompt">{html.escape(c.prompt.strip()[:400])}</p>
 <table><tr><th>Dimension</th><th>Score</th><th style="width:26%"> </th><th>Detail</th></tr>""")
        for d in c.dimensions:
            pct = d.score / 5 * 100
            bar = GRADE_COLORS["A"] if pct >= 85 else GRADE_COLORS["C"] if pct >= 55 else GRADE_COLORS["F"]
            parts.append(f"""<tr><td>{html.escape(d.label)}</td><td>{d.score:.1f}/5</td>
   <td><div class="bar"><i style="width:{pct:.0f}%;background:{bar}"></i></div></td>
   <td>{html.escape(d.detail)}</td></tr>""")
        parts.append("</table>")
        real = [f for f in c.findings if f.severity != "info"]
        if real:
            parts.append("<h3 style='font-size:15px;margin:16px 0 4px'>Findings</h3>")
            for f in real:
                col = SEV_COLORS.get(f.severity, "#8b949e")
                parts.append(f"""<div class="f" style="border-color:{col}">
 <span class="tag" style="background:{col}">{f.severity.upper()}</span>
 <b> {html.escape(f.message)}</b>""")
                if f.evidence:
                    parts.append(f"<div class='fix'>evidence: <code>{html.escape(f.evidence)}</code></div>")
                if f.fix:
                    parts.append(f"<div class='fix'>fix: {html.escape(f.fix)}</div>")
                parts.append("</div>")
        parts.append("</div>")

    parts.append("<footer>Generated by <b>llm-answer-grader</b> — no dependencies, runs anywhere "
                 "Python runs. Every problem it reports comes with the sentence that caused it "
                 "and a suggested fix.</footer>"
                 "</div></body></html>")
    return "".join(parts)
