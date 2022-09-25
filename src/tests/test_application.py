"""Unit tests for application.py."""
import pytest
import unittest.mock

import pyrebar.application

from pyrebar.plugins import PluginModule


@pytest.fixture
def full_plugin() -> PluginModule:
    return PluginModule(
        helpstr="help string",
        command="example_app",
        conf=unittest.mock.MagicMock(),
        func=unittest.mock.MagicMock(),
        aliases=["ex", "app"],
        logger_name="example.pyapp",
    )


def test_add_app():
    """Test adding an app."""
    config_args = unittest.mock.MagicMock()

    parser = unittest.mock.MagicMock()

    plugin = PluginModule(
        helpstr="",
        command=lambda x: 0,
        conf=config_args,
        func=lambda x: 0,
        aliases=[],
        logger_name=None,
    )

    pyrebar.application._add_app(parser=parser, plugin=plugin)

    config_args.assert_called_with(parser)


def test_add_app2():
    """Test adding an app."""
    config_args = unittest.mock.MagicMock()

    parser = unittest.mock.MagicMock()

    plugin = PluginModule(
        helpstr="",
        command=lambda x: 0,
        conf=None,
        func=None,
        aliases=[],
        logger_name=None,
    )

    pyrebar.application._add_app(parser=parser, plugin=plugin)
