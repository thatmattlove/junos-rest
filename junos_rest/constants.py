"""Reusable static data."""

COMMIT = """
<lock-configuration/>
<commit/>
<unlock-configuration/>
"""

COMMIT_CHECK = """
<commit-configuration>
    <check/>
</commit-configuration>
"""

CONFIG_JSON = """
<lock-configuration/>
<load-configuration format="json">
    <configuration-json>
        {config}
    </configuration-json>
</load-configuration>
<commit/>
<unlock-configuration/>
"""

RESULTS = """<results>{results}</results>"""
