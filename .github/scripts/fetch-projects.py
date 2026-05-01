import requests
import yaml
import sys
from pathlib import Path

REPOS = [
    {"repo": "MEdu-lab/2024-2025-SECONDARIA-PUBBLICA-BUZZATI", "id": "buzzati-secondaria-2425"},
    {"repo": "MEdu-lab/2025-2026-INFANZIA-PUBBLICA-BUZZATI",   "id": "buzzati-infanzia-2526"},
    {"repo": "MEdu-lab/2025-2026-SECONDARIA-PUBBLICA-BUZZATI", "id": "buzzati-secondaria-2526"},
    {"repo": "MEdu-lab/2025-2026-INFANZIA-PUBBLICA-CUNEO",     "id": "cuneo-infanzia-2526"},
    {"repo": "MEdu-lab/2025-2026-INFANZIA-PRIVATA-IlGirasole", "id": "girasole-infanzia-2526"},
]

def derive_livello(repo_id):
    if "infanzia"   in repo_id: return "Infanzia"
    if "secondaria" in repo_id: return "Secondaria"
    if "primaria"   in repo_id: return "Primaria"
    return ""

projects = []
for entry in REPOS:
    url = f"https://raw.githubusercontent.com/{entry['repo']}/main/config.yml"
    try:
        r = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"WARNING: {entry['repo']} fetch failed: {e}", file=sys.stderr)
        continue
    if r.status_code != 200:
        print(f"WARNING: {entry['repo']} returned {r.status_code}", file=sys.stderr)
        continue
    cfg = yaml.safe_load(r.text)
    p = cfg.get("progetto", {})
    c = cfg.get("corso", {})
    repo_name = entry["repo"].split("/")[-1]
    projects.append({
        "id":          entry["id"],
        "repo":        entry["repo"],
        "titolo":      p.get("titolo", ""),
        "scuola":      p.get("sottotitolo", ""),
        "anno":        p.get("anno_scolastico", ""),
        "fascia_eta":  c.get("fascia_eta", ""),
        "tipologia":   c.get("tipologia", ""),
        "tipo_scuola": p.get("tipo_scuola", ""),
        "livello":     derive_livello(entry["id"]),
        "pdf_url":     f"https://medu-lab.github.io/{repo_name}/latest.pdf",
        # Added manually once per project after media upload:
        # youtube_id, google_photos_url, thumbnail
    })

out = Path("_data/projects.yml")
out.write_text(yaml.dump(projects, allow_unicode=True, default_flow_style=False))
print(f"Written {len(projects)} projects to {out}")
