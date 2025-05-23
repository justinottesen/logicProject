from flask import Flask, request, jsonify
from flask_cors import CORS
from proof_helper.logic.rule_registry import RuleRegistry
from proof_helper.io.deserialize import build_proof
from proof_helper.io.serialize import dump_proof, dump_formula
from proof_helper.logic.verify import verify_proof, VerificationError
from proof_helper.logic.step_suggestions import generate_next_steps
from proof_helper.io.rule_storage import CustomRuleStore
from typing import Optional
import argparse
import traceback
import json

class ProofApp(Flask):
    def __init__(self, import_name: str, rules_dir: Optional[str] = None):
        super().__init__(import_name)
        self.custom_rule_store = CustomRuleStore(rules_dir) if rules_dir else None
        self.rule_registry = RuleRegistry(custom_rule_store=self.custom_rule_store)

def register_routes(app: ProofApp):
    @app.route('/verify_proof', methods=['POST'])
    def verify_proof_api():
        try:
            data = json.loads(request.data.decode())
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
        
    @app.route('/rules', methods=['POST'])
    def add_custom_rule_api():
        try:
            data = json.loads(request.data.decode())
            name = data.get("name")
            raw_proof = data.get("proof")
            proof = build_proof(raw_proof)
            rule_checker = app.rule_registry

            result = verify_proof(proof, rule_checker)
            if result is not True:
                assert isinstance(result, VerificationError)
                return jsonify({
                    "step_id": result.step_id,
                    "message": result.message
                }), 400

            # Save the raw JSON
            app.custom_rule_store.save_rule(name, raw_proof)

            # Add rule to registry
            app.rule_registry.add_custom_rule(name, proof)

            return "", 200

        except Exception as e:
            return jsonify({
                "step_id": None,
                "message": str(e),
                "trace": traceback.format_exc()
            }), 400
        
    @app.route('/rules', methods=['GET'])
    def list_rules_api():
        try:
            builtin = sorted(app.rule_registry.get_builtin_rules().keys())
            custom = sorted(app.rule_registry.get_custom_rules().keys())
            return jsonify({
                "builtin": builtin,
                "custom": custom
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e),
                "trace": traceback.format_exc()
            }), 500
        
    @app.route('/suggest_rules', methods=['POST'])
    def suggest_rules_api():
        try:
            data = json.loads(request.data.decode())
            raw_proof = data.get("proof")
            max_suggestions = data.get("max", 5)

            if not isinstance(max_suggestions, int) or max_suggestions <= 0:
                return jsonify({
                    "step_id": None,
                    "message": "'max' must be a positive integer"
                }), 400

            proof = build_proof(raw_proof)
            registry = app.rule_registry
            suggestions = generate_next_steps(proof, registry)

            # Build response: only include top N
            top = sorted(suggestions, key=lambda s: -s[1])[:max_suggestions]
            formatted = [{
                "formula": dump_formula(s.formula),
                "str_formula": str(s.formula),
                "rule": s.rule,
                "premises": [str(p) for p in s.premises],
                "score": score
            } for s, score in top]

            return jsonify(formatted)

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
    parser.add_argument('--rules-dir', type=str, default="custom_rules", help='Directory to load/save custom rules')
    args = parser.parse_args()

    app = ProofApp(__name__, rules_dir=args.rules_dir)
    CORS(app)
    register_routes(app)
    print(f"Running with custom rule directory as {app.custom_rule_store.get_path()}")
    app.run(debug=args.debug, port=args.port)
