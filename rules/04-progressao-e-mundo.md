# 04 — Progressão, Carreira e Mundo

## XP e Níveis

`python tools/rpg.py xp <N>` concede XP e avisa quando sobe de nível.

| Nível | XP | | Nível | XP |
|---|---|---|---|---|
| 1 | 0 | | 6 | 100 |
| 2 | 10 | | 7 | 140 |
| 3 | 25 | | 8 | 190 |
| 4 | 45 | | 9 | 250 |
| 5 | 70 | | 10 | 320 |

**Ganhos de XP (guia):** cena marcante resolvida **1–2** · vitória em combate importante **2–4** · resgate bem-sucedido **2–3** · avanço emocional/vínculo **1–2** · ideia brilhante/uso criativo **1** · sobrevivência a evento pivô **4–6**.

**Ao subir de nível:** +2 pontos de perícia, +1 técnica nova (ou aprimoramento), **+1 atributo nos níveis pares** (máx. 10), +1 POT ou CTL a cada **3 níveis** (máx. 10, e nunca acima de 6 sem treino/arco justificando). Recalcule HP/EST máximos (veja `01`) e aumente o valor atual proporcionalmente.

## Tempo Livre (Downtime)

Entre arcos (ou ao pular dias), o PJ tem **2 ações de tempo livre por semana**. Escolha:

- **Treinar atributo**: teste de dedicação (DC 12 + atributo atual); sucesso contribui para o próximo nível; custo de tempo e risco de ferimento.
- **Treinar Individualidade/técnica**: com mentor adequado → vantagem; resultado = nova técnica ou limite reduzido.
- **Aprofundar vínculo**: cena social com um NPC → **+1 de vínculo** (máx. 5).
- **Estudar/pesquisar**: INT/PER vs DC; descobre informações sobre vilões, heróis, a UA.
- **Descansar/curar**: reduz condições e Ferimentos Graves.
- **Trabalho de herói**: patrulha ou voluntariado → Fama/Credibilidade.

## Vínculos

`relationships.<npc_id> = {"bond": 0..5, "notes": "..."}`.

| Vínculo | Significado |
|---|---|
| 0 | desconhecido |
| 1 | colega/familiar |
| 2 | amigo |
| 3 | forte aliado: **+1** em ações combinadas, DET-bonus possível |
| 4 | irmão de armas |
| 5 | laço "inquebrável": evento de Plus Ultra compartilhado |

Cada vínculo pode ter **uma promessa** ou **uma ferida**. Quebre-as com consequências.

**Conflito:** vínculos podem **cair** (traição, abandono). Documente em `notes.md`.

## Carreira Heroica

- **Fama** (`player.fame`): reconhecimento público (0–100). Sobe com resgates e vitórias televisionadas; cai com danos colaterais e escândalos.
- **Credibilidade** (`player.credibility`): confiança de heróis/instituições (0–100). Abre portas: estágios, equipamentos, missões, permissão para agir.
- **Grau escolar** (`player.school_rank`): posição da turma, notas, comportamento (afeta recomendações e licenças).
- **Nome de herói** e **traje**: registrados na ficha; o traje pode ter bônus de DEF/EST.
- **Licença Provisória / Licença Profissional:** marcos de autonomia legal. Sem licença, **usar Individualidade em público** é ilegal (consequência: Fama −, Credibilidade −, multa/expulsão).
- **Billboard Chart:** posições e rivalidades apenas para profissionais.

## Equipamento

Itens de apoio (Mei Hatsume): cada item tem **1 bônus** e **1 defeito**. Traje padrão: +1 DEF ou +2 EST. Itens consumíveis são gastos de verdade.

## Mundo e Facções

Mantenha `factions.<nome> = {"attitude": -5..+5, "notes": ""}` para: UA, Comissão de Segurança, Liga dos Vilões, Mídia, Polícia, Yakuza, Sociedade Heróica. Ações do PJ movem essas atitudes. O mundo reage: opinião pública, patrulhas, manchetes, ataques.

## Relógios

Use `flags.relogio_<nome> = {"max": 4, "cur": 1}` para perigos que avançam com o tempo (um incêndio, uma negociação, a ascensão de um vilão). Avance relógios nas falhas e quando o PJ perde tempo.
