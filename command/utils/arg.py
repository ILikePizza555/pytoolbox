from typing import List, Union
from pathlib import Path

def resolve_paths(paths: List[str], base_dir: Path = Path.cwd()) -> List[Path]:
    """
    Given a list of paths (say from the arguments), return a list of Path objects to
    real files.
    """
    real_paths = []

    for p in paths:
        real_paths.extend(base_dir.glob(p))
    
    return real_paths