from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).parent.parent / "app.py")
EXPECTED = {
    "first-1000": "Your First $1,000",
    "life-happens": "Life Happens",
    "investment-risk": "Investment Risk Lab",
    "green-investing": "Green Investing Lab",
    "responsible-consumption": "Responsible Consumption Lab",
}


def run(lab=None):
    at = AppTest.from_file(APP, default_timeout=30)
    if lab is not None:
        at.query_params["lab"] = lab
    return at.run()


def test_default_is_dashboard_with_all_modules():
    at = run()
    assert not at.exception
    assert at.session_state["academy_page"] == "Dashboard"
    assert at.sidebar.radio[0].options == ["Dashboard"] + list(EXPECTED.values())


@pytest.mark.parametrize("slug,name", EXPECTED.items())
def test_deep_link_selects_radio(slug, name):
    at = run(slug)
    assert not at.exception
    assert at.sidebar.radio[0].value == name
    assert at.query_params["lab"] == slug


@pytest.mark.parametrize("lab", ["", "nope", "GREEN-INVESTING "])
def test_invalid_or_odd_slug(lab):
    at = run(lab)
    assert not at.exception
    expected = "Green Investing Lab" if lab.strip().lower() == "green-investing" else "Dashboard"
    assert at.sidebar.radio[0].value == expected


def test_invalid_slug_removed_from_url():
    at = run("nope")
    assert "lab" not in at.query_params


@pytest.mark.parametrize("slug,name", EXPECTED.items())
def test_manual_switch_updates_url(slug, name):
    at = run()
    at.sidebar.radio[0].set_value(name).run()
    assert not at.exception
    assert at.query_params["lab"] == slug
    at.sidebar.radio[0].set_value("Dashboard").run()
    assert "lab" not in at.query_params
