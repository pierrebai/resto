# Description

This Python repo contains three elements of interest:

- A small single-file module to help easily test REST API.
- A small single-file module to easily add Swagger (OpenApi) documentations to Python flask routes.
- A small single-file module to emulate the AWS Lambda API.


## Resto

Resto is the REST API helper. Its source code is found in the file
`src/integration-tests/resto.py`. The bulk of its functionality is in the
`Expected` class.

The class constructor takes many parameters. They can be divided in two categories: input and output.

The input parameters are:

- The URL to call.
- The HTTP method to use: GET, POST, PUT or DELETE.
- The request parameters, as a Python dict.
- The headers to send, as a Python dict.
- The JSON body to send, as a Python dict.

The output parameters are:

- The headers expected to be received, as a Python dict.
- The JSON body expected to be received, as a Python dict.
- The request status code expected to be received.
- If the output JSON should be strictly compared.

Once an instance of Expected is built, you can invoke its call() function. It
will send the request and compare the expected results with the actual results
and return the difference. It tries to be smart when matching JSON and headers.

See the various integration tests in the repo for examples of how to use resto.


## Easy Swag

The easy-swagger documentation module is called easy swag. Its source code is
found in the file `src/flask-app/easy_swag.py`. The easy swag module is built
on top of the flask_apispec module and the marshmallow module. It contains two
functions and a decorator:

- set_error_schema(): sets the marshmallow schema to be used as error report
  for all REST API.
- register_with_swagger_docs(): registers all swagger/OpenApi doc that have
  been declared with the flask app.
- swag(): the decorator taking input and output schemas, documentation string,
  tag and returned HTTP status code. It generates the proper doc.

## AWS Lambda emulator

The AWS Lambda emulator bridges Python's flask with the Lambda API. It takes
the flask request and response and converts them into the corresponding Lambda
event, context and result.

The code is contained in the file `src/flask-app/aws_emulator.py`. It has three
functions:

- get_event(): creates an AWS Lambda event from the current flask request.
- get_context(): creates a dummy AWS Lambda context.
- convert_result(): converts an AWS Lambda result dictionary into a flask response.

This allows writing a small flask app that emulates the AWS Lambda by calling
the same implementation code. In our integration tests, we've found that this
yields about 80x (yes eighty times) the speed of running AWS Lambda locally in
docker. The reason for the amazing speed-up is that Lambda starts and stops the
docker for *every* request! In our application, using the AWS emulator cuts the
testing time from 15 minutes down to 10 seconds.


# Setup

You will need the following to use this code:

- Python 3.7+: see [Python official site for an installer](https://www.python.org/)
- pipenv: run `pip install pipenv` in a shell that has Python in its command path.
- Python dependencies: run `pipenv install` in the root of the project.


# Running Tests

## Preparing to run the tests

In order for the tests to work, the example flask application must be ready to
answer web requests. This can be done by running the applicatin with the
manager command. Use the command script (`manager.cmd` on Windows) or shell
script (`manager` on Linux/MacOS):

```Running through Flask
manager flask
```

You can also get code coverage analysis with this command instead:

```Running through Flask with code coverage
manager coverage flask
```

## Running integration tests normally

***WARNING: you should always restart the flask application before running the
integration tests so that data is in its original form!!!***

This is required so that the integration tests always run from a reproducible
state.

To run the integration tests, run the following script:

```cmd
manager integration-tests
```

## Running integration tests with code coverage

The integration tests themselves don't need code coverage, but the Flask app
does. See above how to run the Flask app with code coverage.

## Running unit tests

You can run the unit-tests with this command:

```Running unit-tests
manager unit-tests
```

You can also get code coverage analysis with this command instead:

```Running unit-tests with code coverage
manager coverage unit-tests
```

## Generating the code coverage report

The following command will generate the code coverage report in HTML
format, after you've run the tests with code coverage:

```Generate code coverage report in HTML
manager coverage report --html
```

If you run both the unit-tests and integration tests with code coverage, you
will find that they reach 99% total coverage. Not bad!


# Update Package Requirements

If you modify the code and need an additional Python package, you can add it
using pipenv or the manager. To add or update a package, use these commands:

```cmd
manager dependency add *new-package-name*
```

```cmd
manager dependency update
```


# Running Tests in VSCode

To run the integration tests in Visual Studio Code, you need to setup VSCode to
find the necessary packages and use the correct Python virtual environment.
Here is brief overview of what you will have to do:

1. Setup VSCode to use the correct virtual environment.
2. Setup VSCode to find the tests.

## 1. Setup VSCode venv

In VSCode, you must select the Python environment created by pipenv. It will
typically be found under a `virtualenv` folder and have a complicated name with
the words `manager in it. For example:

```
C:\\Users\\Your-User-Name\\.virtualenvs\\resto-_1USwq01\\Scripts\\python.exe
```

## 2. Setup VSCode integration-tests

In VSCode, you must setup the test pane to use unittest. Clicking on the test
pane in the left-hand panel (it looks like a chemistry flask), and then trying
to run tests, VSCode should prompt you to select the test configuration. Select
the following:

* For testing package, select `unittest`
* For testing folder, select `src/unit-tests` or `src/integration-tests`
* For tests pattern, select `test*.py`

You may have to edit the generated `settings.json`, under `.vscode` to change
the testing folder from `src` to `src\integration-tests`. For some reason,
VSCode does not allow to select a sub-folder when it prompts you.

