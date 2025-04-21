from flask import Flask, request, jsonify
from proof_helper.logic.rule_registry import RuleRegistry
from proof_helper.io.deserialize import build_proof
from proof_helper.logic.verify import verify_proof, VerificationError
import argparse
import traceback

class ProofApp(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name)
        self.rule_registry = RuleRegistry()

app = ProofApp(__name__)

@app.route('/verify/proof', methods=['POST'])
def verify_proof_api():
    try:
        data = request.get_json()
        proof = build_proof(data)
        rule_checker = app.rule_registry

        result = verify_proof(proof, rule_checker)

        if result is True:
            return "", 200
        else:
            assert isinstance(result, VerificationError)
            return jsonify({
                "step_id": result.step_id,
                "message": result.message
            }), 400

    except Exception as e:
        return jsonify({
            "step_id": None,
            "message": str(e),
            "trace": traceback.format_exc()
        }), 400

def main():
    parser = argparse.ArgumentParser(description="Proof Helper Flask Server")
    parser.add_argument('--debug', action='store_true', help='Run Flask in debug mode')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()

    app.run(debug=args.debug, port=args.port)