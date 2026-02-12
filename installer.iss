; Elden Ring Mods Package Installer
; Auto-detects Elden Ring installation via Steam registry

#define MyAppName "Elden Ring Mods Package"
#define MyAppVersion "1.0"
#define MyAppPublisher "distance1186"
#define MyAppURL "https://github.com/distance1186/Eldenring_seamless_coop-map_goblin"

[Setup]
AppId={{8F3E2B1A-5C4D-4E6F-9A8B-7C2D1E0F3A4B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={code:GetEldenRingPath}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=EldenRing_Mods_Installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=compiler:SetupClassicIcon.ico
UninstallDisplayIcon={app}\modengine2_launcher.exe
DisableDirPage=no
DirExistsWarning=no
UsePreviousAppDir=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
SelectDirLabel3=Setup will install the mod files into the following folder.%n%nThis should be your Elden Ring Game folder (the folder containing eldenring.exe).
SelectDirBrowseLabel=To continue, click Next. If you need to select a different folder, click Browse.

[Files]
; Seamless Co-op files
Source: "SeamlessCoop\*"; DestDir: "{app}\SeamlessCoop"; Flags: ignoreversion recursesubdirs createallsubdirs

; Map for Goblins files
Source: "mod\*"; DestDir: "{app}\mod"; Flags: ignoreversion recursesubdirs createallsubdirs

; Mod Engine 2 files
Source: "modengine2\*"; DestDir: "{app}\modengine2"; Flags: ignoreversion recursesubdirs createallsubdirs

; Root files
Source: "config_eldenring.toml"; DestDir: "{app}"; Flags: ignoreversion
Source: "launchmod_eldenring.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "modengine2_launcher.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "ersc_launcher.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Elden Ring (Modded)"; Filename: "{app}\launchmod_eldenring.bat"; WorkingDir: "{app}"; Comment: "Launch Elden Ring with Seamless Co-op and Map for Goblins"
Name: "{autodesktop}\Elden Ring (Modded)"; Filename: "{app}\launchmod_eldenring.bat"; WorkingDir: "{app}"; Comment: "Launch Elden Ring with Seamless Co-op and Map for Goblins"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\launchmod_eldenring.bat"; Description: "Launch Elden Ring with mods"; Flags: nowait postinstall skipifsilent unchecked

[Code]
var
  EldenRingDetected: Boolean;
  DetectedPath: String;

function GetSteamPath: String;
var
  SteamPath: String;
begin
  Result := '';
  // Try 64-bit registry first
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\WOW6432Node\Valve\Steam', 'InstallPath', SteamPath) then
    Result := SteamPath
  // Then try 32-bit/current user
  else if RegQueryStringValue(HKEY_CURRENT_USER, 'SOFTWARE\Valve\Steam', 'InstallPath', SteamPath) then
    Result := SteamPath
  else if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Valve\Steam', 'InstallPath', SteamPath) then
    Result := SteamPath;
end;

function FindEldenRingInLibraryFolders(SteamPath: String): String;
var
  LibraryFile: String;
  GamePath: String;
  DriveLetters: array[0..25] of String;
  i: Integer;
begin
  Result := '';
  
  // Check default Steam location first
  GamePath := SteamPath + '\steamapps\common\ELDEN RING\Game';
  if FileExists(GamePath + '\eldenring.exe') then
  begin
    Result := GamePath;
    Exit;
  end;
  
  // Check common alternate locations
  DriveLetters[0] := 'C';
  DriveLetters[1] := 'D';
  DriveLetters[2] := 'E';
  DriveLetters[3] := 'F';
  DriveLetters[4] := 'G';
  
  for i := 0 to 4 do
  begin
    GamePath := DriveLetters[i] + ':\SteamLibrary\steamapps\common\ELDEN RING\Game';
    if FileExists(GamePath + '\eldenring.exe') then
    begin
      Result := GamePath;
      Exit;
    end;
    
    GamePath := DriveLetters[i] + ':\Steam\steamapps\common\ELDEN RING\Game';
    if FileExists(GamePath + '\eldenring.exe') then
    begin
      Result := GamePath;
      Exit;
    end;
    
    GamePath := DriveLetters[i] + ':\Games\Steam\steamapps\common\ELDEN RING\Game';
    if FileExists(GamePath + '\eldenring.exe') then
    begin
      Result := GamePath;
      Exit;
    end;
  end;
end;

function GetEldenRingPath(Param: String): String;
var
  SteamPath: String;
begin
  // Return cached result if available
  if DetectedPath <> '' then
  begin
    Result := DetectedPath;
    Exit;
  end;
  
  SteamPath := GetSteamPath;
  
  if SteamPath <> '' then
  begin
    DetectedPath := FindEldenRingInLibraryFolders(SteamPath);
    if DetectedPath <> '' then
    begin
      EldenRingDetected := True;
      Result := DetectedPath;
      Exit;
    end;
  end;
  
  // Default fallback
  EldenRingDetected := False;
  Result := 'C:\Program Files (x86)\Steam\steamapps\common\ELDEN RING\Game';
  DetectedPath := Result;
end;

procedure InitializeWizard;
var
  Path: String;
begin
  Path := GetEldenRingPath('');
  
  if EldenRingDetected then
    MsgBox('Elden Ring detected!' + #13#10 + #13#10 + 
           'Found at: ' + Path + #13#10 + #13#10 +
           'Click Next to install mods to this location, or Browse to change.', 
           mbInformation, MB_OK)
  else
    MsgBox('Elden Ring not auto-detected.' + #13#10 + #13#10 +
           'Please browse to your Elden Ring Game folder.' + #13#10 +
           '(The folder containing eldenring.exe)', 
           mbInformation, MB_OK);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  GameExePath: String;
begin
  Result := True;
  
  if CurPageID = wpSelectDir then
  begin
    GameExePath := ExpandConstant('{app}') + '\eldenring.exe';
    
    if not FileExists(GameExePath) then
    begin
      Result := (MsgBox('Warning: eldenring.exe was not found in the selected folder.' + #13#10 + #13#10 +
                        'Selected: ' + ExpandConstant('{app}') + #13#10 + #13#10 +
                        'Are you sure this is your Elden Ring Game folder?', 
                        mbConfirmation, MB_YESNO) = IDYES);
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('Installation Complete!' + #13#10 + #13#10 +
           'To play with mods:' + #13#10 +
           '  1. Use the "Elden Ring (Modded)" shortcut, or' + #13#10 +
           '  2. Run launchmod_eldenring.bat from your Game folder' + #13#10 + #13#10 +
           'IMPORTANT: Do NOT launch from Steam!' + #13#10 + #13#10 +
           'Map markers are OFF by default. Enable them at any Site of Grace via the Map Configuration menu.',
           mbInformation, MB_OK);
  end;
end;
