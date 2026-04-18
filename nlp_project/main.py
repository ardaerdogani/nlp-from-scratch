"""
Main entry point for the complete NLP project.

Runs the full pipeline:
1. Generate datasets (text corpus + QA pairs)
2. Train all 6 text generation models
3. Train both chatbot models
4. Evaluate and compare all models
"""

import os
import sys
import json
import torch

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from data.generate_dataset import main as generate_corpus
from data.generate_qa_dataset import main as generate_qa
from train.train_text_gen import train_all_text_gen_models
from train.train_chatbot import train_all_chatbots
from evaluate.evaluate_text_gen import evaluate_text_gen_models
from evaluate.evaluate_chatbot import evaluate_chatbots


def main():
    """Run the complete NLP pipeline."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"{'=' * 60}")
    print(f"  NLP PROJECT - Complete Pipeline")
    print(f"  Device: {device}")
    print(f"{'=' * 60}")

    data_dir = os.path.join(PROJECT_ROOT, "data")

    # =========================================
    # Step 1: Generate datasets
    # =========================================
    print(f"\n{'=' * 60}")
    print("  STEP 1: Dataset Generation")
    print(f"{'=' * 60}")

    corpus_path = os.path.join(data_dir, "corpus.txt")
    if not os.path.exists(corpus_path):
        print("\nGenerating text corpus...")
        generate_corpus()
    else:
        print(f"\nCorpus already exists at {corpus_path}")

    qa_path = os.path.join(data_dir, "qa_pairs.json")
    if not os.path.exists(qa_path):
        print("\nGenerating QA pairs...")
        generate_qa()
    else:
        print(f"QA pairs already exist at {qa_path}")

    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = f.read()
    print(f"Corpus: {len(corpus.split())} words, {len(corpus)} characters")

    with open(qa_path, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)
    print(f"QA pairs: {len(qa_pairs)} pairs")

    # =========================================
    # Step 2: Train text generation models
    # =========================================
    print(f"\n{'=' * 60}")
    print("  STEP 2: Training Text Generation Models (6 models)")
    print(f"{'=' * 60}")

    text_gen_results = train_all_text_gen_models(
        corpus, device=device, epochs=20
    )

    # =========================================
    # Step 3: Train chatbot models
    # =========================================
    print(f"\n{'=' * 60}")
    print("  STEP 3: Training Chatbot Models (2 models)")
    print(f"{'=' * 60}")

    chatbot_tokenizer, chatbot_results = train_all_chatbots(
        qa_pairs, device=device, epochs=30
    )

    # =========================================
    # Step 4: Evaluate text generation models
    # =========================================
    print(f"\n{'=' * 60}")
    print("  STEP 4: Evaluating Text Generation Models")
    print(f"{'=' * 60}")

    text_gen_report = evaluate_text_gen_models(text_gen_results, device=device)

    # =========================================
    # Step 5: Evaluate chatbot models
    # =========================================
    print(f"\n{'=' * 60}")
    print("  STEP 5: Evaluating Chatbot Models")
    print(f"{'=' * 60}")

    chatbot_report = evaluate_chatbots(
        chatbot_tokenizer, chatbot_results, device=device
    )

    # =========================================
    # Save reports
    # =========================================
    report_path = os.path.join(PROJECT_ROOT, "evaluation_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("NLP PROJECT - EVALUATION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write("PART 1: TEXT GENERATION MODELS\n")
        f.write(text_gen_report)
        f.write("\n\n")
        f.write("PART 2: CHATBOT MODELS\n")
        f.write(chatbot_report)

    print(f"\n{'=' * 60}")
    print(f"  Pipeline complete!")
    print(f"  Evaluation report saved to: {report_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
