#define AppName "Excel to Prism Studio"
#define AppVersion "1.2.0"
[Setup]
AppId={{6F6C1DF0-8DA3-4500-AE3E-C77B94E02723}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Progress Ajayi
DefaultDirName={localappdata}\Programs\ExcelToPrismStudio
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..\dist\installer
OutputBaseFilename=Excel_to_Prism_Studio_Setup_1.2.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\ExcelToPrismStudio.exe
VersionInfoVersion=1.2.0.0
VersionInfoProductName={#AppName}
VersionInfoDescription={#AppName} Installer
[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; Flags: unchecked
[Files]
Source: "..\dist\ExcelToPrismStudio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\ExcelToPrismStudio.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\ExcelToPrismStudio.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\ExcelToPrismStudio.exe"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent
