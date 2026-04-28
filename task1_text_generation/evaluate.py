import os
import sys
from tabulate import tabulate

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 10 test prompts for text generation
CHAR_PROMPTS = [
    "The ancient forest",
    "In the world of",
    "Science reveals",
    "The computer proc",
    "Every day the",
    "Through careful",
    "The importance of",
    "Many believe that",
    "Understanding how",
    "The connection bet",
]

WORD_PROMPTS = [
    "the ancient forest stretches",
    "in the world of science",
    "the computer processes data",
    "every day the student learns",
    "through careful effort the",
    "the importance of education",
    "many believe that the",
    "understanding how the system",
    "the role of the artist",
    "the athlete trains hard",
]

def truncate_output(text, min_chars=20, max_chars=80):
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "..."
    return text

def evaluate_text_gen_models(results, device="cpu"):
    output_lines = []

    # =============================================
    # Training performance comparison
    # =============================================
    output_lines.append("\n" + "=" * 80)
    output_lines.append("TEXT GENERATION MODELS - TRAINING PERFORMANCE COMPARISON")
    output_lines.append("=" * 80)

    perf_table = []
    model_display_names = {
        "char_mcm": "Char Markov Chain",
        "word_mcm": "Word Markov Chain",
        "char_rnn": "Char RNN",
        "word_rnn": "Word RNN",
        "char_lstm": "Char LSTM",
        "word_lstm": "Word LSTM",
    }

    for key in ["char_mcm", "word_mcm", "char_rnn", "word_rnn", "char_lstm", "word_lstm"]:
        if key not in results:
            continue
        _, _, stats = results[key]
        final_loss = stats.get("final_loss", "N/A")
        if isinstance(final_loss, float):
            final_loss = f"{final_loss:.4f}"
        perf_table.append([
            model_display_names[key],
            f"{stats['time']:.2f}s",
            f"{stats['memory']:.1f} MB",
            final_loss
        ])

    output_lines.append(tabulate(
        perf_table,
        headers=["Model", "Training Time", "Memory Usage", "Final Loss"],
        tablefmt="grid"
    ))

    # =============================================
    # Output quality comparison
    # =============================================
    output_lines.append("\n" + "=" * 80)
    output_lines.append("TEXT GENERATION MODELS - OUTPUT COMPARISON (10 PROMPTS)")
    output_lines.append("=" * 80)

    # Character-level comparison
    output_lines.append("\n--- Character-Level Models ---\n")
    char_table = []

    for i, prompt in enumerate(CHAR_PROMPTS):
        row = [f"#{i+1}", prompt]

        # Markov Chain character
        if "char_mcm" in results:
            model = results["char_mcm"][0]
            gen = model.generate_text(length=120, seed_text=prompt, mode="char", seed_value=42 + i)
            row.append(truncate_output(gen))
        else:
            row.append("N/A")

        # RNN character
        if "char_rnn" in results:
            model, tok = results["char_rnn"][0], results["char_rnn"][1]
            gen = model.generate(tok, prompt, length=80, temperature=0.8, mode="char", device=device)
            row.append(truncate_output(gen))
        else:
            row.append("N/A")

        # LSTM character
        if "char_lstm" in results:
            model, tok = results["char_lstm"][0], results["char_lstm"][1]
            gen = model.generate(tok, prompt, length=80, temperature=0.8, mode="char", device=device)
            row.append(truncate_output(gen))
        else:
            row.append("N/A")

        char_table.append(row)

    output_lines.append(tabulate(
        char_table,
        headers=["#", "Prompt", "Markov Chain", "RNN", "LSTM"],
        tablefmt="grid",
        maxcolwidths=[4, 22, 28, 28, 28]
    ))

    # Word-level comparison
    output_lines.append("\n--- Word-Level Models ---\n")
    word_table = []

    for i, prompt in enumerate(WORD_PROMPTS):
        row = [f"#{i+1}", prompt]

        # Markov Chain word
        if "word_mcm" in results:
            model = results["word_mcm"][0]
            gen = model.generate_text(length=30, seed_text=prompt, mode="word", seed_value=42 + i)
            row.append(truncate_output(gen))
        else:
            row.append("N/A")

        # RNN word
        if "word_rnn" in results:
            model, tok = results["word_rnn"][0], results["word_rnn"][1]
            gen = model.generate(tok, prompt, length=25, temperature=0.8, mode="word", device=device)
            row.append(truncate_output(gen))
        else:
            row.append("N/A")

        # LSTM word
        if "word_lstm" in results:
            model, tok = results["word_lstm"][0], results["word_lstm"][1]
            gen = model.generate(tok, prompt, length=25, temperature=0.8, mode="word", device=device)
            row.append(truncate_output(gen))
        else:
            row.append("N/A")

        word_table.append(row)

    output_lines.append(tabulate(
        word_table,
        headers=["#", "Prompt", "Markov Chain", "RNN", "LSTM"],
        tablefmt="grid",
        maxcolwidths=[4, 30, 28, 28, 28]
    ))

    # =============================================
    # Quality observations
    # =============================================
    output_lines.append("\n" + "=" * 80)
    output_lines.append("OUTPUT QUALITY OBSERVATIONS")
    output_lines.append("=" * 80)
    output_lines.append("""
1. Markov Chain Models:
   - Character-level: Produces text that looks like English but with frequent
     nonsense words. Good at capturing local character patterns.
   - Word-level: Produces grammatically plausible phrases since it operates on
     real words, but lacks long-range coherence.

2. RNN Models:
   - Character-level: Better than Markov at learning spelling patterns and common
     word structures. Can struggle with long-term dependencies.
   - Word-level: Generates somewhat coherent phrases but may repeat patterns.
     Limited by vanishing gradient problem.

3. LSTM Models:
   - Character-level: Best character-level model for capturing longer patterns.
     Produces more coherent sequences than RNN.
   - Word-level: Best neural word-level model. Better at maintaining context
     across the generated sequence due to gating mechanism.

General Notes:
- All models trained from scratch on ~12,000 words, which limits output quality.
- Character-level models need longer training and more data for coherent words.
- Word-level models produce real words but may lack grammatical structure.
- LSTM consistently outperforms RNN due to better gradient flow.
- Markov Chain is fastest to train but has no learning of underlying structure.
""")

    result_text = "\n".join(output_lines)
    print(result_text)
    return result_text
