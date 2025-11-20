#!/usr/bin/env python3
"""
Add claim to mockData.ts
Appends a new claim to the mockClaims array in mockData.ts
"""

import json
import sys
import re
from pathlib import Path


def add_claim_to_mockdata(claim_data: dict, mockdata_path: str):
    """
    Add a claim to mockData.ts
    
    Args:
        claim_data: Claim in frontend format
        mockdata_path: Path to mockData.ts file
    """
    # Read current mockData.ts
    with open(mockdata_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the mockClaims array
    # Look for: export const mockClaims: Claim[] = [
    pattern = r'(export const mockClaims: Claim\[\] = \[)(.*?)(\n\])'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Error: Could not find mockClaims array in mockData.ts")
        return False
    
    # Convert claim to TypeScript object string
    claim_str = json.dumps(claim_data, indent=8, ensure_ascii=False)
    
    # Replace JSON syntax with TypeScript
    claim_str = claim_str.replace('"type":', 'type:')
    claim_str = claim_str.replace('"flag_name":', 'flag_name:')
    claim_str = claim_str.replace('"score":', 'score:')
    claim_str = claim_str.replace('"message":', 'message:')
    claim_str = claim_str.replace('"patient":', 'patient:')
    claim_str = claim_str.replace('"faskes":', 'faskes:')
    claim_str = claim_str.replace('"ai":', 'ai:')
    claim_str = claim_str.replace('"total":', 'total:')
    
    # Add comma to existing last item if needed
    existing_claims = match.group(2).strip()
    if existing_claims and not existing_claims.endswith(','):
        existing_claims += ','
    
    # Build new content
    new_claims = f"{existing_claims}\n    {claim_str},"
    new_content = content[:match.start(2)] + new_claims + content[match.end(2):]
    
    # Write back
    with open(mockdata_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Added claim {claim_data['id']} to mockData.ts")
    return True


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python add_to_mockdata.py <frontend_claim.json>")
        sys.exit(1)
    
    claim_file = sys.argv[1]
    
    # Read claim
    with open(claim_file, 'r', encoding='utf-8') as f:
        claim_data = json.load(f)
    
    # Path to mockData.ts
    backend_dir = Path(__file__).parent.parent
    mockdata_path = backend_dir.parent.parent / "app" / "data" / "mockData.ts"
    
    if not mockdata_path.exists():
        print(f"Error: mockData.ts not found at {mockdata_path}")
        sys.exit(1)
    
    # Add claim
    success = add_claim_to_mockdata(claim_data, str(mockdata_path))
    
    if success:
        print("\n✓ Claim successfully added to mockData.ts")
        print("  The UI should auto-reload with the new claim")
    else:
        print("\n✗ Failed to add claim")
        sys.exit(1)


if __name__ == '__main__':
    main()
