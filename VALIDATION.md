# Validation at delivery

Performed in the available Linux environment:
- Eight unittest cases passed: Column values/blanks, XY values, all/single
  worksheet selection and empty-sheet exclusion, invalid-cell address,
  overwrite protection, missing/unsupported input, XY minimum columns,
  missing worksheet.
- Python compilation passed for app.py and excel_to_prism.py.
- Original converter matches the supplied source byte for byte.

Not performed:
- Live GUI interaction or visual review: no graphical display is available.
- Windows build, packaged GUI startup, installation or uninstall.
- GitHub upload, Actions execution or Release publication.
- Opening generated PZFX files in licensed GraphPad Prism 10.
- Actual .xls/.xlsm input cases, cached-formula behavior, permission errors,
  Windows scaling/accessibility, very large workbooks or antivirus checks.

The included Windows workflow provides automated startup/install/uninstall
checks when run. It does not replace manual conversion and data verification
inside Prism 10. See README.md for the remaining user checks.
