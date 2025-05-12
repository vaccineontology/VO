from pathlib import Path
import pandas as pd

from collections import ChainMap

HERE = Path(__file__).parent.resolve()

COLUMNS = [
    "subject_id",
    "subject_label",
    "object_id",
    "object_label",
    "predicate_id",
    "mapping_justification",
]

DEFAULT_PREFIX_MAP = {
    "VO": "http://purl.obolibrary.org/obo/VO_",
    "oboInOwl": "http://www.geneontology.org/formats/oboInOwl#",
}


def write_sssom(
    df: pd.DataFrame,
    prefix_map: dict[str, str],
    path: Path,
    mapping_set_title: str,
) -> None:
    mapping_set_id = f"http://purl.obolibrary.org/obo/vo/mappings/{path.name}"
    df = df[[x for x in COLUMNS if x in df.columns]]
    with open(path, "w") as file:
        print(f"#mapping_set_id: {mapping_set_id}", file=file)
        print(f"#mapping_set_title: {mapping_set_title}", file=file)
        print("#license: https://creativecommons.org/licenses/by/4.0/", file=file)
        print("#curie_map:", file=file)
        for k, v in sorted(ChainMap(DEFAULT_PREFIX_MAP, prefix_map).items()):
            print(f"#  {k}: '{v}'", file=file)
        df.to_csv(file, sep="\t", index=False)


def _add_sssom_boilerplate(df):
    df["mapping_justification"] = "semapv:UnspecifiedMatching"
    df["predicate_id"] = "oboInOwl:hasDbXref"


def _add_object_prefixes(df, column, prefix) -> None:
    df["object_id"] = df[column].map(lambda luid: f"{prefix}:{luid}")
    del df[column]


def fix_cvx():
    df = pd.read_csv(HERE.joinpath("VO_CVXcodes.csv"), dtype=str)
    df = df.rename(
        columns={
            "ID": "subject_id",
            "LABEL in VO": "subject_label",
            "CVX Full Vaccine Name": "object_label",
        }
    )
    _add_sssom_boilerplate(df)
    _add_object_prefixes(df, "CVX Code", "cvx")
    del df["CVX Short Description"]
    pm = {
        "cvx": "https://biopragmatics.github.io/providers/cvx/",
    }
    write_sssom(
        df,
        pm,
        HERE.joinpath("vo-cvx.sssom.tsv"),
        mapping_set_title="Vaccine Ontology to CVX Mappings",
    )


def fix_fda_stn():
    df = pd.read_csv(HERE.joinpath("VO_FDA.csv"), dtype=str)
    df = df.rename(
        columns={
            "ID": "subject_id",
            "LABEL in VO": "subject_label",
        }
    )
    _add_sssom_boilerplate(df)
    _add_object_prefixes(df, "FDA STN#", "stn")
    df["object_id"] = df["object_id"].map(lambda s: s.replace(" ", ""))
    pm = {
        "stn": "https://bioregistry.io/stn:",
    }
    write_sssom(
        df,
        pm,
        HERE.joinpath("vo-fda.sssom.tsv"),
        mapping_set_title="Vaccine Ontology to FDA STN Mappings",
    )


def fix_omop():
    df = pd.read_csv(HERE.joinpath("VO_OMOP.csv"), dtype=str)
    df = df.rename(
        columns={
            "ID": "subject_id",
            "LABEL in VO": "subject_label",
        }
    )
    _add_sssom_boilerplate(df)
    _add_object_prefixes(df, "OMOP concept ID", "omop")
    # remove malformed mappings
    df = df[df["object_id"].map(lambda s: "|" not in s)]
    pm = {
        "omop": "http://api.ohdsi.org/WebAPI/vocabulary/concept/",
    }
    write_sssom(
        df,
        pm,
        HERE.joinpath("vo-omop.sssom.tsv"),
        mapping_set_title="Vaccine Ontology to OMOP Mappings",
    )


def fix_rxnorm():
    df = pd.read_csv(HERE.joinpath("VO_RxNorm.csv"), dtype=str)
    df = df.rename(
        columns={
            "ID": "subject_id",
            "LABEL in VO": "subject_label",
            "RxNorm preferred Name": "object_label",
        }
    )
    _add_sssom_boilerplate(df)
    _add_object_prefixes(df, "RxNorm ID", "rxnorm")
    pm = {
        "rxnorm": "http://purl.bioontology.org/ontology/RXNORM/",  # TODO check
    }
    write_sssom(
        df,
        pm,
        HERE.joinpath("vo-rxnorm.sssom.tsv"),
        mapping_set_title="Vaccine Ontology to RxNorm Mappings",
    )


def fix_rxnorm_extension():
    pass


def fix_usda():
    df = pd.read_csv(HERE.joinpath("VO_USDA.csv"), dtype=str)
    df = df.rename(
        columns={
            "ID": "subject_id",
            "LABEL in VO": "subject_label",
        }
    )
    usda_prefix = "usda.cvb.pcn"
    usda_uri_prefix = "https://bioregistry.io/usda.cvb.pcn:"
    df["object_id"] = df["USDA Code"].map(
        lambda s: usda_prefix + ":" + s.removeprefix("USDA: ")
    )
    _add_sssom_boilerplate(df)
    pm = {
        usda_prefix: usda_uri_prefix,
    }
    write_sssom(
        df,
        pm,
        HERE.joinpath("vo-usda.sssom.tsv"),
        mapping_set_title="Vaccine Ontology to USDA Vaccine Mappings",
    )


def fix_vac():
    df = pd.read_csv(HERE.joinpath("VO_VAC.csv"), dtype=str)
    df = df.rename(
        columns={
            "ID": "subject_id",
            "LABEL in VO": "subject_label",
        }
    )
    _add_sssom_boilerplate(df)
    _add_object_prefixes(df, "VAC ID", "vac")
    pm = {
        "vac": "https://vac.niaid.nih.gov/view?id=",
    }
    write_sssom(
        df,
        pm,
        HERE.joinpath("vo-vac.sssom.tsv"),
        mapping_set_title="Vaccine Ontology to Vaccine Adjuvant Compendium (VAC) Mappings",
    )


if __name__ == "__main__":
    fix_cvx()
    fix_fda_stn()
    fix_omop()
    fix_rxnorm()
    fix_rxnorm_extension()
    fix_usda()
    fix_vac()
