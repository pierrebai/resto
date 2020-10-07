import os
import subprocess
import glob
import json
import shutil

import click
import coverage
import unittest
import contextlib


############################################################################
#
# Main command.


@click.group()
def main():
    """
    Manage the flask app, tests, coverage, etc.
    """


############################################################################
#
# Dependency commands.


@main.group()
def dependency():
    """
    Manage the Python dependencies.
    """


@dependency.command("add")
@click.argument("package", type=click.Path())
def add_dependency(package):
    """
    Add a new dependency.
    """
    subprocess.run(['pipenv', 'install', f'{package}'])


@dependency.command("update")
def update_dependencies():
    """
    Setup (or update) the known dependencies.
    """
    subprocess.run(['pipenv', 'install'])


############################################################################
#
# Unit tests commands.


@main.command()
def unit_tests():
    """
    Run unit-tests.
    """
    tests_dir = relative_path(['src', 'unit-tests'])
    tests = unittest.TestLoader().discover(tests_dir, pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return 0 if result.wasSuccessful() else 1


############################################################################
#
# Integration tests commands.


@main.command()
@click.pass_context
@click.option("--tests", default='', help="Pattern to match test names to run.")
def integration_tests(ctx, tests):
    """
    Run the integration tests. Note: the flask app must already run in parallel.
    """
    tests_pattern = f'test*{tests}*.py'
        
    tests_dir = relative_path(['src', 'integration-tests'])
    tests = unittest.TestLoader().discover(tests_dir, pattern=tests_pattern)
    result = unittest.TextTestRunner(verbosity=1).run(tests)
    return 0 if result.wasSuccessful() else 1


############################################################################
#
# Flask commands.


@main.command()
def flask():
    """
    Run the flask-based web app.
    """
    import example_app
    example_app.main()


############################################################################
#
# Python commands.


@main.group('python')
def python():
    """
    Manage Python interactions.
    """


@python.command('prompt')
def interactive_prompt_to_python():
    """
    Start an interactive Python session in the manager pipenv environment.
    """
    subprocess.run([ 'python' ], shell=True, cwd=relative_path(['.']))


############################################################################
#
# Code coverage helpers.


@contextlib.contextmanager
def covered(source: str, omit: list = []):
    """
    Python context that produces code coverage reports about the code being run within.
    """
    include=os.path.join(source, '*.py')
    cov = coverage.Coverage(
        data_suffix=True,
        omit=omit,
        source=[source]
    )
    cov.start()
    yield
    cov.stop()
    cov.save()


############################################################################
#
# Code coverage commands.


@main.group('coverage')
def code_coverage():
    """
    Manage the code coverage.
    """


@code_coverage.command('unit-tests')
@click.pass_context
def unit_tests_coverage(ctx):
    """
    Run the unit tests with code coverage for the lambda functions.
    """
    with covered(relative_path(['src', 'flask-app'])):
        ctx.forward(unit_tests)


@code_coverage.command('flask')
@click.pass_context
def flask_coverage(ctx):
    """
    Run the flask web app with code coverage.
    """
    with covered(relative_path(['src', 'flask-app'])):
        ctx.forward(flask)


@code_coverage.command('report')
@click.option("--html", is_flag=True, help="Create the report in HTML format and open it.")
def report_coverage(html):
    """
    Analyze the code coverage and output a report.
    """
    source = relative_path(['src', 'flask-app'])
    include=os.path.join(source, '*.py')
    cov = coverage.Coverage(
        data_suffix=True,
        source=[source]
    )
    cov.load()
    cov.combine(data_paths=[relative_path('.')])
    cov.save()
    if html:
        covdir = relative_path('htmlcov')
        cov.html_report(ignore_errors=True, include=include, directory=covdir)
        covindex = os.path.join(covdir, 'index.html')
        click.launch(covindex)
    else:
        cov.report(show_missing=True, ignore_errors=True, include=include)


@code_coverage.command('clear')
def clear_coverage():
    """
    Delete all the code coverage data.
    """
    data_files = relative_path(['manager', '.coverage*'])
    for fn in glob.iglob(data_files):
        os.remove(fn)


############################################################################
#
# Helpers.


def relative_path(path):
    """
    Create an absolute path pointing to a path relative to the root of the project.
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    if isinstance(path, list):
        return os.path.join(basedir, *path)
    else:
        return os.path.join(basedir, path)


import sys
sys.path.append(relative_path(['src', 'flask-app']))
sys.path.append(relative_path(['src', 'integration-tests']))
sys.path.append(relative_path(['src', 'unit-tests']))


############################################################################
#
# Entry point.


main()

