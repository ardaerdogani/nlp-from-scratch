"""
Training script for all 6 text generation models:
- Character-level: Markov Chain, RNN, LSTM
- Word-level: Markov Chain, RNN, LSTM
"""

import time
import os
import sys
import psutil
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.markov_chain import MarkovChain
from models.rnn_model import RNNModel
from models.lstm_model import LSTMModel
from utils.tokenizer import CharTokenizer, WordTokenizer
from utils.dataset import TextGenDataset


def get_memory_mb():
    """Get current process memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def train_markov_char(corpus, order=5):
    """Train character-level Markov Chain model."""
    print("\n--- Training Character-level Markov Chain (order={}) ---".format(order))
    start_time = time.time()
    start_mem = get_memory_mb()

    model = MarkovChain(order=order)
    tokens = list(corpus)
    model.fit(tokens)

    elapsed = time.time() - start_time
    mem_used = get_memory_mb() - start_mem

    print(f"  Training time: {elapsed:.2f}s")
    print(f"  Memory delta: {mem_used:.1f} MB")
    print(f"  States learned: {len(model.transitions)}")

    return model, {"time": elapsed, "memory": mem_used}


def train_markov_word(corpus, order=2):
    """Train word-level Markov Chain model."""
    print("\n--- Training Word-level Markov Chain (order={}) ---".format(order))
    start_time = time.time()
    start_mem = get_memory_mb()

    model = MarkovChain(order=order)
    tokens = corpus.lower().split()
    model.fit(tokens)

    elapsed = time.time() - start_time
    mem_used = get_memory_mb() - start_mem

    print(f"  Training time: {elapsed:.2f}s")
    print(f"  Memory delta: {mem_used:.1f} MB")
    print(f"  States learned: {len(model.transitions)}")

    return model, {"time": elapsed, "memory": mem_used}


def train_neural_model(model, tokenizer, corpus, mode="char",
                       seq_length=100, batch_size=64, epochs=20,
                       lr=0.002, device="cpu", model_name="Model"):
    """
    Train a neural text generation model (RNN or LSTM).

    Args:
        model: RNNModel or LSTMModel instance.
        tokenizer: CharTokenizer or WordTokenizer instance.
        corpus: Raw text corpus string.
        mode: 'char' or 'word'.
        seq_length: Length of training sequences.
        batch_size: Batch size for training.
        epochs: Number of training epochs.
        lr: Learning rate.
        device: Torch device.
        model_name: Name for logging.

    Returns:
        Trained model and training stats dict.
    """
    print(f"\n--- Training {model_name} ---")
    start_time = time.time()
    start_mem = get_memory_mb()

    tokenizer.fit(corpus if mode == "char" else corpus)
    encoded = tokenizer.encode(corpus)

    dataset = TextGenDataset(encoded, seq_length)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=max(1, epochs // 3), gamma=0.5)

    losses = []
    model.train()

    for epoch in range(epochs):
        epoch_loss = 0
        num_batches = 0

        for x_batch, y_batch in dataloader:
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)

            optimizer.zero_grad()
            logits, _ = model(x_batch)
            loss = criterion(logits.view(-1, model.vocab_size), y_batch.view(-1))
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

    return model, tokenizer, {
        "time": elapsed,
        "memory": mem_used,
        "losses": losses,
        "final_loss": losses[-1]
    }


def train_all_text_gen_models(corpus, device="cpu", epochs=20):
    """
    Train all 6 text generation models and return them with stats.

    Returns:
        Dictionary mapping model names to (model, tokenizer, stats) tuples.
    """
    results = {}

    # 1. Character-level Markov Chain
    mcm_char, stats = train_markov_char(corpus, order=5)
    results["char_mcm"] = (mcm_char, None, stats)

    # 2. Word-level Markov Chain
    mcm_word, stats = train_markov_word(corpus, order=2)
    results["word_mcm"] = (mcm_word, None, stats)

    # 3. Character-level RNN
    char_tok_rnn = CharTokenizer()
    char_tok_rnn.fit(corpus)
    char_rnn = RNNModel(
        vocab_size=char_tok_rnn.vocab_size,
        embed_dim=64,
        hidden_dim=128,
        num_layers=2,
        dropout=0.2
    )
    char_rnn, char_tok_rnn, stats = train_neural_model(
        char_rnn, char_tok_rnn, corpus, mode="char",
        seq_length=100, batch_size=64, epochs=epochs,
        lr=0.003, device=device, model_name="Character-level RNN"
    )
    results["char_rnn"] = (char_rnn, char_tok_rnn, stats)

    # 4. Word-level RNN
    word_tok_rnn = WordTokenizer()
    word_tok_rnn.fit(corpus)
    word_rnn = RNNModel(
        vocab_size=word_tok_rnn.vocab_size,
        embed_dim=64,
        hidden_dim=128,
        num_layers=2,
        dropout=0.2
    )
    word_rnn, word_tok_rnn, stats = train_neural_model(
        word_rnn, word_tok_rnn, corpus, mode="word",
        seq_length=20, batch_size=32, epochs=epochs,
        lr=0.003, device=device, model_name="Word-level RNN"
    )
    results["word_rnn"] = (word_rnn, word_tok_rnn, stats)

    # 5. Character-level LSTM
    char_tok_lstm = CharTokenizer()
    char_tok_lstm.fit(corpus)
    char_lstm = LSTMModel(
        vocab_size=char_tok_lstm.vocab_size,
        embed_dim=64,
        hidden_dim=128,
        num_layers=2,
        dropout=0.2
    )
    char_lstm, char_tok_lstm, stats = train_neural_model(
        char_lstm, char_tok_lstm, corpus, mode="char",
        seq_length=100, batch_size=64, epochs=epochs,
        lr=0.003, device=device, model_name="Character-level LSTM"
    )
    results["char_lstm"] = (char_lstm, char_tok_lstm, stats)

    # 6. Word-level LSTM
    word_tok_lstm = WordTokenizer()
    word_tok_lstm.fit(corpus)
    word_lstm = LSTMModel(
        vocab_size=word_tok_lstm.vocab_size,
        embed_dim=64,
        hidden_dim=128,
        num_layers=2,
        dropout=0.2
    )
    word_lstm, word_tok_lstm, stats = train_neural_model(
        word_lstm, word_tok_lstm, corpus, mode="word",
        seq_length=20, batch_size=32, epochs=epochs,
        lr=0.003, device=device, model_name="Word-level LSTM"
    )
    results["word_lstm"] = (word_lstm, word_tok_lstm, stats)

    return results


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    corpus_path = os.path.join(data_dir, "corpus.txt")

    if not os.path.exists(corpus_path):
        print("Generating corpus...")
        from data.generate_dataset import main as gen_corpus
        gen_corpus()

    with open(corpus_path, "r", encoding="utf-8") as f:
        corpus = f.read()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    results = train_all_text_gen_models(corpus, device=device, epochs=20)

    print("\n=== Training Summary ===")
    for name, (model, tok, stats) in results.items():
        print(f"{name}: time={stats['time']:.2f}s, memory={stats['memory']:.1f}MB")
