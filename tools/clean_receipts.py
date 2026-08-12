#!/usr/bin/env python3
"""Clean a messy expense-receipts CSV.

Nadia runs this once a month against whatever the three staff members send in. It reads a messy
CSV and writes a tidy one, then prints a short summary of what it changed so she can sanity-check
the result instead of trusting it blindly.

Standard library only. No pandas, nothing to install.

    python tools/clean_receipts.py receipts/messy-receipts.csv receipts/cleaned-receipts.csv
"""

import argparse
import csv
import re
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Header names
# ---------------------------------------------------------------------------

def normalize_header(name):
    """Turn a header like '  Vendor Name ' or 'AMOUNT' into 'vendor_name' / 'amount'.

    Staff export these files from different tools, so the same column arrives capitalized three
    different ways. Everything downstream expects one predictable spelling.
    """
    if name is None:
        return ""
    cleaned = name.strip().lower()
    # Anything that is not a letter or digit becomes an underscore: spaces, dashes, slashes.
    cleaned = re.sub(r"[^a-z0-9]+", "_", cleaned)
    return cleaned.strip("_")


# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------

# Tried in order. The first one that parses wins, so put the unambiguous formats first.
DATE_FORMATS = [
    "%Y-%m-%d",      # 2026-03-14
    "%Y/%m/%d",      # 2026/03/14
    "%d-%b-%Y",      # 14-Mar-2026
    "%d %b %Y",      # 14 Mar 2026
    "%b %d, %Y",     # Mar 14, 2026
    "%B %d, %Y",     # March 14, 2026
    "%d %B %Y",      # 14 March 2026
    "%m/%d/%Y",      # 03/14/2026  (US order, which is what our staff use)
    "%m-%d-%Y",      # 03-14-2026
    "%m/%d/%y",      # 03/14/26
    "%m-%d-%y",      # 03-14-26
    "%d.%m.%Y",      # 14.03.2026
]


def normalize_date(value):
    """Return an ISO date string (YYYY-MM-DD), or None if the value cannot be read as a date.

    A value we cannot parse is left alone rather than guessed at, and it gets counted in the
    summary so nothing disappears quietly.
    """
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Amounts
# ---------------------------------------------------------------------------

# Finds the first number in a string, allowing thousands commas and decimals.
# It deliberately ignores everything around the number, so "$45.00", "USD 12", and
# "9.5 dollars" all give up their figure.
AMOUNT_PATTERN = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


# A single comma followed by exactly two digits, with no decimal point anywhere: '45,00'.
# US thousands separators always have THREE digits after the comma ('1,234'), so two digits is
# the giveaway that the comma is being used as a decimal point.
DECIMAL_COMMA_PATTERN = re.compile(r"^\d+,\d{2}$")


def normalize_amount(value):
    """Pull a plain number out of an amount cell, or return None if there is no number in it.

    Handles: '$45.00', 'USD 12', '9.5 dollars', '1,234.56', '(45.00)' for a negative, and a
    trailing minus like '45.00-' that some accounting exports produce.

    Returns a (amount_string, assumed_decimal_comma) pair so the caller can report the one case
    where the tool had to make a judgement call.
    """
    if value is None:
        return None, False
    text = value.strip()
    if not text:
        return None, False

    # Accountants write negatives in parentheses, and some systems put the minus on the end.
    is_negative = (text.startswith("(") and text.endswith(")")) or text.rstrip().endswith("-")

    match = AMOUNT_PATTERN.search(text)
    if not match:
        return None, False

    raw = match.group(0)

    # '45,00' means forty-five, not four thousand five hundred. Getting this wrong is a 100x
    # error in an accounting file, and it fails silently, so it is worth the special case.
    assumed_decimal_comma = bool(DECIMAL_COMMA_PATTERN.match(raw))
    if assumed_decimal_comma:
        number = raw.replace(",", ".")
    else:
        number = raw.replace(",", "")

    try:
        amount = float(number)
    except ValueError:
        return None, False

    if is_negative:
        amount = -abs(amount)

    # Money, so always two decimal places.
    return f"{amount:.2f}", assumed_decimal_comma


# ---------------------------------------------------------------------------
# The main pass
# ---------------------------------------------------------------------------

def clean(input_path, output_path):
    with open(input_path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        rows = list(reader)

    if not rows:
        print(f"'{input_path}' is empty. Nothing to do.")
        return 1

    headers = [normalize_header(h) for h in rows[0]]
    data_rows = rows[1:]

    rows_in = len(data_rows)
    blanks_removed = 0
    duplicates_removed = 0
    amounts_parsed = 0
    amounts_unparsed = 0
    decimal_comma_assumptions = 0
    dates_parsed = 0
    dates_unparsed = 0

    # Which columns to treat as a date and as money. Matching on the normalized header means we
    # do not care how the sender capitalized it.
    date_columns = {i for i, h in enumerate(headers) if h in ("date", "transaction_date", "receipt_date")}
    amount_columns = {i for i, h in enumerate(headers) if h in ("amount", "total", "cost", "value")}

    seen = set()
    cleaned_rows = []

    for row in data_rows:
        # Pad or trim so a short row does not throw an index error later.
        row = (row + [""] * len(headers))[: len(headers)]

        # 1. Trim whitespace off every field. This alone fixes the trailing spaces in vendor names.
        row = [(cell or "").strip() for cell in row]

        # 2. Drop rows where every single field is empty.
        if not any(row):
            blanks_removed += 1
            continue

        # 3. Remove exact duplicates. The check runs on the trimmed row, so two rows that differ
        #    only by trailing spaces count as the same row, which is what we want.
        fingerprint = tuple(row)
        if fingerprint in seen:
            duplicates_removed += 1
            continue
        seen.add(fingerprint)

        # 4. Normalize dates.
        for i in date_columns:
            iso = normalize_date(row[i])
            if iso:
                row[i] = iso
                dates_parsed += 1
            elif row[i]:
                dates_unparsed += 1

        # 5. Normalize amounts.
        for i in amount_columns:
            number, assumed_comma = normalize_amount(row[i])
            if number is not None:
                row[i] = number
                amounts_parsed += 1
                if assumed_comma:
                    decimal_comma_assumptions += 1
            elif row[i]:
                amounts_unparsed += 1

        cleaned_rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    # ---- Summary. Printed so Nadia can check the counts against what she expected. ----
    print(f"Cleaned '{input_path}' -> '{output_path}'")
    print(f"  Rows in:             {rows_in}")
    print(f"  Rows out:            {len(cleaned_rows)}")
    print(f"  Blank rows removed:  {blanks_removed}")
    print(f"  Duplicates removed:  {duplicates_removed}")
    print(f"  Amounts parsed:      {amounts_parsed}")
    print(f"  Dates normalized:    {dates_parsed}")

    # Anything the tool could not read is reported rather than swallowed.
    if amounts_unparsed:
        print(f"  !! Amounts it could NOT read: {amounts_unparsed} (left as-is, check these by hand)")
    if dates_unparsed:
        print(f"  !! Dates it could NOT read:   {dates_unparsed} (left as-is, check these by hand)")

    # A judgement call, not a failure, but Nadia should still see it rather than discover it later.
    if decimal_comma_assumptions:
        print(
            f"  ?? Read {decimal_comma_assumptions} amount(s) like '45,00' as a decimal comma "
            f"(45.00, not 4500.00). Confirm these."
        )

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Clean a messy expense-receipts CSV and report what changed."
    )
    parser.add_argument("input", help="path to the messy CSV")
    parser.add_argument("output", help="path to write the cleaned CSV to")
    args = parser.parse_args()

    try:
        return clean(args.input, args.output)
    except FileNotFoundError:
        print(f"Could not find '{args.input}'. Check the path and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
