#!/usr/bin/env python3
"""
Modified generate_patient.py to automatically trigger main.py
"""

import subprocess
import sys
import os
from pathlib import Path

# Get the original generate_patient module
sys.path.insert(0, str(Path(__file__).parent))
from generate_patient_original import *  # Import everything from original


def generate_and_process(quality_level: int = 1):
    """
    Generate patient claim and automatically process it through main.py
    
    Args:
        quality_level: 1=good, 2=suspicious, 3=fraudulent
    """
    # Generate claim using original function
    claim_data, claim_file = generate_claim(quality_level)
    
    print(f"\n{'='*60}")
    print("AUTO-PROCESSING CLAIM THROUGH FRAUD DETECTION")
    print(f"{'='*60}\n")
    
    # Run main.py with the generated claim
    backend_dir = Path(__file__).parent.parent
    main_py = backend_dir / "main.py"
    
    result = subprocess.run(
        [sys.executable, str(main_py), claim_file],
        capture_output=True,
        text=True,
        cwd=str(backend_dir)
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    # Convert to frontend format
    converter_script = backend_dir / "utils" / "convert_to_frontend.py"
    claims_db = backend_dir / "data" / "claims.json"
    
    if claims_db.exists():
        # Get the last claim (just processed)
        import json
        with open(claims_db, 'r') as f:
            claims = json.load(f)
        
        if claims:
            last_claim = claims[-1]
            
            # Save to temp file for conversion
            temp_file = backend_dir / "data" / "temp_claim.json"
            with open(temp_file, 'w') as f:
                json.dump(last_claim, f, indent=2)
            
            # Convert
            subprocess.run([sys.executable, str(converter_script), str(temp_file)])
            
            # Read converted result
            frontend_file = str(temp_file).replace('.json', '_frontend.json')
            if Path(frontend_file).exists():
                with open(frontend_file, 'r') as f:
                    frontend_claim = json.load(f)
                
                print(f"\n{'='*60}")
                print("FRONTEND-READY FORMAT")
                print(f"{'='*60}")
                print(json.dumps(frontend_claim, indent=2, ensure_ascii=False))
                
                # TODO: Add to mockData.ts via API endpoint
                print(f"\n✓ Ready to add to mockData.ts")
    
    return claim_data, claim_file


if __name__ == "__main__":
    quality = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    generate_and_process(quality)
