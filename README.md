# Flappy Bird Clone - QA Automation 

This project is a clone of the popular [FlapPyBird repository](https://github.com/sourabhv/FlapPyBird.git), enhanced with an automated test suite to demonstrate **Game QA Automation** principles.

The core game logic has been isolated and wrapped with automated test frameworks, detailed logging, and HTML reporting to prove build stability and catch regressions headlessly.

---

## 🛠️ Project Setup & Installation

The automation framework and game dependencies are fully optimized for **Python 3.10**. Follow these steps to set up the clean, isolated virtual environment and run the project:

### 1. Initialize Virtual Environment
```powershell
py -3.10 -m venv venv
```

### 2. Activate the Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install .
pip install pytest pytest-html
```

### 4. Play the Game (Manual Check)
```powershell
python main.py
```


Controls: Use `Space` or `Up Arrow` to jump, `Esc` to close.

---

## Run Automated Tests

### Description of the tests
`test_boundary_and_physics`: This test verifies that the bird's downward velocity correctly increases on each game tick due to gravity, and that simulating a "flap" action properly overrides this to an upward velocity.
`test_collision_detection_logic`: This test checks the game's collision system by manually positioning the bird so it overlaps with the floor and confirming that a collision is detected and correctly recorded as crashing into the floor.
`test_scoring_logic`: This test ensures that the game can properly detect when a player successfully navigates an obstacle by confirming the crossing logic triggers once the bird's horizontal center position passes the back edge of a pipe.
`test_state_management`: This test validates the game's internal state progression by ensuring the bird initializes in an idle "floating" state (SHM), properly transitions into an active playing state (NORMAL), and finally can be put into a crashed state (CRASH).

### Stable Build Validation
To avoid UI flashing and reduce execution overhead during continuous integration, the tests run headlessly using unittest.mock to patch Pygame’s window components globally.
Run the complete test suite against the stable game build using **Pytest**. This generates a detailed, self-contained HTML report for stakeholders.

**Command:**
```powershell
pytest tests/test_game_logic.py --html=reports/stable_test_report.html --self-contained-html
```

![Passed tests report](readme_images/passed_tests_image.png)

**Report Location:**
- `reports/stable_test_report.html`
- **Log File:** `tests/test_run.log`

### 📊 QA Sandbox: Mutation Testing (Simulating a Broken Build)
To demonstrate the test suite's robustness, we intentionally inject bugs into the core game logic. The automated tests should fail when these mutations are introduced.

#### Example Mutation: Broken Flap Mechanics
**File Location:** `src/entities/player.py`

**Mutated Code:**
```python
    def flap(self) -> None:
        if self.y > self.min_y:
            self.vel_y = 0  # INTENTIONAL BUG: flap no longer provides upward velocity (was self.flap_acc)
            self.vel_y = self.flap_acc

    if self.collide(floor):
    if False:  # INTENTIONAL BUG: player ignores floor boundaries entirely    
```

**Verification Command:**
```powershell
pytest tests/test_game_logic.py --html=reports/mutation_test_report.html --self-contained-html
```

**Expected Result:** The test `test_boundary_and_physics` should fail, and the HTML report will show the specific assertion failure, proving that the test suite successfully detected the regression.

![Failed tests report](readme_images/failed_tests_image.png)

**Reverse the code to the valid state:**
```powershell
git checkout src/
```
