############################
# Libraries used as plugins
############################

try:
    import karateclub as _

    has_karateclub = True
except ImportError:
    has_karateclub = False


import metagraph

# Use this as the entry_point object
registry = metagraph.PluginRegistry("metagraph_karateclub")


def find_plugins():
    # Ensure we import all items we want registered
    from . import karateclub

    registry.register_from_modules(
        karateclub, name="metagraph_karateclub_karateclub"
    )  # TODO should we have a better naming convention?
    return registry.plugins
