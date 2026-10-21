# Version 1.1.0 validation

Performed in the available Linux environment:
- 14 automated tests passed (original conversion and new duration handling).
- Python compilation passed for GUI and converter.
- Both uploaded workbooks converted successfully as XY, duration unit seconds.
- Recovery: 15 worksheets, 3,372 data rows, 47,208 cells checked.
- Warming Up: 15 worksheets, 2,818 data rows, 16,908 cells checked.
- Every exported cell compared against source cached values, including blanks,
  using a numerical tolerance of 1e-14 relative / 1e-10 absolute. Time text was
  checked against its duration in seconds. Sheet and column counts matched.
- All numeric columns, summary values, blanks and row order retained.

Not performed: GUI visual or interaction tests (no display available), Windows
build/install/uninstall for this update, GitHub workflow execution, or opening
outputs in GraphPad Prism 10. PZFX XML/data checks do not prove Prism acceptance.
Original user workbooks were read only and excluded from the project ZIP.
The Tidy participant-ID workbook was not supplied and remains untested/unsupported.


# Version 1.2.0 interface update

- Conversion module unchanged from 1.1.0; all 14 regression tests passed again.
- Python compilation passed for GUI and settings module.
- Settings write/read round-trip passed in a temporary user-data directory.
- URL checks rejected script/file schemes, embedded credentials and whitespace.
- No display server is available: themes, dialogs, browser launching, clipboard,
  scaling and live interface behavior remain unverified. Windows build and
  installation of this update have not been run here. No GitHub Release created.
