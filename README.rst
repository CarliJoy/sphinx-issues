=============
sphinx-issues
=============

.. image:: https://badgen.net/pypi/v/sphinx-issues
  :alt: pypi badge
  :target: https://pypi.org/project/sphinx-issues/

.. image:: https://github.com/OpenASL/HowSignBot/workflows/.github/workflows/test.yml/badge.svg
  :alt: github actions status
  :target: .github/workflows/test.yml

.. image:: https://badgen.net/badge/code%20style/black/000
   :target: https://github.com/ambv/black
   :alt: Code style: Black

A Sphinx extension for linking to your project's issue tracker. Includes roles for linking to issues, pull requests, user profiles, with built-in support for GitHub (though this works with other services).

Example
*******

For an example usage, check out `marshmallow's changelog <http://marshmallow.readthedocs.org/en/latest/changelog.html>`_, which makes use of the roles in this library.

Installation and Configuration
******************************

.. code-block:: console

    pip install sphinx-issues


Add ``sphinx_issues`` to ``extensions`` in your ``conf.py``.

The extension has default values for GitHub projects.
Simply set the add the ``issues_default_group_project`` config variable and you are good
to go:

.. code-block:: python

    # docs/conf.py

    # ...
    extensions = [
        # ...
        "sphinx_issues"
    ]

    # Path to GitHub repo {group}/{project}  (note that `group` is the GitHub user or organization)
    issues_github_path = "sloria/marshmallow"

    # which is the equivalent to:
    issues_uri = "https://github.com/{group}/{project}/issues/{issue}"
    issues_prefix = "#"
    issues_pr_uri = "https://github.com/{group}/{project}/pull/{pr}"
    issues_pr_prefix = "#"
    issues_commit_uri = "https://github.com/{group}/{project}/commit/{commit}"
    issues_commit_prefix = "@"
    issues_user_uri = "https://github.com/{user}"
    issues_user_prefix = "@"

The extension is very configurable and can be used with any kind of
issue tracker. Here is how you could configure it for use
with a custom hosed GitLab instance:

.. code-block:: python

    # docs/conf.py

    # ...
    extensions = [
        # ...
        "sphinx_issues"
    ]

    #  Default repo {group}/{project} of gitlab project
    issues_default_group_project = "myteam/super_great_project"
    issues_uri = "https://gitlab.company.com/{group}/{project}/-/issues/{issue}"
    issues_prefix = "#"
    issues_pr_uri = "https://gitlab.company.com/{group}/{project}/-/merge_requests/{pr}"
    issues_pr_prefix = "!"
    issues_commit_uri = "https://gitlab.company.com/{group}/{project}/-/commit/{commit}"
    issues_commit_prefix = "@"
    issues_user_uri = "https://gitlab.company.com/{user}"
    issues_user_prefix = "@"


Usage inside the documentation
******************************

Use the ``:issue:``  and ``:pr:`` roles in your docs like so:

.. code-block:: rst

    See issue :issue:`42`

    See issues :issue:`12,13`

    See :issue:`sloria/konch#45`.

    See PR :pr:`58`


Use the ``:user:`` role in your docs to link to user profiles (GitHub by default, but can be configured via the ``issues_user_uri`` config variable).


Use the ``:commit:`` role to link to commits.

.. code-block:: rst

    Fixed in :commit:`6bb9124d5e9dbb2f7b52864c3d8af7feb1b69403`.

Use the ``:cve:`` role to link to CVEs on https://cve.mitre.org.

.. code-block:: rst

    :cve:`CVE-2018-17175` - Addresses possible vulnerability when...

.. code-block:: rst

    Thanks to :user:`bitprophet` for the idea!

You can also use explicit names if you want to use a different name than the github user name:

.. code-block:: rst

    This change is due to :user:`Andreas Mueller <amueller>`.

The syntax ``:role:`My custom title <target>``` works for all roles of this extension.

It can be also used in combination with a list:

.. code-block:: rst

    Fix bad bug :issue:`123, (Duplicate) <199>`

Use the ``:cwe:`` role to link to CWEs on https://cwe.mitre.org.

.. code-block:: rst

    :cwe:`CWE-787` - The software writes data past the end, or...

Credits
*******

Credit goes to Jeff Forcier for his work on the `releases <https://github.com/bitprophet/releases>`_ extension, which is a full-featured solution for generating changelogs. I just needed a quick way to reference GitHub issues in my docs, so I yoinked the bits that I needed.

License
*******

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/sphinx-issues/blob/master/LICENSE>`_ file for more details.


Changelog
*********

3.0.0 (unreleased)
------------------

- The `:commit:` role now outputs with an `@` prefix.
- Add configuration options for changing prefixes.
- Allow `{group}` to be specified within `issues_uri`, `issues_pr_uri`, `issues_commit_uri`, and 

2.0.0 (2022-01-01)
------------------

- Drop support for Python 2.7 and 3.5.
- Test against Python 3.8 to 3.10.
- Add ``:cwe:`` role for linking to CVEs on https://cwe.mitre.org.
  Thanks @hugovk for the PR.

1.3.0 (unreleased)
------------------
- Add support for custom urls and separators `Issue #93 <https://github.com/sloria/sphinx-issues/issues/93>`_
- Allow custom titles for all roles `Issue #116 <https://github.com/sloria/sphinx-issues/issues/116>`_
- Added setting `issues_default_group_project` as future replacement of `issues_github_path`, to reflect the now to universal nature of the extension

1.2.0 (2018-12-26)
------------------

- Add ``:commit:`` role for linking to commits.
- Add support for linking to external repos.
- Test against Python 3.7.

1.1.0 (2018-09-18)
------------------

- Add ``:cve:`` role for linking to CVEs on https://cve.mitre.org.

1.0.0 (2018-07-14)
------------------

- Add ``:pr:`` role. Thanks @jnotham for the suggestion.
- Drop support for Python 3.4.

0.4.0 (2017-11-25)
------------------

- Raise ``ValueError`` if neither ``issues_uri`` nor ``issues_github_path`` is set. Thanks @jnothman for the PR.
- Drop support for Python 2.6 and 3.3.

0.3.1 (2017-01-16)
------------------

- ``setup`` returns metadata, preventing warnings about parallel reads and writes. Thanks @jfinkels for reporting.

0.3.0 (2016-10-20)
------------------

- Support anchor text for ``:user:`` role. Thanks @jnothman for the suggestion and thanks @amueller for the PR.

0.2.0 (2014-12-22)
------------------

- Add ``:user:`` role for linking to GitHub user profiles.

0.1.0 (2014-12-21)
------------------

- Initial release.
