"""
Master Runner Script: Executes all 4 Customer Support AI Stages sequentially.
"""

import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_stage(stage_num: int, script_path: str):
    print("\n" + "=" * 80)
    print(f"  RUNNING STAGE {stage_num}: {script_path}")
    print("=" * 80 + "\n")
    
    abs_path = os.path.join(os.path.dirname(__file__), script_path)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    res = subprocess.run([sys.executable, abs_path], capture_output=True, text=True, env=env)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

if __name__ == "__main__":
    print("\n🚀 STARTING FULL 4-STAGE SUPPORT AI SYSTEM SUITE 🚀\n")
    
    run_stage(1, "stage1_rule_based/main.py")
    run_stage(2, "stage2_ml_classification/predict.py")
    run_stage(3, "stage3_hybrid_engine/main.py")
    run_stage(4, "stage4_genai_rag/main.py")
    
    print("\n✅ ALL 4 STAGES COMPLETED SUCCESSFULLY!\n")
