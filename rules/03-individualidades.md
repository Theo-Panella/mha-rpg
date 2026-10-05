# 03 — Individualidades (Quirks)

## Estatísticas da Individualidade

| Estatística | Faixa | Significado |
|---|---|---|
| **POT** (Potência) | 1–10 | poder bruto; define dados de dano (veja `02`) e EST máx. |
| **CTL** (Controle) | 0–10 | precisão, economia de EST, uso criativo; soma ao ataque (POT+CTL) e ao dano (CTL/2). |

**Criação:** POT e CTL começam em 1 e você distribui **+6 pontos** (ex.: POT 4 / CTL 3). Máximo 6 cada na criação. O **POT 7+** só vem com treino ou arcos específicos.

## Categoria

**Emissão** (projeta/ataca de longe), **Transformação** (altera o corpo por efeitos), **Mutante** (corpo permanentemente diferente, com benefícios e desvantagens). A categoria define só o **sabor**; as regras são as mesmas.

## Limites (obrigatórios!)

Toda Individualidade tem **ao menos 1 Limite**, que o mestre usa **de fato**: cansaço, recuo, tempo de recarga, alcance, ponto fraco, custo no corpo, efeito colateral (ex.: Mina: ácido que corrói o próprio traje; Iida: motor que sobreaquece).

Exemplos:
- **Recuo físico:** técnicas fortes causam dano ao usuário (Deku sem treino).
- **Estamina/Gasto:** recarrega com comida/descanso.
- **Alcance/Condição:** só funciona se tocar, ver, ou com uma condição.
- **Efeito imprevisível ao falhar:** na FALHA CRÍTICA o Limite piora.

**Limite aumenta com Plus Ultra** (ver `02`).

## Técnicas

Comece com **3 técnicas** (podem ter 0–3 de custo EST):

| Nível | Custo EST | Descrição |
|---|---|---|
| Básica | 0–1 | uso corriqueiro, seguro |
| Técnica | 2 | golpe/efeito sólido, +1d6 |
| Especial | 3–4 | marcante, mudar o curso de uma cena |
| Suprema | 5+ | só em clímax; Limite grave e risco real |

Cada técnica é registrada em `player.quirk.moves` como `{"name":..., "cost":..., "effect":...}`. Efeitos: dano, controle de campo, defesa, mobilidade, suporte, utilidade fora de combate.

## Criatividade

Recompense usos criativos (usar a Individualidade em contexto inesperado) com **vantagem** ou **+2**. O PJ **evolui** o poder usando-o (veja treino em `04`), mas nunca "sem custo".

## Balanceamento

Evite Individualidades que anulem todo risco (onisciência, tempo, imortalidade). Se o jogador quer algo assim, **adicione limite pesado** ou reduza escopo. Combos óbvios com personagens canônicos? Funciona, mas gera atenção (de aliados e de vilões).

## Exemplos de arquétipos (inspiração)

- **Gelo/Fogo/Terra** (elementais): versáteis, EST variável.
- **Corpo reforçado/Endurecimento**: tanque, Limite: peso/lentidão.
- **Controle/Manipulação**: alcance, Limite: condição.
- **Sentidos/Rastreamento**: apoio e investigação.
- **Mutante (cauda, asas, fisionomia)**: benefícios fixos + custo social.
- **Suporte (cura, criação)**: custo pessoal alto (Momo come, Recovery Girl cansa).

## A Individualidade como ficha

```
player.quirk = {
  "name": "...", "category": "Emissao|Transformacao|Mutante",
  "description": "...", "pot": 4, "ctl": 3,
  "limits": "...",
  "moves": [{"name":"...","cost":0,"effect":"..."}, ...]
}
```
