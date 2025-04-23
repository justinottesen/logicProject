export type Token =
  | { type: "identifier"; value: string }
  | { type: "symbol"; value: string }
  | { type: "bottom"; value: string }
  | { type: "eof"; value?: undefined };

export function tokenize(input: string): Token[] {
  const tokens: Token[] = [];
  const regex = /\s*([A-Za-z_][A-Za-z0-9_]*|[¬∧∨→↔∃∀(),⊥])/g;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(input)) !== null) {
    const token = match[1].trim();
    if (!token) continue;

    if (/^[A-Za-z_][A-Za-z0-9_]*$/.test(token)) {
      tokens.push({ type: "identifier", value: token });
    } else if (token === "⊥") {
      tokens.push({ type: "bottom", value: "⊥" });
    }
    else {
      tokens.push({ type: "symbol", value: token });
    }
  }

  tokens.push({ type: "eof" });
  return tokens;
}
