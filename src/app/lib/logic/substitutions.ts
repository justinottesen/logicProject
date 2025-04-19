// Define mappings from shortcuts to symbols
const shortcuts: { [key: string]: string } = {
    '~': '¬',      // Logical negation
    '@': '∀',      // Logical forAll
    '#': '≠',      // Logical not equals
    '$': '→',      // Logical implication
    '%': '↔',      // Logical biconditional
    '^': '⊥',      // Logical false
    '&': '∧',      // Logical AND
    '_': '⊆',      // Logical subset
    '|': '∨',       // Logical OR
    '/': '∃',      // Logical exists
}

// Build a regex pattern that escapes any special characters in keys
const pattern: string = Object.keys(shortcuts)
    .map(k => k.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&'))
    .join('|');
const regex = new RegExp(pattern, 'g');

export const replaceSubstitutions = (text: string) => {
    console.log(text);
    return text.replace(regex, (match) => shortcuts[match])
};