# Deep learning — training a network

Use with [`training.md`](training.md), which still applies.

## Setup
- [ ] ☠ A simpler model tried first and beaten — trees usually win on tabular data
- [ ] Enough data for the capacity, or transfer learning used instead of scratch
- [ ] Inputs normalised; images and text preprocessed consistently between train and inference
- [ ] Device confirmed (MPS on Apple Silicon) — silent CPU fallback wastes hours

## Architecture
- [ ] Smallest architecture that could work, first
- [ ] Task-appropriate output layer and loss (softmax + cross-entropy; sigmoid + BCE; linear + MSE)
- [ ] Residual connections and normalisation where depth warrants them
- [ ] Parameter count sane relative to sample count

## Training loop
- [ ] Overfit a single batch deliberately, first — if it can't, the loop is broken, not the model
- [ ] Learning rate found by sweep, not guessed; schedule chosen
- [ ] Batch size set by memory, and its effect on stability understood
- [ ] Gradient clipping if loss spikes
- [ ] Checkpoints saved, best-by-validation kept

## Regularisation
- [ ] Early stopping in place
- [ ] Dropout / weight decay tuned against validation, not vibes
- [ ] Augmentation applied to train only, never to validation or test

## Smells
- Loss NaN → learning rate too high; drop 10× before anything else
- Loss flat from step one → wiring bug, wrong loss, or labels not connected
- Train loss falls, validation flat → overfitting; more data or more regularisation
- Cannot overfit one batch → the bug is in the loop
