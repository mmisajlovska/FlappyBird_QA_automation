import pygame
from unittest.mock import MagicMock
from tests.test_base import BaseQATestCase, logger
from src.entities.player import Player, PlayerMode
from src.entities.pipe import Pipe, Pipes
from src.entities.floor import Floor
from src.utils.game_config import GameConfig
from src.utils.window import Window

class TestGameLogic(BaseQATestCase):
    
    def setUp(self):
        super().setUp()
        logger.info("Initializing dummy GameConfig and Player for test scenario")
        
        # Setup dummy configurations
        self.mock_window = Window(288, 512)
        self.mock_screen = pygame.Surface((self.mock_window.width, self.mock_window.height))
        
        # Setup dummy surfaces instead of mocks so hitmasks can be generated
        mock_surface = pygame.Surface((34, 24))
        mock_pipe_surface = pygame.Surface((52, 320))
        mock_floor_surface = pygame.Surface((336, 112))
        
        mock_images = MagicMock()
        mock_images.player = [mock_surface, mock_surface, mock_surface, mock_surface]
        mock_images.pipe = (mock_pipe_surface, mock_pipe_surface)
        mock_images.base = mock_floor_surface
        mock_images.background = pygame.Surface((288, 512))
        mock_images.message = pygame.Surface((184, 267))
        mock_images.gameover = pygame.Surface((192, 42))
        mock_images.numbers = [pygame.Surface((24, 36))] * 10
        
        self.mock_config = GameConfig(
            screen=self.mock_screen,
            clock=MagicMock(),
            fps=30,
            window=self.mock_window,
            images=mock_images,
            sounds=MagicMock() # We mocked Sounds class in base so this won't break
        )
        
        self.player = Player(self.mock_config)

    def test_boundary_and_physics(self):
        """1. Boundary & Physics Tests: Verify gravity decreases Y-coordinate and flapping increments it."""
        try:
            logger.info("Setting player mode to NORMAL to activate physics")
            self.player.set_mode(PlayerMode.NORMAL)
            
            initial_y = self.player.y
            initial_vel = self.player.vel_y
            
            logger.info(f"Simulating a game tick (Gravity check). Initial Y: {initial_y}, Initial Vel: {initial_vel}")
            self.player.tick() # In NORMAL mode, this triggers tick_normal()
            
            # Since player Y goes down on the screen, Y value actually increases in Pygame coordinates.
            logger.info("Asserting that velocity increases due to gravity")
            self.assertGreater(self.player.vel_y, initial_vel, "Gravity should increase velocity")
            logger.info("Assertion passed: Velocity increased.")
            
            logger.info("Simulating a player flap")
            self.player.flap()
            self.player.tick()
            
            logger.info("Asserting that flapping sets negative velocity (upward movement)")
            self.assertEqual(self.player.vel_y, self.player.flap_acc, "Flapping should set velocity to flap_acc")
            logger.info("Assertion passed: Flapping logic sets correct velocity.")
            
        except AssertionError as e:
            logger.error(f"Assertion failed in test_boundary_and_physics: {e}")
            raise

    def test_collision_detection_logic(self):
        """2. Collision Detection Logic Tests: Mock overlapping bounds and verify game-over trigger."""
        try:
            logger.info("Setting up Player and Floor for collision check")
            # Create a floor that overlaps with the player
            floor = Floor(self.mock_config)
            
            # Manually position player to intersect with the floor
            self.player.y = floor.y - self.player.h + 5 
            
            # We need dummy pipes to pass to collided
            pipes = Pipes(self.mock_config)
            pipes.upper = []
            pipes.lower = []
            
            logger.info("Asserting player.collided returns True when overlapping with floor")
            has_collided = self.player.collided(pipes, floor)
            self.assertTrue(has_collided, "Player should register a collision when overlapping with the floor")
            logger.info("Assertion passed: Floor collision detected successfully.")
            
            logger.info("Asserting that crash entity is correctly set to 'floor'")
            self.assertEqual(self.player.crash_entity, "floor", "Crash entity should be floor")
            logger.info("Assertion passed: Crash entity logged as 'floor'.")
            
        except AssertionError as e:
            logger.error(f"Assertion failed in test_collision_detection_logic: {e}")
            raise

    def test_scoring_logic(self):
        """3. Scoring Logic Tests: Verify score increments when pipe X-coordinate passes behind bird."""
        try:
            logger.info("Setting up Player and Pipe for scoring logic check")
            pipe = Pipe(self.mock_config)
            
            # Position pipe slightly behind the player's center X (cx)
            pipe.x = self.player.cx - pipe.w - 1 
            
            logger.info(f"Asserting player.crossed(pipe) is True when player X ({self.player.cx}) > pipe X ({pipe.x + pipe.w})")
            has_crossed = self.player.crossed(pipe)
            self.assertTrue(has_crossed, "Player should register crossing the pipe")
            logger.info("Assertion passed: Pipe crossing detected successfully.")
            
        except AssertionError as e:
            logger.error(f"Assertion failed in test_scoring_logic: {e}")
            raise

    def test_state_management(self):
        """4. State Management Tests: Ensure transitions from Idle -> Active -> Game Over work properly."""
        try:
            logger.info("Asserting initial Idle state (SHM)")
            self.assertEqual(self.player.mode, PlayerMode.SHM, "Player should start in SHM (Idle) mode")
            logger.info("Assertion passed: Idle state confirmed.")
            
            logger.info("Transitioning to Active (NORMAL) state")
            self.player.set_mode(PlayerMode.NORMAL)
            self.assertEqual(self.player.mode, PlayerMode.NORMAL, "Player should transition to NORMAL mode")
            logger.info("Assertion passed: Active state transition confirmed.")
            
            logger.info("Transitioning to Game Over (CRASH) state")
            self.player.set_mode(PlayerMode.CRASH)
            self.assertEqual(self.player.mode, PlayerMode.CRASH, "Player should transition to CRASH mode")
            logger.info("Assertion passed: Game Over state transition confirmed.")
            
        except AssertionError as e:
            logger.error(f"Assertion failed in test_state_management: {e}")
            raise
