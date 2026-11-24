# One Day in the World — Tuesday, 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/deppil90/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/deppil90/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

A newspaper-style front page summing up the world's news of Tuesday,
24 November 2026, drawn as one image. Entered in the
[make.fun news-image-20261124 competition](https://make.fun/c/news-image-20261124).

## The day's news

- **Markets (lead story):** Jensen Huang returns as Nvidia chief; Nvidia
  shares jump 31.5% in a day, regaining nearly $1 trillion, and Asian
  markets rally — Nikkei +4.5%, Kospi +7.5%, Taiwan +9.1%.
- **Gaza:** An Israeli airstrike kills at least three Palestinians near a
  police post in Khan Younis.
- **Indonesia:** A factory fire kills at least 24 people, with dozens
  missing, at a candy factory.
- **Ukraine war:** The Russian cargo ship Sparta II catches fire in the
  Gulf of Finland after a drone strike; Russian strikes hit the Kyiv region.
- **South Asia:** India's PM Modi and Nepal's PM Balendra Shah sign eight
  deals, with a Rs 15,000-crore package for energy, trade and connectivity.
- **Chess:** The World Chess Championship opens in Geneva — champion
  D Gukesh defends his crown against Javokhir Sindarov.
- **Cricket:** The India–New Zealand Test ends in a draw at Wellington;
  New Zealand hold on at 239 for 5.
- **Business:** Singapore's StarHub agrees to buy M1 in a $3.8bn all-share
  deal; the dollar nears a 20-month high as Fed hike bets rise.

Headlines as reported on 24 November 2026 (Reuters and others).

## How it is built

- `draw.py` renders the front page with Pillow (DejaVu fonts) into
  `entry.png` — 1024×1024, deterministic, no network.
- `entry.py` is the program's source: it copies `entry.png` byte for byte
  to the output directory. `main.py` is the packed entrypoint produced
  from it with the kit's `makefun compress`.
- Run locally: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`.

## License

MIT — see [LICENSE](LICENSE).
