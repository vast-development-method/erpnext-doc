# Supporting services · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-6b008a84ff6669"></a>
### Party exists

`operation_enterprise_portal_utils_business_behavior_party_exists`

**Inputs** doctype, user.

**Record and data access** read “Contact” via get\_value · resolve a document from “Contact” via get\_doc.

**Explicit results** doctype belongs to doctypes · false.

**Local steps**

- Set contact\_name from Platform.db.get\_value(“Contact”, mapping(“email\_id” → user)).
- If contact\_name.
  - Set contact from Platform.get\_doc(“Contact”, contact\_name).
  - Set doctypes from list of d.link\_doctype for d drawn from contact.links.
    - Draw d from contact.links.
  - Return doctype belongs to doctypes.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0599.json#L6296) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L658)

<a id="op-f6bf0ea17bfdcc"></a>
### Send message

`operation_enterprise_templates_utils_business_behavior_send_message`

**Inputs** sender, message, subject = “Website Query”.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“POST”)), rate\_limit(limit = 10, seconds = (3 × 60)).

**Record and data access** read “Contact Us Settings” via get\_single\_value · read “CRM Settings” via get\_single\_value · execute query text (SELECT, Dynamic Link, Contact) · read “Lead” via get\_value · resolve a document from “Lead” via get\_doc · 2 additional forms in the steps below.

**State and service calls** call insert on Platform.get\_doc(doctype = “Lead”, email\_id = sender, lead\_name = sender.split(“@”) at 0.title()) · call insert on opportunity · call insert on comm.

**Explicit results** no value.

**Local steps**

- Bind dependencies website\_send\_message.
- If Platform.get\_single\_value(“Contact Us Settings”, “is\_disabled”).
  - Return no value.
- Evaluate website\_send\_message(sender, message, subject).
- Set sender from validate\_email\_address(sender, throw = true).
- Set message from escape\_html(message).
- Set subject from strip\_html(subject).
- Set oppotunity\_creation from Platform.get\_single\_value(“CRM Settings”, “enable\_opportunity\_creation\_from\_contact\_us”).
- If not oppotunity\_creation.
  - Return no value.
- Set lead, customer from no value.
- If Platform.session.user.lower() equals sender.lower().
  - Set customer from Platform.db.sql(query text (SELECT, Dynamic Link, Contact), sender).
- If not customer.
  - Set lead from Platform.db.get\_value(“Lead”, dict(email\_id = sender)).
  - If not lead.
    - Set new\_lead from Platform.get\_doc(doctype = “Lead”, email\_id = sender, lead\_name = nested operand in the contract(nested operand in the contract) at 0.title()).insert(ignore\_permissions = true).
- Set opportunity from Platform.get\_doc(doctype = “Opportunity”, opportunity\_from = “Customer” when customer, otherwise “Lead”, status = “Open”, title = subject, …).
  - Value choice on customer — true gives “Customer”, false gives “Lead”.
- If customer.
  - Set opportunity.party\_name from customer at 0 at 0.
- Otherwise.
  - If lead.
    - Set opportunity.party\_name from lead.
  - Otherwise.
    - Set opportunity.party\_name from new\_lead.name.
- Evaluate opportunity.insert(ignore\_permissions = true).
- Set comm from Platform.get\_doc(mapping(“doctype” → “Communication”, “subject” → subject, “content” → message, “sender” → sender, …)).
- Evaluate comm.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Contact Us Settings”, “is\_disabled”), Platform.get\_single\_value(“CRM Settings”, “enable\_opportunity\_creation\_from\_contact\_us”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L161) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1372)

## Record · Video

[Record definition](../../../../data/record-types/video.json)

<a id="op-cf2e3cfe0d6fcc"></a>
### Video.validate

`operation_enterprise_utilities_record_definitions_video_business_behavior_video_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.provider differs from “YouTube”.
  - Return no value.
- Evaluate self.set\_video\_id().
- If is\_tracking\_enabled().
  - Evaluate self.set\_youtube\_statistics().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set video id](operations-009.md#op-c36c5a22065ccd), [set youtube statistics](operations-009.md#op-bccc94bafbe11b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L88)

<a id="op-c36c5a22065ccd"></a>
### Video.set video id

`operation_enterprise_utilities_record_definitions_video_business_behavior_video_set_video_identifier`

**Inputs** self.

**Local steps**

- If (self.url and (not self.get(“youtube\_video\_id”) or self.has\_value\_changed(“url”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.url → (not self.get(“youtube\_video\_id”) or self.has\_value\_changed(“url”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“youtube\_video\_id”) → self.has\_value\_changed(“url”).
  - Set self.youtube\_video\_id from get\_id\_from\_url(self.url).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L86)

<a id="op-bccc94bafbe11b"></a>
### Video.set youtube statistics

`operation_enterprise_utilities_record_definitions_video_business_behavior_video_set_youtube_statistics`

**Inputs** self.

**Record and data access** read “Video Settings” via get\_single\_value.

**Local steps**

- Set api\_key from Platform.db.get\_single\_value(“Video Settings”, “api\_key”).
- Attempt the following.
  - Set api from Api(api\_key = api\_key).
  - Set video from api.get\_video\_by\_id(video\_id = self.youtube\_video\_id).
  - Set video\_stats from video.items at 0.to\_dict().get(“statistics”).
  - Set self.like\_count from video\_stats.get(“likeCount”).
  - Set self.view\_count from video\_stats.get(“viewCount”).
  - Set self.dislike\_count from video\_stats.get(“dislikeCount”).
  - Set self.comment\_count from video\_stats.get(“commentCount”).
- On failure (Exception).
  - Evaluate self.log\_error(“Unable to update YouTube statistics”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Video Settings”, “api\_key”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L87)

<a id="op-2ca605a3ec2a0a"></a>
### Is tracking enabled

`operation_enterprise_utilities_record_definitions_video_business_behavior_is_tracking_enabled`

**Inputs** no declared parameters.

**Record and data access** read “Video Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“Video Settings”, “enable\_youtube\_tracking”).

**Local steps**

- Return Platform.db.get\_single\_value(“Video Settings”, “enable\_youtube\_tracking”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Video Settings”, “enable\_youtube\_tracking”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0989.json#L1475) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L84)

<a id="op-6aa0efb778903c"></a>
### Update youtube data

`operation_enterprise_utilities_record_definitions_video_business_behavior_update_youtube_data`

**Inputs** no declared parameters.

**Record and data access** read “Video Settings” via get\_single.

**State and service calls** request set\_single\_value on “Video Settings”.

**Explicit results** no value.

**Local steps**

- Set video\_settings from Platform.get\_single(“Video Settings”).
- If (not video\_settings.enable\_youtube\_tracking or not is\_update\_due(video\_settings)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not video\_settings.enable\_youtube\_tracking → not is\_update\_due(video\_settings).
  - Return no value.
- Evaluate batch\_update\_youtube\_data().
- Evaluate Platform.db.set\_single\_value(“Video Settings”, “last\_youtube\_update”, now\_datetime()).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L85)

<a id="op-96c5112ca65b62"></a>
### Is update due

`operation_enterprise_binding_enterprise_utilities_doctype_video_video_is_update_due`

**Inputs** video\_settings.

**Declared result** bool.

**Explicit results** true · hours\_since\_update ≥ get\_frequency\_in\_hours(video\_settings.frequency).

**Local steps**

- If not video\_settings.last\_youtube\_update.
  - Return true.
- Set hours\_since\_update from time\_diff\_in\_hours(start\_of\_hour(now\_datetime()), start\_of\_hour(get\_datetime(video\_settings.last\_youtube\_update))).
- Return hours\_since\_update ≥ get\_frequency\_in\_hours(video\_settings.frequency).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L36) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1317)

<a id="op-46e6e1b7a2d695"></a>
### Get frequency in hours

`operation_enterprise_binding_enterprise_utilities_doctype_video_video_get_frequency_in_hours`

**Inputs** frequency.

**Declared result** int.

**Explicit results** mapping(“6 hrs” → 6, “Daily” → 24).get(frequency, 1).

**Local steps**

- Return mapping(“6 hrs” → 6, “Daily” → 24).get(frequency, 1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L35) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1316)

<a id="op-2027a819d8cbc7"></a>
### Start of hour

`operation_enterprise_binding_enterprise_utilities_doctype_video_video_start_of_hour`

**Inputs** value.

**Declared result** datetime.

**Explicit results** value.replace(minute = 0, second = 0, microsecond = 0).

**Local steps**

- Return value.replace(minute = 0, second = 0, microsecond = 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L38) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1319)

<a id="op-f4bfd73b4f8e29"></a>
### Get formatted ids

`operation_enterprise_utilities_record_definitions_video_business_behavior_get_formatted_identifiers`

**Inputs** video\_list.

**Explicit results** “,”.join(ids).

**Local steps**

- Set ids from list().
- For each video in video\_list.
  - Evaluate ids.append(video.youtube\_video\_id).
- Return “,”.join(ids).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0989.json#L1990) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L82)

<a id="op-be4d89c85c3b12"></a>
### Get id from url

`operation_enterprise_utilities_record_definitions_video_business_behavior_get_identifier_from_resource_address`

**Inputs** url.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** video\_id.

**Explicit failure paths** validation helper — translated “URL can only be a string” · validation helper — translated “Could not find a YouTube video ID in the URL”.

**Local steps**

- If not isinstance(url, str).
  - Call the validation error handler Platform.throw(translated “URL can only be a string”, title = translated “Invalid URL”).
- Set video\_id from parse\_youtube\_video\_id(url).
- If not video\_id.
  - Call the validation error handler Platform.throw(translated “Could not find a YouTube video ID in the URL”, title = translated “Invalid URL”).
- Return video\_id.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L83)

<a id="op-855d4e37695dde"></a>
### Parse youtube video id

`operation_enterprise_binding_enterprise_utilities_doctype_video_video_parse_youtube_video_id`

**Inputs** url.

**Declared result** (str bitwise or no value).

**Explicit results** no value · video\_id when (video\_id and YOUTUBE\_VIDEO\_ID.fullmatch(video\_id)), otherwise no value.

**Local steps**

- Set parsed from urlparse(url.strip() when “://” belongs to url, otherwise formatted command or address in the contract).
  - Value choice on “://” belongs to url — true gives url.strip(), false gives formatted command or address in the contract.
- Set host from (parsed.hostname or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.hostname → empty text.
- If not any(generator of (host equals domain or host.endswith(formatted text .{domain})) for domain drawn from YOUTUBE\_DOMAINS).
  - Draw domain from YOUTUBE\_DOMAINS.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in host equals domain → host.endswith(formatted text .{domain}).
  - Return no value.
- Set segments from list of segment for segment drawn from parsed.path.split(“/”) where segment.
  - Draw segment from parsed.path.split(“/”), keep a combination only if (segment).
- If host.endswith(“youtu.be”).
  - Set video\_id from segments at 0 when segments, otherwise no value.
    - Value choice on segments — true gives segments at 0, false gives no value.
- Otherwise.
  - If (len(segments) &gt; 1 and segments at 0 belongs to tuple(“embed”, “shorts”, “live”, “v”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(segments) &gt; 1 → segments at 0 belongs to tuple(“embed”, “shorts”, “live”, “v”).
    - Set video\_id from segments at 1.
  - Otherwise.
    - Set video\_id from parse\_qs(parsed.query).get(“v”, list(no value)) at 0.
- Return video\_id when (video\_id and YOUTUBE\_VIDEO\_ID.fullmatch(video\_id)), otherwise no value.
  - Value choice on (video\_id and YOUTUBE\_VIDEO\_ID.fullmatch(video\_id)) — true gives video\_id, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in video\_id → YOUTUBE\_VIDEO\_ID.fullmatch(video\_id).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1318)

<a id="op-099a0037cc69d8"></a>
### Batch update youtube data

`operation_enterprise_utilities_record_definitions_video_business_behavior_batch_update_youtube_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Video” via get\_all.

**Local steps**

- Evaluate Platform.has\_permission(“Video Settings”, “write”, throw = true).
- Bind local operation get\_youtube\_statistics for subsequent calls.
- Bind local operation prepare\_and\_set\_data for subsequent calls.
- Bind local operation set\_youtube\_data for subsequent calls.
- Set video\_list from Platform.get\_all(“Video”, filters = mapping(“provider” → “YouTube”, “youtube\_video\_id” → list(“is”, “set”)), fields = list(“youtube\_video\_id”)).
- If len(video\_list) &gt; 50.
  - Set tuple(start, end) from tuple(0, 50).
  - While start &lt; len(video\_list).
    - Set batch from video\_list at slice start to end.
    - Evaluate prepare\_and\_set\_data(batch).
    - Update start using + 50.
    - Update end using + 50.
- Otherwise.
  - Evaluate prepare\_and\_set\_data(video\_list).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Video Settings”, “write”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L78)

<a id="op-5189ded04a6746"></a>
### Batch update youtube data.get youtube statistics

`operation_enterprise_utilities_record_definitions_video_business_behavior_batch_update_youtube_data_get_youtube_statistics`

**Inputs** video\_ids.

**Record and data access** read “Video Settings” via get\_single\_value.

**Explicit results** video\_stats.

**Local steps**

- Set api\_key from Platform.db.get\_single\_value(“Video Settings”, “api\_key”).
- Set api from Api(api\_key = api\_key).
- Attempt the following.
  - Set video from api.get\_video\_by\_id(video\_id = video\_ids).
  - Set video\_stats from video.items.
  - Return video\_stats.
- On failure (Exception).
  - Evaluate Platform.log\_error(“Unable to update YouTube statistics”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Video Settings”, “api\_key”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0989.json#L3260) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L79)

<a id="op-6df58f5e0653ff"></a>
### Batch update youtube data.prepare and set data

`operation_enterprise_utilities_record_definitions_video_business_behavior_batch_update_youtube_data_prepare_and_set_data`

**Inputs** video\_list.

**Local steps**

- Set video\_ids from get\_formatted\_ids(video\_list).
- Set stats from get\_youtube\_statistics(video\_ids).
- If stats.
  - Evaluate set\_youtube\_data(stats).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L80)

<a id="op-33171a4ff08d8a"></a>
### Batch update youtube data.set youtube data

`operation_enterprise_utilities_record_definitions_video_business_behavior_batch_update_youtube_data_set_youtube_data`

**Inputs** entries.

**State and service calls** request set\_value on “Video”.

**Local steps**

- For each entry in entries.
  - Set video\_stats from entry.to\_dict().get(“statistics”).
  - Set video\_id from entry.to\_dict().get(“id”).
  - Set stats from mapping(“like\_count” → cint(video\_stats.get(“likeCount”)), “view\_count” → cint(video\_stats.get(“viewCount”)), “dislike\_count” → cint(video\_stats.get(“dislikeCount”)), “comment\_count” → cint(video\_stats.get ….
  - Evaluate Platform.db.set\_value(“Video”, mapping(“youtube\_video\_id” → video\_id), stats).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L81)

## Record · Video settings

[Record definition](../../../../data/record-types/video_settings.json)

<a id="op-84bbab08f44973"></a>
### Video Settings.validate

`operation_enterprise_utilities_record_definitions_video_settings_business_behavior_video_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.replace\_removed\_frequency().
- Evaluate self.validate\_tracking\_settings().
- Evaluate self.validate\_youtube\_api\_key().

If control reaches the end, it returns no value.

**Methods declared on this owner** [replace removed frequency](operations-009.md#op-3a307026d01ba0), [validate tracking settings](operations-009.md#op-468af4a6b902ff), [validate youtube api key](operations-009.md#op-1f76e6c65f2b47).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L89)

<a id="op-3a307026d01ba0"></a>
### Video Settings.replace removed frequency

`operation_enterprise_binding_enterprise_utilities_doctype_video_settings_video_settings_videosettings_replace_removed_frequency`

**Inputs** self.

**Local steps**

- If self.frequency equals “30 mins”.
  - Set self.frequency from “1 hr”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L33) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1314)

<a id="op-468af4a6b902ff"></a>
### Video Settings.validate tracking settings

`operation_enterprise_binding_enterprise_utilities_doctype_video_settings_video_settings_videosettings_validate_tracking_settings`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is required to enable YouTube tracking”.format(translated self.meta.get\_label(fieldname)).

**Local steps**

- If not self.enable\_youtube\_tracking.
  - Return no value.
- For each fieldname in tuple(“api\_key”, “frequency”).
  - If not self.get(fieldname).
    - Call the validation error handler Platform.throw(translated “{0} is required to enable YouTube tracking”.format(translated self.meta.get\_label(fieldname))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L34) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1315)

<a id="op-1f76e6c65f2b47"></a>
### Video Settings.validate youtube api key

`operation_enterprise_utilities_record_definitions_video_settings_business_behavior_video_settings_validate_youtube_application_programming_interface_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L90)

## Report · Youtube interactions

<a id="op-64126e49c653c5"></a>
### Execute

`operation_enterprise_utilities_report_youtube_interactions_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Video Settings” via get\_single\_value.

**Explicit results** tuple(list(), list()) · tuple(columns, data, no value, chart\_data, …).

**Local steps**

- If (not Platform.db.get\_single\_value(“Video Settings”, “enable\_youtube\_tracking”) or not filters).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.db.get\_single\_value(“Video Settings”, “enable\_youtube\_tracking”) → not filters.
  - Return tuple(list(), list()).
- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Set tuple(chart\_data, summary) from get\_chart\_summary\_data(data).
- Return tuple(columns, data, no value, chart\_data, …).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Video Settings”, “enable\_youtube\_tracking”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L92)

<a id="op-845c36c9816bed"></a>
### Get columns

`operation_enterprise_utilities_report_youtube_interactions_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Published Date”, “fieldname” → “publish\_date”, “fieldtype” → “Date”, “width” → 100), mapping(“label” → translated “Title”, “fieldname” → “title”, “fieldtype” → “Data”, “w ….

**Local steps**

- Return list(mapping(“label” → translated “Published Date”, “fieldname” → “publish\_date”, “fieldtype” → “Date”, “width” → 100), mapping(“label” → translated “Title”, “fieldname” → “title”, “fieldtype” → “Data”, “w ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0990.json#L5532) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L94)

<a id="op-6dc871b359aaf1"></a>
### Get data

`operation_enterprise_utilities_report_youtube_interactions_business_behavior_get_data`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set video from Platform.qb.DocType(“Video”).
- Set query from nested operand in the contract(nested operand in the contract).select(video.publish\_date, video.title, video.provider, video.duration, …).where(video.view\_count.isnotnull()).orderby(video.view\_count, order ….
- If filters.get(“from\_date”).
  - Set query from query.where(video.publish\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set query from query.where(video.publish\_date ≤ filters.get(“to\_date”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L95)
