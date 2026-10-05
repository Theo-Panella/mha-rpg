# 07 — Cânone e Divergência

Objetivo: o mundo parece a história que o jogador conhece, **até que ele a mude de verdade**. Aí o mundo muda de forma coerente e rastreável.

## 1. Inércia do cânone

Cada evento em `canon/events.json` tem **hinge** (⭐ 1–3):

| Hinge | Significado | Dificuldade de mudar |
|---|---|---|
| ⭐ | evento menor (cena de escola, treino, festival) | acontece como no cânone **ou** muda livremente por ações simples |
| ⭐⭐ | evento importante (Festival Esportivo, Stain) | exige preparação e risco; DC 16–20 |
| ⭐⭐⭐ | evento pivô (USJ, Kamino, Hassaikai, Guerra) | exige **plano real, aliados, informação e custo**; DC 20–30 e/ou várias cenas |

**Prioridade:** *lógica da cena > dados > inércia > "o que o mangá diz".* O cânone é um guia de intenções dos NPCs, não um trilho.

## 2. O que muda o resultado de um evento?

Mudanças são **legítimas** quando o PJ:
- **Sabe** (ou descobre) o que vai acontecer e age antes (info + prova);
- **Está lá** e usa poder/engenhosidade no momento;
- **Altera atores-chave** (salva, mata, convence, recruta, afasta);
- **Altera condições** (terreno, horário, aliados, mídia).

O mestre decide por **testes** (DC pelo hinge e pelo preparo) e por **lógica**. Preparo concede vantagem; falta dele, desvantagem.

## 3. Procedimento de divergência (siga sempre)

1. **Identifique o evento** (`python tools/rpg.py canon show <ID>`).
2. **Resolva** a cena (testes/narração).
3. **Se o desfecho divergiu:** `python tools/rpg.py diverge "<título>" --event <ID> --cause "<ação do PJ>" --effect "<resultado>" --ripple <ID1,ID2>`.
4. **Reescreva o futuro (obrigatório)**: para cada evento ripple, pergunte (a) quem estaria envolvido; (b) quem agora está morto/ferido/mudado; (c) o que os vilões fazem diferente; (d) o que mídia/Comissão/UA fazem; (e) se o evento ainda faz sentido, é adiado, antecipado, cancelado ou substituído.
5. **Registre notas:** `rpg.py note "<o que o mundo agora fará>"` e `rpg.py thread add "<linha aberta>"`.
6. **Atualize NPCs:** `set npcs.<id>.status "morto|ferido|desaparecido|preso|aliado"` etc.
7. **Marque eventos:** `event <ID> <canon|diverged|prevented|delayed|accelerated>`.

## 4. Quando o PJ não interfere

Narre o evento **fielmente** (beats emocionais, falas e momentos icônicos), **com o PJ presente e relevante** (um papel de apoio, um momento próprio de risco/escolha). Marque `event <ID> canon`.

## 5. Efeito borboleta (com regras)

- **Cascata só com causalidade clara.** Ex.: se Nighteye vive, o arco de luto de Mirio muda, e Deku talvez não ganhe o mesmo gatilho emocional para um treino.
- **Contrapesos:** O mundo tem tendência a **reequilibrar**: se o PJ remove uma ameaça, outra ocupa o espaço (vilão alternativo, reorganização da Liga).
- **O PJ é parte do mundo.** Heróis e vilões **reagem** a ele (admiração, rivalidade, recrutamento, ameaça).

## 6. Atores-chave comprometidos

`canon next` mostra `!! ator-chave comprometido` se algum `key_npcs` do evento tem status diferente de vivo/ativo/ferido. Nesse caso: adapte o evento (substituto), adie, ou crie novo evento que cumpra a **função dramática** (a ameaça, o dilema, a revelação).

## 7. Modos de cânone (se o jogador quiser)

- **Fiel (padrão):** como acima.
- **Solto:** o cânone é só pano de fundo; muitos eventos podem não ocorrer.
- **What-if:** o jogador altera um ponto na criação (ex.: Todoroki não vai à UA). Registre como **divergência inicial**.

## 8. Eventos fora da linha do tempo

Inclua **mini-arcos originais** (casos de herói, missões, rivais, vilões novos) entre eventos canônicos, para dar espaço ao PJ. Mantenha-os coerentes com o mundo: deixam marcas, mas não atrapalham pivôs.

## 9. Conhecimento do PJ

O PJ só sabe o que viveu/ouviu. **O jogador sabe mais** (pode conhecer o anime): se usar esse conhecimento, exija **justificativa no mundo** (rumor, investigação, intuição, teste de INT/PER). Se o jogador tentar "prever tudo" sem fundamento, o mundo não coopera: os vilões podem ter planos B.

## 10. Confiança de cada evento

Cada evento em `canon/events.json` tem o campo `confidence`: `confirmado`, `corrigido apos verificacao`, `geral (revisar)`, `sem fonte independente (revisar)` ou `escrito do zero (revisar contra a wiki)`. Nos três últimos casos, **não prometa detalhes de cena ao jogador como se fossem fato**: use a função dramática do evento (quem luta, o que está em jogo, o resultado geral) e adapte. Se o jogador confirmar um detalhe pela wiki ou mangá, corrija o evento no `events.json`.
