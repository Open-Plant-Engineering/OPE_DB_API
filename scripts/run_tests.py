from subprocess import run
import sys

tests = [
]

for test in tests:
    result = run([sys.executable, test])
    if result.returncode != 0:
        sys.exit(result.returncode)

print("✅ All tests passed")