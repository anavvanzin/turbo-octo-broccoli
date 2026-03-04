"""Parser for the ICONCLASS textbase flat-file format.

Records are separated by ``\\n$`` (a dollar sign on its own line).
Each line within a record has the form ``FIELD value``.  A line that
starts with ``;`` is a continuation value for the most-recently seen
field.  Lines starting with ``#`` are treated as comments and skipped.
All field names are returned in upper-case; all values are collected
into lists.

Example record (from notations.txt)::

    N 11A
    K 11k
    C 11A1
    ; 11A2
    R 11C

Yields the dict::

    {"N": ["11A"], "K": ["11k"], "C": ["11A1", "11A2"], "R": ["11C"]}
"""


def parse(filename):
    """Yield one dict per record found in *filename*.

    Records are separated by ``$`` on its own line.  Blank records and
    records that contain only comments are silently skipped.
    """
    with open(filename, "rt", encoding="utf8") as fh:
        data = fh.read()

    for chunk in data.split("\n$"):
        obj = {}
        last_field = None
        for line in chunk.split("\n"):
            if line.startswith("#"):
                continue
            parts = line.split(" ", 1)
            if len(parts) < 2:
                continue
            field, value = parts[0].upper(), parts[1]
            if field == ";":
                if last_field is not None:
                    obj[last_field].append(value)
            else:
                obj.setdefault(field, []).append(value)
                last_field = field
        if obj:
            yield obj
