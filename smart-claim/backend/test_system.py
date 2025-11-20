#!/usr/bin/env python3
"""
Test Script for Smart Claim BPJS System
Generates multiple claims and processes them through the fraud detection pipeline
"""

import os
import sys
import json
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_and_process_claims(num_good=5, num_medium=5, num_bad=5):
    """
    Generate and process multiple claims
    
    Args:
        num_good: Number of good claims to generate
        num_medium: Number of medium claims to generate
        num_bad: Number of bad claims to generate
    """
    print("="*60)
    print("SMART CLAIM BPJS - AUTOMATED TESTING")
    print("="*60)
    print(f"\nGenerating claims:")
    print(f"  - Good claims: {num_good}")
    print(f"  - Medium claims: {num_medium}")
    print(f"  - Bad claims: {num_bad}")
    print()
    
    generated_files = []
    
    # Generate good claims
    print("[1/3] Generating GOOD claims (score < 10)...")
    for i in range(num_good):
        result = subprocess.run(
            ['python', 'utils/generate_patient.py', '1'],
            capture_output=True,
            text=True
        )
        # Extract claim ID from output
        for line in result.stdout.split('\n'):
            if 'Saved to:' in line:
                filepath = line.split('Saved to:')[1].strip()
                generated_files.append(('good', filepath))
                print(f"  ✓ Generated: {os.path.basename(filepath)}")
    
    # Generate medium claims
    print(f"\n[2/3] Generating MEDIUM claims (score 10-60)...")
    for i in range(num_medium):
        result = subprocess.run(
            ['python', 'utils/generate_patient.py', '2'],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if 'Saved to:' in line:
                filepath = line.split('Saved to:')[1].strip()
                generated_files.append(('medium', filepath))
                print(f"  ✓ Generated: {os.path.basename(filepath)}")
    
    # Generate bad claims
    print(f"\n[3/3] Generating BAD claims (score > 60)...")
    for i in range(num_bad):
        result = subprocess.run(
            ['python', 'utils/generate_patient.py', '3'],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if 'Saved to:' in line:
                filepath = line.split('Saved to:')[1].strip()
                generated_files.append(('bad', filepath))
                print(f"  ✓ Generated: {os.path.basename(filepath)}")
    
    print(f"\n✓ Total claims generated: {len(generated_files)}")
    
    # Process all claims
    print("\n" + "="*60)
    print("PROCESSING CLAIMS THROUGH FRAUD DETECTION PIPELINE")
    print("="*60 + "\n")
    
    results = []
    for quality, filepath in generated_files:
        print(f"\nProcessing: {os.path.basename(filepath)} (expected: {quality})")
        print("-" * 60)
        
        result = subprocess.run(
            ['python', 'main.py', filepath],
            capture_output=True,
            text=True
        )
        
        # Extract JSON output
        output_lines = result.stdout.split('\n')
        json_started = False
        json_lines = []
        for line in output_lines:
            if line.strip() == 'JSON Output:':
                json_started = True
                continue
            if json_started:
                json_lines.append(line)
        
        if json_lines:
            try:
                claim_result = json.loads('\n'.join(json_lines))
                results.append({
                    'expected_quality': quality,
                    'result': claim_result
                })
                
                print(f"  Decision: {claim_result['decision']}")
                print(f"  Total Score: {claim_result['fraud_scores']['total']}")
                print(f"  Patient Score: {claim_result['fraud_scores']['patient']}")
                print(f"  Faskes Score: {claim_result['fraud_scores']['faskes']}")
                print(f"  AI Score: {claim_result['fraud_scores']['ai']}")
            except json.JSONDecodeError:
                print(f"  ✗ Failed to parse JSON output")
    
    # Summary
    print("\n" + "="*60)
    print("TESTING SUMMARY")
    print("="*60)
    
    decision_counts = {'ACCEPTED': 0, 'NEEDS_REVIEW': 0, 'REJECTED': 0}
    quality_accuracy = {'good': 0, 'medium': 0, 'bad': 0}
    
    for item in results:
        decision = item['result']['decision']
        quality = item['expected_quality']
        decision_counts[decision] += 1
        
        # Check if decision matches expected quality
        if quality == 'good' and decision == 'ACCEPTED':
            quality_accuracy['good'] += 1
        elif quality == 'medium' and decision == 'NEEDS_REVIEW':
            quality_accuracy['medium'] += 1
        elif quality == 'bad' and decision == 'REJECTED':
            quality_accuracy['bad'] += 1
    
    print(f"\nDecision Distribution:")
    print(f"  - Auto Accepted: {decision_counts['ACCEPTED']}")
    print(f"  - Needs Review: {decision_counts['NEEDS_REVIEW']}")
    print(f"  - Auto Rejected: {decision_counts['REJECTED']}")
    
    print(f"\nQuality Matching:")
    print(f"  - Good → Accepted: {quality_accuracy['good']}/{num_good} ({quality_accuracy['good']/num_good*100:.0f}%)")
    print(f"  - Medium → Review: {quality_accuracy['medium']}/{num_medium} ({quality_accuracy['medium']/num_medium*100:.0f}%)")
    print(f"  - Bad → Rejected: {quality_accuracy['bad']}/{num_bad} ({quality_accuracy['bad']/num_bad*100:.0f}%)")
    
    # Save summary
    summary = {
        'total_claims': len(results),
        'decision_counts': decision_counts,
        'quality_accuracy': quality_accuracy,
        'results': results
    }
    
    summary_path = 'data/test_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Test summary saved to: {summary_path}")
    print("\n" + "="*60)
    print("TESTING COMPLETED")
    print("="*60)


if __name__ == '__main__':
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run tests
    generate_and_process_claims(num_good=3, num_medium=3, num_bad=3)
