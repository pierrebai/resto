# Setup

The setup of integration tests is done during the main project setup.
See the `dev-setup.md` file in the root of the project.


# Running Tests

### Preparing to run the tests

In order for the tests to work, the AWS SAM Lambda functions must be ready to answer web requests. This can be done either by running the functions with a SAM CLI command or running the functions through a Flask application.

Running through a Flask application has the benefits or being *much* faster and allowing to optionally record code coverage statistics. See `src/flask-functions/README.md` for more details.

```Running through SAM
manager\manager lambda start
```

```Running through Flask
manager\manager flask
```

```Running through Flask with code coverage
manager\manager coverage flask
```

### Running integration tests normally

***WARNING: you should always recreate the database before running the integration tests!!!***

This is required so that the integration tests always run from a reproducible state.

To run the integration tests, run the following script:

```cmd
manager\manager integration-tests
```

### Running integration tests with code coverage

The integration tests themselves don't need code coverage, but the Flask app does. See above how to run the Flask app with code coverage.

# Update Package Requirements

To update the package requirements when you add a new package:

```cmd
manager\manager dependency update
```


# Running Tests in VSCode

To run the integration tests in Visual Studio Code, you need to setup VSCode to find the necessary packages and use the correct Python virtual environment. Here is brief overview of what you will have to do:

1. Setup VSCode to use the correct virtual environment.
2. Setup VSCode to find the tests.

### 1. Setup VSCode venv

In VSCode, you must select the Python environment created by pipenv. It will typically be found under a `virtualenv` folder and have a complicated name with the words `manager in it. For example:
```
C:\\Users\\Pierre\\.virtualenvs\\manager-_1USwq01\\Scripts\\python.exe
```

### 2. Setup VSCode integration-tests

In VSCode, you must setup the test pane to use unittest. Clicking on the test pane in the left-hand panel (it looks like a chemistry flask), and then trying to run tests, VSCode should prompt you to select the test configuration. Select the following:

* For testing package, select `unittest`
* For testing folder, select `src`
* For tests pattern, select `test*.py`

You may have to edit the generated `settings.json`, under `.vscode` to change the testing folder from `src` to `src\integration-tests`. For some reason, VSCode does not allow to select a sub-folder when it prompts you.
