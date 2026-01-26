import argparse
import yaml
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

from core.engine import create_db_engine
from core.context import SyncContext
from core.worker import run_parallel_sync

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open("config/sync.yaml") as f:
        cfg = yaml.safe_load(f)

    ctx = SyncContext(dry_run=args.dry_run)

    primary_engine = create_db_engine(cfg["primary_db"]["url"])

    replica_engines = [
        {
            "name": r["name"],
            "engine": create_db_engine(r["url"]),
        }
        for r in cfg["replica_dbs"]
    ]

    run_parallel_sync(
        ctx,
        primary_engine,
        replica_engines,
        cfg["tables"],
    )

if __name__ == "__main__":
    main()
