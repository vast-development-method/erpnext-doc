# Live role, record and transaction qualification

Twenty-one observations passed on a dedicated site with the business and foundation applications, a real MariaDB database and a real queue broker. Three synthetic system users exercised ordinary application routes using distinct credentials created solely for this test. The service processed real HTTP requests in process through the web application. The permission checks, document controllers and request commit or rollback behavior ran normally. The exercise began with two ordinary desk users and one user holding the System Manager role. The privileged installation identity was used to create the actors and inspect the test environment. [Recorded observations](observations.json) · [Strict acceptance schema](observations.schema.json)

| Business question | Observed result |
|---|---|
| Who can read a private note? | The creator could fetch it by name and find it through a filtered list. A peer received HTTP 403 on direct read and an empty filtered list. |
| Can the creator make a note public? | The ordinary creator requested a public note. The stored public flag remained zero because the actor lacked write access to its field level. A peer still received HTTP 403. A manager-created public note was readable and listable by the same peer. |
| Does the role gate apply to singleton reads? | The manager retrieved System Settings. The ordinary desk user received HTTP 403 through the same resource route. |
| Is a batch saved atomically at the request boundary? | A valid two-note batch returned two identities. Fresh requests found one record for each title. A second batch supplied a valid first row and a second row missing its required title. The request returned HTTP 417 with a mandatory-field error. A fresh request found no first row from the failed batch. |
| When does an after-commit job become visible? | Both transactions registered a real queue operation and saw no broker job before the boundary. The rolled-back transaction still had no job afterward. After commit the broker held one queued job with the originating site, actor and operation. The runner removed its own job after inspection. |

The note controller provides a concrete parent-level visibility rule, and its metadata reserves publication at an elevated permission level. A peer's ability to read ordinary public content therefore depends on an authorized publishing action. The batch operation inserts its members in sequence before the web request completes. These distinctions matter to a replacement that offers bulk import, private notes or a post-commit notification following a business write. [Note access rule](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/desk/doctype/note/note.py#L74-L82) · [Note field and role levels](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/desk/doctype/note/note.json) · [Batch operation](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/client.py#L231-L243) · [Request recovery](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/app.py#L153-L170)

### Reproduce on a disposable site

The [optional native runner](observe.py) requires the pinned applications, a working database and broker, an isolated site with `allow_tests` and `blueprint_witness` enabled, and a default queue without a consuming worker for the duration of the two broker inspections. It creates synthetic users, roles and records. The site may be reused for another run because fixture names are unique. Run from the Bench root with the documentation repository checked out locally. The prompts accept existing paths and a disposable site name. The result goes into a newly created directory.

```bash
set -eu
read -r -p 'Path to documentation checkout: ' docs
read -r -p 'Disposable site name: ' site
result_dir=$(mktemp -d)
env/bin/python "$docs/docs/rebuild/platform-live/observe.py" \
    --site "$site" --sites-path "$PWD/sites" --output "$result_dir/observations.json"
cat "$result_dir/observations.json"
```

The runner records the installed source commit identities and database version along with observed outcomes. The receipt excludes site configuration, keys, credentials, personal data and request tracebacks. The test site retains the synthetic users and data until retired. The queue check proves broker admission. Worker entry, task completion, retry identity, multi-site isolation, simultaneous transactions and external HTTP ingress remain independent qualification cases.
