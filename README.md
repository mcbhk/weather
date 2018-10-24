#  Integration Tests

This folder contains Gherkin Feature files and associated test step implementations for the project.

## Prerequisites

1. Install python requirements:
```
pip install -r requirements.txt
```
2. Install Chrome driver locally and ensure that it is accessible within your $PATH: 

### Executing on Local PC

* change directory into the top level folder of this project
```
Behave -Denv=localhost -Dbrowser=chrome --tags=-wip --tags=browser /functional_tests/features
```

## Next Steps I'd do in the real world

* The Hourly data summary 'maximum' value tests fail, looks to be a bug. Discuss with team.
* what does 'most dominant or current' mean in the requirements? Surely it must be one or the other? Clarify with PO.
* I didn't finish all the features/requirements or get as far as considering accessibility/ edge cases - I just tried to cover core cases in the time.
* Do some exploratory testing around the points above

### Some other comments / things I'd refactor/change

* I'm not convinced that the Page Object Model I chose to use was required for this one page application - it works well on more complex apps, but was perhaps over-engineering for this one.
* I'd prefer to identify elements consistently using ID's - normally I'd work with Developers to add these to the AUT in order to aid testability.  In this application I found identifying elements could be more complex than necessary, and I think that impacts some of the code readability.
* Could import the JSON test data 'src' files used by the AUT (or use requests to get the source data from the API directly) and compare these dictionaries with data displayed on the UI
* The check for page refresh after showing/hiding page data needs rework/rethought - it works, but..




