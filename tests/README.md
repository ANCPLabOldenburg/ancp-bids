The data folder contains synthetic datasets that can be used in the unit tests.
Do not change these datasets as they fulfill specific requirements that may break.
In case a modification is needed, and you cannot guarantee that the semantics of existing unit tests might be affected,
copy and paste the dataset you need, then modify.

unit test types:

- *auto*: unit tests that can be safely run automatically within a CI/CD pipeline
- *manual*: unit tests that may be not reliably reproducible, for example, because of timing issues, should be run
  manually

