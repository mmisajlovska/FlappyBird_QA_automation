import logging
import os
import unittest
from unittest.mock import patch

# Set Pygame to run headlessly BEFORE importing pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.display.set_mode((288, 512)) # Initialize a dummy display for surface generation

# Configure log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "test_run.log")

# Configure root logger
logger = logging.getLogger("QA_Automation")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

class BaseQATestCase(unittest.TestCase):
    """
    Base QA Test Case that provides:
    - Centralized logging initialization
    - Standard setup/teardown logging
    - Headless mode by patching Pygame display and audio
    """

    @classmethod
    def setUpClass(cls):
        logger.info(f"=== Starting Test Suite: {cls.__name__} ===")
        
        # We don't need to patch Pygame globals as we use SDL_VIDEODRIVER=dummy
        # but we can patch specific custom classes if needed.
        
        cls.patcher_mixer = patch("pygame.mixer.init")
        cls.patcher_mixer.start()
        
        cls.patcher_sounds = patch("src.utils.sounds.Sounds")
        cls.patcher_sounds.start()

        cls.patcher_images = patch("src.utils.images.Images")
        cls.patcher_images.start()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()
        logger.info(f"=== Finished Test Suite: {cls.__name__} ===\n")

    def setUp(self):
        logger.info(f"[TEST START] {self._testMethodName}")

    def tearDown(self):
        # Determine test outcome for logging
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)
            error = self.list2reason(result.errors)
            failure = self.list2reason(result.failures)
            
            if error or failure:
                logger.error(f"[TEST FAILED] {self._testMethodName}: {error or failure}")
            else:
                logger.info(f"[TEST PASSED] {self._testMethodName}")
        else:
            logger.info(f"[TEST FINISHED] {self._testMethodName}")

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]
