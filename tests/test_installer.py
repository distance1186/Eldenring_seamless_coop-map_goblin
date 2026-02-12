"""
Unit tests for the Elden Ring Mods Package installer logic.

Tests cover:
1. Detection of Elden Ring in default Steam location
2. Detection of Elden Ring in alternate Steam library folders
3. Default path suggestion when Elden Ring is not found
4. Warning when eldenring.exe is not in selected directory
5. Post-installation instructions display
"""

import pytest
from installer_logic import InstallerLogic, DEFAULT_ELDEN_RING_PATH, POST_INSTALL_MESSAGE


class TestEldenRingPathDetection:
    """Tests for Elden Ring installation path detection."""

    def test_detects_elden_ring_in_default_steam_location(self):
        """
        Test case 1: Installer correctly detects Elden Ring path when
        installed in default Steam location.
        """
        steam_path = r"C:\Program Files (x86)\Steam"
        expected_game_path = r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"
        expected_exe = r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe"

        def mock_registry_reader(key, subkey, value_name):
            if "WOW6432Node" in subkey and value_name == "InstallPath":
                return steam_path
            return None

        def mock_file_checker(path):
            return path == expected_exe

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        path, detected = installer.get_elden_ring_path()

        assert detected is True
        assert path == expected_game_path

    def test_detects_elden_ring_in_alternate_steam_library_d_drive(self):
        """
        Test case 2a: Installer correctly detects Elden Ring path when
        installed in an alternate Steam library folder on D: drive.
        """
        steam_path = r"C:\Program Files (x86)\Steam"
        expected_game_path = r"D:\SteamLibrary\steamapps\common\ELDEN RING\Game"
        expected_exe = r"D:\SteamLibrary\steamapps\common\ELDEN RING\Game\eldenring.exe"

        def mock_registry_reader(key, subkey, value_name):
            if "WOW6432Node" in subkey and value_name == "InstallPath":
                return steam_path
            return None

        def mock_file_checker(path):
            return path == expected_exe

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        path, detected = installer.get_elden_ring_path()

        assert detected is True
        assert path == expected_game_path

    def test_detects_elden_ring_in_alternate_steam_folder_e_drive(self):
        r"""
        Test case 2b: Installer correctly detects Elden Ring path when
        installed in E:\Steam folder.
        """
        steam_path = r"C:\Program Files (x86)\Steam"
        expected_game_path = r"E:\Steam\steamapps\common\ELDEN RING\Game"
        expected_exe = r"E:\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe"

        def mock_registry_reader(key, subkey, value_name):
            if "WOW6432Node" in subkey and value_name == "InstallPath":
                return steam_path
            return None

        def mock_file_checker(path):
            return path == expected_exe

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        path, detected = installer.get_elden_ring_path()

        assert detected is True
        assert path == expected_game_path

    def test_detects_elden_ring_in_games_steam_folder(self):
        r"""
        Test case 2c: Installer correctly detects Elden Ring path when
        installed in F:\Games\Steam folder.
        """
        steam_path = r"C:\Program Files (x86)\Steam"
        expected_game_path = r"F:\Games\Steam\steamapps\common\ELDEN RING\Game"
        expected_exe = r"F:\Games\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe"

        def mock_registry_reader(key, subkey, value_name):
            if "WOW6432Node" in subkey and value_name == "InstallPath":
                return steam_path
            return None

        def mock_file_checker(path):
            return path == expected_exe

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        path, detected = installer.get_elden_ring_path()

        assert detected is True
        assert path == expected_game_path

    def test_suggests_default_path_when_elden_ring_not_found(self):
        """
        Test case 3: Installer correctly suggests the default path if
        Elden Ring is not found in any known location.
        """
        steam_path = r"C:\Program Files (x86)\Steam"

        def mock_registry_reader(key, subkey, value_name):
            if "WOW6432Node" in subkey and value_name == "InstallPath":
                return steam_path
            return None

        def mock_file_checker(path):
            # eldenring.exe not found anywhere
            return False

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        path, detected = installer.get_elden_ring_path()

        assert detected is False
        assert path == DEFAULT_ELDEN_RING_PATH

    def test_suggests_default_path_when_steam_not_installed(self):
        """
        Test case 3b: Installer suggests default path when Steam
        registry keys are not found (Steam not installed).
        """
        def mock_registry_reader(key, subkey, value_name):
            # Steam not installed - no registry entries
            return None

        def mock_file_checker(path):
            return False

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        path, detected = installer.get_elden_ring_path()

        assert detected is False
        assert path == DEFAULT_ELDEN_RING_PATH


class TestInstallationDirectoryValidation:
    """Tests for installation directory validation."""

    def test_valid_directory_with_eldenring_exe(self):
        """
        Test that validation passes when eldenring.exe exists in the
        selected directory.
        """
        selected_path = r"D:\Games\ELDEN RING\Game"
        exe_path = r"D:\Games\ELDEN RING\Game\eldenring.exe"

        def mock_file_checker(path):
            return path == exe_path

        installer = InstallerLogic(file_checker=mock_file_checker)

        is_valid, warning = installer.validate_installation_directory(selected_path)

        assert is_valid is True
        assert warning is None

    def test_warns_when_eldenring_exe_not_found(self):
        """
        Test case 4: Installer warns the user if eldenring.exe is not
        found in the selected installation directory.
        """
        selected_path = r"C:\SomeRandomFolder"

        def mock_file_checker(path):
            # eldenring.exe not found
            return False

        installer = InstallerLogic(file_checker=mock_file_checker)

        is_valid, warning = installer.validate_installation_directory(selected_path)

        assert is_valid is False
        assert warning is not None
        assert "eldenring.exe was not found" in warning
        assert selected_path in warning
        assert "Are you sure this is your Elden Ring Game folder?" in warning

    def test_warning_message_includes_selected_path(self):
        """
        Test that the warning message includes the user's selected path
        for clarity.
        """
        selected_path = r"E:\MyGames\WrongFolder"

        def mock_file_checker(path):
            return False

        installer = InstallerLogic(file_checker=mock_file_checker)

        _, warning = installer.validate_installation_directory(selected_path)

        assert f"Selected: {selected_path}" in warning


class TestPostInstallationInstructions:
    """Tests for post-installation instructions."""

    def test_post_install_message_content(self):
        """
        Test case 5: Installer displays correct post-installation instructions.
        """
        message = InstallerLogic.get_post_install_message()

        # Verify key instructions are present
        assert "Installation Complete!" in message
        assert "Elden Ring (Modded)" in message
        assert "launchmod_eldenring.bat" in message
        assert "Do NOT launch from Steam" in message
        assert "Map markers are OFF by default" in message
        assert "Site of Grace" in message
        assert "Map Configuration" in message

    def test_post_install_message_matches_expected(self):
        """
        Test that post-install message exactly matches the expected content.
        """
        message = InstallerLogic.get_post_install_message()
        assert message == POST_INSTALL_MESSAGE


class TestSteamPathDetection:
    """Tests for Steam installation path detection."""

    def test_finds_steam_in_64bit_registry(self):
        """Test finding Steam path from 64-bit registry location."""
        expected_path = r"C:\Program Files (x86)\Steam"

        def mock_registry_reader(key, subkey, value_name):
            if key == "HKEY_LOCAL_MACHINE" and "WOW6432Node" in subkey:
                return expected_path
            return None

        installer = InstallerLogic(registry_reader=mock_registry_reader)
        steam_path = installer.get_steam_path()

        assert steam_path == expected_path

    def test_finds_steam_in_current_user_registry(self):
        """Test finding Steam path from current user registry when 64-bit not found."""
        expected_path = r"D:\Steam"

        def mock_registry_reader(key, subkey, value_name):
            if key == "HKEY_CURRENT_USER":
                return expected_path
            return None

        installer = InstallerLogic(registry_reader=mock_registry_reader)
        steam_path = installer.get_steam_path()

        assert steam_path == expected_path

    def test_finds_steam_in_32bit_registry(self):
        """Test finding Steam path from 32-bit registry as last resort."""
        expected_path = r"C:\Steam"

        def mock_registry_reader(key, subkey, value_name):
            if key == "HKEY_LOCAL_MACHINE" and "WOW6432Node" not in subkey:
                return expected_path
            return None

        installer = InstallerLogic(registry_reader=mock_registry_reader)
        steam_path = installer.get_steam_path()

        assert steam_path == expected_path

    def test_returns_none_when_steam_not_found(self):
        """Test that None is returned when Steam is not found in registry."""
        def mock_registry_reader(key, subkey, value_name):
            return None

        installer = InstallerLogic(registry_reader=mock_registry_reader)
        steam_path = installer.get_steam_path()

        assert steam_path is None


class TestPathCaching:
    """Tests for path detection caching behavior."""

    def test_caches_detected_path(self):
        """Test that detected path is cached and not re-computed."""
        steam_path = r"C:\Program Files (x86)\Steam"
        expected_path = r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"
        expected_exe = r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe"

        call_count = {"registry": 0, "file": 0}

        def mock_registry_reader(key, subkey, value_name):
            call_count["registry"] += 1
            if "WOW6432Node" in subkey:
                return steam_path
            return None

        def mock_file_checker(path):
            call_count["file"] += 1
            return path == expected_exe

        installer = InstallerLogic(
            registry_reader=mock_registry_reader,
            file_checker=mock_file_checker
        )

        # First call
        path1, detected1 = installer.get_elden_ring_path()
        first_call_registry = call_count["registry"]
        first_call_file = call_count["file"]

        # Second call - should use cache
        path2, detected2 = installer.get_elden_ring_path()

        assert path1 == path2 == expected_path
        assert detected1 == detected2 is True
        # Verify no additional calls were made
        assert call_count["registry"] == first_call_registry
        assert call_count["file"] == first_call_file


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
