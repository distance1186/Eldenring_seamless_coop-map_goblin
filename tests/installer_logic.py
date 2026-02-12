"""
Installer logic module - mirrors the Inno Setup installer's path detection functionality.
This module is used for unit testing the installer logic.
"""

import os
from typing import Optional, Tuple

# Windows registry paths for Steam
STEAM_REGISTRY_PATHS = [
    (r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),  # 64-bit
    (r"SOFTWARE\Valve\Steam", "InstallPath"),  # 32-bit/current user
]

DEFAULT_ELDEN_RING_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game"

DRIVE_LETTERS = ["C", "D", "E", "F", "G"]

POST_INSTALL_MESSAGE = """Installation Complete!

To play with mods:
  1. Use the "Elden Ring (Modded)" shortcut, or
  2. Run launchmod_eldenring.bat from your Game folder

IMPORTANT: Do NOT launch from Steam!

Map markers are OFF by default. Enable them at any Site of Grace via the Map Configuration menu."""


class InstallerLogic:
    """Handles Elden Ring installation path detection and validation."""

    def __init__(self, registry_reader=None, file_checker=None):
        """
        Initialize the installer logic.

        Args:
            registry_reader: Callable that takes (key, subkey, value_name) and returns
                           the registry value or None if not found.
            file_checker: Callable that takes a file path and returns True if it exists.
        """
        self._registry_reader = registry_reader or self._default_registry_reader
        self._file_checker = file_checker or os.path.isfile
        self._detected_path: Optional[str] = None
        self._elden_ring_detected: bool = False

    @staticmethod
    def _default_registry_reader(key: str, subkey: str, value_name: str) -> Optional[str]:
        """Default registry reader - attempts to read from Windows registry."""
        try:
            import winreg
            key_map = {
                "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
                "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            }
            with winreg.OpenKey(key_map.get(key, winreg.HKEY_LOCAL_MACHINE), subkey) as reg_key:
                value, _ = winreg.QueryValueEx(reg_key, value_name)
                return value
        except (ImportError, OSError, FileNotFoundError):
            return None

    def get_steam_path(self) -> Optional[str]:
        """
        Get the Steam installation path from the registry.

        Returns:
            Steam installation path or None if not found.
        """
        # Try 64-bit registry first (HKEY_LOCAL_MACHINE)
        result = self._registry_reader(
            "HKEY_LOCAL_MACHINE",
            r"SOFTWARE\WOW6432Node\Valve\Steam",
            "InstallPath"
        )
        if result:
            return result

        # Try current user
        result = self._registry_reader(
            "HKEY_CURRENT_USER",
            r"SOFTWARE\Valve\Steam",
            "InstallPath"
        )
        if result:
            return result

        # Try 32-bit registry
        result = self._registry_reader(
            "HKEY_LOCAL_MACHINE",
            r"SOFTWARE\Valve\Steam",
            "InstallPath"
        )
        return result

    def find_elden_ring_in_library_folders(self, steam_path: str) -> Optional[str]:
        """
        Search for Elden Ring installation in Steam library folders.

        Args:
            steam_path: The Steam installation path.

        Returns:
            Path to Elden Ring Game folder or None if not found.
        """
        # Check default Steam location first
        game_path = os.path.join(steam_path, "steamapps", "common", "ELDEN RING", "Game")
        if self._file_checker(os.path.join(game_path, "eldenring.exe")):
            return game_path

        # Check common alternate locations
        for drive in DRIVE_LETTERS:
            alternate_paths = [
                f"{drive}:\\SteamLibrary\\steamapps\\common\\ELDEN RING\\Game",
                f"{drive}:\\Steam\\steamapps\\common\\ELDEN RING\\Game",
                f"{drive}:\\Games\\Steam\\steamapps\\common\\ELDEN RING\\Game",
            ]
            for game_path in alternate_paths:
                if self._file_checker(os.path.join(game_path, "eldenring.exe")):
                    return game_path

        return None

    def get_elden_ring_path(self) -> Tuple[str, bool]:
        """
        Get the Elden Ring installation path.

        Returns:
            Tuple of (path, detected) where path is the installation path
            and detected is True if auto-detected, False if using default.
        """
        # Return cached result if available
        if self._detected_path is not None:
            return self._detected_path, self._elden_ring_detected

        steam_path = self.get_steam_path()

        if steam_path:
            detected = self.find_elden_ring_in_library_folders(steam_path)
            if detected:
                self._detected_path = detected
                self._elden_ring_detected = True
                return self._detected_path, self._elden_ring_detected

        # Default fallback
        self._elden_ring_detected = False
        self._detected_path = DEFAULT_ELDEN_RING_PATH
        return self._detected_path, self._elden_ring_detected

    def validate_installation_directory(self, path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that the selected directory contains eldenring.exe.

        Args:
            path: The selected installation directory.

        Returns:
            Tuple of (is_valid, warning_message) where is_valid is True if valid,
            and warning_message is the warning text if not valid.
        """
        exe_path = os.path.join(path, "eldenring.exe")
        if self._file_checker(exe_path):
            return True, None

        warning = (
            f"Warning: eldenring.exe was not found in the selected folder.\n\n"
            f"Selected: {path}\n\n"
            f"Are you sure this is your Elden Ring Game folder?"
        )
        return False, warning

    @staticmethod
    def get_post_install_message() -> str:
        """Get the post-installation instructions message."""
        return POST_INSTALL_MESSAGE
