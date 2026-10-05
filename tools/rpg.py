#!/usr/bin/env python3
"""Ferramenta de mesa da campanha de MHA (sem dependencias externas).

O mestre (Codex) usa este script para: rolar dados com atributos, manter o estado
da campanha, salvar/carregar, registrar o diario, controlar o canone e as divergencias.
Rode `python tools/rpg.py --help` para ver os comandos.
"""
import argparse
import json
import os
import random
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CAMP = ROOT / "campaign"
STATE = CAMP / "state.json"
SAVES = CAMP / "saves"
AUTO = CAMP / "autosave"
JOURNAL = CAMP / "journal.md"
NOTES = CAMP / "notes.md"
DIVERG = CAMP / "divergences.md"
ROLLLOG = CAMP / "roll_log.jsonl"
CANON = ROOT / "canon" / "events.json"
NPC_SEED = ROOT / "canon" / "npcs.json"
CHARS = CAMP / "characters"
HONOR_LEDGER = CAMP / "honor.md"
TEMPLATE = ROOT / "tools" / "templates" / "state.json"

RNG = random.SystemRandom()
ATTRS = ["FOR", "AGI", "VIG", "INT", "PER", "CAR"]
LEVEL_XP = [0, 10, 25, 45, 70, 100, 140, 190, 250, 320]  # xp minimo para o nivel (indice+1)
DEGREES = ["FALHA CRITICA", "FALHA", "PARCIAL (sucesso com custo)", "SUCESSO", "SUCESSO SUPERIOR"]
ALIVE = {"vivo", "alive", "ativo", "ferido"}


def die(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- estado
def load_state():
    if not STATE.exists():
        die("nao ha campanha. Rode: python tools/rpg.py new")
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(st):
    CAMP.mkdir(exist_ok=True)
    AUTO.mkdir(exist_ok=True)
    if STATE.exists():
        rev = st["meta"].get("revision", 0)
        shutil.copy2(STATE, AUTO / f"state_{rev:05d}.json")
        for old in sorted(AUTO.glob("state_*.json"))[:-25]:
            old.unlink()
    st["meta"]["revision"] = st["meta"].get("revision", 0) + 1
    st["meta"]["last_saved"] = datetime.now().isoformat(timespec="seconds")
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, STATE)
    mirror_characters(st)


def parse_value(raw):
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw


def split_path(path):
    return [int(p) if p.isdigit() else p for p in re.split(r"[.\[\]]+", path) if p != ""]


def walk(root, parts, create=False):
    cur = root
    for p in parts:
        if isinstance(cur, list):
            if not isinstance(p, int) or p >= len(cur):
                die(f"indice invalido: {p}")
            cur = cur[p]
        elif isinstance(cur, dict):
            if p not in cur:
                if create:
                    cur[p] = {}
                else:
                    die(f"caminho nao existe: {p}")
            cur = cur[p]
        else:
            die(f"nao e possivel descer em '{p}'")
    return cur


def get_path(st, path):
    return walk(st, split_path(path))


def set_path(st, path, value):
    parts = split_path(path)
    parent = walk(st, parts[:-1], create=True)
    key = parts[-1]
    if isinstance(parent, list):
        parent[key] = value
    else:
        parent[key] = value


def clamp_resource(parent, key):
    if key == "cur" and isinstance(parent, dict) and "max" in parent:
        parent["cur"] = max(0, min(parent["cur"], parent["max"]))


def today(st):
    return st.get("world", {}).get("date", "?")


# ---------------------------------------------------------------- dados
TERM = re.compile(r"([+-]?)(?:(\d*)d(\d+)|(\d+))")


def roll_expr(expr):
    expr = expr.replace(" ", "").lower()
    if not re.fullmatch(r"(?:[+-]?(?:\d*d\d+|\d+))+", expr):
        die(f"expressao invalida: {expr}")
    total, parts, rolls = 0, [], []
    for sign, n, sides, const in TERM.findall(expr):
        s = -1 if sign == "-" else 1
        if sides:
            n = int(n) if n else 1
            if n > 100:
                die("dados demais")
            dice = [RNG.randint(1, int(sides)) for _ in range(n)]
            total += s * sum(dice)
            rolls.append(dice)
            parts.append(f"{'-' if s < 0 else ''}{n}d{sides}{dice}")
        else:
            total += s * int(const)
            parts.append(f"{'-' if s < 0 else '+'}{const}")
    return total, " ".join(parts), rolls


def log_roll(entry):
    CAMP.mkdir(exist_ok=True)
    entry["at"] = datetime.now().isoformat(timespec="seconds")
    with ROLLLOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cmd_roll(a):
    results = [roll_expr(a.expr) for _ in range(2 if (a.adv or a.dis) else 1)]
    pick = results[0]
    if a.adv:
        pick = max(results, key=lambda r: r[0])
    elif a.dis:
        pick = min(results, key=lambda r: r[0])
    mode = " (vantagem)" if a.adv else " (desvantagem)" if a.dis else ""
    label = f"[{a.label}] " if a.label else ""
    if len(results) == 2:
        print(f"{label}{a.expr}{mode}: {results[0][1]} = {results[0][0]} | {results[1][1]} = {results[1][0]}")
    print(f"{label}{a.expr}{mode}: {pick[1]} = {pick[0]}")
    log_roll({"kind": "roll", "expr": a.expr, "label": a.label, "total": pick[0], "mode": mode.strip()})


def degree(total, dc, nat):
    margin = total - dc
    idx = 4 if margin >= 5 else 3 if margin >= 0 else 2 if margin >= -4 else 1
    if nat == 20:
        idx = min(4, max(idx + 1, 3))
    elif nat == 1:
        idx = max(0, min(idx - 1, 2))
    return margin, DEGREES[idx]


def cmd_check(a):
    st = load_state()
    p = st["player"]
    attr = a.attr.upper()
    if attr not in ATTRS:
        die(f"atributo deve ser um de {ATTRS}")
    skill_rank, skill_name = 0, ""
    if a.skill:
        match = [k for k in p.get("skills", {}) if k.lower() == a.skill.lower()]
        if match:
            skill_name, skill_rank = match[0], p["skills"][match[0]]
        else:
            skill_name = a.skill + " (sem treino)"
    base = p["attrs"][attr]
    rolls = [RNG.randint(1, 20) for _ in range(2 if (a.adv or a.dis) else 1)]
    nat = max(rolls) if a.adv else min(rolls) if a.dis else rolls[0]
    total = nat + base + skill_rank + a.mod
    mode = " vantagem" if a.adv else " desvantagem" if a.dis else ""
    shown = f"d20{rolls}" if len(rolls) > 1 else f"d20[{nat}]"
    line = f"{p['name']} | {attr}{'+' + skill_name if skill_name else ''}{mode}: {shown} +{base}(atr) +{skill_rank}(pericia) {a.mod:+d}(mod) = {total}"
    entry = {"kind": "check", "attr": attr, "skill": skill_name, "nat": nat, "total": total, "label": a.label}
    if a.dc is not None:
        margin, deg = degree(total, a.dc, nat)
        line += f" vs DC {a.dc} -> margem {margin:+d} => {deg}"
        entry.update(dc=a.dc, degree=deg)
    if nat == 20:
        line += "  *** 20 NATURAL ***"
    elif nat == 1:
        line += "  *** 1 NATURAL ***"
    print(line)
    log_roll(entry)


# ---------------------------------------------------------------- estado: comandos
def cmd_new(a):
    if STATE.exists():
        if not a.force:
            die("ja existe campanha. Use --force para arquivar a atual e comecar outra.")
        SAVES.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy2(STATE, SAVES / f"arquivada-{stamp}.json")
        for f in (JOURNAL, NOTES, DIVERG, ROLLLOG, HONOR_LEDGER):
            if f.exists():
                shutil.move(f, SAVES / f"arquivada-{stamp}-{f.name}")
    CAMP.mkdir(exist_ok=True)
    st = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    st["meta"]["created"] = datetime.now().isoformat(timespec="seconds")
    st["canon_events"] = {e["id"]: {"status": "canon" if e["id"].startswith("P") else "pending"} for e in load_canon()}
    if NPC_SEED.exists():
        st["npcs"] = {n["id"]: {k: v for k, v in n.items() if k != "id"} for n in json.loads(NPC_SEED.read_text(encoding="utf-8"))}
    for f in (CHARS.glob("*") if CHARS.exists() else []):
        f.unlink()
    JOURNAL.write_text("# Diario da Campanha\n", encoding="utf-8")
    NOTES.write_text("# Notas do Mestre (segredos, foreshadowing, promessas feitas aos jogadores)\n\n", encoding="utf-8")
    DIVERG.write_text("# Registro de Divergencias do Canone\n", encoding="utf-8")
    save_state(st)
    print("Campanha criada em campaign/state.json. Preencha a ficha com `set` e inicie a historia.")


def cmd_get(a):
    print(json.dumps(get_path(load_state(), a.path), ensure_ascii=False, indent=2))


def cmd_set(a):
    st = load_state()
    set_path(st, a.path, parse_value(a.value))
    save_state(st)
    print(f"{a.path} = {json.dumps(get_path(st, a.path), ensure_ascii=False)}")


def cmd_add(a):
    st = load_state()
    parts = split_path(a.path)
    parent = walk(st, parts[:-1])
    key = parts[-1]
    cur = parent[key]
    if not isinstance(cur, (int, float)):
        die("o valor atual nao e numerico")
    parent[key] = cur + parse_value(a.delta)
    clamp_resource(parent, key)
    save_state(st)
    extra = f" / {parent['max']}" if key == "cur" and "max" in parent else ""
    print(f"{a.path}: {cur} -> {parent[key]}{extra}")


def cmd_push(a):
    st = load_state()
    lst = get_path(st, a.path)
    if not isinstance(lst, list):
        die("o caminho nao e uma lista")
    lst.append(parse_value(a.value))
    save_state(st)
    print(f"{a.path}: {json.dumps(lst, ensure_ascii=False)}")


def cmd_pull(a):
    st = load_state()
    lst = get_path(st, a.path)
    val = parse_value(a.value)
    if val not in lst:
        die("valor nao encontrado na lista")
    lst.remove(val)
    save_state(st)
    print(f"{a.path}: {json.dumps(lst, ensure_ascii=False)}")


def resource_cmd(path):
    def run(a):
        a.path, a.delta = path, a.delta
        cmd_add(a)
    return run


def cmd_time(a):
    st = load_state()
    st["world"]["date"] = a.date
    if a.tod:
        st["world"]["time_of_day"] = a.tod
    if a.location:
        st["world"]["location"] = a.location
    save_state(st)
    w = st["world"]
    print(f"{w['date']} | {w.get('time_of_day', '')} | {w.get('location', '')}")


def level_for(xp):
    lvl = 1
    for i, need in enumerate(LEVEL_XP):
        if xp >= need:
            lvl = i + 1
    return lvl


def cmd_xp(a):
    st = load_state()
    p = st["player"]
    old = p["level"]
    p["xp"] += a.amount
    p["level"] = level_for(p["xp"])
    save_state(st)
    print(f"XP {p['xp']} (nivel {p['level']})")
    if p["level"] > old:
        n = p["level"] - old
        print(f"*** SUBIU {n} NIVEL(IS)! Ganhos por nivel: +2 pontos de pericia, +1 tecnica nova; "
              f"nos niveis pares tambem +1 atributo (max 10). Aplique com `set`/`push`. ***")


def cmd_status(a):
    st = load_state()
    p, w = st["player"], st["world"]
    attrs = " ".join(f"{k}{p['attrs'][k]}" for k in ATTRS)
    skills = ", ".join(f"{k}+{v}" for k, v in p.get("skills", {}).items()) or "-"
    q = p.get("quirk", {})
    print(f"== {p['name']} ('{p.get('hero_name', '-')}') | Nv {p['level']} | XP {p['xp']} ==")
    print(f"Local: {w.get('location')} | {w.get('date')} {w.get('time_of_day', '')}")
    print(f"HP {p['hp']['cur']}/{p['hp']['max']} | EST {p['est']['cur']}/{p['est']['max']} | DET {p['det']['cur']}/{p['det']['max']}")
    print(f"Atributos: {attrs}")
    print(f"Pericias: {skills}")
    print(f"Individualidade: {q.get('name', '-')} (POT {q.get('pot', '-')}, CTL {q.get('ctl', '-')})")
    for m in q.get("moves", []):
        print(f"  - {m.get('name')} [{m.get('cost', 0)} EST]: {m.get('effect', '')}")
    print(f"Limites: {q.get('limits', '-')}")
    print(f"Condicoes: {', '.join(p.get('conditions', [])) or '-'} | Ferimentos: {', '.join(p.get('wounds', [])) or '-'}")
    print(f"Inventario: {', '.join(p.get('inventory', [])) or '-'}")
    print(f"Honra: {p.get('honor', 0):+d} ({honor_tier(p.get('honor', 0))}) | Reputacao: {p.get('reputation', 0):+d} ({rep_tier(p.get('reputation', 0))}) | Codigo: {p.get('code', '-') or '-'}")
    print(f"Fama: {p.get('fame', 0)} | Credibilidade: {p.get('credibility', 0)} | Grau: {p.get('school_rank', '-')}")
    rel = st.get("relationships", {})
    if rel:
        print("Vinculos: " + ", ".join(f"{k} {v.get('bond', 0)}" for k, v in rel.items()))


# ---------------------------------------------------------------- diario / notas
def cmd_log(a):
    st = load_state()
    st["meta"]["turn"] = st["meta"].get("turn", 0) + 1
    entry = f"\n### [S{st['meta'].get('session', 1)} T{st['meta']['turn']}] {today(st)} - {a.type}\n{a.text}\n"
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(entry)
    save_state(st)
    print("Diario atualizado.")


def cmd_note(a):
    with NOTES.open("a", encoding="utf-8") as f:
        f.write(f"- ({datetime.now().strftime('%Y-%m-%d')}) {a.text}\n")
    print("Nota do mestre registrada.")


def cmd_thread(a):
    st = load_state()
    threads = st.setdefault("threads", [])
    if a.action == "add":
        threads.append({"id": a.text, "status": "aberta"})
    elif a.action == "close":
        for t in threads:
            if t["id"] == a.text:
                t["status"] = "resolvida"
    save_state(st)
    for t in threads:
        print(f"[{t['status']}] {t['id']}")


# ---------------------------------------------------------------- saves
def cmd_save(a):
    st = load_state()
    SAVES.mkdir(exist_ok=True)
    name = re.sub(r"[^\w\-]", "_", a.name)
    snap = SAVES / name
    snap.mkdir(exist_ok=True)
    shutil.copy2(STATE, snap / "state.json")
    for f in (JOURNAL, NOTES, DIVERG, HONOR_LEDGER):
        if f.exists():
            shutil.copy2(f, snap / f.name)
    if CHARS.exists():
        shutil.copytree(CHARS, snap / 'characters', dirs_exist_ok=True)
    (snap / "info.txt").write_text(f"{datetime.now().isoformat(timespec='seconds')} | {today(st)} | {st['world'].get('location')}\n", encoding="utf-8")
    print(f"Save '{name}' criado.")


def cmd_load(a):
    snap = SAVES / re.sub(r"[^\w\-]", "_", a.name)
    if not (snap / "state.json").exists():
        die(f"save '{a.name}' nao existe. Veja: python tools/rpg.py saves")
    if STATE.exists():
        AUTO.mkdir(exist_ok=True)
        shutil.copy2(STATE, AUTO / f"pre-load-{datetime.now().strftime('%H%M%S')}.json")
    for f in (STATE, JOURNAL, NOTES, DIVERG, HONOR_LEDGER):
        if (snap / f.name).exists():
            shutil.copy2(snap / f.name, f)
    if (snap / 'characters').exists():
        shutil.copytree(snap / 'characters', CHARS, dirs_exist_ok=True)
    print(f"Save '{a.name}' carregado. Rode `resume` para o briefing.")


def cmd_saves(a):
    if not SAVES.exists():
        print("Nenhum save manual.")
        return
    for d in sorted(p for p in SAVES.iterdir() if p.is_dir()):
        info = (d / "info.txt").read_text(encoding="utf-8").strip() if (d / "info.txt").exists() else ""
        print(f"{d.name}: {info}")


# ---------------------------------------------------------------- canone
def load_canon():
    return json.loads(CANON.read_text(encoding="utf-8"))


def canon_by_id():
    return {e["id"]: e for e in load_canon()}


def sync_canon(st):
    ev = st.setdefault("canon_events", {})
    for e in load_canon():
        ev.setdefault(e["id"], {"status": "pending"})
    return ev


def fmt_event(e, status=None):
    hinge = "*" * e.get("hinge", 1)
    s = f" [{status}]" if status else ""
    return f"{e['order']:>3} {e['id']} {hinge} ({e['date']}) {e['title']}{s}"


def cmd_canon(a):
    st = load_state()
    ev = sync_canon(st)
    events = load_canon()
    if a.action == "list":
        for e in events:
            if not a.arg or a.arg.lower() in e["arc"].lower():
                print(fmt_event(e, ev[e["id"]]["status"]))
    elif a.action == "show":
        e = canon_by_id().get(a.arg) or die("evento inexistente")
        print(json.dumps({**e, "estado": ev[e["id"]]}, ensure_ascii=False, indent=2))
    elif a.action == "next":
        pend = [e for e in events if ev[e["id"]]["status"] in ("pending", "at_risk")]
        for e in pend[: int(a.arg or 5)]:
            print(fmt_event(e, ev[e["id"]]["status"]))
            comp = [n for n in e.get("key_npcs", []) if st.get("npcs", {}).get(n, {}).get("status", "vivo") not in ALIVE]
            if comp:
                print(f"     !! ator-chave comprometido: {', '.join(comp)} -> adapte ou registre divergencia")
    save_state(st)


def cmd_event(a):
    st = load_state()
    ev = sync_canon(st)
    if a.id not in ev:
        die("evento inexistente (veja `canon list`)")
    if a.status not in ("pending", "canon", "diverged", "prevented", "delayed", "accelerated", "at_risk"):
        die("status invalido")
    ev[a.id]["status"] = a.status
    if a.note:
        ev[a.id]["note"] = a.note
    ev[a.id]["when"] = today(st)
    save_state(st)
    print(f"{a.id}: {a.status}")


def cmd_diverge(a):
    st = load_state()
    ev = sync_canon(st)
    cb = canon_by_id()
    if a.event:
        if a.event not in ev:
            die("evento inexistente")
        ev[a.event]["status"] = "diverged"
        ev[a.event]["note"] = a.effect
    ripple = [r for r in (a.ripple or "").split(",") if r]
    for r in ripple:
        if r not in ev:
            die(f"evento de efeito cascata inexistente: {r}")
        if ev[r]["status"] == "pending":
            ev[r]["status"] = "at_risk"
    entry = {"title": a.title, "event": a.event, "cause": a.cause, "effect": a.effect, "ripple": ripple, "date": today(st)}
    st.setdefault("divergences", []).append(entry)
    with DIVERG.open("a", encoding="utf-8") as f:
        f.write(f"\n## {a.title}  ({today(st)})\n- Evento canonico: {a.event and cb[a.event]['title']}\n"
                f"- Causa (acao do jogador): {a.cause}\n- Resultado: {a.effect}\n- Efeitos em cadeia: {', '.join(ripple) or '-'}\n")
    save_state(st)
    print(f"Divergencia registrada: {a.title}. Eventos em risco: {', '.join(ripple) or '-'}")


# ---------------------------------------------------------------- combate
def cmd_combat(a):
    st = load_state()
    c = st.get("combat")
    if a.action == "start":
        st["combat"] = {"round": 1, "turn": 0, "order": []}
        print("Combate iniciado (rodada 1). Adicione combatentes com `combat add`.")
    elif not c:
        die("nao ha combate ativo")
    elif a.action == "add":
        name = a.name
        if name == "player":
            p = st["player"]
            hp, mod, team, df = p["hp"]["cur"], p["attrs"]["AGI"], "ally", 10 + p["attrs"]["AGI"]
        else:
            hp, mod, team, df = a.hp, a.init_mod, a.team, a.defense
        init = RNG.randint(1, 20) + mod
        c["order"].append({"name": name, "init": init, "hp": hp, "max": hp, "team": team, "def": df})
        c["order"].sort(key=lambda x: -x["init"])
        print(f"{name}: iniciativa {init}")
    elif a.action == "hit":
        tgt = next((x for x in c["order"] if x["name"] == a.name), None) or die("combatente nao encontrado")
        dmg = int(a.hp)
        if a.name == "player":
            p = st["player"]
            p["hp"]["cur"] = max(0, min(p["hp"]["max"], p["hp"]["cur"] - dmg))
            tgt["hp"] = p["hp"]["cur"]
        else:
            tgt["hp"] = max(0, min(tgt["max"], tgt["hp"] - dmg))
        print(f"{a.name}: HP {tgt['hp']}/{tgt['max']}" + ("  -> FORA DE COMBATE" if tgt["hp"] == 0 else ""))
    elif a.action == "remove":
        c["order"] = [x for x in c["order"] if x["name"] != a.name]
    elif a.action == "next":
        live = [x for x in c["order"] if x["hp"] > 0]
        if not live:
            die("ninguem em pe")
        c["turn"] += 1
        if c["turn"] >= len(c["order"]):
            c["turn"], c["round"] = 0, c["round"] + 1
            print(f"=== RODADA {c['round']} ===")
        while c["order"][c["turn"]]["hp"] <= 0:
            c["turn"] = (c["turn"] + 1) % len(c["order"])
        print(f"Vez de: {c['order'][c['turn']]['name']}")
    elif a.action == "end":
        st["combat"] = None
        print("Combate encerrado.")
        save_state(st)
        return
    if st.get("combat"):
        c = st["combat"]
        print(f"-- Rodada {c['round']} --")
        for i, x in enumerate(c["order"]):
            mark = ">" if i == c["turn"] else " "
            print(f"{mark} {x['init']:>2} {x['name']:<18} {x['team']:<5} HP {x['hp']}/{x['max']} DEF {x['def']}")
    save_state(st)



# ---------------------------------------------------------------- personagens, honra, reputacao
def honor_tier(v):
    return ("Lendario" if v >= 8 else "Honrado" if v >= 5 else "Integro" if v >= 2 else "Neutro" if v >= -1
            else "Questionavel" if v >= -4 else "Desonrado" if v >= -7 else "Sem Honra")


def rep_tier(v):
    return ("Icone" if v >= 8 else "Admirado" if v >= 5 else "Bem visto" if v >= 2 else "Desconhecido" if v >= -1
            else "Mal visto" if v >= -4 else "Temido/Odiado" if v >= -7 else "Infame")


def find_char(st, who):
    if who in ("player", "pj"):
        return st["player"], "player"
    if who not in st.get("npcs", {}):
        die(f"personagem '{who}' nao existe. Veja `char list` ou crie com `char add`.")
    return st["npcs"][who], who


def hist_add(who, entry):
    CHARS.mkdir(parents=True, exist_ok=True)
    entry["at"] = datetime.now().isoformat(timespec="seconds")
    with (CHARS / f"{who}.history.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def mirror_characters(st):
    """Grava um arquivo por personagem (inclusive o do jogador) em campaign/characters/."""
    CHARS.mkdir(exist_ok=True)
    recs = {"player": st["player"], **st.get("npcs", {})}
    for who, rec in recs.items():
        (CHARS / f"{who}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_honor(a):
    st = load_state()
    rec, who = find_char(st, a.who)
    out = []
    for field, delta in (("honor", a.delta), ("reputation", a.rep)):
        if not delta:
            continue
        old = rec.get(field, 0)
        new = max(-10, min(10, old + delta))
        rec[field] = new
        tier = honor_tier if field == "honor" else rep_tier
        mark = f"  >>> NOVA FAIXA: {tier(old)} -> {tier(new)} (veja rules/08-honra-e-personagens.md)" if tier(old) != tier(new) else ""
        out.append(f"{who} {field}: {old:+d} -> {new:+d} [{tier(new)}]{mark}")
        entry = {"who": who, "field": field, "delta": new - old, "value": new, "reason": a.reason, "date": today(st)}
        st.setdefault("honor_log", []).append(entry)
        hist_add(who, entry)
        with HONOR_LEDGER.open("a", encoding="utf-8") as f:
            f.write(f"- {today(st)} | {who} | {field} {new - old:+d} (agora {new:+d}) | {a.reason}\n")
    st["honor_log"] = st.get("honor_log", [])[-200:]
    save_state(st)
    print("\n".join(out) or "Nada alterado (informe delta e/ou --rep).")


def char_line(who, rec):
    return (f"{who:<14} {rec.get('status', 'vivo'):<12} honra {rec.get('honor', 0):+d} {honor_tier(rec.get('honor', 0)):<12} "
            f"rep {rec.get('reputation', 0):+d} {rep_tier(rec.get('reputation', 0)):<13} {rec.get('location', '') or '-'}")


def cmd_char(a):
    st = load_state()
    npcs = st.setdefault("npcs", {})
    if a.action == "list":
        print(char_line("player", st["player"]))
        for who, rec in npcs.items():
            if not a.arg or a.arg.lower() in (rec.get("role", "") + who + rec.get("status", "")).lower():
                print(char_line(who, rec))
    elif a.action == "show":
        rec, who = find_char(st, a.arg)
        print(json.dumps(rec, ensure_ascii=False, indent=2))
        rel = st.get("relationships", {}).get(who)
        if rel:
            print("Relacao com o PJ:", json.dumps(rel, ensure_ascii=False))
    elif a.action == "add":
        if not a.arg or a.arg in npcs:
            die("informe um id novo (ou ele ja existe)")
        npcs[a.arg] = {"name": a.name or a.arg, "role": a.role, "quirk": a.quirk, "honor": a.honor, "reputation": a.rep,
                       "traits": [t for t in (a.traits or "").split(",") if t], "status": "vivo",
                       "location": a.location, "notes": a.note}
        print(f"Personagem '{a.arg}' criado.")
    elif a.action == "status":
        rec, who = find_char(st, a.arg)
        old = rec.get("status", "vivo")
        rec["status"] = a.value
        if a.note:
            rec["notes"] = (rec.get("notes", "") + f" [{today(st)}] {a.note}").strip()
        hist_add(who, {"field": "status", "from": old, "to": a.value, "reason": a.note, "date": today(st)})
        print(f"{who}: {old} -> {a.value}. Se isto afeta eventos futuros, use `canon next` e `diverge`.")
    elif a.action == "history":
        f = CHARS / f"{a.arg}.history.jsonl"
        print(f.read_text(encoding="utf-8") if f.exists() else "(sem historico)")
    save_state(st)


# ---------------------------------------------------------------- briefing
def tail_entries(path, n):
    if not path.exists():
        return []
    chunks = path.read_text(encoding="utf-8").split("\n### ")[1:]
    return ["### " + c.strip() for c in chunks[-n:]]


def cmd_resume(a):
    st = load_state()
    if a.new_session:
        st["meta"]["session"] = st["meta"].get("session", 1) + 1
        save_state(st)
    m = st["meta"]
    print(f"##### BRIEFING | {m.get('campaign_name')} | sessao {m.get('session')} | modo {m.get('difficulty')} | rev {m.get('revision')}")
    cmd_status(a)
    print("\n--- Ultimas entradas do diario ---")
    for e in tail_entries(JOURNAL, 5) or ["(vazio)"]:
        print(e + "\n")
    print("--- Linhas abertas ---")
    for t in st.get("threads", []):
        if t["status"] == "aberta":
            print(f"* {t['id']}")
    print("\n--- Divergencias ativas ---")
    for d in st.get("divergences", []) or []:
        print(f"* {d['title']}: {d['effect']}")
    print("\n--- Proximos eventos canonicos ---")
    a.action, a.arg = "next", "5"
    ev = sync_canon(st)
    for e in [e for e in load_canon() if ev[e["id"]]["status"] in ("pending", "at_risk")][:5]:
        print(fmt_event(e, ev[e["id"]]["status"]))
    if NOTES.exists():
        print("\n--- Notas do mestre (fim do arquivo) ---")
        print("\n".join(NOTES.read_text(encoding="utf-8").splitlines()[-25:]))
    if st.get("combat"):
        print("\n!! COMBATE ATIVO: `python tools/rpg.py combat show`")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, help_):
        sp = sub.add_parser(name, help=help_)
        sp.set_defaults(fn=fn)
        return sp

    sp = add("new", cmd_new, "cria uma campanha nova")
    sp.add_argument("--force", action="store_true")

    sp = add("roll", cmd_roll, "rola uma expressao: 2d6+3, d20+7")
    sp.add_argument("expr")
    sp.add_argument("--adv", action="store_true")
    sp.add_argument("--dis", action="store_true")
    sp.add_argument("--label", default="")

    sp = add("check", cmd_check, "teste do jogador: d20 + atributo + pericia (+mod) vs DC")
    sp.add_argument("attr", help="FOR AGI VIG INT PER CAR")
    sp.add_argument("--skill")
    sp.add_argument("--dc", type=int)
    sp.add_argument("--mod", type=int, default=0)
    sp.add_argument("--adv", action="store_true")
    sp.add_argument("--dis", action="store_true")
    sp.add_argument("--label", default="")

    add("status", cmd_status, "ficha resumida").set_defaults(fn=cmd_status)
    sp = add("resume", cmd_resume, "briefing de retomada (use no inicio da sessao)")
    sp.add_argument("--new-session", action="store_true")

    sp = add("get", cmd_get, "le um valor do estado")
    sp.add_argument("path")
    sp = add("set", cmd_set, "define um valor (JSON ou texto)")
    sp.add_argument("path")
    sp.add_argument("value")
    sp = add("add", cmd_add, "soma ao valor numerico (recursos .cur sao limitados a 0..max)")
    sp.add_argument("path")
    sp.add_argument("delta")
    sp = add("push", cmd_push, "adiciona item a uma lista")
    sp.add_argument("path")
    sp.add_argument("value")
    sp = add("pull", cmd_pull, "remove item de uma lista")
    sp.add_argument("path")
    sp.add_argument("value")
    for nm, path in (("hp", "player.hp.cur"), ("est", "player.est.cur"), ("det", "player.det.cur")):
        sp = add(nm, resource_cmd(path), f"ajusta {nm.upper()} do jogador (ex: {nm} -5)")
        sp.add_argument("delta")

    sp = add("xp", cmd_xp, "concede XP")
    sp.add_argument("amount", type=int)
    sp = add("time", cmd_time, "atualiza data/hora/local")
    sp.add_argument("date")
    sp.add_argument("--tod")
    sp.add_argument("--location")

    sp = add("log", cmd_log, "escreve no diario")
    sp.add_argument("text")
    sp.add_argument("--type", default="cena")
    sp = add("note", cmd_note, "nota secreta do mestre")
    sp.add_argument("text")
    sp = add("thread", cmd_thread, "linhas narrativas abertas: add|close|list")
    sp.add_argument("action", choices=["add", "close", "list"])
    sp.add_argument("text", nargs="?", default="")

    sp = add("save", cmd_save, "cria save nomeado")
    sp.add_argument("name")
    sp = add("load", cmd_load, "carrega um save")
    sp.add_argument("name")
    add("saves", cmd_saves, "lista saves")

    sp = add("canon", cmd_canon, "consulta o canone: list [arco] | show ID | next [N]")
    sp.add_argument("action", choices=["list", "show", "next"])
    sp.add_argument("arg", nargs="?")
    sp = add("event", cmd_event, "marca o destino de um evento canonico")
    sp.add_argument("id")
    sp.add_argument("status")
    sp.add_argument("--note")
    sp = add("diverge", cmd_diverge, "registra uma divergencia do canone")
    sp.add_argument("title")
    sp.add_argument("--event")
    sp.add_argument("--cause", required=True)
    sp.add_argument("--effect", required=True)
    sp.add_argument("--ripple", help="ids separados por virgula")

    sp = add("honor", cmd_honor, "altera honra/reputacao: honor <quem|player> <delta> motivo [--rep N]")
    sp.add_argument("who")
    sp.add_argument("delta", type=int)
    sp.add_argument("reason")
    sp.add_argument("--rep", type=int, default=0)

    sp = add("char", cmd_char, "personagens: list [filtro] | show ID | add ID | status ID VALOR | history ID")
    sp.add_argument("action", choices=["list", "show", "add", "status", "history"])
    sp.add_argument("arg", nargs="?")
    sp.add_argument("value", nargs="?")
    sp.add_argument("--name", default="")
    sp.add_argument("--role", default="")
    sp.add_argument("--quirk", default="")
    sp.add_argument("--honor", type=int, default=0)
    sp.add_argument("--rep", type=int, default=0)
    sp.add_argument("--traits", default="")
    sp.add_argument("--location", default="")
    sp.add_argument("--note", default="")

    sp = add("combat", cmd_combat, "rastreador: start|add|hit|next|remove|end|show")
    sp.add_argument("action", choices=["start", "add", "hit", "next", "remove", "end", "show"])
    sp.add_argument("name", nargs="?")
    sp.add_argument("hp", nargs="?", help="para `hit`: dano (negativo cura)")
    sp.add_argument("--hp", dest="hp_opt", type=int, default=30)
    sp.add_argument("--init-mod", type=int, default=3)
    sp.add_argument("--team", default="enemy")
    sp.add_argument("--defense", type=int, default=12)

    a = ap.parse_args()
    if a.cmd == "combat":
        if a.action == "add":
            a.hp = a.hp_opt if a.hp in (None, "") else int(a.hp)
    a.fn(a)


if __name__ == "__main__":
    main()
