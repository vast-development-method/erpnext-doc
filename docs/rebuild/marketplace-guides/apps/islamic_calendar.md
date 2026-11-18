# Islamic Calendar

[Business workflow and acceptance cases](../../../capabilities/guides/data.md#hijri-civil-day-conversion).

## Publisher evidence

Kanak Infosystems lists version 15. Users can enter a date through a Hijri picker or switch to Gregorian in date fields across ERP modules. The vendor also describes conversion in forms and reports and RTL layout support. The marketplace calls the license MIT. The publisher's product page identifies proprietary licensing. The terms attached to a particular distributed revision need confirmation. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/islamic_calendar) · [Publisher's v15 feature and license page](https://www.kanakinfosystems.com/frappe/apps/15.0/islamic_calendar) · [Listed repository](https://github.com/kanakinfo/islamic_calendar)

## Pinned public copy

A third-party copy credits Kanak and loads two date-format preferences for authenticated users. The control requests the Islamic calendar with an English locale identifier and declines Gregorian years later than 2076 on its forward path. Its two conversion functions use a bundled Umm al-Qura month-start table. Presence of a right-to-left picker or a localized month pack does not establish the calendar used by every deployed site. [Copy identity](https://github.com/ashish-greycube/islamic_calendar/blob/3a6ee95cb5d57bea4bfe4d091ccfd309164972ed/islamic_calendar/hooks.py#L1) · [Boot preferences](https://github.com/ashish-greycube/islamic_calendar/blob/3a6ee95cb5d57bea4bfe4d091ccfd309164972ed/islamic_calendar/islamic_calendar/islamic_configure.py#L4) · [Date control](https://github.com/ashish-greycube/islamic_calendar/blob/3a6ee95cb5d57bea4bfe4d091ccfd309164972ed/islamic_calendar/public/js/custom_control_date.js#L1) · [Conversion and table](https://github.com/ashish-greycube/islamic_calendar/blob/3a6ee95cb5d57bea4bfe4d091ccfd309164972ed/islamic_calendar/public/hijri_libary/jquery.calendars.islamic.js#L154)

## Proposed multilingual rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/data.md#hijri-civil-day-conversion-3).

## Remaining evidence

The current vendor revision, exact table coverage, treatment of date/time fields near midnight and translated month sets on a delivered site remain unverified. The dated conversion above was calculated from the public copy's table. It is a regression fixture for that conversion policy.
