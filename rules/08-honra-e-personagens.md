# 08 — Honra, Reputação e Estado dos Personagens

Todo personagem (o PJ **e** cada NPC, incluindo vilões) tem um registro persistente em `campaign/state.json` (espelhado em `campaign/characters/<id>.json`, com histórico em `<id>.history.jsonl`). A semente vem de `canon/npcs.json`. Isto torna o mundo reativo: o que o PJ faz muda **quem as pessoas são**, não só o que sabem.

## Dois eixos (−10 a +10)

| Eixo | O que mede | Quem enxerga |
|---|---|---|
| **Honra** | **Integridade pessoal**: cumprir a palavra, coragem, misericórdia, lealdade, assumir consequências. Independe de lado: Stain tem código, All For One não. | Os outros sentem em ações; o PJ percebe por convivência. |
| **Reputação** | **Como o mundo vê o personagem** (público, mídia, heróis, submundo). Pode ser injusta. | Todos; afeta portas que se abrem ou fecham. |

Faixas de **Honra**: ≥8 Lendário · 5–7 Honrado · 2–4 Íntegro · −1–1 Neutro · −2–−4 Questionável · −5–−7 Desonrado · ≤−8 Sem Honra.
Faixas de **Reputação**: ≥8 Ícone · 5–7 Admirado · 2–4 Bem visto · −1–1 Desconhecido · −2–−4 Mal visto · −5–−7 Temido/Odiado · ≤−8 Infame.

Comandos:
- `python tools/rpg.py honor player +2 "Protegeu civil à custa de um ferimento" --rep 1`
- `python tools/rpg.py honor katsuki +1 "Admitiu que errou"`
- `python tools/rpg.py char list [filtro]` · `char show <id>` · `char status <id> <vivo|ferido|preso|desaparecido|morto|aliado|traidor|...> --note ".."` · `char history <id>` · `char add <id> --name .. --role ..`
- `player.code` guarda o **Código** do PJ (a regra que ele não quebra); `player.traits` os traços.

## Quando mexer na Honra (guia; valores de −2 a +2; use ±3 só em atos definidores)

| Ato | Honra |
|---|---|
| Arrisca-se para salvar quem não conhece, sem testemunhas | +1 / +2 |
| Cumpre promessa difícil; assume culpa por erro | +1 |
| Poupa inimigo derrotado e rendido; oferece mão ao caído | +1 |
| Age por glória, mente para ganhar vantagem, rouba mérito | −1 |
| Abandona aliado/civil em perigo, quebra promessa | −1 / −2 |
| Tortura, crueldade gratuita, traição de confiança, assassinato | −3 |

Honra muda por **ação demonstrada**, nunca por palavra. Se o jogador toma uma decisão moralmente significativa, **pare e registre**.

## Quando mexer na Reputação

Muda pelo que **os outros veem ou ouvem**: resgate televisionado (+), dano colateral (−), vazamento de segredo, depoimento, mídia, rumores. Um ato heroico anônimo muda **Honra**, não Reputação. Um ato vergonhoso com testemunhas muda **ambos**. Reputação pode ser **diferente por grupo** (`factions.<grupo>.attitude`): um herói pode ser Ícone para civis e Infame para o submundo.

## Efeitos mecânicos (PJ)

**Honra do PJ:**
- **Íntegro (2+):** +1 em testes de Persuasão/Liderança com NPCs de honra ≥ 2. Pode **se negar a quebrar o Código** sem teste.
- **Honrado (5+):** Acima, e **+1 DET máx.** (4). Uma vez por sessão, **Vontade de Ferro**: ignora um efeito de medo/intimidação/lavagem cerebral.
- **Lendário (8+):** Aliados de honra ≥ 5 podem **ajudar sem custo** em momentos pivô; inimigos podem **hesitar** (teste de Honra do NPC, DC 15).
- **Neutro (−1 a 1):** sem efeito.
- **Questionável (−2 a −4):** −1 em Persuasão com heróis/civis honrados; +1 Intimidação.
- **Desonrado (−5 a −7):** −2 com heróis/autoridades; o **submundo** oferece portas (contatos, informações, recrutamento).
- **Sem Honra (≤ −8):** o PJ não recupera DET por vínculos; **vilões o tratam como igual** (e o cobram), heróis o tratam como ameaça. Considere um **arco de queda ou redenção**.

**Reputação do PJ:**
- Aplicada **ao grupo relevante**: ±1 por faixa (Bem visto +1, Admirado +2, Ícone +3; Mal visto −1, Temido −2, Infame −3) em testes **sociais/institucionais** (estágios, licenças, mídia, polícia).
- Reputação alta traz **atenção**: vilões, imprensa, admiradores, rivais.
- Reputação baixa fecha estágios e licenças (**Credibilidade** cai; veja `04`).

## Efeitos nos NPCs (o mundo reage)

- **Honra dos NPCs guia decisões:** NPC com honra alta **recusa** traições e **sacrifica-se**; honra baixa **trai**, foge ou negocia. Em dúvida, o mestre rola `roll d20+<honra do NPC> --label "fidelidade"` contra DC 12–18.
- **Limiares de virada** (considere uma cena e, se houver causa, `diverge`):
  - Aliado ou herói com honra **≤ −4** → pode **trair** ou abandonar.
  - Vilão com honra **≥ 2** e vínculo com o PJ ≥ 3 → possibilidade de **redenção ou deserção** (Twice, Spinner, Dabi, Toga, Gigantomachia podem vir a mudar).
  - Rival com honra **≥ 6** → respeita o PJ, vira **aliado**.
  - NPC com honra **≥ 8** e em perigo → **sacrifício heroico** é plausível.
- **Mudanças de honra dos NPCs também vêm do PJ** (exemplo: Katsuki +1 quando o PJ o trata como igual e ele reconhece).
- **`char status`** registra morte/ferimento/prisão/desaparecimento. O `canon next` avisa quando um evento tem **ator-chave comprometido**. Cada mudança de estado deve ser pensada com `diverge`.

## Efeitos na campanha

- **Finais e epílogo:** o evento Z01 e os finais de arco refletem a **Honra e a Reputação finais** do PJ e das pessoas próximas: o PJ amado/odiado/esquecido, quem sobreviveu e o que a UA se tornou.
- **Recrutamento:** PJ com Honra ≤ −5 recebe **convites** da Liga (Shigaraki), Hassaikai, ELM. Com Honra ≥ 5 e Reputação ≥ 5, **Comissão** e agências o cortejam (estágios, missões).
- **Dilemas obrigatórios (1 por arco):** crie uma situação em que a escolha mais fácil custa Honra e a mais difícil custa recursos. Registre a decisão.
- **Reputação x Cânone:** a reação pública a Kamino, ao fim de All Might, à revelação de Dabi etc. pende para o **lado** onde o PJ está: ajude e o público tende à esperança; falhe e tende ao pânico.

## Rotina do mestre

1. A cada cena marcante: pergunte-se **"alguém mudou por causa do que aconteceu?"** → `honor`, `char status`, `add relationships.<id>.bond`.
2. Ao fim de cada arco: `char list` e revise **quem mudou de faixa**; escreva `note` com as consequências.
3. Antes de eventos canônicos: confira as honras/estados dos `key_npcs` (`char show <id>`).
4. Ao encerrar a sessão: `save <nome>` (os personagens vão junto no `state.json`; os espelhos em `campaign/characters/` ficam como arquivo legível).
