# Ferramentas usadas (e opções)

Pesquisa feita para montar o perfil. Tudo gratuito e sem precisar de servidor
próprio.

## O que está no kit

| Ferramenta | Para quê | Link |
| --- | --- | --- |
| **github-readme-stats** | Card de stats + linguagens | https://github.com/anuraghazra/github-readme-stats |
| **github-readme-streak-stats** | Sequência de contribuições | https://github.com/DenverCoder1/github-readme-streak-stats |
| **readme-typing-svg** | Texto animado do topo | https://github.com/DenverCoder1/readme-typing-svg |
| **github-profile-3d-contrib** | Gráfico de contribuições em 3D | https://github.com/yoshi389111/github-profile-3d-contrib |
| **Platane/snk** | Cobrinha comendo o gráfico | https://github.com/Platane/snk |
| **shields.io** | Badges (seguidores, commit, status) | https://shields.io |
| **komarev views** | Contador de visitas | https://github.com/antonkomarev/github-profile-views-counter |
| **skillicons.dev** | Ícones da stack | https://skillicons.dev |
| **PokeAPI/sprites** | Sprites pixel (GIF/PNG) | https://github.com/PokeAPI/sprites |
| **Pokémon Showdown sprites** | Formas animadas (Mega/Ash/Speed) | https://play.pokemonshowdown.com/sprites/ |
| **GitHub Actions** | Atualiza 3D e snake todo dia | https://docs.github.com/actions |

### Versões / detalhes

- **3d-contrib**: usei `yoshi389111/github-profile-3d-contrib@v0.9.3`
  (release de jun/2026). Temas: `profile-night-green.svg`,
  `profile-night-view.svg`, `profile-night-rainbow.svg`, `profile-green.svg`,
  `profile-season.svg`, `profile-gitblock.svg`, etc.
- **snk**: `Platane/snk/svg-only@v3`. Aceita `color_snake` e `color_dots`
  (5 cores: zero contribuição + 4 níveis). Usei ciano/verde no tema dark.
- **github-readme-stats**: tema customizado via `bg_color=05070F`,
  `title_color=00E5FF`, `icon_color=3DDC97`, `text_color=E6F7FF`.
- **readme-typing-svg**: `font=Fira+Code`, cor `00E5FF`, tamanho 20.
- **Sprites animados**: GIFs do Showdown/PokeAPI em `tools/anim/` (Mega Rayquaza,
  Deoxys Speed, Mega Sceptile e Ash-Greninja). Eles têm entre 47 e 119 frames e
  são embutidos em base64 nos SVGs — o movimento aparece no navegador. Os PNGs
  em `tools/sprites/` são o primeiro frame, usados como fallback estático.
- **Banner**: `banner.svg` na raiz, gerado por `banner()` no script. O README
  aponta para `./banner.svg`; os demais SVGs ficam em `assets/`.
- **Nome**: fonte pixel customizada 7×9 (`FONT_BIG`) desenhada em camadas para
  o 3D, com brilho animado e flutuação lateral/vertical. Não depende de fonte
  externa. A frase do Stan Lee corre num ticker abaixo do nome, com palavras
  em fontes e cores diferentes.
- **Quote**: card SVG com animação de entrada, fontes diferentes (serifada,
  sans, monoespaçada e condensada) e crédito a Stan Lee.

## Extras que valem a pena

| Ferramenta | Para quê |
| --- | --- |
| **lowlighter/metrics** | Card gigante com estatísticas e plugins (mais pesado) |
| **github-readme-activity-graph** | Gráfico de atividade dos últimos dias |
| **github-profile-trophy** | Troféus de marcos (followers, commits, stars) |
| **capsule-render** | Header/wave pronto (não usei porque o banner é artesanal) |
| **GitHubCard** | Designer de card único com vários widgets |
| **CommitPulse** | Cidade 3D isométrica das contribuições |

## Observações

- Os widgets públicos dependem da API do GitHub; em perfis com muito tráfego,
  vale self-host (Vercel) para não estourar rate limit.
- Repositório precisa ser **público** para stats, visitas e streak.
- Sprites de Pokémon são propriedade da Nintendo / Creatures / GAME FREAK.
  Uso fan e não comercial; o crédito está no rodapé do README.
