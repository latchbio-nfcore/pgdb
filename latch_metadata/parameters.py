
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'add_reference': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title='ENSEMBL canonical proteomes',
        description='Add the reference proteome to the file',
    ),
    'ensembl_downloader_config': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to configuration file for ENSEMBL download parameters',
    ),
    'ensembl_config': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to configuration file for parameters in generating protein databases from ENSMEBL sequences',
    ),
    'gencode_url': NextflowParameter(
        type=typing.Optional[str],
        default='ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19',
        section_title=None,
        description='URL for downloading GENCODE datafiles',
    ),
    'ensembl_name': NextflowParameter(
        type=typing.Optional[str],
        default='homo_sapiens',
        section_title=None,
        description='Taxonomic term for the species to download from ENSEMBL',
    ),
    'ncrna': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Non canonical proteome parameters',
        description='Generate protein database from non-coding RNA',
    ),
    'pseudogenes': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Generate protein database from pseudogenes',
    ),
    'altorfs': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Generate alternative ORFs from canonical proteins',
    ),
    'ensembl': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Download ENSEMBL variants and generate protein database',
    ),
    'vcf': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Custom VCF-based variant proteomes',
        description='Enable translation of a given VCF file',
    ),
    'vcf_file': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='VCF file path to be translated. Generate variants proteins by modifying sequences of affected transcripts.',
    ),
    'af_field': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Allele frequency identifier string in VCF Info column, if no AF info is given set it to empty.',
    ),
    'cbioportal': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='cBioportal variant proteomes',
        description='Download cBioPortal studies and generate protein database',
    ),
    'cbioportal_accepted_values': NextflowParameter(
        type=typing.Optional[str],
        default='all',
        section_title=None,
        description='Specify a tissue type to limit the cBioPortal mutations to a particular caner type',
    ),
    'cbioportal_filter_column': NextflowParameter(
        type=typing.Optional[str],
        default='CANCER_TYPE',
        section_title=None,
        description='Specify a column from the clinical sample file to be used for filtering records',
    ),
    'cbioportal_study_id': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Download mutations from a specific study in cbiportal default is all which downloads mutations from all studies',
    ),
    'cbioportal_config': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='cBioPortal configuration file',
    ),
    'cosmic': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='COSMIC variant proteomes',
        description='Download COSMIC mutation files and generate protein database',
    ),
    'cosmic_celllines': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Download COSMIC cell line files and generate protein database',
    ),
    'cosmic_user_name': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='User name (or email) for COSMIC account',
    ),
    'cosmic_password': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Password for COSMIC account',
    ),
    'cosmic_config': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to configuration file for parameters in generating',
    ),
    'cosmic_cancer_type': NextflowParameter(
        type=typing.Optional[str],
        default='all',
        section_title=None,
        description='Specify a tissue type to limit the COSMIC mutations to a particular caner type',
    ),
    'cosmic_cellline_name': NextflowParameter(
        type=typing.Optional[str],
        default='all',
        section_title=None,
        description='Specify a sample name to limit the COSMIC cell line mutations to a particular  cell line',
    ),
    'gnomad': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='GNOMAD variant proteomes',
        description='Add gNOMAD variants to the database',
    ),
    'gnomad_file_url': NextflowParameter(
        type=typing.Optional[str],
        default='gs://gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz',
        section_title=None,
        description='gNOMAD url',
    ),
    'decoy': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Decoy generation',
        description='Append the decoy proteins to the database',
    ),
    'decoy_prefix': NextflowParameter(
        type=typing.Optional[str],
        default='Decoy_',
        section_title=None,
        description='String to be used as prefix for the generated decoy sequences',
    ),
    'decoy_method': NextflowParameter(
        type=typing.Optional[str],
        default='decoypyrat',
        section_title=None,
        description='Method used to generate the decoy database',
    ),
    'decoy_enzyme': NextflowParameter(
        type=typing.Optional[str],
        default='Trypsin',
        section_title=None,
        description='Enzyme used to generate the decoy',
    ),
    'protein_decoy_config': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Configuration file to perform the decoy generation',
    ),
    'clean_database': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Clean and process database',
        description='Clean the database for stop codons, short protein sequences',
    ),
    'minimum_aa': NextflowParameter(
        type=typing.Optional[int],
        default=6,
        section_title=None,
        description='Minimum number of AminoAcids for a protein to be included in the database',
    ),
    'add_stop_codons': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If an stop codons is found, create two proteins from it',
    ),
    'outdir': NextflowParameter(
        type=typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]],
        default=None,
        section_title='Input/output options',
        description='The output directory where the results will be saved.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'final_database_protein': NextflowParameter(
        type=typing.Optional[str],
        default='final_proteinDB.fa',
        section_title=None,
        description='Filename for the final protein database',
    ),
}

