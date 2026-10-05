# MHA — Mestre de RPG no Codex

Um projeto para transformar o **Codex** em mestre de uma campanha solo de *My Hero Academia*, com estado salvo, cânone com divergências, sistema d20 com atributos e narração cinematográfica. Roda 100% dentro da sua sessão do Codex (sem API, sem dependências além do Python 3).

## Como jogar

1. Abra esta pasta no Codex (CLI, IDE ou app) e inicie uma sessão.
2. Cole o conteúdo de [prompts/start.md](prompts/start.md), ou apenas diga: **"Comece o jogo."** O Codex lê o [AGENTS.md](AGENTS.md) automaticamente.
3. Ele conduzirá a criação do personagem e a abertura.
4. Para **continuar depois**, em uma sessão nova diga: **"Continuar a campanha."** Ele roda o briefing e retoma do ponto exato.

## Comandos de jogo (digite no chat)

| Você diz | Ele faz |
|---|---|
| `!ficha` | mostra a ficha |
| `!diario` | resume as últimas cenas |
| `!canon` | mostra o que já divergiu e o que vem aí (sem spoilers pesados se pedir "sem spoilers") |
| `!regras <tema>` | explica uma regra |
| `!salvar <nome>` / `!carregar <nome>` | save manual |
| `!rolar 2d6+3` | rola dados |
| `!recap` | "anteriormente em..." |
| `!pausa` | encerra a sessão salvando |

## Estrutura

```
AGENTS.md        instruções do mestre (o Codex lê isto)
rules/           sistema de jogo, combate, Individualidades, progressão, narração, cânone, honra
canon/           linha do tempo (events.json), personagens-semente (npcs.json), enciclopédia (spoilers!)
campaign/        sua campanha: state.json, diário, notas, divergências, honra, characters/, saves (criada em jogo)
tools/rpg.py     dados, estado, saves, cânone, combate
prompts/         prompts de partida
```

## Ferramenta (opcional, para você também)

```
python tools/rpg.py status            # ficha
python tools/rpg.py resume            # briefing
python tools/rpg.py roll 2d6+3
python tools/rpg.py check FOR --skill Luta --dc 14
python tools/rpg.py canon next        # próximos eventos canônicos
python tools/rpg.py honor player 2 "salvou um civil" --rep 1
python tools/rpg.py char list         # todos os personagens: status, honra, reputação
python tools/rpg.py char show katsuki
python tools/rpg.py char history aizawa
python tools/rpg.py save arco-usj     # save manual
python tools/rpg.py --help
```

## Salvamento

- **Autosave** a cada alteração em `campaign/autosave/` (últimas 25 versões).
- **Saves nomeados** em `campaign/saves/<nome>/` (estado, diário, notas, divergências).
- Tudo em arquivos de texto: dá para copiar a pasta `campaign/` para levar a campanha a outro lugar.

## Honra e personagens

O PJ e os 60 personagens canônicos têm **Honra** (integridade) e **Reputação** (como o mundo os vê), status, local, traços e histórico, salvos em `state.json` e espelhados em `campaign/characters/`. Isso afeta testes sociais, lealdade e traição de NPCs, recrutamento e o epílogo. Regras em [rules/08-honra-e-personagens.md](rules/08-honra-e-personagens.md).

## Reiniciar

`python tools/rpg.py new --force` arquiva a campanha atual em `campaign/saves/` e começa outra.

## Aviso

O arquivo `canon/` contém **spoilers** da história completa. O mestre os usa; evite lê-los se quiser jogar "às cegas". A fidelidade de datas e detalhes é aproximada: o mestre adapta à história da campanha.
