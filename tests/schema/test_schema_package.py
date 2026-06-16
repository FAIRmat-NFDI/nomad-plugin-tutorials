import math
import os.path
import pytest

from nomad.client import normalize_all, parse

@pytest.mark.skip('Skipping test in `tutorial-mode` branch.')
def test_schema_package():
    test_file = os.path.join('tests', 'data', 'schema', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert math.isclose(entry_archive.data.temperature.magnitude, 1800.0, rel_tol=1e-9)
    assert entry_archive.results.material.material_name == 'Molten Iron'
    print(
        entry_archive.data.results.peak_wavelength.magnitude,
    )
    assert math.isclose(
        entry_archive.data.results.peak_wavelength.magnitude,
        1609.873308,
        rel_tol=1e-9,
    )


if __name__ == '__main__':
    test_schema_package()
