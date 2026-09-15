import csv
from io import StringIO


def export_to_csv(
    rows: list[dict],
) -> str:
    if not rows:
        return ""

    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=rows[0].keys(),
    )

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()
