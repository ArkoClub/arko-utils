import os
import site
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=64)
def resolve_path(path: str | Path, root: Path = Path(os.curdir).resolve()) -> str:
    root = root.resolve().absolute()
    if path != "<input>":
        path = Path(path)

        if path.is_relative_to(root):
            path = str(Path(path).relative_to(root))
            path_string = path.split(".")[0].replace(os.sep, ".")
        else:
            _path = None
            for s in site.getsitepackages() + [site.getusersitepackages()]:
                site_path = Path(s).resolve().absolute()
                if Path(path).is_relative_to(site_path):
                    _path = str(Path(path).relative_to(site_path))
                    break
            if _path is None:
                path_string = "<SITE>"
            else:
                path_string = _path.split(".")[0].replace(os.sep, ".")
    else:
        path_string = "<INPUT>"
    return path_string.replace("lib.site-packages.", "")
