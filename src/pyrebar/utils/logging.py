"""Configure the python logger."""
import logging
import logging.config


CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        }
    },
    "handlers": {
        "standard": {"class": "logging.StreamHandler", "formatter": "standard"}
    },
    "loggers": {
        "": {
            "handlers": ["standard"],
            "level": "ERROR",
            "propagate": False,
        }
    },
}
"""Config dictionary."""


def config_args(parser):
    """Add command line arguments for logging.

    Args:
        parser (argparse.ArgumentParser): The command line parser.
    """
    loglevel = parser.add_argument_group(
        title="Log level", description="Set detail level of application log output."
    ).add_mutually_exclusive_group()
    loglevel.add_argument(
        "--quiet",
        action="store_const",
        const="CRITICAL",
        dest="log_level",
        help="Suppress all but the most critical log statements.",
    )
    loglevel.add_argument(
        "--error",
        action="store_const",
        const="ERROR",
        dest="log_level",
        help="Display error logs.",
    )
    loglevel.add_argument(
        "--warn",
        action="store_const",
        const="WARNING",
        dest="log_level",
        help="Display error and warning logs.",
    )
    loglevel.add_argument(
        "--info",
        action="store_const",
        const="INFO",
        dest="log_level",
        help="Print informational logging.",
    )
    loglevel.add_argument(
        "--debug",
        action="store_const",
        const="DEBUG",
        dest="log_level",
        help="Display highly detailed level of logging.",
    )

    loglevel = parser.add_argument_group(
        title="Root log level", description="Set detail level of root log output."
    ).add_mutually_exclusive_group()
    loglevel.add_argument(
        "--root_quiet",
        action="store_const",
        const="CRITICAL",
        dest="log_root_level",
        help="Suppress all but the most critical log statements.",
    )
    loglevel.add_argument(
        "--root_error",
        action="store_const",
        const="ERROR",
        dest="log_root_level",
        help="Display error logs.",
    )
    loglevel.add_argument(
        "--root_warn",
        action="store_const",
        const="WARNING",
        dest="log_root_level",
        help="Display error and warning logs.",
    )
    loglevel.add_argument(
        "--root_info",
        action="store_const",
        const="INFO",
        dest="log_root_level",
        help="Print informational logging.",
    )
    loglevel.add_argument(
        "--root_debug",
        action="store_const",
        const="DEBUG",
        dest="log_root_level",
        help="Display highly detailed level of logging.",
    )
    parser.set_defaults(log_root_level=None, log_level="INFO")


def config_logging(args=None):
    """Configure logging based on the provided command line arguments.

    Args:
        args (argparse.Namespace, optional): The parsed command line arguments.
        Defaults to None.
    """
    app_logger_name = None
    if args:
        if args.logger_name is not None:
            app_logger_name = args.logger_name
        elif args.func:
            m: str = args.func.__module__
            f: str = args.func.__name__
            app_logger_name = m.removesuffix(f".{f}")

    root_level = args.log_root_level or "ERROR"
    if app_logger_name:
        CONFIG["loggers"][app_logger_name] = {
            "handlers": ["standard"],
            "level": args.log_level or "INFO",
            "propagate": False,
        }
    else:
        root_level = args.log_level

    CONFIG["loggers"][""]["level"] = root_level

    logging.config.dictConfig(CONFIG)
