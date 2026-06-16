import os
from typing import (
    TYPE_CHECKING,
)

from nomad.parsing.parser import MatchingParser

from nomad_plugin_tutorials.parsers.reader import read_data_file
from nomad_plugin_tutorials.parsers.tutorial_1.schema.schema_package import (
    OpticalMicroscopy,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive


class OpticalMicroscopyParser(MatchingParser):
    def parse(
        self, mainfile: str, archive: 'EntryArchive', logger=None, child_archives=None
    ) -> None:
        data_file_path = mainfile.rsplit('/raw/', maxsplit=1)[-1]
        data_dict = read_data_file(data_file_path, archive, logger)

        measurement = OpticalMicroscopy(data_file=data_file_path)
        if datetime := data_dict.get('datetime'):
            measurement.datetime = datetime
        if (
            'sample' in data_dict
            and isinstance(data_dict['sample'], dict)
            and 'sample_ID' in data_dict['sample']
        ):
            measurement.m_setdefault('samples/0')
            measurement.samples[0].lab_id = data_dict['sample']['sample_ID']
            if 'description' in data_dict['sample']:
                measurement.description = data_dict['sample']['description']

        ## Tutorial 1.1 ##
        # Populate `measurement.settings` and `measurement.results` section using the
        # parsed data dictionary and assign it to archive.data.
        #
        # Hints:
        # - Use `measurement.m_setdefault` method to instantiate `settings` and
        #   `results` sections. Remember `results` is a list of sub-sections.
        #   Instantiate it with `results/0` to append the first list element.
        # - When setting the `measurement.results[0].image` path, join the image path
        #   from the data_dict with the directory name of the `data_file_path`
        # - Assign `measurement` to `archive.data`
