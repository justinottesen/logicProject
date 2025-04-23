import os
import json
from typing import Optional, Dict
from proof_helper.core.proof import Proof
from proof_helper.io.deserialize import build_proof

class CustomRuleStore:
    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
    
    def get_path(self):
        return os.path.abspath(self.directory)

    def save_rule(self, name: str, raw_json: dict) -> None:
        path = os.path.join(self.directory, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(raw_json, f, indent=2, ensure_ascii=False)

    def load_rule(self, name: str) -> Optional[Proof]:
        path = os.path.join(self.directory, f"{name}.json")
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        return build_proof(raw)

    def list_rules(self) -> Dict[str, Proof]:
        rules = {}
        for fname in os.listdir(self.directory):
            if not fname.endswith(".json"):
                continue
            name = fname[:-5]
            proof = self.load_rule(name)
            if proof is not None:
                rules[name] = proof
        return rules
