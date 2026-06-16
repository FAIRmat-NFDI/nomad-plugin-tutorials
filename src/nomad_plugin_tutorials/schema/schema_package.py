"""
Tutorial schema package demonstrating the following NOMAD schema concepts:
    - Quantities and sub-sections
    - ELN annotations for user-editable quantities
    - Using basesections as a standardized starting point for schema
    - EntryData section for creating ELN entries
    - Populating `archive.results` based on entry data
    - Creating a Plotly plot from array quantities

Physics example: Planck's law of blackbody radiation
    Given the temperature T of a body, this schema computes and stores the
    full spectral radiance profile B(λ, T). The peak wavelength is derived
    via Wien's displacement law. A plot is also generated automatically based
    on the profile.
"""

from typing import TYPE_CHECKING

from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
    ELNComponentEnum,
)
from nomad.datamodel.metainfo.basesections import Activity
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import Quantity, SchemaPackage, Section, SubSection

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

m_package = SchemaPackage()


class BlackbodyResults(ArchiveSection):
    """
    Results of the Planck spectral radiance calculation.
    """

    temperature = Quantity(
        type=float,
        unit='K',
        description='Temperature of the blackbody in Kelvin.',
    )
    wavelength = Quantity(
        type=float,
        shape=['*'],
        unit='nm',
        description='Wavelength array in nm.',
    )

    ## Tutorial 1.1 ##
    # Add the quantities `spectral_radiance` and `peak_wavelength` with suitable type,
    # shape, unit, and description.
    # Hints:
    #
    # - `spectral_radiance` should be an array of type `float` with units 'W sr⁻¹ m⁻³'.
    # - `peak_wavelength` should be a scalar of type `float` with units 'nm'.


class BlackbodyResultsPlot(BlackbodyResults, PlotSection):
    """
    Section that generates a Plotly plot of the spectral radiance profile and populates
    `figures` subsection with JSON-serialized Plotly figure data.

    The `figures` subsection comes from the PlotSection base class and is used by the
    UI to display plots.
    """

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        Creates a Plotly line plot of B(λ, T) and marks the peak wavelength.
        Stores the figure in `self.figures` for display in the NOMAD UI.
        """
        super().normalize(archive, logger)

        ## Tutorial 1.2 ##
        # Configure the `normalize`` method to generate the Plotly plot.
        #
        # Hints:
        # - Verify that `wavelength` and `spectral_radiance` are not None.
        # - Import the helper plotting function plot_blackbody_spectrum from the
        #   visualization module: nomad_plugin_tutorials.schema.visualize.
        # - Generate a plotly figure using the plotting function
        # - Instantiate a `PlotlyFigure` section and set `PlotlyFigure.figure` to
        #   the JSON-serialized figure (use `plotly_figure.to_plotly_json()`). Also
        #   set the `PlotlyFigure.label`
        # - Wrap the `PlotlyFigure` object in a list and assign it to `self.figures`



class BlackbodyRadiation(Activity, EntryData):
    """
    ELN schema for a Planck blackbody radiation calculation.

    Set a material/source name, temperature, and optional wavelength bounds.
    The normalize method computes B(λ, T), stores the spectrum in `results`, and writes
    the source name to `archive.results` for searchability.
    """

    m_def = Section(label="Blackbody Radiation (Planck's Law)")

    name = Quantity(
        type=str,
        label='Source name',
        description='Name of the emitting body, e.g. "Molten Iron" or "Solar surface".',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )
    temperature = Quantity(
        type=float,
        unit='K',
        description=(
            'Temperature of the blackbody in Kelvin. '
            'Examples: molten iron ≈ 1800 K, solar surface ≈ 5778 K, '
            'hot furnace ≈ 1200 K.'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )

    ## Tutorial 1.3 ##
    # Add the definition for quantities `wavelength_min` and `wavelength_max` along with
    # ELN annotations.
    # Also define the `results` sub-section.
    #
    # Hints:
    # - `wavelength_min` and `wavelength_max` should be of scalars of type `float` with
    #   units `nm`. You can also set the `Quantity.default` to 100.0 and 3000.0
    #   respectively. For both, you can use the `NumberEditQuantity` for ELN component.
    # - Use `SubSection` class to define `results` sub-section by setting its
    #   `SubSection.section_def` to the `BlackbodyResultsPlot`.

    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        """
        Computes the Planck spectral radiance B(λ, T) based on user inputs, stores
        the arrays in results, and writes the source name to `archive.results`.
        """
        self.method = 'Planck Spectral Radiance'

        from nomad_plugin_tutorials.schema.calculate import (
            planck_spectrum,
        )

        if self.temperature:

            ## Tutorial 1.4 ##
            # Run the Planck spectrum calculation using the `plack_spectrum` helper
            # function. Then populate the `results` using the output.
            #
            # Hints:
            # - When using the quantity values in the helper function, use only
            #   their magnitude. For example,
            #       ps = planck_spectrum(
            #           temperature=self.temperature.to('K').magnitude,
            #           ...
            #       )
            # - Instantiate and populate the `BlackbodyResultsPlot` section for
            #   `results` using the computed spectrum.

            ps = None
            results = None

            results.normalize(archive, logger)
            self.results = results
        else:
            logger.warning(
                'Temperature not provided; skipping Planck spectrum calculation.'
            )
            self.results = None

        if self.name:
            archive.m_setdefault('results/material')
            archive.results.material.material_name = self.name

        super().normalize(archive, logger)


m_package.__init_metainfo__()
