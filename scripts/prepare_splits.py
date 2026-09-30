import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.baseline_common import MANIFEST, prepare_data

if __name__ == "__main__":
    parts, _ = prepare_data()
    print("Train/validation/test sizes:", [len(part) for part in parts])
    print("Frozen manifest:", MANIFEST)
    print("No test model evaluation was performed.")
