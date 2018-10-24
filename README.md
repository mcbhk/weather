#  Integration Tests

This folder contains Gherkin Feature files and associated test step implementations for the project.

## Prerequisites

1. Install python requirements (running the command from within the 'functional_tests' directory):
```
pip install -r requirements.txt
```
2. Install Chrome driver locally and ensure that it is accessible within your $PATH: 

### Executing on Local PC

* change directory into the top level folder of this project
* Behave -Denv=localhost -Dbrowser=chrome --tags=-wip --tags=browser (INSERT PATH TO acceptance-test/functional_tests/features)


## Next Steps

* The Hourly data summary 'maximum' value tests fail, looks to be a bug.
* what does 'most dominant or current' mean in the requirements? Surely it must be one or the other?

* I'm not convinced that the Page Object Model was required for this one page application - it works well on more complex apps
* I'd prefer to identify elements consistently using IDs - normally I'd work with Developers to add these to the AUT to help with testability.  In this application I found identifying elements could be more complex than necessary.
* Could import the JSON test data 'src' files and compare these dictionaries with data displayed on the UI
* The check for page refresh after showing/hiding page data needs rework/rethought - it works, but..




