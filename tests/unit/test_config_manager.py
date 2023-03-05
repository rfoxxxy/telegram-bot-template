import logging
import sys

LOGGER = logging.getLogger(__name__)

sys.path.append('./')

from bot_template.core.config_manager import \
    ConfigManager  # pylint: disable=import-error


def test_cfgmgr(config_manager: ConfigManager):

    assert isinstance(config_manager.get_item("core", "supported_modules"),
                      list)

    assert isinstance(config_manager.get_item("telegram", "prod"), bool)

    assert isinstance(
        config_manager.get_item("features.webhook", "webapp_port"), int)
