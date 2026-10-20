# Setup no GitHub

Kit do perfil **Adriarley** — banner pixel com **Mega Rayquaza**, **Deoxys Speed**,
**Mega Sceptile** e **Ash-Greninja**, nome animado em 3D, terminal com mensagens,
ticker colorido do Stan Lee e widgets automáticos.

## 1. Crie o repositório

O repositório precisa se chamar **exatamente igual ao seu usuário** do GitHub.

Usuário `EuSouEu223` → repositório `EuSouEu223`.

- Público (os cards de status não carregam em repo privado).
- Branch padrão `main`.
- Se ele não existir, crie com "Add a README file".

## 2. Copie os arquivos para a raiz

```
README.md
banner.svg
assets/
.github/
tools/        (opcional, só para regerar a arte)
```

O `preview.html` é só para visualizar localmente — pode deixar de fora.

## 3. Usuário

O README já está configurado com **`EuSouEu223`** nos links, badges, stats,
gráfico 3D e cobrinha. Se mudar de conta, troque `EuSouEu223` pelo novo usuário.

O nome **Adriarley** flutua no banner (sobe, desce e vai para os lados), e a
frase do Stan Lee corre num ticker logo abaixo dele.

## 4. Ative as Actions

`Settings` → `Actions` → `General` → `Workflow permissions` →
**Read and write permissions** → `Save`.

Sem isso os workflows não conseguem publicar os branches das imagens.

## 5. Rode os dois workflows

Na aba `Actions`:

1. **3D contribution graph** → `Run workflow`
2. **Snake** → `Run workflow`

Eles criam os branches:

- `3d-contrib` → `profile-night-green.svg`
- `output` → `github-snake.svg` e `github-snake-dark.svg`

O `README.md` já aponta para esses caminhos.

## 6. Personalize a arte

Tudo é gerado por `tools/make_assets.py`:

- **Banner**: sai como `banner.svg` na raiz do projeto. O README aponta para
  `./banner.svg`; os outros SVGs ficam em `assets/`.
- **Cores**: constantes no topo (`CYAN`, `GREEN`, `LIME`, `GOLD`, `ORANGE`,
  `BLUE`, `RED`).
- **Quem fica em cada canto**: em `banner()`, as chamadas
  `mon_anim("rayquaza", 150, 160, 200, ...)`, `mon_anim("deoxys", 1072, 128, 185, ...)`,
  etc. Os parâmetros são `(nome, centro_x, centro_y, tamanho)`. `flip=True`
  espelha o sprite; `sway="l"` / `"r"` inclina para o centro.
- **Nome**: `name_text = "ADRIARLEY"` em `banner()`. A fonte `FONT_BIG` (7×9) é
  desenhada em camadas para o efeito 3D; o brilho que passa é `.name-shine` e
  o movimento lateral/vertical é `@keyframes nameFloat`.
- **Ticker**: a frase do Stan Lee corre abaixo do nome em `.ticker-track`
  (24s, loop). O texto e o rótulo ficam no bloco `ticker` de `banner()`. Se mudar
  muito o texto, ajuste `translateX(-780px)` e o x da segunda cópia (`1156`)
  para o loop continuar emendado.
- **Terminal**: a lista `lines` em `terminal()` tem `(comando, saída, cor)`.
  As barras de status ficam logo abaixo.
- **Quote**: o texto, as fontes e a animação ficam em `quote()`. A frase é de
  **Stan Lee**.
- **Anime mode**: cena de batalha em `anime_shelf()` (Mega Rayquaza vs Deoxys Speed).
- **Sprites animados**: GIFs em `tools/anim/*.gif` (Showdown/PokeAPI). Os PNGs
  em `tools/sprites/` são o primeiro frame, usados como fallback estático.
  Para trocar, substitua o GIF mantendo o mesmo nome. O script embute os GIFs
  em base64 dentro dos SVGs.

Depois de editar:

```powershell
python tools\make_assets.py
```

Commit os SVGs novos. Se o GitHub cachear, adicione `?v=2` no final da URL da
imagem no README.

## Sprites e direitos

- Fontes: [PokeAPI/sprites](https://github.com/PokeAPI/sprites) e
  [Pokémon Showdown sprites](https://play.pokemonshowdown.com/sprites/).
- Pokémon © Nintendo / Creatures / GAME FREAK.
- Uso **fan, não comercial**. Se quiser 100% original, troque os sprites por
  arte própria — o resto do banner continua funcionando.
- Frase: **Stan Lee** (“If you have an idea that you genuinely think is good,
  don't let some idiot talk you out of it.”).

## Dicas

- O repositório precisa ser público para os cards de stats e visitas.
- O gráfico 3D e a cobrinha só aparecem depois da primeira execução das Actions.
- O banner tem 1200×480, o terminal 1200×300, a quote 1200×230 e o anime mode
  700×240.
- Os SVGs são autocontidos: as animações e os sprites vão dentro do arquivo.
- Os GIFs animam dentro do SVG no navegador; o preview local mostra o movimento.
- Se algum dia o GitHub bloquear as imagens embutidas (raro), troque os sprites
  por `<img>` separados ou gere um PNG do banner com o `preview.html`.
