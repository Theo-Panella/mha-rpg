# 01 — Sistema Base

Sistema d20 enxuto, feito para solo: poucas regras, muita consequência. Tudo que segue é lei; o script `tools/rpg.py` aplica as contas.

## Atributos (1–10)

| Sigla | Nome | Usos típicos |
|---|---|---|
| FOR | Força | golpes físicos, carregar, quebrar, potência de Individualidades de força |
| AGI | Agilidade | esquiva, iniciativa, acrobacia, furtividade, mira rápida |
| VIG | Vigor | HP, resistir dor/veneno/cansaço, resistência |
| INT | Intelecto | tática, estudo, tecnologia, deduzir |
| PER | Percepção | notar, rastrear, mira, leitura de ambiente e de pessoas |
| CAR | Carisma | persuadir, liderar, inspirar, falar com a mídia |

Escala: **1–2** civil fraco · **3** civil comum · **4–5** aluno da UA (nível de admissão) · **6–7** herói profissional · **8–9** top herói / elite · **10** limite humano/ícone (All Might em seu auge passa disso).

**Criação:** todos os atributos começam em **2**; distribua **+10 pontos** (soma final 22). Máximo **7** na criação. A Individualidade dá **POT** e **CTL** à parte (veja `03`).

## Perícias (0–5)

Atletismo, Acrobacia, Luta, Pontaria, Furtividade, Investigação, Resgate (herói: evacuar, estabilizar, proteger civis), Primeiros Socorros, Tática, Tecnologia, Persuasão, Intimidação, Atuação (mídia/imagem), Sobrevivência, Conhecimento (Individualidades/heróis/história), Liderança, Pilotagem. Outras podem surgir.

**Criação:** **12 pontos** de perícia, máximo **3** por perícia. Perícia **não treinada** = +0 (sem penalidade).
Cada ponto de perícia é um bônus direto.

## O Teste

> **d20 + Atributo + Perícia + modificadores** contra uma **DC** (ou contra o resultado do oponente).

Via script: `python tools/rpg.py check FOR --skill Luta --dc 14 --mod 2`.

**Tabela de DC:** 8 trivial-com-pressão · 10 fácil · 12 comum · 14 desafiador · 16 difícil · 18 muito difícil · 20 heroico · 25 lendário · 30 impossível para um aluno.

**Graus de resultado** (margem = total − DC):

| Margem | Resultado |
|---|---|
| ≥ +5 | **SUCESSO SUPERIOR** (bônus narrativo/mecânico) |
| 0 a +4 | **SUCESSO** |
| −1 a −4 | **PARCIAL** — consegue, mas paga um custo (HP, tempo, posição, informação) |
| ≤ −5 | **FALHA** — o mundo reage |

**20 natural:** sobe um grau (e garante pelo menos sucesso). **1 natural:** desce um grau (e o melhor possível é parcial).

**Vantagem/Desvantagem:** role 2d20, fica com o melhor/pior. Concedida por posição, preparo, ajuda de aliado ou terreno. Não acumula (anulam-se).

**Testes opostos:** ambos rolam (NPC via `roll d20+X`); o maior vence; empate favorece o defensor.

**Ajuda:** um aliado com sentido concede **vantagem**; vínculo ≥ 3 com o aliado também dá +1.

**Testes em grupo/perícia compartilhada:** uma rolagem do PJ, aliados ajudam por narrativa.

## Recursos

| Recurso | Fórmula inicial | Uso |
|---|---|---|
| **HP** | 10 + 6 × VIG | dano físico. Veja `02` para 0 de HP. |
| **EST** (Estamina de Individualidade) | 4 + POT + VIG | técnicas custam EST; regenera em descanso. |
| **DET** (Determinação) | 3 | gaste 1 para **rerrolar** um teste, **+1d6** a um teste, ou **resistir** a uma Condição; recupera em **momentos de vínculo**, vitórias emocionais e 1 por sessão (máx. 3, ou 4 com Vínculo ≥ 4 em algum NPC). |

**Descansos:** *Respirar* (1 min): +2 EST. *Descanso curto* (horas): recupera 1/2 EST e HP/2 se tratado. *Noite de sono*: EST e DET cheios, HP +VIG×2 (ou Recovery Girl: cura rápida, mas **gasta energia do corpo**: sono forçado e fome).

## Condições (lista curta)

Atordoado (desvantagem em tudo, 1 rodada) · Derrubado · Agarrado · Cego · Surdo · Em chamas (1d6/rod.) · Exausto (−2 em tudo, acumula) · Medo · Quirk-dor (limite de Individualidade piorado).

## Tempo e Escalas

Rodadas de ~6 s em combate; cenas livres em minutos; saltos de tempo em dias/semanas para progressão (veja `04`).
