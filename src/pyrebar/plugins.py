"""Load and manage application plugins."""
import inspect
import sys
from dataclasses import dataclass
from typing import Any

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points, EntryPoint, EntryPoints
else:
    from importlib.metadata import entry_points, EntryPoint, EntryPoints


@dataclass(frozen=True)
class PluginModule:
    """Plugin module data class, describing a plugin."""

    helpstr: str
    """The help string to display for this plugin."""
    command: str
    """The command to use on the command line."""
    conf: Any
    """Function to configure the command line parameters."""
    func: Any
    """The execution function for this plugin."""
    aliases: list
    """Various aliases for this module."""
    logger_name: str
    """Name of the logger to automatically configure."""


@dataclass(frozen=True)
class ProcessedPlugins:
    """Data after processing the various entrypoints."""

    pre_init: tuple[EntryPoint]
    """Pre-init plugin functions."""
    post_init: tuple[EntryPoint]
    """Post-init plugin functions."""
    apps: tuple[EntryPoint]
    """Application plugin modules."""
    shutdown: tuple[EntryPoint]
    """Post-application shutdown."""

    @staticmethod
    def loadapp(ep: EntryPoint) -> PluginModule:
        """Load an process an entrypoint into a plugin module.

        Args:
            ep (EntryPoint): The `EntryPoint` representing a plugin module.

        Returns:
            PluginModule: The processed plugin module.
        """
        module = ep.load()
        aliases = []
        helpstr = ""
        func = None
        conf = None
        command = ep.name
        logger_name = module.__name__

        for n, value in inspect.getmembers(module):
            if n == "__doc__":
                helpstr = value
            elif n == "SUBCOMMAND":
                command = value
            elif n == "config_args":
                conf = value
            elif n == "execute":
                func = value
            elif n == "ALIASES":
                aliases = value
            elif n == "LOGGER_NAME":
                logger_name = value

        return PluginModule(
            helpstr=helpstr,
            func=func,
            conf=conf,
            command=command,
            aliases=aliases,
            logger_name=logger_name,
        )


class Plugins:
    """Module enabling bootstrapping the `entry_points()` list."""

    PREINIT_GROUP = "pyrebar.preinit"
    """Group used for the pre-init step."""

    POSTINIT_GROUP = "pyrebar.postinit"
    """Group used for the post-init step."""

    APP_GROUP = "pyrebar.app"
    """Group used for applications."""

    SHUTDOWN_GROUP = "pyrebar.shutdown"
    """Group used for the post-application shutdown."""

    __entrypoints: list[EntryPoint] = []

    @classmethod
    def add_entrypoint(cls, ep: EntryPoint):
        """Explicitly add an entrypoint.

        These `EntryPoint` instances will be provided in addition to the results of those
        from the importlib metadata module.  Call this method to bootstrap applications
        running from `__main__` rather than as an installed module.

        Args:
            ep (EntryPoint): The entrypoint to add.
        """
        if ep:
            cls.__entrypoints.append(ep)

    @classmethod
    def entry_points(cls) -> EntryPoints:
        """Provide entry points from the installed modules.

        This method aggregates the installed modules with any included via
        bootstrapping.

        Returns:
            EntryPoints: The resulting entrypoints
        """
        points = entry_points()

        for e in cls.__entrypoints:
            if e.name in points.names:
                points[e.name].append(e)
            else:
                points[e.name] = [e]

        return points

    @classmethod
    def extract_plugins(cls) -> ProcessedPlugins:
        """Extract the py-rebar plugins from the entrypoints.

        Returns:
            ProcessedPlugins: The processed entrypoints
        """
        entry_points = Plugins.entry_points()

        pre_init = tuple(e for e in entry_points.select(group=Plugins.PREINIT_GROUP))
        post_init = tuple(e for e in entry_points.select(group=Plugins.POSTINIT_GROUP))
        apps = tuple(e for e in entry_points.select(group=Plugins.APP_GROUP))
        shutdown = tuple(e for e in entry_points.select(group=Plugins.SHUTDOWN_GROUP))

        return ProcessedPlugins(
            pre_init=pre_init, post_init=post_init, apps=apps, shutdown=shutdown
        )
