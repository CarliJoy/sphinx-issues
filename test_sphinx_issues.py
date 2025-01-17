from tempfile import mkdtemp
from shutil import rmtree
from unittest.mock import Mock

from sphinx.application import Sphinx
from sphinx_issues import (
    issue_role,
    user_role,
    pr_role,
    cve_role,
    cwe_role,
    commit_role,
    setup as issues_setup,
)

import pytest


@pytest.fixture(
    params=[
        # Parametrize config
        {"issues_github_path": "marshmallow-code/marshmallow"},
        {"issues_default_group_project": "marshmallow-code/marshmallow"},
        {
            "issues_uri": "https://github.com/marshmallow-code/marshmallow/issues/{issue}",
            "issues_pr_uri": "https://github.com/marshmallow-code/marshmallow/pull/{pr}",
            "issues_commit_uri": "https://github.com/marshmallow-code/marshmallow/commit/{commit}",
        },
    ]
)
def app(request):
    src, doctree, confdir, outdir = [mkdtemp() for _ in range(4)]
    Sphinx._log = lambda self, message, wfile, nonl=False: None
    app = Sphinx(
        srcdir=src, confdir=None, outdir=outdir, doctreedir=doctree, buildername="html"
    )
    issues_setup(app)
    # Stitch together as the sphinx app init() usually does w/ real conf files
    app.config._raw_config = request.param
    try:
        app.config.init_values()
    except TypeError:
        app.config.init_values(lambda x: x)
    yield app
    [rmtree(x) for x in (src, doctree, confdir, outdir)]


@pytest.fixture()
def inliner(app):
    return Mock(document=Mock(settings=Mock(env=Mock(app=app))))


@pytest.mark.parametrize(
    ("role", "role_name", "text", "expected_text", "expected_url"),
    [
        (
            issue_role,
            "issue",
            "42",
            "#42",
            "https://github.com/marshmallow-code/marshmallow/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Hard Issue <42>",
            "Hard Issue",
            "https://github.com/marshmallow-code/marshmallow/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Not my business <foo/bar#42>",
            "Not my business",
            "https://github.com/foo/bar/issues/42",
        ),
        (
            pr_role,
            "pr",
            "42",
            "#42",
            "https://github.com/marshmallow-code/marshmallow/pull/42",
        ),
        (user_role, "user", "sloria", "@sloria", "https://github.com/sloria"),
        (
            user_role,
            "user",
            "Steven Loria <sloria>",
            "Steven Loria",
            "https://github.com/sloria",
        ),
        (
            cve_role,
            "cve",
            "CVE-2018-17175",
            "CVE-2018-17175",
            "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-17175",
        ),
        (
            cwe_role,
            "cve",
            "CWE-787",
            "CWE-787",
            "https://cwe.mitre.org/data/definitions/787.html",
        ),
        (
            commit_role,
            "commit",
            "123abc456def",
            "@123abc4",
            "https://github.com/marshmallow-code/marshmallow/commit/123abc456def",
        ),
        # External issue
        (
            issue_role,
            "issue",
            "sloria/webargs#42",
            "sloria/webargs#42",
            "https://github.com/sloria/webargs/issues/42",
        ),
        # External PR
        (
            pr_role,
            "pr",
            "sloria/webargs#42",
            "sloria/webargs#42",
            "https://github.com/sloria/webargs/pull/42",
        ),
        # External commit
        (
            commit_role,
            "commit",
            "sloria/webargs@abc123def456",
            "sloria/webargs@abc123d",
            "https://github.com/sloria/webargs/commit/abc123def456",
        ),
    ],
)
def test_roles(inliner, role, role_name, text, expected_text, expected_url):
    result = role(role_name, rawtext="", text=text, lineno=None, inliner=inliner)
    link = result[0][0]
    assert link.astext() == expected_text
    assert link.attributes["refuri"] == expected_url


def test_issue_role_multiple(inliner):
    result = issue_role(
        name=None, rawtext="", text="a title <42>,43", inliner=inliner, lineno=None
    )
    link1 = result[0][0]
    assert link1.astext() == "a title"
    issue_url = "https://github.com/marshmallow-code/marshmallow/issues/"
    assert link1.attributes["refuri"] == issue_url + "42"

    sep = result[0][1]
    assert sep.astext() == ", "

    link2 = result[0][2]
    assert link2.astext() == "#43"
    assert link2.attributes["refuri"] == issue_url + "43"


def test_issue_role_multiple_with_external(inliner):
    result = issue_role(
        "issue", rawtext="", text="42,sloria/konch#43", inliner=inliner, lineno=None
    )
    link1 = result[0][0]
    assert link1.astext() == "#42"
    issue_url = "https://github.com/marshmallow-code/marshmallow/issues/42"
    assert link1.attributes["refuri"] == issue_url

    sep = result[0][1]
    assert sep.astext() == ", "

    link2 = result[0][2]
    assert link2.astext() == "sloria/konch#43"
    assert link2.attributes["refuri"] == "https://github.com/sloria/konch/issues/43"


@pytest.fixture
def app_custom_uri():
    src, doctree, confdir, outdir = [mkdtemp() for _ in range(4)]
    Sphinx._log = lambda self, message, wfile, nonl=False: None
    app = Sphinx(
        srcdir=src, confdir=None, outdir=outdir, doctreedir=doctree, buildername="html"
    )
    issues_setup(app)
    # Stitch together as the sphinx app init() usually does w/ real conf files
    app.config._raw_config = {
        "issues_default_group_project": "myteam/super_great_project",
        "issues_uri": "https://gitlab.company.com/{group}/{project}/-/issues/{issue}",
        "issues_prefix": "#",
        "issues_pr_uri": "https://gitlab.company.com/{group}/{project}/-/merge_requests/{pr}",
        "issues_pr_prefix": "!",
        "issues_commit_uri": "https://gitlab.company.com/{group}/{project}/-/commit/{commit}",
        "issues_commit_prefix": "@",
        "issues_user_uri": "https://gitlab.company.com/{user}",
        "issues_user_prefix": "@",
    }
    try:
        app.config.init_values()
    except TypeError:
        app.config.init_values(lambda x: x)
    yield app
    [rmtree(x) for x in (src, doctree, confdir, outdir)]


@pytest.fixture()
def inliner_custom_uri(app_custom_uri):
    return Mock(document=Mock(settings=Mock(env=Mock(app=app_custom_uri))))


@pytest.mark.parametrize(
    ("role", "role_name", "text", "expected_text", "expected_url"),
    [
        (
            issue_role,
            "issue",
            "42",
            "#42",
            "https://gitlab.company.com/myteam/super_great_project/-/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Hard Issue <42>",
            "Hard Issue",
            "https://gitlab.company.com/myteam/super_great_project/-/issues/42",
        ),
        (
            issue_role,
            "issue",
            "Not my business <foo/bar#42>",
            "Not my business",
            "https://gitlab.company.com/foo/bar/-/issues/42",
        ),
        (
            pr_role,
            "pr",
            "42",
            "!42",
            "https://gitlab.company.com/myteam/super_great_project/-/merge_requests/42",
        ),
        (user_role, "user", "sloria", "@sloria", "https://gitlab.company.com/sloria"),
        (
            user_role,
            "user",
            "Steven Loria <sloria>",
            "Steven Loria",
            "https://gitlab.company.com/sloria",
        ),
        (
            commit_role,
            "commit",
            "123abc456def",
            "@123abc4",
            "https://gitlab.company.com/myteam/super_great_project/-/commit/123abc456def",
        ),
        # External issue
        (
            issue_role,
            "issue",
            "sloria/webargs#42",
            "sloria/webargs#42",
            "https://gitlab.company.com/sloria/webargs/-/issues/42",
        ),
        # External PR
        (
            pr_role,
            "pr",
            "sloria/webargs#42",
            "sloria/webargs!42",
            "https://gitlab.company.com/sloria/webargs/-/merge_requests/42",
        ),
        # External commit
        (
            commit_role,
            "commit",
            "sloria/webargs@abc123def456",
            "sloria/webargs@abc123d",
            "https://gitlab.company.com/sloria/webargs/-/commit/abc123def456",
        ),
    ],
)
def test_roles_custom_uri(
    inliner_custom_uri, role, role_name, text, expected_text, expected_url
):
    result = role(
        role_name, rawtext="", text=text, lineno=None, inliner=inliner_custom_uri
    )
    link = result[0][0]
    assert link.astext() == expected_text
    assert link.attributes["refuri"] == expected_url
