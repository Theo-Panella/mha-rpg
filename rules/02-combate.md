# 02 — Combate

Combate é cinema: claro, rápido, com stakes e reviravoltas. Use o rastreador: `tools/rpg.py combat start | add | hit | next | end`.

## Estrutura

1. **Início:** `combat start`; `combat add player`; `combat add "Capanga A" --hp 18 --init-mod 2 --defense 11`. Iniciativa = d20 + AGI (NPCs: `--init-mod`).
2. **Turno:** cada combatente tem **1 Ação + 1 Movimento + 1 Reação** (reação: esquiva/bloqueio/ajuda, **1 por rodada**).
   - **Ação:** atacar, usar técnica, empurrar/agarrar, resgatar civil, preparar (concede vantagem no próximo teste), usar item, falar longamente (curto = grátis).
   - **Movimento:** ~10 m (+AGI/2 arredondado p/ baixo). Pode trocar por uma segunda ação **gastando 1 DET**.
3. **Fim de rodada:** aplique condições (fogo, veneno...) e regenere o que o terreno/técnicas indicarem.

## Ataque e Defesa

- **Ataque:** `d20 + Atributo + Perícia` vs **DEF** do alvo.
  - Corpo a corpo: FOR (ou AGI para armas leves/artes marciais) + **Luta**.
  - À distância: AGI ou PER + **Pontaria**.
  - Individualidade: **POT + CTL** (ver `03`). Exemplo: `check FOR --skill Luta --dc <DEF>`. Para ataques de Individualidade use `roll d20+<POT+CTL> --label "..."` ou `check` com `--mod`.
- **DEF = 10 + AGI** (+ bônus de traje/escudo/terreno).
- **Reação de esquiva:** o defensor pode rolar **AGI + Acrobacia** oposta; vale o maior.
- **Acerto crítico:** 20 natural → dano máximo dos dados + **efeito especial** (derruba, atordoa).

## Dano e Resistência

- **Corpo a corpo desarmado:** 1d6 + FOR. **Arma comum:** 1d8 + FOR.
- **Individualidade:** dados de dano por **POT**:

| POT | Dano base |
|---|---|
| 1–2 | 1d6 |
| 3–4 | 2d6 |
| 5–6 | 3d6 |
| 7–8 | 4d6 |
| 9–10 | 5d6 |

  Some **CTL/2** (arredondado para baixo) ao dano. Técnicas fortes custam EST e podem somar +1d6 por 2 EST extras (máx. +2d6).
- **Redução:** subtraia **VIG/2** (arred. baixo) + armadura/traje do alvo. Mínimo de dano 1 para acertos bem-sucedidos.
- **Superior em ataque (margem ≥ 5):** +1d6 de dano ou efeito tático.

## Plus Ultra!

Uma vez por **cena**, o jogador pode declarar **PLUS ULTRA** (gasta **1 DET** + até **3 EST**):
- Um **ataque ou teste** ganha **+5** e conta como sucesso mínimo se a margem for ≥ −4.
- **Custo:** recuo — o PJ sofre **1d6 de dano + 1 ponto de Limite de Individualidade** (veja `03`) ou fica *Exausto* na próxima rodada.
- É a hora de **brilhar**: narre dramaticamente (recomendação: o jogador descreve o que o PJ grita e o que está em jogo).

## 0 de HP

- **Modo Heroico:** o PJ cai inconsciente/KO. A cena segue; o resultado depende do resto da turma e dos vilões. Roll `VIG` DC 14: falha = **Ferimento Grave** (tabela abaixo) por ficar "quebrado".
- **Modo Lenda:** inconsciente e sangrando. Rode VIG DC 12 a cada rodada: 3 falhas = **morte**; 3 sucessos = estabilizado. Alguém pode estabilizar com **Primeiros Socorros** DC 14.
- **Overkill:** dano ≥ HP máximo em um único golpe = incapacitado e **Ferimento Grave automático**.

## Ferimentos Graves (role d6 ou escolha o mais coerente)

1. Costelas fraturadas: −1 FOR/VIG até tratar.
2. Braço (ou perna) quebrado: não usa o membro, **Recovery Girl** cura rápido mas custa tempo.
3. Concussão: desvantagem em INT/PER por 1 semana.
4. Queimadura/Cicatriz: marca visível; +1 em Intimidação, −1 em Persuasão com civis.
5. Trauma: Medo de algo específico; testes de coragem em desvantagem até tratado.
6. Lesão duradoura **de Individualidade**: um Limite da Individualidade piora até tratamento/treino.

Cada Ferimento vai em `player.wounds`. Cicatrizes importantes viram **parte da narrativa permanente** (Todoroki, Iida...).

## Terreno, Posição, Civis

- **Terreno**: cobertura (+2 DEF), altura (vantagem à distância), escuridão (desvantagem de mira), caos urbano (testes de **Resgate** para proteger civis).
- **Civis em perigo** são o coração do herói: o mestre cria **relógios** (2–5 casas) que avançam se o PJ ignorar; resgatar demanda ação **Resgate** DC 12–16.
- **Danos colaterais** afetam **Fama/Credibilidade** (veja `04`).

## Combate com muitos inimigos

- **Capangas (fracos):** 1 acerto = fora de combate; 1 por ataque. Os agrupe em "bandos" com dados de dano coletivo.
- **Elite/Chefe:** possuem **Fases**: a cada ~1/3 do HP, mude a tática, revele uma técnica nova, ou o ambiente se altera.
- **Reviravoltas:** vilões inteligentes **adaptam** suas táticas ao que o PJ usou.

## Rendição, fuga, e vitória

Nem todo combate precisa de KO: **render, fugir, convencer** são resultados válidos. Vilões podem fugir para voltar mais fortes; NPCs ficam marcados pelas lutas.
