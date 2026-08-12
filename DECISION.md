# Chat or tool? Deciding for the monthly receipt cleanup

For the receipts that arrive every month from three different staff, a reusable tool beats a chat, and
building this one showed me why.

**It runs the same way every time.** A chat re-reads my instructions from scratch each month, and small
changes in how I word them produce small changes in the output. The script applies identical rules to
identical inputs, so February's file is cleaned exactly like January's.

**It reports what it did, and what it was unsure about.** My first version silently turned `45,00` into
`4500.00`, a hundredfold error I only caught by testing edge cases. I fixed the parsing and made the tool
announce that assumption in its summary. A chat would have produced the same wrong number with no way for
me to notice it.

It also runs in seconds on the whole file, with no size limit and no re-explaining.

**When a chat is better:** the one-off. A vendor sends a strangely formatted file once, or I need to
understand what a column means before I decide any rule at all. Judgement calls belong in a conversation.
Repetition belongs in a script.
