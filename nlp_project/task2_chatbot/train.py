"""
Training script for both chatbot models:
- LSTM seq2seq chatbot
- Transformer chatbot
"""

import time
import json
import os
import sys
import psutil
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.lstm_chatbot import LSTMChatbot
from models.transformer_chatbot import TransformerChatbot
from utils.tokenizer import WordTokenizer
from utils.dataset import QADataset, qa_collate_fn


def get_memory_mb():
    """Get current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def build_tokenizer(qa_pairs):
    """Build a shared word tokenizer from QA pairs."""
    all_text = []
    for pair in qa_pairs:
        all_text.append(pair["question"])
        all_text.append(pair["answer"])
    tokenizer = WordTokenizer(min_freq=1)
    tokenizer.fit(all_text)
    return tokenizer


def train_lstm_chatbot(qa_pairs, tokenizer, batch_size=32, epochs=30,
                       lr=0.001, device="cpu"):
    """
    Train LSTM seq2seq chatbot.

    Returns:
        Trained model and training stats.
    """
    print("\n--- Training LSTM Chatbot ---")
    start_time = time.time()
    start_mem = get_memory_mb()

    dataset = QADataset(qa_pairs, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True,
                            collate_fn=qa_collate_fn, drop_last=True)

    model = LSTMChatbot(
        vocab_size=tokenizer.vocab_size,
        embed_dim=128,
        hidden_dim=256,
        num_layers=2,
        dropout=0.2
    ).to(device)

    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_idx)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=max(1, epochs // 3), gamma=0.5)

    losses = []
    model.train()

    for epoch in range(epochs):
        epoch_loss = 0
        num_batches = 0

        for src, trg in dataloader:
            src = src.to(device)
            trg = trg.to(device)

            optimizer.zero_grad()

            teacher_forcing = max(0.5, 1.0 - epoch / epochs)
            output = model(src, trg, teacher_forcing_ratio=teacher_forcing)

            output_flat = output.reshape(-1, output.shape[-1])
            trg_flat = trg[:, 1:].reshape(-1)

            min_len = min(output_flat.shape[0], trg_flat.shape[0])
            loss = criterion(output_flat[:min_len], trg_flat[:min_len])

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item()
            num_batches += 1

        scheduler.step()
        avg_loss = epoch_loss / max(num_batches, 1)
        losses.append(avg_loss)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

    elapsed = time.time() - start_time
    mem_used = get_memory_mb() - start_mem

    print(f"  Training time: {elapsed:.2f}s")
    print(f"  Memory delta: {mem_used:.1f} MB")
    print(f"  Final loss: {losses[-1]:.4f}")

    return model, {
        "time": elapsed,
        "memory": mem_used,
        "losses": losses,
        "final_loss": losses[-1]
    }


def train_transformer_chatbot(qa_pairs, tokenizer, batch_size=32, epochs=30,
                               lr=0.0005, device="cpu"):
    """
    Train Transformer chatbot.

    Returns:
        Trained model and training stats.
    """
    print("\n--- Training Transformer Chatbot ---")
    start_time = time.time()
    start_mem = get_memory_mb()

    dataset = QADataset(qa_pairs, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True,
                            collate_fn=qa_collate_fn, drop_last=True)

    model = TransformerChatbot(
        vocab_size=tokenizer.vocab_size,
        d_model=128,
        num_heads=4,
        d_ff=512,
        num_encoder_layers=3,
        num_decoder_layers=3,
        max_len=256,
        dropout=0.1
    ).to(device)

    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_idx)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.98), eps=1e-9)

    # Warmup + decay schedule
    warmup_steps = 400

    def lr_lambda(step):
        step = max(step + 1, 1)
        return min(step ** (-0.5), step * warmup_steps ** (-1.5))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    losses = []
    model.train()

    for epoch in range(epochs):
        epoch_loss = 0
        num_batches = 0

        for src, trg in dataloader:
            src = src.to(device)
            trg = trg.to(device)

            trg_input = trg[:, :-1]
            trg_target = trg[:, 1:]

            optimizer.zero_grad()
            output = model(src, trg_input)

            output_flat = output.reshape(-1, output.shape[-1])
            trg_flat = trg_target.reshape(-1)

            loss = criterion(output_flat, trg_flat)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            scheduler.step()

            epoch_loss += loss.item()
            num_batches += 1

        avg_loss = epoch_loss / max(num_batches, 1)
        losses.append(avg_loss)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"  Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

    elapsed = time.time() - start_time
    mem_used = get_memory_mb() - start_mem

    print(f"  Training time: {elapsed:.2f}s")
    print(f"  Memory delta: {mem_used:.1f} MB")
    print(f"  Final loss: {losses[-1]:.4f}")

    return model, {
        "time": elapsed,
        "memory": mem_used,
        "losses": losses,
        "final_loss": losses[-1]
    }


def train_all_chatbots(qa_pairs, device="cpu", epochs=30):
    """
    Train both chatbot models.

    Returns:
        tokenizer, dict of (model, stats) for each chatbot.
    """
    tokenizer = build_tokenizer(qa_pairs)
    print(f"Chatbot vocabulary size: {tokenizer.vocab_size}")

    results = {}

    lstm_model, lstm_stats = train_lstm_chatbot(
        qa_pairs, tokenizer, batch_size=32, epochs=epochs, device=device
    )
    results["lstm_chatbot"] = (lstm_model, lstm_stats)

    transformer_model, transformer_stats = train_transformer_chatbot(
        qa_pairs, tokenizer, batch_size=32, epochs=epochs, device=device
    )
    results["transformer_chatbot"] = (transformer_model, transformer_stats)

    return tokenizer, results


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    qa_path = os.path.join(data_dir, "qa_pairs.json")

    if not os.path.exists(qa_path):
        print("Generating QA pairs...")
        from data.generate_qa_dataset import main as gen_qa
        gen_qa()

    with open(qa_path, "r", encoding="utf-8") as f:
        qa_pairs = json.load(f)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    tokenizer, results = train_all_chatbots(qa_pairs, device=device, epochs=30)

    print("\n=== Chatbot Training Summary ===")
    for name, (model, stats) in results.items():
        print(f"{name}: time={stats['time']:.2f}s, memory={stats['memory']:.1f}MB, "
              f"final_loss={stats['final_loss']:.4f}")
