import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from tqdm import tqdm
from .db import record_install


def run_docker_install(package, method):
    Path(package).mkdir(exist_ok=True)
    log_path = Path(package) / "install.log"
    time_path = Path(package) / "time.log"
    start = time.time()
    if method == "goinstall":
        cmd = ["docker", "run", "ghcr.io/credoproject/core:v0.19.0-amd64", "--rm", "credo", "bioconductor", package]
    elif method == "rinstall":
        cmd = [
            "docker",
            "run",
            "base-install-r:latest",
            "Rscript",
            "-e",
            f'install.packages("{package}", repos="https://cloud.r-project.org")',
            "library({package})",
        ]
    else:
        raise ValueError("Unknown method")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=package)
        duration = int(time.time() - start)
        with open(log_path, "w") as f:
            f.write(proc.stdout + "\n" + proc.stderr)
        with open(time_path, "w") as f:
            f.write(str(duration))
        record_install(
            package,
            method,
            proc.returncode == 0,
            duration,
            proc.stdout + proc.stderr,
        )
        return package, True
    except Exception as e:
        record_install(package, method, False, 0, str(e))
        return package, False


def parallel_install(packages, method, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                run_docker_install,
                pkg,
                method,
            ): pkg
            for pkg in packages
        }
        for f in tqdm(
            as_completed(futures),
            total=len(futures),
            desc=f"{
                method}",
        ):
            pkg, success = f.result()
