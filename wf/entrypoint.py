from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, ensembl_downloader_config: typing.Optional[str], ensembl_config: typing.Optional[str], ncrna: typing.Optional[bool], pseudogenes: typing.Optional[bool], altorfs: typing.Optional[bool], ensembl: typing.Optional[bool], vcf: typing.Optional[bool], vcf_file: typing.Optional[str], af_field: typing.Optional[str], cbioportal: typing.Optional[bool], cbioportal_study_id: typing.Optional[str], cbioportal_config: typing.Optional[str], cosmic: typing.Optional[bool], cosmic_celllines: typing.Optional[str], cosmic_user_name: typing.Optional[str], cosmic_password: typing.Optional[str], cosmic_config: typing.Optional[str], gnomad: typing.Optional[bool], decoy: typing.Optional[bool], protein_decoy_config: typing.Optional[str], clean_database: typing.Optional[bool], add_stop_codons: typing.Optional[bool], outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], add_reference: typing.Optional[bool], gencode_url: typing.Optional[str], ensembl_name: typing.Optional[str], cbioportal_accepted_values: typing.Optional[str], cbioportal_filter_column: typing.Optional[str], cosmic_cancer_type: typing.Optional[str], cosmic_cellline_name: typing.Optional[str], gnomad_file_url: typing.Optional[str], decoy_prefix: typing.Optional[str], decoy_method: typing.Optional[str], decoy_enzyme: typing.Optional[str], minimum_aa: typing.Optional[int], final_database_protein: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('add_reference', add_reference),
                *get_flag('ensembl_downloader_config', ensembl_downloader_config),
                *get_flag('ensembl_config', ensembl_config),
                *get_flag('gencode_url', gencode_url),
                *get_flag('ensembl_name', ensembl_name),
                *get_flag('ncrna', ncrna),
                *get_flag('pseudogenes', pseudogenes),
                *get_flag('altorfs', altorfs),
                *get_flag('ensembl', ensembl),
                *get_flag('vcf', vcf),
                *get_flag('vcf_file', vcf_file),
                *get_flag('af_field', af_field),
                *get_flag('cbioportal', cbioportal),
                *get_flag('cbioportal_accepted_values', cbioportal_accepted_values),
                *get_flag('cbioportal_filter_column', cbioportal_filter_column),
                *get_flag('cbioportal_study_id', cbioportal_study_id),
                *get_flag('cbioportal_config', cbioportal_config),
                *get_flag('cosmic', cosmic),
                *get_flag('cosmic_celllines', cosmic_celllines),
                *get_flag('cosmic_user_name', cosmic_user_name),
                *get_flag('cosmic_password', cosmic_password),
                *get_flag('cosmic_config', cosmic_config),
                *get_flag('cosmic_cancer_type', cosmic_cancer_type),
                *get_flag('cosmic_cellline_name', cosmic_cellline_name),
                *get_flag('gnomad', gnomad),
                *get_flag('gnomad_file_url', gnomad_file_url),
                *get_flag('decoy', decoy),
                *get_flag('decoy_prefix', decoy_prefix),
                *get_flag('decoy_method', decoy_method),
                *get_flag('decoy_enzyme', decoy_enzyme),
                *get_flag('protein_decoy_config', protein_decoy_config),
                *get_flag('clean_database', clean_database),
                *get_flag('minimum_aa', minimum_aa),
                *get_flag('add_stop_codons', add_stop_codons),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('final_database_protein', final_database_protein)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_pgdb", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_pgdb(ensembl_downloader_config: typing.Optional[str], ensembl_config: typing.Optional[str], ncrna: typing.Optional[bool], pseudogenes: typing.Optional[bool], altorfs: typing.Optional[bool], ensembl: typing.Optional[bool], vcf: typing.Optional[bool], vcf_file: typing.Optional[str], af_field: typing.Optional[str], cbioportal: typing.Optional[bool], cbioportal_study_id: typing.Optional[str], cbioportal_config: typing.Optional[str], cosmic: typing.Optional[bool], cosmic_celllines: typing.Optional[str], cosmic_user_name: typing.Optional[str], cosmic_password: typing.Optional[str], cosmic_config: typing.Optional[str], gnomad: typing.Optional[bool], decoy: typing.Optional[bool], protein_decoy_config: typing.Optional[str], clean_database: typing.Optional[bool], add_stop_codons: typing.Optional[bool], outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], add_reference: typing.Optional[bool] = True, gencode_url: typing.Optional[str] = 'ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_19', ensembl_name: typing.Optional[str] = 'homo_sapiens', cbioportal_accepted_values: typing.Optional[str] = 'all', cbioportal_filter_column: typing.Optional[str] = 'CANCER_TYPE', cosmic_cancer_type: typing.Optional[str] = 'all', cosmic_cellline_name: typing.Optional[str] = 'all', gnomad_file_url: typing.Optional[str] = 'gs://gnomad-public/release/2.1.1/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz', decoy_prefix: typing.Optional[str] = 'Decoy_', decoy_method: typing.Optional[str] = 'decoypyrat', decoy_enzyme: typing.Optional[str] = 'Trypsin', minimum_aa: typing.Optional[int] = 6, final_database_protein: typing.Optional[str] = 'final_proteinDB.fa') -> None:
    """
    nf-core/pgdb

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, add_reference=add_reference, ensembl_downloader_config=ensembl_downloader_config, ensembl_config=ensembl_config, gencode_url=gencode_url, ensembl_name=ensembl_name, ncrna=ncrna, pseudogenes=pseudogenes, altorfs=altorfs, ensembl=ensembl, vcf=vcf, vcf_file=vcf_file, af_field=af_field, cbioportal=cbioportal, cbioportal_accepted_values=cbioportal_accepted_values, cbioportal_filter_column=cbioportal_filter_column, cbioportal_study_id=cbioportal_study_id, cbioportal_config=cbioportal_config, cosmic=cosmic, cosmic_celllines=cosmic_celllines, cosmic_user_name=cosmic_user_name, cosmic_password=cosmic_password, cosmic_config=cosmic_config, cosmic_cancer_type=cosmic_cancer_type, cosmic_cellline_name=cosmic_cellline_name, gnomad=gnomad, gnomad_file_url=gnomad_file_url, decoy=decoy, decoy_prefix=decoy_prefix, decoy_method=decoy_method, decoy_enzyme=decoy_enzyme, protein_decoy_config=protein_decoy_config, clean_database=clean_database, minimum_aa=minimum_aa, add_stop_codons=add_stop_codons, outdir=outdir, email=email, final_database_protein=final_database_protein)

