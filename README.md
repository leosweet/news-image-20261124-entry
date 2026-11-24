# The World in One Picture — Tuesday 24 November 2026

One image summing up the world news of Tuesday 24 November 2026, built for
make.fun's `news-image-20261124` bounty ($100, 50 paid places).

## What the image shows

A morning snapshot of the day's news so far (built Tuesday morning, Beijing
time), six stories plus three more in the footer strip:

1. **Asia / Security** — A Russian jet enters South Korean airspace; Seoul
   briefly orders Ulleung islanders to take shelter.
2. **Europe / Space** — NATO vows space defence as allies warn Russia may
   launch a satellite weapon next month (German media report).
3. **USA / Politics** — Rep. Jimmy Gomez resigns after a House ethics panel
   finds sexual misconduct.
4. **USA / Tech** — US states sue Musk companies over sexualised images made
   by the AI chatbot Grok.
5. **World / Climate** — COP31 talks stall as negotiators fail to agree a
   cover text, a setback for ocean-climate action.
6. **UK / Courts** — GTA VI hacker Arion Kurtaj, 21, jailed for 7 years but
   walks free on time served after the 2021–22 Rockstar hacks.

Footer: the World Chess Championship title defence opens in Geneva; more
bodies found after the Indonesia candy-factory fire; storms threaten US
Thanksgiving travel.

Every story was first reported on 24 November 2026; nothing is invented,
and reported claims are attributed on the image ("allies warn", "media
report").

## How it was built

- `render.py` draws the 1024×1024 infographic programmatically with
  Python + PIL (DejaVu fonts) — masthead, six story cards with drawn
  pictograms, footer strip. No AI image generation, so no garbled text.
- `main.ts` (Node 22, standard library only, no network) copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. Both runs write
  byte-identical output.

## Sources

Reuters, AP, SCMP, AFP, Japan Times — morning editions of 24 November 2026.
