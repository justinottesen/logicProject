(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push([typeof document === "object" ? document.currentScript : undefined, {

"[project]/app/lib/parser/tokenizer.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "tokenize": (()=>tokenize)
});
function tokenize(input) {
    const tokens = [];
    const regex = /\s*([A-Za-z_][A-Za-z0-9_]*|[¬∧∨→↔∃∀(),])/g;
    let match;
    while((match = regex.exec(input)) !== null){
        const token = match[1].trim();
        if (!token) continue;
        if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(token)) {
            tokens.push({
                type: "identifier",
                value: token
            });
        } else {
            tokens.push({
                type: "symbol",
                value: token
            });
        }
    }
    tokens.push({
        type: "eof"
    });
    return tokens;
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/lib/parser/parser.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
// app/lib/parser/parser.ts
__turbopack_context__.s({
    "Parser": (()=>Parser)
});
class Parser {
    tokens;
    pos = 0;
    constructor(tokens){
        this.tokens = tokens;
    }
    current() {
        return this.tokens[this.pos];
    }
    advance() {
        this.pos++;
    }
    matchSymbol(sym) {
        const token = this.current();
        if (token.type === "symbol" && token.value === sym) {
            this.advance();
            return true;
        }
        return false;
    }
    expectSymbol(sym) {
        if (!this.matchSymbol(sym)) {
            throw new Error(`Expected symbol '${sym}', got '${this.current().type === "symbol" ? this.current().value : this.current().type}'`);
        }
    }
    expectEOF() {
        if (this.current().type !== "eof") {
            throw new Error("Unexpected input after formula");
        }
    }
    parseFormula() {
        return this.parseIff();
    }
    // === Operator precedence ===
    parseIff() {
        let left = this.parseImplies();
        while(this.matchSymbol("↔")){
            const right = this.parseImplies();
            left = {
                type: "iff",
                left,
                right
            };
        }
        return left;
    }
    parseImplies() {
        let left = this.parseOr();
        while(this.matchSymbol("→")){
            const right = this.parseOr();
            left = {
                type: "implies",
                left,
                right
            };
        }
        return left;
    }
    parseOr() {
        let left = this.parseAnd();
        while(this.matchSymbol("∨")){
            const right = this.parseAnd();
            left = {
                type: "or",
                left,
                right
            };
        }
        return left;
    }
    parseAnd() {
        let left = this.parseUnary();
        while(this.matchSymbol("∧")){
            const right = this.parseUnary();
            left = {
                type: "and",
                left,
                right
            };
        }
        return left;
    }
    parseUnary() {
        if (this.matchSymbol("¬")) {
            const operand = this.parseUnary();
            return {
                type: "not",
                operand
            };
        }
        return this.parseQuantifier();
    }
    parsePrimary() {
        const token = this.current();
        if (token.type === "symbol" && token.value === "(") {
            this.advance();
            const inner = this.parseFormula();
            this.expectSymbol(")");
            return inner;
        }
        if (token.type === "identifier") {
            return this.parsePredicate();
        }
        throw new Error(`Unexpected token: ${JSON.stringify(token)}`);
    }
    parsePredicate() {
        const nameToken = this.current();
        if (nameToken.type !== "identifier") {
            throw new Error("Expected predicate name");
        }
        const name = nameToken.value;
        this.advance();
        const args = [];
        if (this.matchSymbol("(")) {
            if (!this.matchSymbol(")")) {
                do {
                    const argToken = this.current();
                    if (argToken.type !== "identifier") {
                        throw new Error("Expected term identifier");
                    }
                    const argName = argToken.value;
                    this.advance();
                    const isVariable = /^[a-z]$/.test(argName);
                    const term = isVariable ? {
                        type: "variable",
                        name: argName
                    } : {
                        type: "constant",
                        name: argName
                    };
                    args.push(term);
                }while (this.matchSymbol(","))
                this.expectSymbol(")");
            }
        }
        return {
            type: "predicate",
            name,
            args
        };
    }
    parseQuantifier() {
        const token = this.current();
        let quantifierType = null;
        if (token.type === "symbol" && token.value === "∀") {
            quantifierType = "forall";
        } else if (token.type === "symbol" && token.value === "∃") {
            quantifierType = "exists";
        }
        if (!quantifierType) {
            return this.parsePrimary(); // defer to next rule
        }
        this.advance(); // consume ∀ or ∃
        const varToken = this.current();
        if (varToken.type !== "identifier" || !/^[a-z]$/.test(varToken.value)) {
            throw new Error(`Expected variable name after '${token.value}'`);
        }
        this.advance(); // consume variable name
        const body = this.parseFormula(); // not parseUnary — we allow full formulas here
        return {
            type: quantifierType,
            variable: {
                type: "variable",
                name: varToken.value
            },
            body: body
        };
    }
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/lib/parser/index.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "parseFormulaInput": (()=>parseFormulaInput)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$tokenizer$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/parser/tokenizer.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$parser$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/parser/parser.ts [app-client] (ecmascript)");
;
;
function parseFormulaInput(raw) {
    if (raw.trim() === "") {
        return {
            status: "empty"
        };
    }
    try {
        const formula = parseFormula(raw);
        return {
            status: "ok",
            formula
        };
    } catch (err) {
        return {
            status: "error",
            error: getErrorMessage(err)
        };
    }
}
function parseFormula(input) {
    const tokens = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$tokenizer$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["tokenize"])(input);
    const parser = new __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$parser$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Parser"](tokens);
    const formula = parser.parseFormula();
    parser.expectEOF();
    return formula;
}
function getErrorMessage(err) {
    if (err instanceof Error) return err.message;
    return String(err);
}
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/lib/logic/rules/index.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "rules": (()=>rules)
});
const rules = [
    "∧Elim",
    "∨Elim",
    "¬Elim",
    "⊥Elim",
    "→Elim",
    "↔Elim",
    "∀Elim",
    "∃Elim",
    "∧Intro",
    "∨Intro",
    "¬Intro",
    "⊥Intro",
    "→Intro",
    "↔Intro",
    "∀Intro",
    "∃Intro",
    "P-Ind",
    "S-Ind"
];
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/components/StatementEditor.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>StatementEditor)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/parser/index.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$logic$2f$rules$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/logic/rules/index.ts [app-client] (ecmascript)");
;
;
;
function StatementEditor({ statement, onChange, deleteStatement }) {
    const handleChange = (raw)=>{
        const result = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(raw);
        onChange({
            ...statement,
            raw,
            result
        });
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-row w-full h-full",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "h-full p-1 text-lg",
                children: statement.number
            }, void 0, false, {
                fileName: "[project]/app/components/StatementEditor.tsx",
                lineNumber: 23,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                value: statement.raw,
                onChange: (e)=>handleChange(e.target.value),
                className: "border px-2 py-1 rounded w-full",
                placeholder: "Statement"
            }, void 0, false, {
                fileName: "[project]/app/components/StatementEditor.tsx",
                lineNumber: 24,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                value: statement.rule,
                onChange: (e)=>onChange({
                        ...statement,
                        rule: e.target.value
                    }),
                className: "border px-2 py-1 rounded ml-2",
                children: __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$logic$2f$rules$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["rules"].map((rule)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                        value: rule,
                        children: rule
                    }, "statment-rule-" + rule, false, {
                        fileName: "[project]/app/components/StatementEditor.tsx",
                        lineNumber: 36,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/app/components/StatementEditor.tsx",
                lineNumber: 30,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                className: "ml-2 border px-2 py-1 rounded bg-base hover-bg-dark-base text-white",
                onClick: deleteStatement,
                children: "Delete"
            }, void 0, false, {
                fileName: "[project]/app/components/StatementEditor.tsx",
                lineNumber: 41,
                columnNumber: 7
            }, this),
            statement.result.status === "error" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "text-red-600 text-sm mt-1",
                children: statement.result.error
            }, void 0, false, {
                fileName: "[project]/app/components/StatementEditor.tsx",
                lineNumber: 49,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/components/StatementEditor.tsx",
        lineNumber: 22,
        columnNumber: 5
    }, this);
}
_c = StatementEditor;
var _c;
__turbopack_context__.k.register(_c, "StatementEditor");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/components/SubproofEditor.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>SubproofEditor)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/parser/index.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$StepEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/components/StepEditor.tsx [app-client] (ecmascript)");
"use client";
;
;
;
function SubproofEditor({ subproof, onChange, deleteSubproof }) {
    const updateStepAt = (index, updated)=>{
        const newSteps = [
            ...subproof.steps
        ];
        newSteps[index] = updated;
        onChange({
            ...subproof,
            steps: newSteps
        });
    };
    const addStep = ()=>{
        onChange({
            ...subproof,
            steps: [
                ...subproof.steps,
                {
                    type: "line",
                    raw: "",
                    result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(""),
                    rule: "∧Elim",
                    parents: [],
                    number: subproof.steps.length + 1
                }
            ]
        });
    };
    const addSubproof = ()=>{
        onChange({
            ...subproof,
            steps: [
                ...subproof.steps,
                {
                    type: "subproof",
                    premise: {
                        type: "line",
                        raw: "",
                        result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(""),
                        rule: "none",
                        parents: [],
                        number: subproof.steps.length + 1
                    },
                    steps: [],
                    constants: [],
                    number: subproof.steps.length + 1
                }
            ]
        });
    };
    const onChangePremise = (text)=>{
        const updatedPremise = {
            ...subproof.premise,
            raw: text,
            result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(text)
        };
        onChange({
            ...subproof,
            premise: updatedPremise
        });
    };
    const deleteStep = (index)=>{
        const newSteps = [
            ...subproof.steps
        ];
        newSteps.splice(index, 1);
        onChange({
            ...subproof,
            steps: newSteps
        });
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-col gap-2 pl-4 sub relative",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex flex-row w-full h-full mb-2",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "h-full p-1 text-lg",
                        children: subproof.number
                    }, void 0, false, {
                        fileName: "[project]/app/components/SubproofEditor.tsx",
                        lineNumber: 84,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        type: "text",
                        value: subproof.premise.raw,
                        onChange: (e)=>onChangePremise(e.target.value),
                        className: "px-2 py-1 rounded w-full sub-premise",
                        placeholder: "Subproof Premise"
                    }, void 0, false, {
                        fileName: "[project]/app/components/SubproofEditor.tsx",
                        lineNumber: 85,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        className: "ml-2 border px-2 py-1 rounded bg-base hover-bg-dark-base text-white",
                        onClick: deleteSubproof,
                        children: "Delete"
                    }, void 0, false, {
                        fileName: "[project]/app/components/SubproofEditor.tsx",
                        lineNumber: 92,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/components/SubproofEditor.tsx",
                lineNumber: 83,
                columnNumber: 7
            }, this),
            subproof.steps.map((step, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$StepEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                    step: step,
                    updateStep: (updated)=>updateStepAt(i, updated),
                    deleteStep: ()=>deleteStep(i)
                }, "step-" + i, false, {
                    fileName: "[project]/app/components/SubproofEditor.tsx",
                    lineNumber: 100,
                    columnNumber: 9
                }, this)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex gap-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: addStep,
                        className: "mt-2 text-sm text-blue-600",
                        children: "+ Add Step"
                    }, void 0, false, {
                        fileName: "[project]/app/components/SubproofEditor.tsx",
                        lineNumber: 108,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: addSubproof,
                        className: "mt-2 text-sm text-blue-600",
                        children: "+ Add Subproof"
                    }, void 0, false, {
                        fileName: "[project]/app/components/SubproofEditor.tsx",
                        lineNumber: 111,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/components/SubproofEditor.tsx",
                lineNumber: 107,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/components/SubproofEditor.tsx",
        lineNumber: 82,
        columnNumber: 5
    }, this);
}
_c = SubproofEditor;
var _c;
__turbopack_context__.k.register(_c, "SubproofEditor");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/components/StepEditor.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>StepEditor)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$StatementEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/components/StatementEditor.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$SubproofEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/components/SubproofEditor.tsx [app-client] (ecmascript)");
;
;
;
function StepEditor({ step, updateStep, deleteStep }) {
    if (step.type === "line") {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$StatementEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
            statement: step,
            onChange: (updated)=>updateStep(updated),
            deleteStatement: deleteStep
        }, void 0, false, {
            fileName: "[project]/app/components/StepEditor.tsx",
            lineNumber: 14,
            columnNumber: 7
        }, this);
    } else {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$SubproofEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
            subproof: step,
            onChange: updateStep,
            deleteSubproof: deleteStep
        }, void 0, false, {
            fileName: "[project]/app/components/StepEditor.tsx",
            lineNumber: 22,
            columnNumber: 7
        }, this);
    }
}
_c = StepEditor;
var _c;
__turbopack_context__.k.register(_c, "StepEditor");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/lib/logic/substitutions.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
// Define mappings from shortcuts to symbols
__turbopack_context__.s({
    "replaceSubstitutions": (()=>replaceSubstitutions)
});
const shortcuts = {
    '~': '¬',
    '@': '∀',
    '#': '≠',
    '$': '→',
    '%': '↔',
    '^': '⊥',
    '&': '∧',
    '_': '⊆',
    '|': '∨',
    '/': '∃'
};
// Build a regex pattern that escapes any special characters in keys
const pattern = Object.keys(shortcuts).map((k)=>k.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&')).join('|');
const regex = new RegExp(pattern, 'g');
const replaceSubstitutions = (text)=>{
    console.log(text);
    return text.replace(regex, (match)=>shortcuts[match]);
};
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/components/ProofEditor.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>ProofEditor)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$StepEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/components/StepEditor.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$logic$2f$substitutions$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/logic/substitutions.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/lib/parser/index.ts [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
;
;
function ProofEditor({ proof, setProof }) {
    _s();
    const updatePremise = (index, raw)=>{
        const newPremises = [
            ...proof.premises
        ];
        newPremises[index] = {
            type: "line",
            raw,
            result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(raw),
            rule: "none",
            parents: [],
            number: proof.premises[index].number
        };
        setProof({
            ...proof,
            premises: newPremises
        });
    };
    const addPremise = ()=>{
        setProof({
            ...proof,
            premises: [
                ...proof.premises,
                {
                    type: "line",
                    raw: "",
                    result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(""),
                    rule: "none",
                    parents: [],
                    number: proof.premises.length + 1
                }
            ]
        });
    };
    const updateStepAt = (index, updated)=>{
        const newSteps = [
            ...proof.steps
        ];
        newSteps[index] = updated;
        setProof({
            ...proof,
            steps: newSteps
        });
    };
    const addStep = ()=>{
        setProof({
            ...proof,
            steps: [
                ...proof.steps,
                {
                    type: "line",
                    raw: "",
                    result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(""),
                    rule: "∧Elim",
                    parents: [],
                    number: proof.steps.length + 1
                }
            ]
        });
    };
    const addSubproof = ()=>{
        setProof({
            ...proof,
            steps: [
                ...proof.steps,
                {
                    type: "subproof",
                    premise: {
                        type: "line",
                        raw: "",
                        result: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$parser$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["parseFormulaInput"])(""),
                        rule: "none",
                        parents: [],
                        number: proof.steps.length + 1
                    },
                    steps: [],
                    constants: [],
                    number: proof.steps.length + 1
                }
            ]
        });
    };
    const deleteStep = (index)=>{
        const newSteps = [
            ...proof.steps
        ];
        newSteps.splice(index, 1);
        setProof({
            ...proof,
            steps: newSteps
        });
    };
    // add the substutions to the proof
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ProofEditor.useEffect": ()=>{
            let changed = false;
            const oldPremises = proof.premises;
            for (const premise of oldPremises){
                const oldRaw = premise.raw;
                premise.raw = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$logic$2f$substitutions$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["replaceSubstitutions"])(premise.raw);
                if (oldRaw !== premise.raw) {
                    changed = true;
                }
            }
            const oldSteps = proof.steps;
            for (const step of oldSteps){
                if (step.type === "line") {
                    const oldRaw = step.raw;
                    step.raw = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$lib$2f$logic$2f$substitutions$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["replaceSubstitutions"])(step.raw);
                    if (oldRaw !== step.raw) {
                        changed = true;
                    }
                }
            }
            if (changed) {
                setProof({
                    ...proof
                });
            }
        }
    }["ProofEditor.useEffect"], [
        proof,
        setProof
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-col gap-6",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                        className: "font-semibold mb-2",
                        children: "Premises"
                    }, void 0, false, {
                        fileName: "[project]/app/components/ProofEditor.tsx",
                        lineNumber: 129,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex flex-col gap-2",
                        children: [
                            proof.premises.map((p, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                    value: p.raw,
                                    onChange: (e)=>updatePremise(i, e.target.value),
                                    className: "border px-2 py-1 rounded w-full",
                                    placeholder: `Premise ${i + 1}`
                                }, i, false, {
                                    fileName: "[project]/app/components/ProofEditor.tsx",
                                    lineNumber: 132,
                                    columnNumber: 13
                                }, this)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: addPremise,
                                className: "mt-2 text-sm text-blue-600",
                                children: "+ Add Premise"
                            }, void 0, false, {
                                fileName: "[project]/app/components/ProofEditor.tsx",
                                lineNumber: 140,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/components/ProofEditor.tsx",
                        lineNumber: 130,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/components/ProofEditor.tsx",
                lineNumber: 128,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h3", {
                        className: "font-semibold mb-2",
                        children: "Steps"
                    }, void 0, false, {
                        fileName: "[project]/app/components/ProofEditor.tsx",
                        lineNumber: 147,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex flex-col gap-2",
                        children: [
                            proof.steps.map((step, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$StepEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                    step: step,
                                    updateStep: (updated)=>updateStepAt(i, updated),
                                    deleteStep: ()=>deleteStep(i)
                                }, i, false, {
                                    fileName: "[project]/app/components/ProofEditor.tsx",
                                    lineNumber: 150,
                                    columnNumber: 13
                                }, this)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex gap-4 mt-2",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: addStep,
                                        className: "mt-2 text-sm text-blue-600",
                                        children: "+ Add Step"
                                    }, void 0, false, {
                                        fileName: "[project]/app/components/ProofEditor.tsx",
                                        lineNumber: 158,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: addSubproof,
                                        className: "mt-2 text-sm text-blue-600",
                                        children: "+ Add Subproof"
                                    }, void 0, false, {
                                        fileName: "[project]/app/components/ProofEditor.tsx",
                                        lineNumber: 161,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/app/components/ProofEditor.tsx",
                                lineNumber: 157,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/components/ProofEditor.tsx",
                        lineNumber: 148,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/components/ProofEditor.tsx",
                lineNumber: 146,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                children: "TODO: Add the goals & conclusion at the bottom. I put it in the proof type. See the other TODO that shows up when you click Add subproof."
            }, void 0, false, {
                fileName: "[project]/app/components/ProofEditor.tsx",
                lineNumber: 168,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/components/ProofEditor.tsx",
        lineNumber: 127,
        columnNumber: 5
    }, this);
}
_s(ProofEditor, "OD7bBpZva5O2jO+Puf00hKivP7c=");
_c = ProofEditor;
var _c;
__turbopack_context__.k.register(_c, "ProofEditor");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/app/page.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>Home)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$ProofEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/components/ProofEditor.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
function Home() {
    _s();
    const [proof, setProof] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])({
        type: "proof",
        premises: [],
        steps: [],
        goals: []
    });
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-col w-full min-h-screen",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
            className: "flex-1 border p-4 overflow-auto",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-xl font-bold mb-4",
                    children: "Proof"
                }, void 0, false, {
                    fileName: "[project]/app/page.tsx",
                    lineNumber: 18,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$components$2f$ProofEditor$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                    proof: proof,
                    setProof: setProof
                }, void 0, false, {
                    fileName: "[project]/app/page.tsx",
                    lineNumber: 19,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/page.tsx",
            lineNumber: 17,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/page.tsx",
        lineNumber: 16,
        columnNumber: 5
    }, this);
}
_s(Home, "w96tZEbHOrcmDZRIHhj2MxTBO+E=");
_c = Home;
var _c;
__turbopack_context__.k.register(_c, "Home");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/node_modules/next/dist/compiled/react/cjs/react-jsx-dev-runtime.development.js [app-client] (ecmascript)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
/**
 * @license React
 * react-jsx-dev-runtime.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */ var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
"use strict";
"production" !== ("TURBOPACK compile-time value", "development") && function() {
    function getComponentNameFromType(type) {
        if (null == type) return null;
        if ("function" === typeof type) return type.$$typeof === REACT_CLIENT_REFERENCE ? null : type.displayName || type.name || null;
        if ("string" === typeof type) return type;
        switch(type){
            case REACT_FRAGMENT_TYPE:
                return "Fragment";
            case REACT_PROFILER_TYPE:
                return "Profiler";
            case REACT_STRICT_MODE_TYPE:
                return "StrictMode";
            case REACT_SUSPENSE_TYPE:
                return "Suspense";
            case REACT_SUSPENSE_LIST_TYPE:
                return "SuspenseList";
            case REACT_ACTIVITY_TYPE:
                return "Activity";
        }
        if ("object" === typeof type) switch("number" === typeof type.tag && console.error("Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue."), type.$$typeof){
            case REACT_PORTAL_TYPE:
                return "Portal";
            case REACT_CONTEXT_TYPE:
                return (type.displayName || "Context") + ".Provider";
            case REACT_CONSUMER_TYPE:
                return (type._context.displayName || "Context") + ".Consumer";
            case REACT_FORWARD_REF_TYPE:
                var innerType = type.render;
                type = type.displayName;
                type || (type = innerType.displayName || innerType.name || "", type = "" !== type ? "ForwardRef(" + type + ")" : "ForwardRef");
                return type;
            case REACT_MEMO_TYPE:
                return innerType = type.displayName || null, null !== innerType ? innerType : getComponentNameFromType(type.type) || "Memo";
            case REACT_LAZY_TYPE:
                innerType = type._payload;
                type = type._init;
                try {
                    return getComponentNameFromType(type(innerType));
                } catch (x) {}
        }
        return null;
    }
    function testStringCoercion(value) {
        return "" + value;
    }
    function checkKeyStringCoercion(value) {
        try {
            testStringCoercion(value);
            var JSCompiler_inline_result = !1;
        } catch (e) {
            JSCompiler_inline_result = !0;
        }
        if (JSCompiler_inline_result) {
            JSCompiler_inline_result = console;
            var JSCompiler_temp_const = JSCompiler_inline_result.error;
            var JSCompiler_inline_result$jscomp$0 = "function" === typeof Symbol && Symbol.toStringTag && value[Symbol.toStringTag] || value.constructor.name || "Object";
            JSCompiler_temp_const.call(JSCompiler_inline_result, "The provided key is an unsupported type %s. This value must be coerced to a string before using it here.", JSCompiler_inline_result$jscomp$0);
            return testStringCoercion(value);
        }
    }
    function getTaskName(type) {
        if (type === REACT_FRAGMENT_TYPE) return "<>";
        if ("object" === typeof type && null !== type && type.$$typeof === REACT_LAZY_TYPE) return "<...>";
        try {
            var name = getComponentNameFromType(type);
            return name ? "<" + name + ">" : "<...>";
        } catch (x) {
            return "<...>";
        }
    }
    function getOwner() {
        var dispatcher = ReactSharedInternals.A;
        return null === dispatcher ? null : dispatcher.getOwner();
    }
    function UnknownOwner() {
        return Error("react-stack-top-frame");
    }
    function hasValidKey(config) {
        if (hasOwnProperty.call(config, "key")) {
            var getter = Object.getOwnPropertyDescriptor(config, "key").get;
            if (getter && getter.isReactWarning) return !1;
        }
        return void 0 !== config.key;
    }
    function defineKeyPropWarningGetter(props, displayName) {
        function warnAboutAccessingKey() {
            specialPropKeyWarningShown || (specialPropKeyWarningShown = !0, console.error("%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)", displayName));
        }
        warnAboutAccessingKey.isReactWarning = !0;
        Object.defineProperty(props, "key", {
            get: warnAboutAccessingKey,
            configurable: !0
        });
    }
    function elementRefGetterWithDeprecationWarning() {
        var componentName = getComponentNameFromType(this.type);
        didWarnAboutElementRef[componentName] || (didWarnAboutElementRef[componentName] = !0, console.error("Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release."));
        componentName = this.props.ref;
        return void 0 !== componentName ? componentName : null;
    }
    function ReactElement(type, key, self, source, owner, props, debugStack, debugTask) {
        self = props.ref;
        type = {
            $$typeof: REACT_ELEMENT_TYPE,
            type: type,
            key: key,
            props: props,
            _owner: owner
        };
        null !== (void 0 !== self ? self : null) ? Object.defineProperty(type, "ref", {
            enumerable: !1,
            get: elementRefGetterWithDeprecationWarning
        }) : Object.defineProperty(type, "ref", {
            enumerable: !1,
            value: null
        });
        type._store = {};
        Object.defineProperty(type._store, "validated", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: 0
        });
        Object.defineProperty(type, "_debugInfo", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: null
        });
        Object.defineProperty(type, "_debugStack", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: debugStack
        });
        Object.defineProperty(type, "_debugTask", {
            configurable: !1,
            enumerable: !1,
            writable: !0,
            value: debugTask
        });
        Object.freeze && (Object.freeze(type.props), Object.freeze(type));
        return type;
    }
    function jsxDEVImpl(type, config, maybeKey, isStaticChildren, source, self, debugStack, debugTask) {
        var children = config.children;
        if (void 0 !== children) if (isStaticChildren) if (isArrayImpl(children)) {
            for(isStaticChildren = 0; isStaticChildren < children.length; isStaticChildren++)validateChildKeys(children[isStaticChildren]);
            Object.freeze && Object.freeze(children);
        } else console.error("React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.");
        else validateChildKeys(children);
        if (hasOwnProperty.call(config, "key")) {
            children = getComponentNameFromType(type);
            var keys = Object.keys(config).filter(function(k) {
                return "key" !== k;
            });
            isStaticChildren = 0 < keys.length ? "{key: someKey, " + keys.join(": ..., ") + ": ...}" : "{key: someKey}";
            didWarnAboutKeySpread[children + isStaticChildren] || (keys = 0 < keys.length ? "{" + keys.join(": ..., ") + ": ...}" : "{}", console.error('A props object containing a "key" prop is being spread into JSX:\n  let props = %s;\n  <%s {...props} />\nReact keys must be passed directly to JSX without using spread:\n  let props = %s;\n  <%s key={someKey} {...props} />', isStaticChildren, children, keys, children), didWarnAboutKeySpread[children + isStaticChildren] = !0);
        }
        children = null;
        void 0 !== maybeKey && (checkKeyStringCoercion(maybeKey), children = "" + maybeKey);
        hasValidKey(config) && (checkKeyStringCoercion(config.key), children = "" + config.key);
        if ("key" in config) {
            maybeKey = {};
            for(var propName in config)"key" !== propName && (maybeKey[propName] = config[propName]);
        } else maybeKey = config;
        children && defineKeyPropWarningGetter(maybeKey, "function" === typeof type ? type.displayName || type.name || "Unknown" : type);
        return ReactElement(type, children, self, source, getOwner(), maybeKey, debugStack, debugTask);
    }
    function validateChildKeys(node) {
        "object" === typeof node && null !== node && node.$$typeof === REACT_ELEMENT_TYPE && node._store && (node._store.validated = 1);
    }
    var React = __turbopack_context__.r("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)"), REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_PORTAL_TYPE = Symbol.for("react.portal"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment"), REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode"), REACT_PROFILER_TYPE = Symbol.for("react.profiler");
    Symbol.for("react.provider");
    var REACT_CONSUMER_TYPE = Symbol.for("react.consumer"), REACT_CONTEXT_TYPE = Symbol.for("react.context"), REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref"), REACT_SUSPENSE_TYPE = Symbol.for("react.suspense"), REACT_SUSPENSE_LIST_TYPE = Symbol.for("react.suspense_list"), REACT_MEMO_TYPE = Symbol.for("react.memo"), REACT_LAZY_TYPE = Symbol.for("react.lazy"), REACT_ACTIVITY_TYPE = Symbol.for("react.activity"), REACT_CLIENT_REFERENCE = Symbol.for("react.client.reference"), ReactSharedInternals = React.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, hasOwnProperty = Object.prototype.hasOwnProperty, isArrayImpl = Array.isArray, createTask = console.createTask ? console.createTask : function() {
        return null;
    };
    React = {
        "react-stack-bottom-frame": function(callStackForError) {
            return callStackForError();
        }
    };
    var specialPropKeyWarningShown;
    var didWarnAboutElementRef = {};
    var unknownOwnerDebugStack = React["react-stack-bottom-frame"].bind(React, UnknownOwner)();
    var unknownOwnerDebugTask = createTask(getTaskName(UnknownOwner));
    var didWarnAboutKeySpread = {};
    exports.Fragment = REACT_FRAGMENT_TYPE;
    exports.jsxDEV = function(type, config, maybeKey, isStaticChildren, source, self) {
        var trackActualOwner = 1e4 > ReactSharedInternals.recentlyCreatedOwnerStacks++;
        return jsxDEVImpl(type, config, maybeKey, isStaticChildren, source, self, trackActualOwner ? Error("react-stack-top-frame") : unknownOwnerDebugStack, trackActualOwner ? createTask(getTaskName(type)) : unknownOwnerDebugTask);
    };
}();
}}),
"[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
'use strict';
if ("TURBOPACK compile-time falsy", 0) {
    "TURBOPACK unreachable";
} else {
    module.exports = __turbopack_context__.r("[project]/node_modules/next/dist/compiled/react/cjs/react-jsx-dev-runtime.development.js [app-client] (ecmascript)");
}
}}),
}]);

//# sourceMappingURL=_f4c4a4c7._.js.map