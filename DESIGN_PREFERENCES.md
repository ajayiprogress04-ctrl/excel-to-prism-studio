# Statistical App Design Preferences

**Owner:** Progress Ajayi  
**Last consolidated:** 17 October 2026  
**Reference project:** Appendicitis Research Statistical Test Learning Hub

## Purpose and precedence

Use this document as the design and behaviour brief when improving my statistical apps. My preferred app is a compact, professional research workspace that makes actual results easy to understand, explore and export.

These are preferences and requirements, not a claim that every feature is already implemented or tested. My latest explicit instruction takes priority when it replaces an earlier requirement. Preserve the existing app, validated calculations and working features. Adapt study-specific names and objectives to the actual research; do not copy appendicitis definitions into another study.

## 1. Overall design

- Improve the existing application rather than rebuilding working components.
- Make the interface elegant, academically credible and understandable to non-statisticians.
- Use compact spacing, consistent alignment and sufficient whitespace.
- Avoid oversized cards, excessive borders, nested panels, unnecessary headings and repeated explanations.
- Use progressive disclosure instead of displaying every control and explanation simultaneously.
- Make focused changes without modifying unrelated features.
- Keep the app fast and responsive. Avoid unnecessary animation, dependencies and duplicate calculations.

## 2. Main navigation

Use only these three primary sections, in this order:

1. **Objectives**
2. **Reports**
3. **Papers**

Keep the Statistical Glossary, Interpretations, User Guide and other useful tools accessible through secondary navigation.

- Place **Supporting Tools beside Appearance** in the top-right area.
- Keep useful features without crowding the primary navigation.
- Remove obsolete categories, duplicate lists and unnecessary shortcuts.
- Do not restore the older five-tab layout as the primary navigation.
- Remove the separate **Bulk Analysis** and **Reports Export** sections and their shortcuts. Retain the actual report-generation and export functions required within Reports.

## 3. Landing-page arrangement

Keep this sequence:

1. **App header:** existing logo, app title, Quick Start Guide, Copy App Link and Share App.
2. **Research topic:** full study title and collapsible Study Background and Purpose.
3. **Import Dataset**
4. **Search the Research Hub**
5. **Objectives, Reports and Papers navigation**
6. **Exports**

Additional requirements:

- Do not show Objective-Linked Results or statistical-testing controls on the landing page.
- Display objective-specific analysis content only after the user opens Objectives.
- Keep one dataset-import section on the landing page; do not duplicate it inside Objectives.
- Remove redundant counters, review-status messages and other content that interrupts this sequence.
- Remove **Explore Tables and Filters**.
- Keep **Quick Start Guide**, **Copy App Link** and **Share App** available and functional.
- Keep the app name, logo and public-sharing identity consistent across the app and its link preview.
- Configure an appropriate page title, description and social-sharing image. Do not show development labels or technical errors in public presentation.

## 4. Objective selection

- Use an objective **dropdown**, not a dropdown plus a duplicate objective list.
- Remove the separate **Search Objective** field from Objectives, Reports and Papers.
- Objectives and Reports should provide **All Objectives** and the individual objectives.
- For this appendicitis app, retain Objectives 1–6, Exploratory Objective 7: AIR score, and Exploratory Objective 8: Abdominal Ultrasound.
- Remove obsolete exploratory categories without deleting valid analyses belonging to Objectives 1–8.
- Keep the selected objective consistent across its methods, generated outputs, report and paper links.
- Keep paper-export state independent so Papers cannot overwrite Reports selections or exports.

## 5. Objectives section

Arrange the interface in this order:

1. **Research Objective Selector**
2. **Relevant Statistical Methods**
3. **Generate Outputs**
4. **View Tables and Figures**
5. **Open Report**
6. **Open Paper**

Show only the selected objective's relevant content. All Objectives should cover all eight approved objectives.

- Do not include a duplicate dataset importer.
- Remove unnecessary controls, duplicate navigation and unrelated exploratory categories.
- Generate supported results from the actual dataset.
- Allow inspection of individual outputs and their interpretations.
- Link directly to the corresponding Report and Paper.

## 6. Reports section

Arrange the interface in this order:

1. **Research Objective Selector**
2. **Report Tables and Figures:** select the relevant outputs.
3. **View Tables and Figures:** inspect actual selected results and interpretations.
4. **Word Document Preview**
5. **Export Report**
6. **Open Objective** and **Open Paper**

Avoid duplicated output displays and unnecessary controls that repeat the Objectives interface.

Selection controls should provide:

- **Select All**
- **Deselect All**
- Individual checkboxes
- An immediately updated selected-item count
- One clear export action

Export only selected content, in its intended scientific order. Preserve a consistent objective across selection, preview, export and navigation.

## 7. Papers section

Arrange the interface in this order:

1. **Objective Selector**
2. **Proposed Manuscript Title**
3. **Sub-objectives**
4. **Statistical Methods**
5. **References**
6. **Export Paper**
7. **Open Objective** and **Open Report**

- Organise planning by objective and keep it compact.
- Suggest scientifically defensible titles based on actual questions and available findings.
- Use verifiable references; never invent citations.
- Avoid repetitive manuscript ideas that merely rearrange the same analyses.
- Identify overlapping questions, outputs and findings; recommend merging substantially overlapping proposals.
- Distinguish proposed manuscripts from completed publications. Do not promise journal acceptance.
- Remove unnecessary sections such as Cross-Objective Manuscript Planning, Manuscript Components and Current Findings.
- Keep editable paper exports independent of report exports, using A4 portrait only.

## 8. Expandable and collapsible sections

**Expandable sections should start closed by default.**

Apply this to long explanations, settings, import controls, Google Drive controls, report tools and nested options.

- Keep headings visible when collapsed.
- Use consistent chevrons and clickable headings with keyboard support.
- Allow sections to open independently; opening one must not toggle unrelated sections.
- Do not automatically expand unrelated sections after tab changes, import or generation.
- Avoid excessive nested accordions.
- Keep essential navigation and primary actions immediately accessible.
- Explicit requests to view content are exceptions: following a glossary link should reveal the matching definition and keep it open while the user reads.
- Preserve generated data and selections when sections are collapsed.

## 9. Typography and hierarchy

Use one coherent, restrained typography system rather than conflicting individual font choices.

- Use an elegant, formal font for the app title and selected major headings.
- Use a highly readable body font.
- Use a clean interface font for navigation, buttons, labels and controls.
- Use cursive only for occasional decorative accents, never essential scientific content or long paragraphs.
- Load fonts reliably and provide dependable fallbacks.
- Keep sizes normal, comfortable and balanced; avoid excessive boldness.

| Element | Preferred treatment |
| --- | --- |
| Appendicitis Research | Distinctive and most prominent, without being oversized |
| Full research title | Clear, formal and proportionate |
| Section headings | Moderately emphasised |
| Body text and interpretations | Comfortable, readable and consistent |
| Tables, labels and controls | Compact without becoming tiny |

Prevent awkward wrapping, overflow, crowded figures and isolated text styles. Apply the system across all sections and themes. Approved Word-report templates govern document typography separately from interface fonts.

## 10. Colours and themes

Preserve the established palette while increasing depth and contrast purposefully:

- **Ruby/crimson:** distinctive primary accent.
- **Gold, amber or bronze:** restrained secondary highlights.
- **Deep navy/blue:** selected scientific elements.
- **Emerald/green:** successful actions and positive interface states.
- **Neutral surfaces:** balance and readability.

Maintain three distinct themes:

- **Light:** clean backgrounds and dark, sharp text.
- **OLED Dark:** true-black backgrounds and clear, high-contrast text.
- **Colored Mode:** richer, saturated colours with readable content.

Use shared design tokens. Apply gradients selectively to headers, selected navigation or key actions. Avoid competing bright colours and excessive shadows. Make hover, focus, selected, disabled, loading and error states clear.

## 11. Mobile layout and scrolling

- Keep the logo completely visible and unobstructed.
- Rearrange or wrap other elements before allowing controls, dropdowns or sticky content to cover the logo.
- Keep navigation, Appearance and Supporting Tools accessible without collisions.
- Prevent clipped labels, horizontal page overflow and crowded controls.
- Preserve a usable desktop layout and readability at approximately **150% browser zoom**.

Scrolling requirements:

- Provide a real, draggable scrollbar at the far-right edge of the **main research content area** on desktop.
- Keep it available whether the left navigation menu is open or closed.
- Make it control the central content, not merely the sidebar or an individual card.
- Preserve mouse-wheel, touchpad and natural mobile touch scrolling.
- Do not force a desktop scrollbar onto mobile browsers that cannot display it consistently.
- Preserve useful independent scrolling where already implemented.

## 12. Tables, figures and interpretations

- Use clear titles that identify what is compared or measured.
- Show actual sample sizes, denominators, units and relevant statistical evidence.
- Keep title, output, caption/legend, statistical results and interpretation distinguishable.
- Avoid duplicate tables or figures conveying the same information.
- Use concise legends and necessary notes instead of long generic explanations.
- Keep **Essence and Practical Importance** directly associated with each relevant output.
- Interpret the actual findings in plain English without exaggeration.
- Do not infer significance from appearance alone.
- Do not remove important scientific information merely to shorten the display.

## 13. Explain This Graph

Show only two short explanations:

1. **What This Graph Shows**
2. **What It Means for This Research**

- Open the panel by clicking or tapping a graph.
- Use everyday English and the selected graph's actual data and results.
- Avoid lectures, extra headings, lengthy notes and unnecessary technical statistics.
- Place the panel **beside the graph on desktop** and **below it on mobile**.
- Keep it open until explicitly closed.
- Preserve the current objective, graph view and reading position.
- Apply the same behaviour in Objectives and Reports previews.
- Retain useful contextual glossary access without adding a long list of extra controls.

## 14. Statistical Glossary

Every entry should answer:

> What does this mean, and what does it tell us about this research?

Preferred concise format:

- **Plain meaning**
- **What it means for this research**

Include numerical interpretation guidance only where useful and scientifically defensible.

- Avoid textbook lectures, repeated explanations and vague research claims.
- Explain actual study coding, measurement units and thresholds accurately.
- Support full names, abbreviations, spelling variants and relevant variable names in search.
- If a term is undefined, say so clearly; do not substitute an unrelated definition.
- Use one central glossary.
- Link relevant terms in tables, figures, methods, dataset views, outputs and previews without disrupting controls.
- Automatically reveal and highlight the matching definition.
- Keep the glossary open while the user explores it.
- Include a four-row combination table for **MAS and hs-CRP** and **MAS or hs-CRP**.
- Include practical definitions for Youden J, FN, TN, Holm adjustment and sensitivity–specificity trade-offs.
- Distinguish contextual meanings, such as odds ratio versus an OR combination rule.

## 15. Back navigation and preserved context

Back must return to the actual previous destination, not a fixed landing page.

Preserve where practical:

- Selected objective and output
- Report selections and working state
- Filters
- Expanded/collapsed sections
- Scroll position
- Current preview and its reading position

Specific requirements:

- Opening the glossary from a preview must not discard the preview.
- Back must restore the same preview at the same reading location, including deep scroll positions.
- Avoid iframe reloads or reinsertion that resets content to the top.
- Keep Back, Close, collapse, tab switching and Home distinct.
- Do not treat every accordion toggle as a navigation destination.
- Keep browser Back and in-app Back coherent; avoid stale entries, loops and invented history.
- Handle direct openings and refreshed sessions gracefully.

## 16. Report presentation and Word exports

**My approved reports are the authoritative presentation templates.**

- Match their structure, writing style, tables, figures, captions, spacing and formatting.
- Organise the report around the original specific objectives, in their original order.
- Include only analyses relevant to the selected objective and outputs.
- Use clear, natural academic English rather than repetitive or generic AI-style prose.
- Remove software instructions, internal commentary, redundant explanations and unnecessary headings.
- Avoid excessive long dashes and dash-separated phrasing.
- Retain a natural final concluding paragraph where appropriate, without an unnecessary **Conclusion** heading.

Mandatory document requirements:

- Editable **.docx** files.
- **A4 portrait throughout**; no landscape pages or automatic orientation switching.
- Readable tables fitted or logically split within portrait margins.
- Native editable tables wherever practical.
- Properly embedded figures, not screenshots of the app interface.
- Consistent numbering, captions, typography, alignment and spacing.
- Use approved template conventions; where the established report specification requires it, use Times New Roman and justified prose.

Preview and export must use the same underlying report content. Partial selections and mixed selections must retain the approved reporting style rather than falling back to a generic layout or including unselected findings. Avoid references or conclusions that misleadingly describe excluded outputs.

When nine standalone reports are requested, deliver Demographics plus Objectives 1–8 as separate editable files, not one combined substitute.

## 17. Progress monitoring and errors

Keep **result generation** and **report preparation/export** separate.

Each monitor should show genuine progress for its own operation:

- Current task
- Completed items and total
- Percentage where measurable
- Successes, failures and legitimate exclusions
- Clear completion state

Also:

- Prevent duplicate runs.
- Explain each failure using the output title and an understandable reason.
- Do not silently omit selected content.
- Continue eligible work when another item fails safely.
- Never mark unfinished work successful or show simulated progress as real completion.
- Provide retries where practical.
- Make export buttons clearly usable when enabled, with visible loading and error states.
- Preserve working individual-analysis and export workflows.

## 18. Dataset access and scientific integrity

- Keep manual upload available.
- Start Google Drive import from one initial click; do not require a second click to begin authentication.
- Preserve secure account selection, authorised access and access to the designated dataset.
- Preserve variable names, labels, value codes, missing values and validation.
- Do not expose private datasets publicly or place secrets in frontend code.

Throughout the application:

- Never invent data, results, p-values, variable definitions or unsupported analyses.
- Preserve validated calculations and approved objectives.
- State exactly why an analysis is unavailable when the required data or design are missing.
- Distinguish diagnostic accuracy, association, prediction and clinical benefit.
- Do not manufacture continuous ROC curves from fixed binary classifications.
- Do not claim cost savings, incremental strategy costs or cost-effectiveness from total recorded costs alone.
- Keep established study thresholds and units consistent; do not silently recode ambiguous categories.

## 19. Delivery and verification

- Work directly on the existing project and reuse its components, calculation functions and export architecture.
- Make only the requested changes; do not start unrelated upgrades.
- Test the affected interaction in the running app, not just the appearance of a button or a CSS change.
- Report only tests actually performed and clearly identify genuine limitations.
- Keep progress updates and completion reports brief and useful.
- Distinguish **packaged**, **tested** and **deployed**.
- Deliver **one complete ZIP containing all cumulative updates**, rather than scattered patches or competing versions, when project delivery is requested.
- Include required configuration, dependencies and concise implementation instructions.
- Exclude secrets, caches, temporary files, unnecessary build outputs and duplicated versions.

## Maintaining this document

When I give a new complaint or design correction, update the relevant preference instead of retaining contradictory instructions. Record the latest requirement without claiming it is implemented until the app has actually been changed and checked. Do not turn a study-specific statistical instruction into a universal rule for unrelated research.
