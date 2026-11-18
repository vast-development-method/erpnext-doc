// Read client declarations without running application or test code.
// Try an installed Acorn package first. Node's bundled parser is available offline.
const fs = require("node:fs");
const path = require("node:path");
const { stripTypeScriptTypes } = require("node:module");
let acorn;
try { acorn = require("acorn"); }
catch { acorn = require("internal/deps/acorn/acorn/dist/acorn"); }

const root = process.argv[2];
const files = JSON.parse(fs.readFileSync(0, "utf8"));
const results = [];

function pathName(node) {
    if (!node) return "";
    if (node.type === "Identifier") return node.name;
    if (node.type === "MemberExpression" && !node.computed) {
        return [pathName(node.object), node.property.name].filter(Boolean).join(".");
    }
    if (node.type === "CallExpression" || node.type === "TaggedTemplateExpression") {
        return pathName(node.callee || node.tag);
    }
    return "";
}

function directValue(node, source) {
    if (!node) return "";
    if (node.type === "Literal" && typeof node.value === "string") return node.value;
    if (node.type === "TemplateLiteral" && node.expressions.length === 0) return node.quasis[0].value.cooked;
    return source.slice(node.start, node.end).replace(/\s+/g, " ").slice(0, 220);
}

for (const file of files) {
    let source = fs.readFileSync(path.join(root, file.path), "utf8");
    if (file.path.endsWith(".ts")) source = stripTypeScriptTypes(source, {mode: "strip"});
    const syntax = acorn.parse(source, {ecmaVersion: "latest",sourceType:"module",allowReturnOutsideFunction:true,
                                       allowAwaitOutsideFunction:true,locations:true,allowHashBang:true});
    function emit(surface, node, detail) {
        results.push([surface,file.path,node.loc.start.line,detail]);
    }
    function visit(node) {
        if (!node || typeof node !== "object") return;
        if (Array.isArray(node)) { for (const child of node) visit(child); return; }
        if (node.type === "CallExpression") {
            const callee = pathName(node.callee);
            if (callee === "frappe.ui.form.on") {
                const [target, handlers] = node.arguments;
                const record = directValue(target,source);
                if (handlers?.type === "ObjectExpression") {
                    for (const prop of handlers.properties) {
                        emit("form-handlers",prop,{record,event:directValue(prop.key||prop.argument,source),
                             registration:prop.type==="SpreadElement"||prop.computed?"computed-key":"object-key"});
                    }
                } else {
                    emit("form-handlers",node,{record,event:directValue(handlers,source),
                         registration:handlers?.type==="Literal"?"named-event":"expression"});
                }
            }
            if (file.test && /^(?:(?:QUnit|Deno)\.test|(?:it|test|t\.test)(?:\.(?:only|skip|todo|each|concurrent|fails|failing|skipIf|runIf))*)$/.test(callee)) {
                // For curried/templated parameterized tests the outer call supplies the case title.
                const title=node.arguments[0];
                if (title && (title.type==="Literal" || title.type==="TemplateLiteral" ||
                             node.arguments[1]?.type?.includes("Function"))) {
                    emit("client-test-declarations",node,{callee,title:directValue(title,source),
                         dynamic:title.type!=="Literal" && !(title.type==="TemplateLiteral" && !title.expressions.length)});
                }
            }
        }
        if (node.type === "AssignmentExpression") {
            const left=pathName(node.left);
            if (/^(?:cur_frm|frm)\.cscript\./.test(left) &&
                ["FunctionExpression","ArrowFunctionExpression"].includes(node.right.type)) {
                emit("form-handlers",node,{record:"active form",event:left.split(".").at(-1),registration:"legacy-controller"});
            }
        }
        for (const [key,value] of Object.entries(node)) {
            if (!["loc","start","end"].includes(key) && value && typeof value==="object") visit(value);
        }
    }
    visit(syntax);
}
process.stdout.write(JSON.stringify(results));
