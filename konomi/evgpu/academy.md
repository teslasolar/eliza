# eVGPU — Edge Compute

CPU-based compute engine for edge inference — tensor operations, convolution, pooling on minimal hardware.

## Key Classes

- **eVGPU** — Virtual GPU compute engine running on CPU
- **Tensor** — N-dimensional array with basic operations

## Core Concepts

- **No GPU Required**: eVGPU runs tensor ops on CPU — works on Raspberry Pi, industrial PCs, anything
- **Edge Inference**: Run classification and detection models at the edge, near the process
- **Minimal Footprint**: Designed for constrained environments where TensorFlow/PyTorch won't fit
