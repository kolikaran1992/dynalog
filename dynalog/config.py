from dynaconf import Dynaconf
from datetime import datetime
import os, sys, pytz
from pathlib import Path


_NOW = datetime.now()
_BASE_DIR = Path(__file__).resolve().parent.parent


def _get_start_ts(tz: str) -> datetime:
    return _NOW.astimezone(pytz.timezone(tz))


def _get_now_iso(tz: str) -> str:
    return datetime.now().astimezone(pytz.timezone(tz)).isoformat()


def _get_now_ts(tz: str) -> str:
    return datetime.now().astimezone(pytz.timezone(tz))


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
