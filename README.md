# Elden Ring Mods Package

Pre-configured package for Elden Ring with Seamless Co-op and Map for Goblins mods.

## What's Included

- **Seamless Co-op** - Multiplayer mod for seamless co-op gameplay without restrictions
- **Map for Goblins v1.16** - Detailed map markers showing bosses, items, graces, and more
- **Mod Engine 2** - Required mod loader (pre-configured)

## Quick Start

1. **Download** this entire repository
2. **Locate** your Elden Ring Game folder:
   - Steam: `C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game`
   - Or wherever you have Elden Ring installed
3. **Copy** all contents from this package into your Game folder
4. **Launch** the game using `launchmod_eldenring.bat` (NOT Steam!)

## Full Instructions

See **[INSTALLATION_GUIDE.txt](INSTALLATION_GUIDE.txt)** for detailed step-by-step instructions, troubleshooting, and multiplayer setup.

## Important Notes

⚠️ **DO NOT launch from Steam** - Always use `launchmod_eldenring.bat`

⚠️ **Map markers disabled by default** - Enable them at Sites of Grace via the Map Configuration menu

⚠️ **For co-op** - Both players need identical mod setup and same password in `SeamlessCoop\cooppassword.ini`

## File Structure

```
EldenRing_Mods_Package/
├── INSTALLATION_GUIDE.txt       # Detailed installation instructions
├── README.md                     # This file
├── config_eldenring.toml         # Mod Engine 2 configuration
├── launchmod_eldenring.bat       # Game launcher (use this!)
├── modengine2_launcher.exe       # Mod Engine 2 executable
├── ersc_launcher.exe             # Seamless Co-op launcher
├── SeamlessCoop/                 # Seamless Co-op mod files
├── mod/                          # Map for Goblins files
└── modengine2/                   # Mod Engine 2 engine files
```

## Using the Mods

### Seamless Co-op
- Automatically loads when using `launchmod_eldenring.bat`
- Create or join sessions via in-game co-op menu
- Share session ID with friends to connect

### Map for Goblins
1. Rest at any Site of Grace
2. Select the new "Map Configuration" menu option
3. Enable desired marker categories (bosses, items, graces, etc.)
4. Open world map to see detailed markers

**Note**: Contains spoilers! Icons disappear as you complete content.

## Multiplayer Setup

To play co-op with friends:
1. Install this package on all machines
2. Set same password in `SeamlessCoop\cooppassword.ini` on all machines
3. Launch via `launchmod_eldenring.bat` on all machines
4. One player creates session and shares the session ID
5. Other players join using that session ID

## Troubleshooting

**Game doesn't launch?**
- Use `launchmod_eldenring.bat`, not Steam
- Run as Administrator if needed

**No Seamless Co-op menu?**
- Verify you launched via `launchmod_eldenring.bat`
- Check `modengine2\logs\` for errors

**Map looks vanilla?**
- Rest at Site of Grace
- Enable markers in Map Configuration menu

**Can't connect to friend?**
- Both must have identical mod setup
- Both must have same password
- Verify session ID is correct

## Credits

- **Seamless Co-op** by LukeYui ([Nexus Mods](https://www.nexusmods.com/eldenring/mods/510))
- **Map for Goblins** by Goblin ([Nexus Mods](https://www.nexusmods.com/eldenring/mods/3091))
- **Mod Engine 2** by SoulsMods ([GitHub](https://github.com/soulsmods/ModEngine2))

## Legal

This package is for personal use only. All mods are property of their respective creators. Elden Ring is property of FromSoftware and Bandai Namco.

**Use at your own risk.** Modding may affect your game experience and is not officially supported by the game developers.

## Version

- **Package Date**: December 18, 2025
- **Map for Goblins**: v1.16
- **Mod Engine 2**: v2.1.0

---

For detailed technical documentation, see the main documentation in the HomeLabAI repository.
