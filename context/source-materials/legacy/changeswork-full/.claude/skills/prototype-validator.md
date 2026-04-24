# Prototype Validator Skill

## Purpose
Automatically validate HTML/JSX prototypes after each modification to catch syntax errors before they reach the user.

## When to Use
- After ANY edit to `.html` files in `prototypes/` directory
- Before reporting success to the user
- When user reports "site not working" or syntax errors

## Validation Steps

### 1. Basic HTML Structure Check
```bash
python3 scripts/validate_prototype.py <file_path>
```

### 2. JSX Bracket Balance Check
Run this Python script to verify bracket balance:
```python
import re

def validate_jsx_balance(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    if not match:
        print("No Babel script found")
        return False

    jsx = match.group(1)

    # Count brackets
    open_braces = jsx.count('{')
    close_braces = jsx.count('}')
    open_parens = jsx.count('(')
    close_parens = jsx.count(')')
    open_brackets = jsx.count('[')
    close_brackets = jsx.count(']')

    print(f"Braces {{ }}: {open_braces} / {close_braces} (diff: {open_braces - close_braces})")
    print(f"Parens ( ): {open_parens} / {close_parens} (diff: {open_parens - close_parens})")
    print(f"Brackets [ ]: {open_brackets} / {close_brackets} (diff: {open_brackets - close_brackets})")

    balanced = (open_braces == close_braces and
                open_parens == close_parens and
                open_brackets == close_brackets)

    if balanced:
        print("✓ Bracket balance OK")
    else:
        print("✗ Bracket imbalance detected!")

    return balanced

validate_jsx_balance('prototypes/deployments.html')
```

### 3. Common Error Patterns to Check

#### A. Extra closing braces
Look for patterns like:
```javascript
};
};  // <-- Extra closing
```

#### B. Unclosed JSX fragments
Check that every `<>` has a matching `</>`

#### C. Mismatched conditionals
For patterns like `{condition && (` ensure there's a matching `)}`

#### D. Return statements outside functions
If you see `return (` preceded by `};`, there's likely an extra closing brace

### 4. Server Test
Start a test server and check for startup errors:
```bash
python3 -m http.server <port> --bind 127.0.0.1 &
```

## Auto-Fix Procedures

### Fix: Extra closing brace
**Pattern:** `};` followed by another `};` on the next line
**Fix:** Remove the extra `};`

### Fix: Unclosed Fragment
**Pattern:** `<>` without matching `</>`
**Fix:** Add `</>` before the closing `)}` of the condition

### Fix: Fragment closes before condition
**Pattern:**
```jsx
{condition && (
    <>
    ...
    </>
)}  // Wrong order
```
**Fix:**
```jsx
{condition && (
    <>
    ...
    </>
)}  // Correct: </> before )}
```

## Workflow After Each Edit

1. **Run validation:**
   ```bash
   python3 scripts/validate_prototype.py <file_path>
   ```

2. **Check bracket balance** (Python script above)

3. **If errors found:**
   - Read the file around the error location
   - Identify the issue (extra brace, unclosed tag, etc.)
   - Apply the appropriate fix
   - Re-run validation

4. **Only report success when:**
   - `validate_prototype.py` reports "Ошибок не найдено"
   - Bracket balance check passes
   - Server starts without errors

## Files to Monitor
- `prototypes/deployments.html`
- `prototypes/current.html`
- Any `.html` file with JSX/Babel

## Quick Fix Command
```bash
# Run validation and show last 15 lines
python3 scripts/validate_prototype.py prototypes/deployments.html 2>&1 | tail -15
```
