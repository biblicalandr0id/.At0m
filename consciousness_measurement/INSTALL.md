# Installation Guide - Consciousness Measurement Framework

## System Requirements

- **Python:** 3.9 or higher
- **RAM:** 8GB minimum, 32GB+ recommended for large systems
- **Optional:** CUDA-capable GPU for acceleration (512×A100 cluster ideal)

## Quick Installation

```bash
# Clone repository
cd consciousness_measurement

# Install dependencies
pip install -r requirements.txt

# Verify installation
python code/phi_calculator.py --demo both
```

## Detailed Setup

### 1. Base Dependencies

```bash
pip install numpy scipy networkx pandas h5py
```

### 2. Optional: Full PyPhi (for validation)

**Note:** PyPhi has complex dependencies. Only needed for exact small-system comparison.

```bash
pip install pyphi
```

### 3. Optional: GPU Acceleration

For large-scale consciousness measurement (n > 1000 elements):

```bash
# Requires CUDA toolkit installed
pip install cupy-cuda12x  # Replace 12x with your CUDA version
```

### 4. Optional: Visualization

```bash
pip install matplotlib seaborn
```

## Testing Installation

```bash
cd consciousness_measurement/code

# Run basic test
python phi_calculator.py --demo simple

# Run full demonstration (synthetic C. elegans + comparison)
python phi_calculator.py --demo both

# Expected output:
# ✓ Integrated information Φ detected
# ✓ Results saved to ../results/
```

## Next Steps

After installation, proceed to:
1. **DATA_INTEGRATION.md** - Download real C. elegans connectome
2. **README.md** - Full framework documentation
3. **Run real measurements** on biological systems

## Troubleshooting

### Import Error: numpy

```bash
pip install --upgrade numpy
```

### Import Error: networkx

```bash
pip install networkx
```

### PyPhi Installation Fails

PyPhi is optional. Framework works without it using minimum cut approximation.

### GPU Acceleration Not Working

Verify CUDA installation:
```bash
nvidia-smi  # Should show GPU info
python -c "import cupy; print(cupy.cuda.runtime.getDeviceCount())"
```

## Performance Notes

**CPU-only mode:**
- n ≤ 20: Exact Φ computation (< 1 second)
- n = 302 (C. elegans): Approximate Φ (2-5 seconds)
- n = 1000: Approximate Φ (30-60 seconds)

**GPU-accelerated mode:**
- n = 302: < 1 second
- n = 10,000: 10-30 seconds
- n = 100,000: 2-5 minutes

## Support

See README.md for full documentation and scientific background.
