#  Integration Tests

This folder contains Gherkin Feature files and associated test step implementations for the project.

### Prerequisites

1. Install python requirements (running the command from within the 'functional_tests' directory):
```
pip install -r requirements.txt
```
2. Install Chrome driver locally and ensure that it is accessible within your $PATH: 

### Executing on Local Dev PC

To use your locally installed Chromedriver (and see the tests running/debug them visually) you will need to pass in a
```
-Dmode=local
```
This overrides the setting in behave.ini - see [Behave Docs](http://pythonhosted.org//behave/new_and_noteworthy_v1.2.5.html#index-7)

