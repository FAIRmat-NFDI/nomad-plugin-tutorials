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
    spectral_radiance = Quantity(
        type=float,
        shape=['*'],
        unit='W sr⁻¹ m⁻³',
        description='Spectral radiance B(λ,T) in W·sr⁻¹·m⁻³ at each wavelength.',
    )
    peak_wavelength = Quantity(
        type=float,
        unit='nm',
        description=(
            "Wavelength of maximum emission in nm, from Wien's displacement law: "
            'λ_max = b / T,  b = 2.898 × 10⁻³ m·K.'
        ),
    )


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

        if self.wavelength is None or self.spectral_radiance is None:
            return

        from nomad_plugin_tutorials.schema.visualize import (
            plot_blackbody_spectrum,
        )

        self.figures = [
            PlotlyFigure(
                label='Spectral Radiance',
                figure=plot_blackbody_spectrum(
                    temperature=self.temperature.to('K').magnitude,
                    wavelength=self.wavelength.to('nm').magnitude,
                    spectral_radiance=self.spectral_radiance.to('W sr⁻¹ m⁻³').magnitude,
                    peak_wavelength=self.peak_wavelength.to('nm').magnitude,
                ).to_plotly_json(),
            )
        ]


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
    wavelength_min = Quantity(
        type=float,
        unit='nm',
        description='Lower bound of the wavelength range in nm. Defaults to 100 nm.',
        default=100.0,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    wavelength_max = Quantity(
        type=float,
        unit='nm',
        description='Upper bound of the wavelength range in nm. Defaults to 3000 nm.',
        default=3000.0,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
    )
    results = SubSection(
        section_def=BlackbodyResultsPlot,
        description='Computed spectral radiance profile and derived quantities.',
    )

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
            ps = planck_spectrum(
                temperature=self.temperature.to('K').magnitude,
                wavelength_min=self.wavelength_min.to('nm').magnitude,
                wavelength_max=self.wavelength_max.to('nm').magnitude,
            )

            results = BlackbodyResultsPlot(
                temperature=self.temperature,
                wavelength=ps['wavelength'],
                spectral_radiance=ps['spectral_radiance'],
                peak_wavelength=ps['peak_wavelength'],
            )
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
