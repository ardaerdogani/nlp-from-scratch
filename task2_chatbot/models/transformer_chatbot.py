"""
Transformer-based chatbot implemented from scratch.
Encoder-decoder architecture with multi-head self-attention.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding for sequence position information."""

    def __init__(self, d_model, max_len=512, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x):
        """Add positional encoding to input embeddings."""
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)


class MultiHeadAttention(nn.Module):
    """Multi-head attention mechanism implemented from scratch."""

    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """Compute scaled dot-product attention."""
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        return torch.matmul(attn_weights, V)

    def forward(self, query, key, value, mask=None):
        """
        Args:
            query, key, value: (batch, seq_len, d_model)
            mask: Optional attention mask.

        Returns:
            output: (batch, seq_len, d_model)
        """
        batch_size = query.size(0)

        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)

        attn_output = self.scaled_dot_product_attention(Q, K, V, mask)

        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        return self.W_o(attn_output)


class FeedForward(nn.Module):
    """Position-wise feed-forward network."""

    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.linear2(self.dropout(F.relu(self.linear1(x))))


class TransformerEncoderLayer(nn.Module):
    """Single encoder layer: self-attention + feed-forward."""

    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, src, src_mask=None):
        attn_out = self.self_attn(src, src, src, src_mask)
        src = self.norm1(src + self.dropout1(attn_out))
        ff_out = self.feed_forward(src)
        src = self.norm2(src + self.dropout2(ff_out))
        return src


class TransformerDecoderLayer(nn.Module):
    """Single decoder layer: masked self-attention + cross-attention + feed-forward."""

    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.cross_attn = MultiHeadAttention(d_model, num_heads, dropout)
        self.feed_forward = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.dropout3 = nn.Dropout(dropout)

    def forward(self, trg, enc_out, trg_mask=None, src_mask=None):
        attn_out = self.self_attn(trg, trg, trg, trg_mask)
        trg = self.norm1(trg + self.dropout1(attn_out))
        attn_out = self.cross_attn(trg, enc_out, enc_out, src_mask)
        trg = self.norm2(trg + self.dropout2(attn_out))
        ff_out = self.feed_forward(trg)
        trg = self.norm3(trg + self.dropout3(ff_out))
        return trg


class TransformerChatbot(nn.Module):
    """
    Full Transformer encoder-decoder model for chatbot.
    Implemented from scratch without pretrained weights.
    """

    def __init__(self, vocab_size, d_model=128, num_heads=4, d_ff=512,
                 num_encoder_layers=3, num_decoder_layers=3, max_len=512, dropout=0.1):
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model

        self.src_embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.trg_embedding = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_encoding = PositionalEncoding(d_model, max_len, dropout)

        self.encoder_layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_encoder_layers)
        ])
        self.decoder_layers = nn.ModuleList([
            TransformerDecoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_decoder_layers)
        ])

        self.fc_out = nn.Linear(d_model, vocab_size)
        self.scale = math.sqrt(d_model)

    def make_src_mask(self, src):
        """Create source padding mask."""
        src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
        return src_mask

    def make_trg_mask(self, trg):
        """Create target causal mask (no peeking ahead)."""
        trg_len = trg.shape[1]
        trg_pad_mask = (trg != 0).unsqueeze(1).unsqueeze(2)
        trg_causal_mask = torch.tril(torch.ones(trg_len, trg_len, device=trg.device)).bool()
        trg_causal_mask = trg_causal_mask.unsqueeze(0).unsqueeze(0)
        return trg_pad_mask & trg_causal_mask

    def encode(self, src, src_mask):
        """Encode source sequence."""
        x = self.pos_encoding(self.src_embedding(src) * self.scale)
        for layer in self.encoder_layers:
            x = layer(x, src_mask)
        return x

    def decode(self, trg, enc_out, trg_mask, src_mask):
        """Decode target sequence given encoder output."""
        x = self.pos_encoding(self.trg_embedding(trg) * self.scale)
        for layer in self.decoder_layers:
            x = layer(x, enc_out, trg_mask, src_mask)
        return x

    def forward(self, src, trg):
        """
        Args:
            src: Source tensor (batch, src_len).
            trg: Target tensor (batch, trg_len).

        Returns:
            output: Logits (batch, trg_len, vocab_size).
        """
        src_mask = self.make_src_mask(src)
        trg_mask = self.make_trg_mask(trg)
        enc_out = self.encode(src, src_mask)
        dec_out = self.decode(trg, enc_out, trg_mask, src_mask)
        return self.fc_out(dec_out)

    def respond(self, tokenizer, question, max_len=50, min_len=5, temperature=1.0, device="cpu"):
        """
        Generate a response to a question using greedy decoding.

        Args:
            tokenizer: WordTokenizer instance.
            question: Input question string.
            max_len: Maximum response length.
            min_len: Minimum tokens before EOS is allowed.
            temperature: Sampling temperature.
            device: Torch device.

        Returns:
            Response string.
        """
        self.eval()
        with torch.no_grad():
            src = torch.tensor([tokenizer.encode(question, add_special=True)],
                               dtype=torch.long, device=device)
            src_mask = self.make_src_mask(src)
            enc_out = self.encode(src, src_mask)

            trg_ids = [tokenizer.sos_idx]
            special_ids = {tokenizer.pad_idx, tokenizer.sos_idx, tokenizer.unk_idx}

            for step in range(max_len):
                trg_tensor = torch.tensor([trg_ids], dtype=torch.long, device=device)
                trg_mask = self.make_trg_mask(trg_tensor)
                dec_out = self.decode(trg_tensor, enc_out, trg_mask, src_mask)
                logits = self.fc_out(dec_out[:, -1, :])

                # Suppress special tokens during generation
                for sid in special_ids:
                    logits[0, sid] = -1e9
                # Suppress EOS before min_len
                if step < min_len:
                    logits[0, tokenizer.eos_idx] = -1e9

                if temperature != 1.0:
                    logits = logits / temperature

                next_id = logits.argmax(dim=1).item()

                if next_id == tokenizer.eos_idx:
                    break

                trg_ids.append(next_id)

            return tokenizer.decode(trg_ids[1:])
