# Installer Unit Tests

This directory contains unit tests for the Elden Ring Mods Package installer logic.

## Test Coverage

The test suite covers all requested scenarios:

1. **Default Steam location detection** - Verifies the installer correctly detects Elden Ring when installed in the default Steam location (`C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game`)

2. **Alternate Steam library detection** - Tests detection across multiple alternate Steam library locations:
   - `D:\SteamLibrary\steamapps\common\ELDEN RING\Game`
   - `E:\Steam\steamapps\common\ELDEN RING\Game`
   - `F:\Games\Steam\steamapps\common\ELDEN RING\Game`

3. **Default path fallback** - Ensures the installer suggests the default path when:
   - Elden Ring is not found in any known location
   - Steam is not installed (no registry entries found)

4. **Installation directory validation** - Verifies the installer:
   - Accepts directories containing `eldenring.exe`
   - Warns users when `eldenring.exe` is not found
   - Includes the selected path in warning messages

5. **Post-installation instructions** - Confirms the installer displays correct instructions including:
   - How to launch the modded game
   - Warning not to launch from Steam
   - Map marker configuration instructions

## Running the Tests

### Prerequisites

Install pytest:

```bash
pip install -r requirements-test.txt
```

Or install manually:

```bash
pip install pytest pytest-cov
```

### Run All Tests

From the repository root:

```bash
python -m pytest tests/ -v
```

From the tests directory:

```bash
python -m pytest test_installer.py -v
```

### Run Specific Test Classes

```bash
# Path detection tests
python -m pytest tests/test_installer.py::TestEldenRingPathDetection -v

# Validation tests
python -m pytest tests/test_installer.py::TestInstallationDirectoryValidation -v

# Post-install message tests
python -m pytest tests/test_installer.py::TestPostInstallationInstructions -v

# Steam path detection tests
python -m pytest tests/test_installer.py::TestSteamPathDetection -v

# Caching tests
python -m pytest tests/test_installer.py::TestPathCaching -v
```

### Run with Coverage

```bash
python -m pytest tests/ --cov=tests --cov-report=html
```

Then open `htmlcov/index.html` in a browser to view the coverage report.

## Test Architecture

The tests use dependency injection to mock:
- **Registry access** - Windows registry reads are mocked to simulate different Steam installation scenarios
- **File system access** - File existence checks are mocked to simulate different Elden Ring installation locations

This allows the tests to run on any platform (Linux, macOS, Windows) without requiring actual Windows registry access or Elden Ring installation.

## Files

- `installer_logic.py` - Python module mirroring the Inno Setup installer's path detection logic
- `test_installer.py` - Unit tests covering all installer scenarios
- `__init__.py` - Package marker
- `README.md` - This file

## Notes

The `installer_logic.py` module mirrors the logic from `installer.iss` (the Inno Setup script) to enable unit testing. The actual installer uses Inno Setup's Pascal scripting, but the logic is functionally equivalent.
