# Setup

You will need the following to use this code:

- Python 3.7+: see [Python official site for an installer](https://www.python.org/)
- pipenv: run `pip install pipenv` in a shell that has Python in ts command path.
- Python dependencies: run `pipenv install` in the root of the project.

# Running Tests

## Preparing to run the tests

In order for the tests to work, the example flask application must be ready to answer web requests. This can be done by running the applicatin with the manager command.

```Running through Flask
manager\manager flask
```

You can also get code coverage analysis with this command instead:

```Running through Flask with code coverage
manager\manager coverage flask
```

## Running integration tests normally

***WARNING: you should always restart the flask application before running the integration tests so that data is in its original form!!!***

This is required so that the integration tests always run from a reproducible state.

To run the integration tests, run the following script:

```cmd
manager\manager integration-tests
```

## Running integration tests with code coverage

The integration tests themselves don't need code coverage, but the Flask app does. See above how to run the Flask app with code coverage.

## Running unit tests

You can run the unit-tests with this command:

```Running unit-tests
manager\manager unit-tests
```

You can also get code coverage analysis with this command instead:

```Running unit-tests with code coverage
manager\manager coverage unit-tests
```

## Generating the code coverage report

The following command will generate the code coverage report in HTML
format, after you've run the tetss with code coverage:

```Generate code coverage report in HTML
manager\manager coverage report --html
```

# Update Package Requirements

To update the package requirements when you add a new package:

```cmd
manager\manager dependency update
```


# Running Tests in VSCode

To run the integration tests in Visual Studio Code, you need to setup VSCode to find the necessary packages and use the correct Python virtual environment. Here is brief overview of what you will have to do:

1. Setup VSCode to use the correct virtual environment.
2. Setup VSCode to find the tests.

## 1. Setup VSCode venv

In VSCode, you must select the Python environment created by pipenv. It will typically be found under a `virtualenv` folder and have a complicated name with the words `manager in it. For example:
```
C:\\Users\\Your-User-Name\\.virtualenvs\\resto-_1USwq01\\Scripts\\python.exe
```

## 2. Setup VSCode integration-tests

In VSCode, you must setup the test pane to use unittest. Clicking on the test pane in the left-hand panel (it looks like a chemistry flask), and then trying to run tests, VSCode should prompt you to select the test configuration. Select the following:

* For testing package, select `unittest`
* For testing folder, select `src/unit-tests` or `src/integration-tests`
* For tests pattern, select `test*.py`

You may have to edit the generated `settings.json`, under `.vscode` to change the testing folder from `src` to `src\integration-tests`. For some reason, VSCode does not allow to select a sub-folder when it prompts you.
