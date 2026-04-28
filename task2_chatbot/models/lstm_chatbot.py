import torch
import torch.nn as nn
import torch.nn.functional as F

class Encoder(nn.Module):

    def __init__(self, vocab_size, embed_dim, hidden_dim, num_layers=2, dropout=0.2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
            bidirectional=True
        )
        self.fc_hidden = nn.Linear(hidden_dim * 2, hidden_dim)
        self.fc_cell = nn.Linear(hidden_dim * 2, hidden_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, src):
        embedded = self.dropout(self.embedding(src))
        outputs, (hidden, cell) = self.lstm(embedded)

        # Combine bidirectional hidden states for the decoder
        hidden = torch.cat((hidden[0::2], hidden[1::2]), dim=2)
        cell = torch.cat((cell[0::2], cell[1::2]), dim=2)
        hidden = torch.tanh(self.fc_hidden(hidden))
        cell = torch.tanh(self.fc_cell(cell))

        return outputs, (hidden, cell)

class Attention(nn.Module):

    def __init__(self, encoder_dim, decoder_dim):
        super().__init__()
        self.attn = nn.Linear(encoder_dim + decoder_dim, decoder_dim)
        self.v = nn.Linear(decoder_dim, 1, bias=False)

    def forward(self, decoder_hidden, encoder_outputs):
        src_len = encoder_outputs.shape[1]
        decoder_hidden = decoder_hidden.unsqueeze(1).repeat(1, src_len, 1)
        energy = torch.tanh(self.attn(torch.cat((decoder_hidden, encoder_outputs), dim=2)))
        attention = self.v(energy).squeeze(2)
        return F.softmax(attention, dim=1)

class Decoder(nn.Module):

    def __init__(self, vocab_size, embed_dim, hidden_dim, encoder_dim, num_layers=2, dropout=0.2):
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim

        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.attention = Attention(encoder_dim, hidden_dim)
        self.lstm = nn.LSTM(
            embed_dim + encoder_dim, hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        self.fc_out = nn.Linear(hidden_dim + encoder_dim + embed_dim, vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_token, hidden, cell, encoder_outputs):
        embedded = self.dropout(self.embedding(input_token))

        attn_weights = self.attention(hidden[-1], encoder_outputs)
        attn_weights = attn_weights.unsqueeze(1)
        context = torch.bmm(attn_weights, encoder_outputs)

        lstm_input = torch.cat((embedded, context), dim=2)
        output, (hidden, cell) = self.lstm(lstm_input, (hidden, cell))

        prediction = self.fc_out(torch.cat((output, context, embedded), dim=2).squeeze(1))
        return prediction, hidden, cell

class LSTMChatbot(nn.Module):

    def __init__(self, vocab_size, embed_dim=128, hidden_dim=256, num_layers=2, dropout=0.2):
        super().__init__()
        encoder_dim = hidden_dim * 2  # bidirectional
        self.encoder = Encoder(vocab_size, embed_dim, hidden_dim, num_layers, dropout)
        self.decoder = Decoder(vocab_size, embed_dim, hidden_dim, encoder_dim, num_layers, dropout)
        self.vocab_size = vocab_size

    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        batch_size = src.shape[0]
        trg_len = trg.shape[1]

        outputs = torch.zeros(batch_size, trg_len - 1, self.vocab_size, device=src.device)

        encoder_outputs, (hidden, cell) = self.encoder(src)

        input_token = trg[:, 0:1]

        for t in range(1, trg_len):
            prediction, hidden, cell = self.decoder(input_token, hidden, cell, encoder_outputs)
            outputs[:, t - 1] = prediction

            if torch.rand(1).item() < teacher_forcing_ratio:
                input_token = trg[:, t:t + 1]
            else:
                input_token = prediction.argmax(dim=1, keepdim=True)

        return outputs

    def respond(self, tokenizer, question, max_len=50, min_len=5, device="cpu"):
        self.eval()
        with torch.no_grad():
            src = torch.tensor([tokenizer.encode(question, add_special=True)],
                               dtype=torch.long, device=device)
            encoder_outputs, (hidden, cell) = self.encoder(src)

            input_token = torch.tensor([[tokenizer.sos_idx]], dtype=torch.long, device=device)
            generated = []
            special_ids = {tokenizer.pad_idx, tokenizer.sos_idx, tokenizer.unk_idx}

            for step in range(max_len):
                prediction, hidden, cell = self.decoder(input_token, hidden, cell, encoder_outputs)

                # Suppress special tokens
                for sid in special_ids:
                    prediction[0, sid] = -1e9
                if step < min_len:
                    prediction[0, tokenizer.eos_idx] = -1e9

                next_id = prediction.argmax(dim=1).item()

                if next_id == tokenizer.eos_idx:
                    break

                generated.append(next_id)
                input_token = torch.tensor([[next_id]], dtype=torch.long, device=device)

            return tokenizer.decode(generated)
