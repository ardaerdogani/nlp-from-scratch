import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tabulate import tabulate

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEST_QUESTIONS = [
    "What is the capital of France?",
    "How does gravity work?",
    "What is a computer?",
    "What is photosynthesis?",
    "Hello!",
    "What is the largest ocean?",
    "Who was the first president of the United States?",
    "What is machine learning?",
    "What is a prime number?",
    "Tell me about climate change.",
]

def plot_loss_curves(lstm_losses, transformer_losses, output_dir):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(range(1, len(lstm_losses) + 1), lstm_losses, "b-o", markersize=3, label="LSTM Chatbot")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("LSTM Chatbot Training Loss")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(range(1, len(transformer_losses) + 1), transformer_losses, "r-o", markersize=3, label="Transformer Chatbot")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.set_title("Transformer Chatbot Training Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "chatbot_loss_curves.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"  Loss curves saved to: {plot_path}")
    return plot_path

def evaluate_chatbots(tokenizer, chatbot_results, device="cpu"):
    output_lines = []

    # =============================================
    # Training performance comparison
    # =============================================
    output_lines.append("\n" + "=" * 80)
    output_lines.append("CHATBOT MODELS - TRAINING PERFORMANCE COMPARISON")
    output_lines.append("=" * 80)

    perf_table = []
    for name in ["lstm_chatbot", "transformer_chatbot"]:
        if name not in chatbot_results:
            continue
        model, stats = chatbot_results[name]
        display = "LSTM Chatbot" if "lstm" in name else "Transformer Chatbot"
        perf_table.append([
            display,
            f"{stats['time']:.2f}s",
            f"{stats['memory']:.1f} MB",
            f"{stats['final_loss']:.4f}",
            f"{sum(p.numel() for p in model.parameters()):,}"
        ])

    output_lines.append(tabulate(
        perf_table,
        headers=["Model", "Training Time", "Memory", "Final Loss", "Parameters"],
        tablefmt="grid"
    ))

    # =============================================
    # Loss curves
    # =============================================
    output_lines.append("\n--- Loss Curves ---")
    output_dir = os.path.dirname(os.path.abspath(__file__))

    lstm_losses = chatbot_results.get("lstm_chatbot", (None, {}))[1].get("losses", [])
    trans_losses = chatbot_results.get("transformer_chatbot", (None, {}))[1].get("losses", [])

    if lstm_losses and trans_losses:
        plot_loss_curves(lstm_losses, trans_losses, output_dir)

    # =============================================
    # Response comparison (10 test questions)
    # =============================================
    output_lines.append("\n" + "=" * 80)
    output_lines.append("CHATBOT MODELS - RESPONSE COMPARISON (10 TEST QUESTIONS)")
    output_lines.append("=" * 80)

    comparison_table = []

    for i, question in enumerate(TEST_QUESTIONS):
        row = [f"#{i+1}", question]

        # LSTM chatbot response
        if "lstm_chatbot" in chatbot_results:
            model = chatbot_results["lstm_chatbot"][0]
            response = model.respond(tokenizer, question, max_len=30, device=device)
            row.append(response[:80] + ("..." if len(response) > 80 else ""))
        else:
            row.append("N/A")

        # Transformer chatbot response
        if "transformer_chatbot" in chatbot_results:
            model = chatbot_results["transformer_chatbot"][0]
            response = model.respond(tokenizer, question, max_len=30, device=device)
            row.append(response[:80] + ("..." if len(response) > 80 else ""))
        else:
            row.append("N/A")

        comparison_table.append(row)

    output_lines.append(tabulate(
        comparison_table,
        headers=["#", "Question", "LSTM Response", "Transformer Response"],
        tablefmt="grid",
        maxcolwidths=[4, 30, 35, 35]
    ))

    # =============================================
    # Qualitative comparison
    # =============================================
    output_lines.append("\n" + "=" * 80)
    output_lines.append("QUALITATIVE COMPARISON")
    output_lines.append("=" * 80)

    result_text = "\n".join(output_lines)
    print(result_text)
    return result_text
