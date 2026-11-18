# Nepali Calendar

[Business workflow and acceptance cases](../../../capabilities/guides/data.md#nepali-civil-day-conversion).

Kanak Infosystems lists version 15. Its datepicker lets a form user select a Nepali date and convert between Nepali and Gregorian dates in either direction. The publisher explicitly covers Date fields across sales, purchasing, HR and accounting. This establishes an input and display capability. Storage format, supported year range, conversion data and treatment of DateTime fields require separate evidence. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nepali_calendar) · [Publisher's v15 product guide](https://www.kanakinfosystems.com/frappe/apps/15.0/nepali_calendar)

A public modified copy names Kanak in the app manifest and installation instructions. Its server-side test declarations specify Gregorian years 1944–2042 and Nepali years 2000–2099. Its browser code adds a Nepali rendering for Date and DateTime controls using configured patterns. The browser and server have separate conversion paths. The test ranges are properties of that historical server converter, rather than a verified promise about the listed package. [Copy manifest](https://github.com/ajiragroup/nepali_calendar/blob/bcfdde64f305d94a564a8a74623688e21877458d/nepali_calendar/hooks.py) · [Converter cases](https://github.com/ajiragroup/nepali_calendar/blob/bcfdde64f305d94a564a8a74623688e21877458d/nepali_calendar/nepali/tests/test_date_converter.py) · [Browser control](https://github.com/ajiragroup/nepali_calendar/blob/bcfdde64f305d94a564a8a74623688e21877458d/nepali_calendar/public/js/custom_control_date.js)

## Proposed rebuild contract

| Proposed acceptance case | Expected result |
|---|---|
| Enter 1 Baisakh 2081 on a purchase document. Open it in a Gregorian view and filter on 13 April 2024. | The saved date is `2024-04-13` and the filter finds exactly the same document. Changing back displays the original date. Radio Nepal independently dates this New Year boundary. [Reference date](https://radionepalonline.com/en/2024/04/13/375928.html) |
| Change only the language and numeral preference on that record. | Localized labels and supported numeral glyphs change. The date, due-date calculations, and selected calendar stay the same. |
| Submit an impossible day or a year beyond the loaded conversion table. | Return a localized validation error, retain the user's entry for correction and leave the stored date unchanged. |
| A user in a distant time zone opens an already-saved civil date. | The Gregorian and Nepali views preserve the civil day across the zone change. |

The publisher's repository remains unpinned in the cohort snapshot. Upstream control code provides the ordinary Date integration point. The deployed marketplace build, calendar-switch persistence and exact coverage shared by its server and browser conversions still need direct evidence. [Named app repository](https://github.com/kanakinfo/nepali_calendar) · [Framework Date control](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/public/js/frappe/form/controls/date.js)

[Read the consolidated workflow](../../../capabilities/guides/data.md#nepali-civil-day-conversion).
