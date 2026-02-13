# Known Limitations

## Scope

1. **Uganda only** — Only tracks Uganda EC data currently
2. **Official sources only** — Compares against EC, not media/observers
3. **English only** — No Luganda or other local language support yet
4. **No historical data** — Only 2021 elections forward
5. **Final results only** — Cannot verify claims about vote tallying process

## Accuracy

6. **Entity extraction accuracy** — ~85% for clear text, ~70% for images
7. **Name matching** — Uses fuzzy matching; unusual name spellings may not match
8. **Number parsing** — Handles common formats but may miss unusual notations

## Operational

9. **Lag time** — Updates when we scrape EC (not real-time)
10. **Seed data** — MVP uses pre-loaded data; live scraping not yet active
11. **No rate limiting** — MVP does not rate-limit API requests

## What breaks

- Handwritten results
- Heavy image compression/distortion
- Ambiguous claims without specifics
- Claims about vote tallying process (vs final results)
- Non-English text in images
- Very low resolution screenshots

## What's next

- Multi-language support (Luganda, Swahili)
- Historical election data (2016, 2011)
- SMS interface for feature phones
- Regional expansion (Kenya, Tanzania)
- Live EC data scraping when results pages are available
- Rate limiting and abuse prevention
