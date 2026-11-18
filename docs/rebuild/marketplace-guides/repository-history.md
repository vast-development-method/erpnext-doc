# Historical repository evidence

A search of the public GitHub event archive found **654 indexed events for 22 of the 69 publisher-named repositories** before 18 November 2026 UTC. Nine names had a recorded fork event. A fork event identifies the account that took the copy and the repository name at the time. That relationship helped locate the source for [Retail Suite](apps/retail.md) and corroborated the independently located [Bulk PDF Downloader](apps/bulk_download.md) copy. An event does not establish which package a customer installed. The archive operator reports that some event types are undercounted. The 47 unmatched names have no exact-name hit in this query. [GitHub event archive](https://www.gharchive.org/) · [ClickHouse dataset and coverage notes](https://ghe.clickhouse.tech/)

## Publicly recoverable snapshots

Five publisher-named repositories had a pull request or review event containing a nonempty head revision. For each repository, the table uses the most recent such event and gives a public copy from which the complete commit archive was successfully retrieved and enumerated. A pull request can contain unmerged work. The individual app guides identify the source used for their particular behavioural claims.

| Listing | Event date, UTC | Event head and recovered archive | Regular files |
|---|---|---|---:|
| [EasyEcom](apps/erpnext_easyecom.md) | 2026-06-16 | [dd693e98f90f8026e01d95bb7329d447e76b728f](https://codeload.github.com/mohsinalimat/ecommerce_super/tar.gz/dd693e98f90f8026e01d95bb7329d447e76b728f) | 478 |
| [Nepali Calendar](apps/nepali_calendar.md) | 2024-09-02 | [bcfdde64f305d94a564a8a74623688e21877458d](https://codeload.github.com/ajiragroup/nepali_calendar/tar.gz/bcfdde64f305d94a564a8a74623688e21877458d) | 269 |
| [PAV](apps/pav.md) | 2021-04-11 | [51bcc913effa9085f546ec4fa7f490bf3c55872e](https://codeload.github.com/questerp/pav/tar.gz/51bcc913effa9085f546ec4fa7f490bf3c55872e) | 169 |
| [PCAT assessment](apps/frappe_pcat_exam.md) | 2025-12-18 | [56fb590eb2230a88b1bdab6faa21349987c646de](https://codeload.github.com/mohsinalimat/frappe_pcat_assessment/tar.gz/56fb590eb2230a88b1bdab6faa21349987c646de) | 55 |
| [Retail Suite](apps/retail.md) | 2026-09-05 | [3c72d03bc2f02bb99255bd3f2b103241627d8af3](https://codeload.github.com/galaxlabs/retail-suite/tar.gz/3c72d03bc2f02bb99255bd3f2b103241627d8af3) | 426 |

For Retail Suite the dated event is a review comment on pull request 36. Raw event `9550935279` records galaxlabs forking the publisher repository on 17 May 2026. The [guide](apps/retail.md) can therefore cite the surviving app independently of an unfetchable publisher branch. For Bulk PDF Downloader raw event `46857876463` recorded Sanprasoftware forking the exact listed repository on 23 February 2025. The public copy's package and commit author independently match the marketplace publisher. [Retail fork event hour](https://data.gharchive.org/2026-05-17-6.json.gz) · [Bulk downloader fork event hour](https://data.gharchive.org/2025-02-23-6.json.gz)

## References with no recovered app tree

- **Frappe BigQuery.** Event `6293110162` records a push to `refs/heads/main` at 13:14:48 UTC on 27 November 2025, with head `131138c2997ae6ac585a1497c88461e75582c10b`. The publisher archive for this commit returned HTTP 404. The guide draws on the publisher's workflow description. [Raw event hour](https://data.gharchive.org/2025-11-27-13.json.gz) · [BigQuery guide](apps/frappe_bigquery.md)
- **NexGen PMS.** Event `11028972947` records a push to `refs/heads/main` at 08:16:18 UTC on 25 April 2026, with head `73ee9ba8b25faad283c34452dcba43eab6f3cb69`. The publisher archive for this commit returned HTTP 404. [Raw event hour](https://data.gharchive.org/2026-04-25-8.json.gz) · [Property management guide](apps/nexgen_pms.md)
- **Sanpra Easypay.** Wiki event `49107456379` records creation of a Home page at 13:43:50 UTC on 27 April 2025, at wiki revision `73d88908fe6f93512a45249591afa646e4a4804c`. A wiki revision refers to documentation, and the current public Home page could not be retrieved. [Raw event hour](https://data.gharchive.org/2025-04-27-13.json.gz) · [Easypay guide](apps/sanpra_easypay.md)

## Reproduce the cohort search

From the repository root, pass the 69 exact, case-sensitive repository names from the preserved listing snapshot as a bound parameter to the public ClickHouse service. This query deliberately preserves the historical names. A repository rename, missed event or unavailable period can affect its coverage. To investigate a specific fork, inspect that repository's rows with event type `ForkEvent`, then verify the surviving repository's package identity and download a full immutable revision before citing code.

```sh
repo_names=$(jq -r '[.listings[] | select(.head_status == "unresolved") |
  .repository_url | sub("^https://github.com/"; "")] | join(",")' docs/rebuild/extensions/marketplace.json)
curl --fail --silent --show-error --get 'https://play.clickhouse.com/' \
  --data-urlencode 'user=play' \
  --data-urlencode "param_names=$repo_names" \
  --data-urlencode "query=SELECT repo_name, count() AS events,
    min(created_at) AS first_seen, max(created_at) AS last_seen,
    arraySort(groupUniqArray(event_type)) AS event_types,
    argMaxIf(head_sha, created_at, head_sha != '') AS last_recorded_head
    FROM github_events
    WHERE repo_name IN (SELECT arrayJoin(splitByChar(',', {names:String})))
      AND created_at < toDateTime('2026-11-18 00:00:00', 'UTC')
    GROUP BY repo_name ORDER BY repo_name FORMAT JSONEachRow"
```
