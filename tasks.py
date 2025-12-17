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


@task
def start(ctx: Context, reload: bool = False, host: str = "localhost", port: int = 8000) -> None:
    ctx.run("echo apply db migrations && uv run alembic upgrade head")
    webbrowser.open(f"http://{host}:{port}/docs", autoraise=True)
    ctx.run(
        f"echo start server &&"
        f" uv run uvicorn mill_sime.primary.main:app --host {host} --port {port} {'--reload' if reload else ''}"
    )
