import math
import pytest

from nomad.client import parse


@pytest.mark.skip('Skipping test in `tutorial-mode` branch.')
def test_parse_file():
    archive = parse('tests/data/parsers/metadata.xml')[0]

    assert math.isclose(archive.data.settings.magnification, 5.0, rel_tol=1e-9)


if __name__ == '__main__':
    test_parse_file()
