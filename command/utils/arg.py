from typing import List, Union
from pathlib import Path
import sys

def resolve_paths(paths: List[str], base_dir: Path = Path.cwd(), ignore: List[str] = ["-"]) -> List[Path]:
    """
    Given a list of paths (say from the arguments), return a list of Path objects to
    real files.
    """
    real_paths = []

    for p in paths:
        if p not in ignore:
            real_paths.extend(base_dir.glob(p))
        else:
            real_paths.append(Path(p))
    
    return real_paths

def iterate_input_files(paths: List[Path], default=sys.stdin, **open_args):
    """
    Generator that returns open file handles. If the path is "-", stdin is returned instead.
    """
    if not paths:
        return default
    
    for path in paths:
        if str(path) == "-":
            yield default
        else:
            f = open(path, **open_args)
            yield f

            if not f.closed:
                f.close()