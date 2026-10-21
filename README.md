# Excel to Prism Studio 1.2.0

Offline Windows interface for your supplied converter. `excel_to_prism.py` retains the original strict mode and adds explicit duration conversion; the GUI calls its conversion function. No GraphPad affiliation.

## Supported conversion

Inputs: .xlsx, .xlsm, .xls. First row: titles; remaining rows: numbers, blanks, or explicitly converted durations.
Column mode: one group per column. XY: X first, then individual Y datasets.
All worksheets or one worksheet can be converted to one .pzfx file. Empty and
header-only sheets are skipped. Invalid cells stop conversion with an address.
Existing outputs are never overwritten. Excel formulas require calculated values
saved by Excel. Formatting and macros are not copied or executed. Numeric
precision follows the original float conversion.

No graphs, analyses, grouped tables or replicate subcolumns are generated.
Prism 10 supports legacy PZFX, but these generated outputs still require checking
in Prism 10. Do not rename .pzfx to .prism. GraphPad is separately licensed.

## Upload and build using GitHub in your browser

1. Extract the project ZIP with Windows **Extract All**.
2. GitHub → **+ → New repository**. Name it `excel-to-prism-studio`; choose
   Private if preferred, then create it.
3. Choose **uploading an existing file** or **Add file → Upload files**.
   Upload the CONTENTS inside `excel-to-prism-studio`, not the enclosing folder
   or the ZIP. `app.py` and `requirements.txt` must be at repository root.
4. Confirm `.github/workflows/build-windows.yml` appears. If folder upload omits
   it, use **Add file → Create new file**, enter that complete path as filename,
   and copy the COMPLETE workflow from the extracted file. Commit changes.
5. Open **Actions → Build Windows Installer**. A push to main/master triggers it;
   alternatively choose **Run workflow → Run workflow**. Enable Actions if asked.
6. Wait for ALL steps to pass. If red, open the failed step and share its log.
7. In the successful run, scroll to **Artifacts**. Download
   **Excel-to-Prism-Studio-Windows-Installer** and extract the downloaded ZIP.
8. Run `Excel_to_Prism_Studio_Setup_1.2.0.exe`. It installs for your Windows user,
   creates a Start Menu shortcut and offers an optional desktop shortcut.
9. Launch from Start, convert a small known workbook, then verify the result
   using Prism 10 File → Open before using it for research.

Workflow artifacts are run-specific ZIP downloads and can expire. GitHub Releases
are separately published versions with attached installers. This workflow creates
an artifact, not a Release. After testing, you can create a Release manually and
attach the installer. Never upload private research workbooks or credentials.

## Use

Browse workbook → worksheet → Column/XY → Convert durations (none/seconds/minutes) → choose a NEW output filename → Convert.
Open result uses the Windows file association. If it fails, open Prism and use
File → Open. Supporting Tools opens the guide. Appearance offers Light, OLED Dark
and Colored Mode; theme choice is saved on this computer. Conversion runs in a worker
thread. The activity bar indicates work, not a fabricated percentage. Close is
blocked during work. Conversion is offline and no telemetry is added.

The compact layout, crimson accent, formal title and three themes adapt the
relevant preferences. Appendicitis-specific objectives, papers, cloud imports
and public web-link sharing do not apply to this offline converter.

## Packaging and installation

Python 3.11 on a Windows x64 runner builds a PyInstaller application folder.
Its executable requires the accompanying `_internal` folder. Inno Setup packages
that entire folder in a conventional installer. A portable app would need that
whole folder; the installer is the intended delivery. End users need neither
Python nor Jupyter. The converter runs without internet access.

The workflow tests conversion and GUI startup, builds the app, starts the packaged
GUI, compiles the installer, installs in a temporary directory, starts the installed
app, then uninstalls and checks removal. Upload happens only after these checks.
The runner must include Inno Setup 6 at its standard location; absence fails clearly.
Pinned Python packages improve repeatability; runner images and action major
versions can still change. No code-signing certificate is supplied, so Windows
may warn about the unsigned installer. Verify its origin before running it;
do not disable antivirus protection. Signing needs your own certificate.

Installation uses your local application-data Programs folder without requesting
administrator rights. Uninstall via Windows Settings → Apps. Outputs at your
chosen locations are not included in installer deletion rules.

## Optional local development: PowerShell, not Jupyter

Install Python 3.11 x64 with Tcl/Tk, open PowerShell in this project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-build.txt
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python app.py
```

Original CLI remains available:

```powershell
.\.venv\Scripts\python excel_to_prism.py experiment.xlsx --type xy -o results.pzfx
```

## Checks still required

See VALIDATION.md for checks actually performed. This delivery contains source
and build configuration, not a Windows-built installer. GitHub Actions has not
been run in your account. Windows installation and Prism compatibility have not
been verified by this delivery.

On Windows, check Start Menu launch, optional desktop shortcut, themes, keyboard
focus, 150% display scaling, dialogs, all/single-sheet selection, invalid files,
read-only folders, closing while busy, and launching outside the source folder.
Try actual .xlsx/.xlsm/.xls workbooks. Recalculate formula workbooks first and
verify cached values; absent caches can become blanks.

In Prism 10, compare Column and XY outputs against Excel: titles, sheet counts,
X/Y placement, values, blanks, negative numbers, zeros and decimal precision.
Include Unicode paths and large tables if relevant. Then create graphs inside
Prism. Verify uninstall preserves your saved outputs. XML correctness alone does
not establish acceptance by Prism.

## Troubleshooting

- Output already exists: choose a new filename.
- Expected a number: correct the reported sheet/cell. Labels and units do not
  belong in the numeric rows.
- Access denied: close Excel or select a writable output folder.
- No data: include titles and at least one numeric data row.
- Open result fails: use Prism File → Open; report any Prism error.
- Build does not start: check workflow path, enable Actions, use Run workflow.


## Version 1.1.0: phase workbook fix

For the supplied Recovery and Warming Up workbooks select **XY**, then
**Convert durations: seconds**. Confirm the conversion prompt. The first Time
column becomes numeric X with the title Time (seconds). Time origin is retained,
so recovery starts at its recorded time, not zero. Each participant worksheet
remains a separate table. In Prism choose Heart Rate as the Y dataset to graph.
All other columns (including the existing Time in Seconds, blank separator,
slopes and recovery summaries) are retained without recalculation. These mixed
metrics should not all be graphed as heart rate or treated as replicate groups.

Minutes converts duration columns only; the existing numeric Time in Seconds
column remains in seconds. Its title is preserved. The app never guesses units
for numeric Excel serial values. Accepted text format is h:mm:ss[.fraction]
with minutes and seconds below 60. Native Excel time/timedelta objects also work.
Mixed duration/numeric columns fail with the cell address rather than guessing.
Default none retains the original strict conversion behavior.

Text participant-ID columns such as P001 are still unsupported in numeric tables.
The Tidy workbook has not been provided, so its layout has not been repaired.
No uploaded research workbooks or generated research outputs are in this source
ZIP. Do not upload those files to GitHub.

For an existing GitHub repository, upload this project's contents to the SAME
paths, replacing matching files. Be sure to replace
.github/workflows/build-windows.yml and installer/setup.iss too. Commit, wait for
the new workflow to pass, download its artifact and run the 1.1.0 installer with
the app closed. It retains the same installation identity/path as 1.0.0.


## Version 1.2.0: appearance, developer and sharing

All 1.1.0 duration fixes are included. Themes now use deeper burgundy, gold,
black and plum, including fields, dropdown menus, progress and secondary dialogs.
Light retains light surfaces for legibility. Theme choice is saved per Windows
user. No conversion calculations were changed for this interface update.

About Developer names Progress Ajayi. No qualifications or external biography
have been invented. Add your preferred biography and professional profile URL
under Link & Profile Settings. An optional Professional Profile button appears
when that URL is set. Defaults for new distributions live in app_settings.py.
User edits affect this computer, not other people's installations.

Copy App Link copies the configured address. Share App opens a panel with Copy
Link and Open Download Page; it does not send messages automatically. The default
is https://github.com/ajayiprogress04-ctrl/excel-to-prism-studio/releases, inferred
from the account/repository used in this project. Verify or correct it in settings.
No public access or published Release has been verified. A private repository
requires recipient access. A public release with the installer attached is needed
for a generally accessible download link. Sharing uses the internet/browser;
Excel conversion itself remains fully offline. No workbook or output is shared.

Settings are stored in %LOCALAPPDATA%/ExcelToPrismStudio/settings.json, outside
installation files. Invalid web URL schemes and credential-bearing URLs are
rejected. Uninstall leaves these preferences and user data untouched.

Upload all contents to matching repository paths, including app_settings.py,
installer/setup.iss and .github/workflows/build-windows.yml. Build the new
workflow, then install Excel_to_Prism_Studio_Setup_1.2.0.exe with the old app closed.
On Windows, check the three themes, clipboard paste, Share dialog, About dialog,
profile editing and settings persistence after restart. Browser/clipboard and
visual behavior have not been tested here because no desktop display is available.
