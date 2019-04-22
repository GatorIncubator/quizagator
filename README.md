# Quiz-A-Gator

![logo](logo.jpg "Professor Spidey")

[![Build Status](https://travis-ci.com/GatorEducator/quizagator.svg?branch=master)](https://travis-ci.com/GatorEducator/quizagator)
[![codecov.io](http://codecov.io/github/GatorEducator/quizagator/coverage.svg?branch=master)](
http://codecov.io/github/GatorEducator/quizagator?branch=master)
[![made-with-python](
https://img.shields.io/badge/Made%20with-Python-blue.svg)](
https://www.python.org/)

## A Quiz Creation Tool for File Upload and Custom Grading

It may seem obvious that there are many other tools for creating quizzes, but
interestingly the quiz creation tools out there all have one thing in common:
Web-based GUI. Quizagator is a web application that provides an interface for
creating quizzes without the overhead of a GUI making quizzes creation tedious
and--in the case that the design of the GUI tool changes--confusing. By allowing
quiz creation through a text-based syntax it is possible to make quiz creation
lightning fast and much more consistent than fiddling with GUI tools. Not to
mention a text-based quiz creation allows for easy question duplication and
modification. Quizagator supports uploading quizzes in CSV format and allows for
grading with a custom grading program. The tool uses Flask with noSQL to manage
quizzes and results, as well as storing any custom grading tools uploaded to the
quizzes.

Quizagator uses it's own custom quiz creation syntax in CSV format that is
designed to be programmer-friendly to allow for more mutable quiz creation that
comes with all the benefits a text-based system allows, namely the ability to use
your favorite text editor rather than the ever-present GUI's.

Quiz questions look like this:

```csv
"Quizquestion?","correct answer","answer1","answer2","answer3","answer4"

"What's the best quiz creation tool?","1","Quizagator","Google Forms","Sakai Quizzes","Quiz Maker"
```

Once a quiz has been created a grading program can be uploaded to implement a
custom grading scheme for the quiz. Quizagator will run the program on the
results of the quiz and return the output.

## Pipenv

Quizagator uses a [Pipenv](https://project/pipenv/)-built virtual environment
to standardize the execution of the project. If you don't have pipenv we highly
recommend installing it using `pip`:

```
pip install pipenv
```

If for some reason this doesn't work for you, you can check out the [pipenv
github](https://github.com/pypa/pipenv).

## Commands

After cloning the repo for the first time, run

```
pipenv install --dev
```

to install the developer and default packages. To get a list of scripts for the
project, inspect the `[scripts]` tag in `Pipfile`:

```
cat Pipfile
```

Finally, to run the project locally:

```
pipenv run server
```

Or use the following to see all the options:

```
pipenv run python run.py --help
```

## Contributors

Check out our contributors!

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table><tr><td align="center"><a href="https://github.com/quigley-c"><img src="https://avatars1.githubusercontent.com/u/35495466?v=4" width="100px;" alt="Carson Quigley"/><br /><sub><b>Carson Quigley</b></sub></a><br /><a href="https://github.com/GatorEducator/quizagator/commits?author=quigley-c" title="Documentation">📖</a></td></tr></table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

Don't know what the emoji's mean? Check out the [key](https://allcontributors.org/docs/en/emoji-key)!
