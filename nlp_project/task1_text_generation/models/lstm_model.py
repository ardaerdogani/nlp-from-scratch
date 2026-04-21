"""
LSTM model for text generation.
Supports both character-level and word-level operation.
"""

import torch
import torch.nn as nn


class LSTMModel(nn.Module):
    """LSTM model for sequence generation."""

    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers=2, dropout=0.2):
        """
        Args:
            vocab_size: Size of the vocabulary.
            embed_dim: Dimension of token embeddings.
            hidden_dim: Dimension of LSTM hidden state.
            num_layers: Number of stacked LSTM layers.
            dropout: Dropout probability.
        """
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        """
        Forward pass.

        Args:
            x: Input tensor of shape (batch, seq_len).
            hidden: Optional tuple of (h_0, c_0) hidden states.

        Returns:
            output: Logits of shape (batch, seq_len, vocab_size).
            hidden: Tuple of final (h_n, c_n) states.
        """
        embed = self.dropout(self.embedding(x))
        out, hidden = self.lstm(embed, hidden)
        out = self.dropout(out)
        logits = self.fc(out)
        return logits, hidden

    def init_hidden(self, batch_size, device):
        """Initialize hidden state (h_0, c_0) with zeros."""
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim, device=device)
        return (h0, c0)

    def generate(self, tokenizer, seed_text, length=200, temperature=0.8, mode="char", device="cpu"):
        """
        Generate text autoregressively.

        Args:
            tokenizer: CharTokenizer or WordTokenizer instance.
            seed_text: Starting text string.
            length: Number of tokens to generate.
            temperature: Sampling temperature (higher = more random).
            mode: 'char' or 'word'.
            device: Torch device.

        Returns:
            Generated text string.
        """
        self.eval()
        with torch.no_grad():
            input_ids = tokenizer.encode(seed_text)
            if not input_ids:
                return seed_text

            generated = list(input_ids)
            input_tensor = torch.tensor([input_ids], dtype=torch.long, device=device)
            hidden = self.init_hidden(1, device)

            _, hidden = self.forward(input_tensor, hidden)

            current_id = input_ids[-1]
            for _ in range(length):
                x = torch.tensor([[current_id]], dtype=torch.long, device=device)
                logits, hidden = self.forward(x, hidden)
                logits = logits[0, -1] / temperature
                probs = torch.softmax(logits, dim=0)
                next_id = torch.multinomial(probs, 1).item()
                generated.append(next_id)
                current_id = next_id

            return tokenizer.decode(generated)
