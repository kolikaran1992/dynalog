from dynaconf import Dynaconf
from datetime import datetime
import os, pytz, requests
from pathlib import Path


_NOW = datetime.now()
_BASE_DIR = Path(__file__).resolve().parent.parent


def _get_start_ts(tz: str) -> datetime:
    return _NOW.astimezone(pytz.timezone(tz))


def _get_now_iso(tz: str) -> str:
    return datetime.now().astimezone(pytz.timezone(tz)).isoformat()


def _get_now_ts(tz: str) -> str:
    return datetime.now().astimezone(pytz.timezone(tz))


###########################
# Download Jars for MinIO #
###########################

# ---- JAR dependencies ----
JARS = {
    "hadoop-aws-3.3.4.jar": "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar",
    "aws-java-sdk-bundle-1.12.262.jar": "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar",
    "jaxb-api-2.3.1.jar": "https://repo1.maven.org/maven2/javax/xml/bind/jaxb-api/2.3.1/jaxb-api-2.3.1.jar",
    "jaxb-core-2.3.0.jar": "https://repo1.maven.org/maven2/com/sun/xml/bind/jaxb-core/2.3.0/jaxb-core-2.3.0.jar",
    "jaxb-impl-2.3.0.jar": "https://repo1.maven.org/maven2/com/sun/xml/bind/jaxb-impl/2.3.0/jaxb-impl-2.3.0.jar",
}

# ---- Target directory for jars ----
jar_dir = Path.home().joinpath(".local/lib/minio-jars").resolve()
jar_dir.mkdir(parents=True, exist_ok=True)

# ---- Download jars if not already present ----
for name, url in JARS.items():
    target_file = jar_dir / name
    if not target_file.exists():
        print(
            f"one time download jar dependency for minio at: '{target_file.as_posix()}'"
        )
        # print(f"Downloading {name} ...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(target_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


###################
# Create Settings #
###################
secrets_dir = os.environ.get("SECRETS_DIRECTORY") or ""
config = Dynaconf(
    preload=[_BASE_DIR.joinpath("dynalog", "settings.toml").as_posix()],
    settings_files=[],
    secrets=[] if not secrets_dir else list(Path(secrets_dir).glob("*.toml")),
    # to enable overriding of single variables at runtime
    environments=True,
    envvar_prefix="EXP_BASE",
    # to enable merging of user defined and base settings
    load_dotenv=True,
    # jinja variables
    _get_now_ts=_get_now_ts,
    _get_now_iso=_get_now_iso,
    _get_start_ts=_get_start_ts,
    now=_NOW,
    partition_date=_NOW.strftime("%Y/%m/%d"),
    root_dir=_BASE_DIR.as_posix(),
    merge_enabled=True,
)
