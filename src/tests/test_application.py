"""Unit tests for application.py."""
import argparse
import pytest
import unittest.mock
import pyrebar.application

from importlib.metadata import EntryPoint
from pyrebar.plugins import PluginModule, ProcessedPlugins, Plugins


@pytest.fixture
def full_plugin() -> PluginModule:
    """Provide a plugin fixture.

    Returns:
        PluginModule: a mock module
    """
    return PluginModule(
        helpstr="help string",
        command="example_app",
        conf=unittest.mock.MagicMock(),
        func=unittest.mock.MagicMock(),
        aliases=["ex", "app"],
        logger_name="example.pyapp",
    )


@pytest.fixture
def processed_plugins() -> ProcessedPlugins:
    """Bootstrap the plugins."""
    return ProcessedPlugins(
        pre_init=(
            EntryPoint(
                name="example-init",
                value="pyrebar.apps.example:initialize",
                group=Plugins.PREINIT_GROUP,
            )
        ),
        post_init=(
            EntryPoint(
                name="example-init",
                value="pyrebar.apps.example:initialize",
                group=Plugins.POSTINIT_GROUP,
            )
        ),
        apps=(
            EntryPoint(
                name="example-init",
                value="pyrebar.apps.example",
                group=Plugins.APP_GROUP,
            )
        ),
        shutdown=(
            EntryPoint(
                name="example-init",
                value="pyrebar.apps.example:shutdown",
                group=Plugins.SHUTDOWN_GROUP,
            )
        ),
    )


@pytest.mark.framework
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


@pytest.mark.framework
def test_add_app2():
    """Test adding an app."""
    parser = argparse.ArgumentParser()

    plugin = PluginModule(
        helpstr="",
        command=lambda x: 0,
        conf=None,
        func=None,
        aliases=[],
        logger_name=None,
    )

    pyrebar.application._add_app(parser=parser, plugin=plugin)

    args = parser.parse_args(args="")
    args.func()


@unittest.mock.patch("sys.exit")
def test_main(mock_exit):
    """Run an example application."""
    Plugins.add_entrypoint(
        EntryPoint(
            name="example-init",
            value="pyrebar.apps.example:initialize",
            group=Plugins.PREINIT_GROUP,
        )
    )
    Plugins.add_entrypoint(
        EntryPoint(
            name="example-init",
            value="pyrebar.apps.example:initialize",
            group=Plugins.POSTINIT_GROUP,
        )
    )
    Plugins.add_entrypoint(
        EntryPoint(
            name="example-init", value="pyrebar.apps.example", group=Plugins.APP_GROUP
        )
    )
    Plugins.add_entrypoint(
        EntryPoint(
            name="example-init",
            value="pyrebar.apps.example:shutdown",
            group=Plugins.SHUTDOWN_GROUP,
        )
    )
    pyrebar.application.main(argv=["--info"])
