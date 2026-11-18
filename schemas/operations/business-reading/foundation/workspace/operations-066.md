# Forms, reports and navigation · operations 66

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio ai session

<a id="op-ff85a23de46044"></a>
### Studio AISession.delete ai messages

`operation_foundation_binding_foundation_studio_doctype_studio_ai_session_studio_ai_session_studioaisession_delete_ai_messages`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1929)

## Record · Studio app

<a id="op-709c2a0de5f0de"></a>
### Studio App Renderer.render

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_render`

**Inputs** self.

**Explicit results** super().render().

**Explicit failure paths** Platform.Redirect(http\_status\_code = 302).

**Local steps**

- If (Platform.session.user equals “Guest” and not self.can\_render\_for\_guest()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Guest” → not self.can\_render\_for\_guest().
  - Set Platform.flags.redirect\_location from formatted text /login?redirect-to=/{quote(self.path)}.
  - Raise Platform.Redirect(http\_status\_code = 302).
- Return super().render().

**Methods declared on this owner** [can render for guest](operations-066.md#op-5d51959441bb17).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2010) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1986)

<a id="op-5d51959441bb17"></a>
### Studio App Renderer.can render for guest

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_can_render_for_guest`

**Inputs** self.

**Record and data access** read “Studio Page” via exists.

**Explicit results** false · bool(Platform.db.exists(“Studio Page”, dict(studio\_app = self.docname, published = 1, allow\_guest = 1))).

**Local steps**

- If self.is\_preview().
  - Return false.
- Return bool(Platform.db.exists(“Studio Page”, dict(studio\_app = self.docname, published = 1, allow\_guest = 1))).

**Methods declared on this owner** [is preview](operations-066.md#op-0e351f74fa746c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1983)

<a id="op-1d5c175eb88b65"></a>
### Studio App Renderer.can render

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_can_render`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- If app bound to self.find\_app\_for\_path().
  - Set self.doctype from “Studio App”.
  - Set self.docname from app.
  - Return true.
- Return false.

**Methods declared on this owner** [find app for path](operations-066.md#op-bd3967e5af86b9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1982)

<a id="op-bd3967e5af86b9"></a>
### Studio App Renderer.find app for path

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_find_app_for_path`

**Inputs** self.

**Record and data access** read “Studio App” via get\_value · read “Studio Page” via exists.

**Explicit results** no value · studio\_app · studio\_app when has\_published\_pages, otherwise no value.

**Local steps**

- Set \_path from self.path.split(“/”).
- If self.is\_preview().
  - Set app\_route from \_path at 1.
- Otherwise.
  - Set app\_route from \_path at 0.
- Set studio\_app from Platform.db.get\_value(“Studio App”, dict(route = app\_route), “name”).
- If not studio\_app.
  - Return no value.
- If self.is\_preview().
  - Return studio\_app.
- Set has\_published\_pages from Platform.db.exists(“Studio Page”, dict(studio\_app = studio\_app, published = 1)).
- Return studio\_app when has\_published\_pages, otherwise no value.
  - Value choice on has\_published\_pages — true gives studio\_app, false gives no value.

**Methods declared on this owner** [is preview](operations-066.md#op-0e351f74fa746c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2008) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1984)

<a id="op-c567515ee10ee9"></a>
### Studio App Renderer.update context

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_update_context`

**Inputs** self.

**Record and data access** read “Studio Page” via get\_all.

**Local steps**

- Evaluate super().update\_context().
- If self.is\_preview().
  - Set self.context.is\_preview from true.
  - Set self.context.app\_route from formatted text dev/{self.context.app\_route}.
  - Evaluate self.use\_studio\_renderer().
  - Set self.context.app\_pages from Platform.get\_all(“Studio Page”, dict(studio\_app = self.context.app\_name), list(“name”, “page\_title”, “route”)).
- Otherwise.
  - Set self.context.template from “templates/generators/app\_renderer.html”.
  - Set manifest from self.context.doc.get\_assets\_from\_manifest().
  - If manifest.
    - Set self.context.stylesheets from manifest.get(“stylesheets”, list()).
    - Set self.context.script from manifest.get(“script”).
  - Otherwise.
    - Evaluate self.use\_studio\_renderer().
    - Set self.context.assets\_not\_found from bool((self.context.doc.is\_standard or can\_build\_bundle())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.context.doc.is\_standard → can\_build\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is preview](operations-066.md#op-0e351f74fa746c), [use studio renderer](operations-066.md#op-a8d03378d514e1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2011) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1987)

<a id="op-a8d03378d514e1"></a>
### Studio App Renderer.use studio renderer

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_use_studio_renderer`

**Inputs** self.

**Local steps**

- Set self.context.template from “templates/generators/studio\_renderer.html”.
- Set self.context.assets from get\_editor\_assets(“renderer.html”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2012) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1988)

<a id="op-0e351f74fa746c"></a>
### Studio App Renderer.is preview

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapprenderer_is_preview`

**Inputs** self.

**Explicit results** self.path.startswith(“dev/”).

**Local steps**

- Return self.path.startswith(“dev/”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2009) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1985)

<a id="op-c30514f7d7be32"></a>
### Get desktop apps

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_get_desktop_apps`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract).distinct().orderby(StudioApp.app\_title).run(as\_dict = true).

**Local steps**

- Set StudioApp from Platform.qb.DocType(“Studio App”).
- Set StudioPage from Platform.qb.DocType(“Studio Page”).
- Return nested operand in the contract(nested operand in the contract).distinct().orderby(StudioApp.app\_title).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1937)

<a id="op-f160a639b98f91"></a>
### Studio App.get context

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_context`

**Inputs** self, context.

**Record and data access** read “Studio Page” via get\_all.

**State and service calls** commit.

**Local steps**

- Bind dependencies check\_app\_permission.
- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Evaluate Platform.db.commit().
- Set context.csrf\_token from csrf\_token.
- Set context.no\_cache from 1.
- Set context.site\_name from Platform.local.site.
- Set context.app\_name from self.app\_name.
- Set context.app\_route from self.route.
- Set context.app\_title from self.app\_title.
- Set context.app\_home from self.app\_home.
- Set context.favicon from self.favicon.
- Set context.Platform\_app from (self.Platform\_app or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.Platform\_app → empty text.
- Set context.is\_guest from Platform.session.user equals “Guest”.
- Set page\_filters from dict(studio\_app = self.name, published = 1).
- If context.is\_guest.
  - Set page\_filters at “allow\_guest” from 1.
- Set context.app\_pages from Platform.get\_all(“Studio Page”, page\_filters, list(“name”, “page\_title”, “route”)).
- Set context.is\_developer\_mode from Platform.utils.cint(Platform.conf.developer\_mode).
- Set context.can\_edit\_app from bool(((context.is\_developer\_mode or not self.is\_standard) and check\_app\_permission())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (context.is\_developer\_mode or not self.is\_standard) → check\_app\_permission().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.is\_developer\_mode → not self.is\_standard.
- Set context.is\_db\_app from not self.is\_standard.
- Set context.router\_file from self.get\_router\_file() when context.is\_developer\_mode, otherwise no value.
  - Value choice on context.is\_developer\_mode — true gives self.get\_router\_file(), false gives no value.
- Set context.base\_url from Platform.utils.get\_url(self.route).
- Set context.boot from self.get\_boot().
- Set context.vite\_dev\_server\_host from get\_vite\_dev\_server\_host().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get router file](operations-066.md#op-cee96475582929), [get boot](operations-066.md#op-bdddd6f9b0eee8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1987) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1963)

<a id="op-cee96475582929"></a>
### Studio App.get router file

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_router_file`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** no value · get\_router\_file(self.Platform\_app, self.name).

**Local steps**

- If not (self.is\_standard and self.Platform\_app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → self.Platform\_app.
  - Return no value.
- Bind dependencies get\_router\_file.
- Return get\_router\_file(self.Platform\_app, self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1990) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1966)

<a id="op-bdddd6f9b0eee8"></a>
### Studio App.get boot

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_boot`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping() · (Platform.get\_attr(handlers at negative 1)() or mapping()).

**Local steps**

- Set handlers from (Platform.get\_hooks(“studio\_app\_boot”, mapping()).get(self.name) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“studio\_app\_boot”, mapping()).get(self.name) → list().
- If not handlers.
  - Return mapping().
- Attempt the following.
  - Return (Platform.get\_attr(handlers at negative 1)() or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(handlers at negative 1)() → mapping().
- On failure (Exception).
  - Evaluate Platform.log\_error(title = formatted text studio\_app\_boot failed for {self.name}).
  - Return mapping().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“studio\_app\_boot”, mapping()), Platform.get\_attr(handlers at negative 1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1961)

<a id="op-71fc0e25fe0039"></a>
### Studio App.autoname

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_autoname`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.name.
  - Return no value.
- Set self.name from (self.app\_name or self.scrub(self.app\_title)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.app\_name → self.scrub(self.app\_title).
- Evaluate validate\_app\_name(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1944)

<a id="op-d23d6d0fa8fccd"></a>
### Studio App.folder name

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_folder_name`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** get\_export\_folder\_name(self.name) when self.name, otherwise empty text.

**Local steps**

- Return get\_export\_folder\_name(self.name) when self.name, otherwise empty text.
  - Value choice on self.name — true gives get\_export\_folder\_name(self.name), false gives empty text.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1958)

<a id="op-ff159834980958"></a>
### Studio App.is published

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_is_published`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Studio Page” via exists.

**Explicit results** Platform.db.exists(“Studio Page”, dict(studio\_app = self.name, published = 1)).

**Local steps**

- Return Platform.db.exists(“Studio Page”, dict(studio\_app = self.name, published = 1)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1967)

<a id="op-7d525d1d3d1070"></a>
### Studio App.is website published

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_is_website_published`

**Inputs** self.

**Explicit results** bool(self.is\_published).

**Local steps**

- Return bool(self.is\_published).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1968)

<a id="op-afd2a79753c28c"></a>
### Studio App.pages

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_pages`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.name), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.name), pluck = “name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1996) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1972)

<a id="op-3690a75197637b"></a>
### Studio App.components

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_components`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Studio Component” via get\_all.

**Explicit results** Platform.get\_all(“Studio Component”, filters = mapping(“studio\_app” → self.name), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Studio Component”, filters = mapping(“studio\_app” → self.name), pluck = “name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1949)

<a id="op-349e6c712bdd6c"></a>
### Studio App.standard pages

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_standard_pages`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.name, “is\_standard” → 1), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.name, “is\_standard” → 1), pluck = “name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1976)

<a id="op-34b4b781326c04"></a>
### Studio App.before insert

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_before_insert`

**Inputs** self.

**Local steps**

- If not self.app\_title.
  - Set self.app\_title from “My App”.
- If not self.route.
  - If not self.name.
    - Evaluate self.autoname().
  - Set self.route from self.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [autoname](operations-066.md#op-71fc0e25fe0039).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1945)

<a id="op-3d482d7325f901"></a>
### Studio App.validate

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_standard\_app\_change(self).
- Evaluate validate\_Platform\_app(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1978)

<a id="op-9e426f86d51e53"></a>
### Studio App.on update

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.export\_app().
- If (not self.flags.in\_insert and self.has\_value\_changed(“is\_standard”) and not self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.in\_insert → self.has\_value\_changed(“is\_standard”) → not self.is\_standard.
  - Evaluate self.delete\_app\_folder().
- Evaluate publish\_doc\_change(“Studio App”, self.name, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [export app](operations-067.md#op-5ca56915cdf791), [delete app folder](operations-066.md#op-c09e49ef35a313).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1995) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1971)

<a id="op-779521cdd5cc49"></a>
### Studio App.on trash

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_on_trash`

**Inputs** self.

**Record and data access** resolve a document from “Studio Component” via get\_doc.

**State and service calls** request delete\_doc for “Studio Page” · request delete on “Studio App File”.

**Local steps**

- Evaluate validate\_standard\_app\_change(self).
- For each page in self.pages.
  - Evaluate Platform.delete\_doc(“Studio Page”, page, force = true).
- Evaluate Platform.db.delete(“Studio App File”, mapping(“studio\_app” → self.name)).
- For each component in self.components.
  - Set doc from Platform.get\_doc(“Studio Component”, component).
  - Set doc.flags.is\_app\_deleted from true.
  - Evaluate doc.delete(force = true).
- Evaluate self.delete\_app\_build().
- If can\_export(self).
  - Evaluate self.delete\_app\_folder().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete app build](operations-067.md#op-92327e4f5188ea), [delete app folder](operations-066.md#op-c09e49ef35a313).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1994) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1970)

<a id="op-c09e49ef35a313"></a>
### Studio App.delete app folder

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_delete_app_folder`

**Inputs** self.

**Local steps**

- Set path from self.get\_folder\_path().
- Evaluate delete\_folder(path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1952)
