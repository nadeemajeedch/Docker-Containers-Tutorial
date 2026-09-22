"""MkDocs hook: build the tutorial website directly from the repository layout.

The tutorial content (README.md, lessons/, cheatsheet/, examples/) lives at
the repository root — exactly the structure we want on the website. Rather
than moving or duplicating any file into docs/, this hook injects the
existing Markdown files into the MkDocs build as generated File objects.

All tutorial content is consumed read-only, byte-for-byte identical on disk;
no source file is moved, renamed or rewritten.
"""

from __future__ import annotations

import pathlib
import re

from mkdocs.structure.files import File, InclusionLevel, Files

ROOT = pathlib.Path(__file__).resolve().parent.parent

LESSONS = [
    "lessons/01-introduction-to-docker.md",
    "lessons/02-containers-vs-virtual-machines.md",
    "lessons/03-docker-architecture.md",
    "lessons/04-installing-docker.md",
    "lessons/05-docker-cli.md",
    "lessons/06-docker-images.md",
    "lessons/07-docker-containers.md",
    "lessons/08-docker-hub.md",
    "lessons/09-running-python-with-docker.md",
    "lessons/10-dockerfile.md",
    "lessons/11-building-python-images.md",
    "lessons/12-python-dependencies.md",
    "lessons/13-dockerignore.md",
    "lessons/14-volumes-and-bind-mounts.md",
    "lessons/15-running-jupyter-with-docker.md",
    "lessons/16-custom-jupyter-image.md",
    "lessons/17-jupyter-project.md",
    "lessons/18-docker-compose.md",
    "lessons/19-python-jupyter-compose.md",
    "lessons/20-environment-variables.md",
    "lessons/21-docker-networking.md",
    "lessons/22-docker-for-data-science.md",
    "lessons/23-docker-for-machine-learning.md",
    "lessons/24-debugging.md",
    "lessons/25-best-practices.md",
    "lessons/26-security.md",
    "lessons/27-advanced-docker.md",
    "lessons/28-image-optimization.md",
    "lessons/29-docker-and-github.md",
    "lessons/30-reproducible-academic-projects.md",
    "lessons/31-final-project.md",
]

CHEATSHEETS = [
    "cheatsheet/complete-docker-cheatsheet.md",
    "cheatsheet/dockerfile.md",
    "cheatsheet/docker-compose.md",
    "cheatsheet/python-docker.md",
    "cheatsheet/jupyter-docker.md",
    "cheatsheet/networking.md",
    "cheatsheet/best-practices.md",
    "cheatsheet/troubleshooting.md",
]

EXAMPLES = [
    "examples/README.md",
    "examples/hello-python/README.md",
    "examples/python-docker-project/README.md",
    "examples/jupyter-project/README.md",
    "examples/jupyter-project/notebooks/welcome.md",
    "examples/compose-jupyter/README.md",
    "examples/compose-jupyter/notebooks/welcome.md",
    "examples/ml-docker/README.md",
    "examples/data-science-docker/README.md",
    "examples/networking-demo/README.md",
    "examples/github-template/README.md",
    "examples/final-project/README.md",
    "examples/final-project/SUBMISSION.md",
]


DIR_LINK_RE = re.compile(
    r"(?P<pre>\]\()(?P<url>(?:\.\./)*(?:[A-Za-z0-9_][\w.-]*/)+)(?P<post>\))"
)


def _fix_dir_links(markdown: str) -> str:
    """Rewrite directory-style relative links ([x](dir/)) to [x](dir/README.md).

    GitHub resolves foo/ to foo/README.md; MkDocs needs the explicit file.
    Only relative URLs ending in '/' inside ](..) constructs are rewritten —
    images, anchors, code and absolute URLs are untouched. Tutorial files on
    disk are never modified; the rewrite happens in memory at build time.
    """
    if "](" not in markdown:
        return markdown

    def repl(m: re.Match) -> str:
        return f"{m.group('pre')}{m.group('url')}README.md{m.group('post')}"

    return DIR_LINK_RE.sub(repl, markdown)


def _page(rel_path: str, config) -> File:
    """Wrap an existing repository Markdown file as a generated MkDocs File.

    src_dir points at the repository root, so MkDocs reads the original file
    from disk (lazily, byte-for-byte) even though it lives outside docs_dir.
    """
    f = File(
        path=rel_path,
        src_dir=str(ROOT),
        dest_dir=config.site_dir,
        use_directory_urls=config.use_directory_urls,
        inclusion=InclusionLevel.INCLUDED,
    )
    f.generated_by = "mkdocs_hooks.inject_repo_content"
    return f


def on_files(files: Files, *, config):
    """Inject every repository Markdown file into the build."""
    all_md = [
        "README.md",
        *LESSONS,
        "lessons/README.md",
        "lessons/part-2-preview.md",
        "cheatsheet.md",
        *CHEATSHEETS,
        *EXAMPLES,
    ]
    for rel in all_md:
        if not (ROOT / rel).is_file():
            raise FileNotFoundError(f"Expected tutorial file is missing: {rel}")
        files.append(_page(rel, config))
    return files


def on_page_markdown(markdown: str, *, page, config, files):
    """Resolve GitHub-style directory links for the website build."""
    return _fix_dir_links(markdown)
