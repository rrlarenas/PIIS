"""Descarga una selección fija de fuentes públicas, sin ejecutar los ejemplos."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import time
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("rhapsody", "CDCgov/NEDSS-DataIngestion", "295871912c017aa1c6459c0a272e5210d03383ee", "Apache-2.0",
     ["LICENSE", "README.md", "data-ingestion-service/src/main/resources/rhapsody/NBS-Data-Ingestion-ELR-Route.rlc"]),
    ("ibm-ace", "ot4i/ace-demo-pipeline", "9a28f4980cefdde46a8ba1aa4e8873bdf1aa8e33", "MIT",
     ["LICENSE", "README.md"], ["TeaRESTApplication/", "TeaCallableApplicationV2/", "TeaSharedLibrary/"]),
    ("apache-camel", "apache/camel-examples", "869cde2a332ab6108572af0b1f93923bc3fc9768", "Apache-2.0",
     ["LICENSE.txt", "NOTICE.txt", "pom.xml"], ["loadbalancing/"]),
    ("wso2-mi", "wso2/product-micro-integrator", "2f73279a4419932472d5b9cd52c9f88fd7fe71d2", "Apache-2.0",
     ["LICENSE", "LICENSE.txt", "README.md"] + [
         "integration/management-api-tests/src/test/resources/artifacts/ESB/server/repository/deployment/server/synapse-configs/default/" + path
         for path in ["api/HelloRestApi.xml", "endpoints/HelloEndPoint.xml", "local-entries/HelloLocalEntry.xml", "message-processors/HelloMessageProcessor.xml", "message-stores/HelloMessageStore.xml", "proxy-services/HelloProxyService.xml"]]),
]


def fetch(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "PIIS-public-samples"})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def collect(spec):
    folder, repo, commit, license_id, paths, *prefixes = spec
    paths = list(paths)
    if prefixes:
        tree = json.loads(fetch(f"https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1"))
        if tree.get("truncated"):
            raise RuntimeError(f"Árbol incompleto: {repo}")
        paths += [entry["path"] for entry in tree["tree"]
                  if entry["type"] == "blob" and any(entry["path"].startswith(p) for p in prefixes[0])
                  and not entry["path"].lower().endswith((".jar", ".png", ".jpg", ".zip", ".bar"))]

    def download(path):
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{path}"
        content = fetch(url)
        destination = ROOT / folder / "upstream" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        return {"path": destination.relative_to(ROOT).as_posix(), "upstream_path": path,
                "url": url, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        files = list(pool.map(download, sorted(set(paths))))
    result = {"engine": folder, "repository": f"https://github.com/{repo}", "commit": commit,
              "license": license_id, "retrieved_on": "2026-11-04", "modified": False,
              "selection": "Fuentes seleccionadas; se omiten binarios y capturas. No es un paquete de despliegue.", "files": files}
    (ROOT / folder / "SOURCE.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{folder}: {len(files)} archivos", flush=True)
    return result


if __name__ == "__main__":
    results = [collect(spec) for spec in SOURCES]
    (ROOT / "manifest.json").write_text(json.dumps({"sources": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
