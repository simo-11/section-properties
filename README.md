<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/logo-dark-mode.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/logo-light-mode.png">
  <img alt="sectionproperties logo" src="docs/_static/logo-light-mode.png">
</picture>

[![PyPI](https://img.shields.io/pypi/v/sectionproperties.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/sectionproperties.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/sectionproperties)][python version]
[![License](https://img.shields.io/pypi/l/sectionproperties)][license]
[![Read the documentation at https://sectionproperties.readthedocs.io/](https://img.shields.io/readthedocs/sectionproperties/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/robbievanleeuwen/section-properties/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/robbievanleeuwen/section-properties/branch/master/graph/badge.svg)][codecov]
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/sectionproperties/
[status]: https://pypi.org/project/sectionproperties/
[python version]: https://pypi.org/project/sectionproperties
[read the docs]: https://sectionproperties.readthedocs.io/
[tests]: https://github.com/robbievanleeuwen/section-properties/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/robbievanleeuwen/section-properties
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

`sectionproperties` is a python package for the analysis of arbitrary cross-sections
using the finite element method. `sectionproperties` can be used to determine
section properties to be used in structural design and visualise cross-sectional
stresses resulting from combinations of applied forces and bending moments.

[Subscribe](http://eepurl.com/dMMUeg) to the `sectionproperties` mailing list!

## Installation

You can install `sectionproperties` via [pip] from [PyPI]:

```shell
pip install sectionproperties
```

## Documentation

`sectionproperties` is fully documented including a user walkthrough, examples,
background theory and an API guide. The documentation can found at
[https://sectionproperties.readthedocs.io/](https://sectionproperties.readthedocs.io/).

## Features

See the complete list of `sectionproperties` features
[here](https://sectionproperties.readthedocs.io/en/latest/user_guide.html).

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license], `sectionproperties` is free
and open source software.

## Support

Found a bug 🐛, or have a feature request ✨, raise an issue on the
GitHub [issue tracker](https://github.com/robbievanleeuwen/section-properties/issues)
Alternatively you can get support on the
[discussions](https://github.com/robbievanleeuwen/section-properties/discussions) page.

## Disclaimer

`sectionproperties` is an open source engineering tool that continues to benefit from
the collaboration of many contributors. Although efforts have been made to ensure the
that relevant engineering theories have been correctly implemented, it remains the
user's responsibility to confirm and accept the output. Refer to the
[license](LICENSE.md) for clarification of the conditions of use.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter]
template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[pip]: https://pip.pypa.io/
[license]: https://github.com/robbievanleeuwen/section-properties/blob/master/LICENSE
[contributor guide]: https://github.com/robbievanleeuwen/section-properties/blob/master/CONTRIBUTING.md
