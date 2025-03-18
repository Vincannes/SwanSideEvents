#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

import logging
from app.constants import EVENT_LOG

_logger = None


def init_logger():
    """
    Initialise le logger avec un fichier de log et une sortie console.
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("SwanSide Events Handler")
        _logger.setLevel(logging.INFO)

        # Format du log
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Handler pour le fichier de log
        file_handler = logging.FileHandler(EVENT_LOG)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)

        # Handler pour la console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        _logger.addHandler(stream_handler)


def get_logger():
    """
    Retourne le logger initialisé.
    """
    if _logger is None:
        raise RuntimeError("Le logger n'a pas été initialisé. Appelle 'init_logger()' d'abord.")
    return _logger
