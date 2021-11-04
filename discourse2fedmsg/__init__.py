# Set the version
try:
    import importlib.metadata

    __version__ = importlib.metadata.version("discourse2fedmsg")
except ImportError:
    try:
        import pkg_resources

        try:
            __version__ = pkg_resources.get_distribution(
                "discourse2fedmsg"
            ).version
        except pkg_resources.DistributionNotFound:
            __version__ = None
    except ImportError:
        __version__ = None
