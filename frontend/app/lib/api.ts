export async function verifyProof(proof: object): Promise<{ valid: true } | { valid: false; step_id: string | null; message: string }> {
    const res = await fetch("http://localhost:5000/verify_proof", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      mode: "no-cors",
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
  