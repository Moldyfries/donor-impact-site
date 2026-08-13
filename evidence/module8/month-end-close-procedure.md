# Month-End Close Procedure and Summary Format

Owner: Nadia Serrano, Accounting Assistant. Reviewer: Controller. Runs on the 3rd working day.

## Inputs

1. Bank export for the month (CSV: date, description, amount, type)
2. Vendor invoices received that month
3. Expense receipts submitted by staff
4. Prior month's summary, for comparison

## The output the Controller expects

A single summary with **exactly these five sections, in this order**:

1. **Header line:** `Month-End Summary: <Month> <Year>` plus the preparation date.
2. **Revenue by account**, with a total.
3. **Expense by account**, with a total.
4. **Net operating result**, revenue total minus expense total.
5. **Exceptions and open questions**, numbered. This section is never omitted. If it is empty, write
   "No exceptions" explicitly so the Controller knows the check ran.

## Non-negotiable rules

- **Every line traces to a source document.** Each figure in the summary must name the bank row, invoice
  number, or receipt it came from. A figure with no traceable source is not reported as a figure; it goes
  in Exceptions.
- **Never invent an account.** If the transaction does not map cleanly to the chart of accounts, mark it
  `UNCATEGORIZED` and list it in Exceptions with what would be needed to resolve it.
- **Never net things together to make the sheet look tidy.** A mixed deposit is split or it is an exception.
- **Never estimate.** If a figure is partially supported, report the supported part and put the remainder
  in Exceptions.
- **Amounts to the cent.** No rounding anywhere.
- The summary is a **draft for the Controller**, never a filing. It carries the line
  "Prepared by Nadia Serrano with AI assistance. Figures not yet reviewed."

## What must never be pasted into the tool

Full bank account numbers, routing numbers, resident names attached to assistance amounts, and any
resident health or hardship detail. Redact to the last four digits before the export goes anywhere.
