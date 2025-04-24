export async function verifyProof(proof: object): Promise<{ valid: true } | { valid: false; step_id: string | null; message: string }> {
  const res = await fetch("http://localhost:5000/verify_proof", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(proof),
  });

  if (res.ok) {
    return { valid: true };
  } else {
    const error = await res.json();
    return {
      valid: false,
      step_id: error.step_id,
      message: error.message,
    };
  }
}

export async function getRules(): Promise<{
  builtins: string[];
  custom: string[];
}> {
  const res = await fetch("http://localhost:5000/rules", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (res.ok) {
    return res.json();
  } else {
    return { builtins: [], custom: [] };
  }
}

export async function addRule(proof: object, string: string): Promise<{ valid: true } | { valid: false; error: string }> {
  const body = JSON.stringify({ proof, name: string });
  const res = await fetch("http://localhost:5000/rules", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body
  });

  if (res.ok) {
    return { valid: true };
  } else {
    const error = await res.json();
    return {
      valid: false,
      error: error
    };
  }
}

export async function suggestRules(proof: object): Promise<string[]> {
  const res = await fetch("http://localhost:5000/suggest_rules", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({proof, max: 5}),
  });

  if (res.ok) {
    return res.json();
  } else {
    return []
  }
}
