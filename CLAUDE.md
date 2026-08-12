# CLAUDE.md — donor-impact-site

Project owner: Nadia Serrano. Built for Syndara Module 5.

## What this project is

Two separate parts that share one repository. They do not depend on each other and should not be edited together.

**Part 1: the donor-impact website.** A one-page site built with Astro, generated from the facts in
`impact-notes.txt`. Nothing on the page may state a figure that is not in that file.

**Part 2: the receipts cleanup tool.** A Python command-line script living in `/tools`, using the
**standard library only** (`csv`, `re`, `datetime`, `argparse`). No pandas. No pip installs. It reads a
messy receipts CSV and writes a cleaned one.

## Design direction for the site

Warm and human. This is a letter from a neighbour, not a product launch.

- Avoid tech-startup blues, purple gradients, and glassmorphism.
- Warm neutrals and a muted accent. Generous whitespace. Real sentences over slogans.
- Image placeholders only. Do not fetch remote images.
- Must be readable on a phone.

## Rules

1. **Never delete or overwrite my source files without asking.** `impact-notes.txt` and anything under
   `receipts/` are inputs, not workspace. Read them, do not rewrite them.
2. **Keep every change tightly scoped to what I asked for.** If I say "only the hero section," change only
   the hero section. Do not tidy adjacent code, rename things, or reformat files I did not mention.
3. **Plain-language comments.** I do not write code. A comment should say what a block does and why, in
   ordinary words, not restate the syntax.
4. **Show the plan before building.** For anything beyond a one-line edit, list the files you will touch
   and what you will do to each, then wait.
5. **Ask before running anything that installs, deletes, or reaches the network.**

## Content rules inherited from the brand voice guide

These apply to any copy that appears on the site.

- Every dollar figure comes from `impact-notes.txt`. If a figure is not there, write `[FIGURE NEEDED]` and
  stop. Never estimate, never round, never carry a number over from somewhere else.
- Banned words: synergy, leverage (as a verb), utilize, impactful, world-class.
- Address the reader as "you." No third-person "our donors" on a supporter-facing page.
- Never name an individual donor or the size of their gift.
- Never claim an outcome for money that has not been spent. Say what it paid for.
- US English, serial comma, dates as "October 14, 2026."

## Honesty note that must stay on the site

Riverside Commons Community Fund is a **fictional organization** and every figure is **invented for
coursework**. The published page carries a footer saying so. Do not remove it. This page is publicly
reachable, and a public page showing invented donation totals without that line would be misleading.
