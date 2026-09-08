import json
from pathlib import Path

def qualify(policy, packet):
    pairs = packet['pairs']
    admitted = [p for p in pairs if p['admitted']]
    correct = all(p['correctness_failures'] == 0 and p['regressions'] == 0 for p in admitted)
    complete = packet['complete'] and len(admitted) == len(pairs) and len(pairs) >= policy['minimum_pairs']
    faster = bool(admitted) and all(p['after_seconds'] < p['before_seconds'] for p in admitted)
    return {'admitted_pairs': len(admitted), 'measured_checks_passed': correct,
            'qualification': 'accepted' if complete and correct and faster else 'pending' if correct else 'rejected'}

if __name__ == '__main__':
    print(json.dumps(qualify(json.loads(Path('qualification.json').read_text()), json.loads(Path('packet.json').read_text()))))
