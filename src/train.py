"""Week 3 model training belongs here; Week 2 EDA delegates to one canonical script."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    from scripts.eda_train import run_eda

    run_eda()


if __name__ == "__main__":
    main()
