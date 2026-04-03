#!/usr/bin/python
import os
import webbrowser

from invoke import Context, task


def _is_ci() -> bool:
    return bool(os.environ.get("CI", False))


@task
def lint(ctx: Context) -> None:
    """Lint code"""

    if _is_ci():
        ctx.run("echo Running lint && uv run ruff check ./src ./tests")
    else:
        ctx.run("echo Running format && uv run ruff format ./src ./tests")
        ctx.run("echo Running lint && uv run ruff check ./src ./tests --fix")

    ctx.run("echo Running mypy && uv run mypy")


@task
def tests(ctx: Context) -> None:
    """Run unit tests"""
    ctx.run("echo Running tests && uv run pytest --cov")
