# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license] and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code]
- [Issue Tracker]
- [Code of Conduct]

[MIT license]: https://opensource.org/licenses/MIT
[source code]: https://github.com/KennethEnevoldsen/augmenty
[issue tracker]: https://github.com/KennethEnevoldsen/augmenty/issues

## How to report a bug

Report bugs on the [Issue Tracker].

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker].

## How to set up your development environment

To install all the development dependencies, you can use the [make] command:

```console
$ make install
```


## How to test the project

Run the full test suite:

```console
$ make test
```

Unit tests are located in the _tests_ directory.

## How to submit changes

Open a [pull request] to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The test suite should ideally pass without errors and warnings.
- Ideally add tests for your changes.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can run the following [make] command:

```console
$ make lint
```

It is recommended to open an issue before starting work on any major changes.
This will allow a chance to talk it over with the owners and validate your approach.

[pull request]: https://github.com/KennethEnevoldsen/augmenty/pulls
[make]: https://makefiletutorial.com

<!-- github-only -->

[code of conduct]: CODE_OF_CONDUCT.md