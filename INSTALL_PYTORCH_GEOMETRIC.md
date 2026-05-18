# Installation Instructions for PyTorch Geometric

## ⚠️ Important: Installation Order Matters

You must install PyTorch **BEFORE** PyTorch Geometric packages!

## 🐍 Step-by-Step Installation

### **Step 1: Install PyTorch (First!)**

```bash
# For CPU-only (recommended for development)
pip3 install torch

# OR for GPU (if you have NVIDIA GPU + CUDA)
pip3 install torch --index-url https://download.pytorch.org/whl/cu118
```

### **Step 2: Verify PyTorch Installation**

```bash
python3 -c "import torch; print(f'PyTorch {torch.__version__}')"
```

**Expected output:**
```
PyTorch 2.0.1  # or your installed version
```

### **Step 3: Install torch-scatter (After PyTorch!)**

```bash
# Find your PyTorch version
python3 -c "import torch; print(torch.__version__)"
```

Then install from the correct URL:

**For PyTorch 2.0.x:**
```bash
pip3 install torch-scatter -f https://data.pyg.org/whl/torch-2.0.0+cu118.html
pip3 install torch-sparse -f https://data.pyg.org/whl/torch-2.0.0+cu118.html
pip3 install torch-cluster -f https://data.pyg.org/whl/torch-2.0.0+cu118.html
```

**For PyTorch 2.1.x:**
```bash
pip3 install torch-scatter -f https://data.pyg.org/whl/torch-2.1.0+cu118.html
pip3 install torch-sparse -f https://data.pyg.org/whl/torch-2.1.0+cu118.html
pip3 install torch-cluster -f https://data.pyg.org/whl/torch-2.1.0+cu118.html
```

### **Step 4: Install torch-geometric**

```bash
pip3 install torch-geometric
```

---

## 🚀 Quick Fix (Copy-Paste)

### **Option 1: CPU-Only (Recommended for Mac)**

```bash
# Install PyTorch CPU version
pip3 install torch torchvision torchaudio

# Then install PyTorch Geometric (CPU)
pip3 install torch-geometric

# Test
python3 -c "import torch_geometric; print('✅ torch-geometric installed!')"
```

### **Option 2: GPU (NVIDIA)**

```bash
# Step 1: Install PyTorch with CUDA
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Step 2: Install PyTorch Geometric
pip3 install torch-geometric

# Step 3: Install scatter/sparse/cluster
pip3 install torch-scatter torch-sparse torch-cluster -f https://data.pyg.org/whl/

# Test
python3 -c "import torch_geometric; print('✅ torch-geometric installed!')"
```

### **Option 3: Alternative Installation**

If the above doesn't work, try:

```bash
# Install from source
pip3 install --no-cache-dir torch-scatter torch-sparse torch-cluster

# Or use conda (if available)
conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia
conda install pyg=torch-geometric -c pyg
```

---

## 🐛 Troubleshooting

### **Error: "Failed building wheel for torch-scatter"**

**Cause:** PyTorch is not installed or wrong version

**Solution:**
```bash
# Check PyTorch
python3 -c "import torch; print(torch.__version__)"

# If not installed:
pip3 install torch

# If version mismatch:
# Uninstall and reinstall matching version
pip3 uninstall torch torch-scatter torch-sparse torch-cluster torch-geometric
pip3 install torch
pip3 install torch-geometric
```

### **Error: "No matching distribution found for torch-scatter"**

**Cause:** Wrong PyTorch version for scatter packages

**Solution:**
```bash
# Check your PyTorch version
python3 -c "import torch; print(torch.__version__)"

# Use the correct URL based on your version:
# PyTorch 2.0.0: https://data.pyg.org/whl/torch-2.0.0+cu118.html
# PyTorch 2.0.1: https://data.pyg.org/whl/torch-2.0.1+cu118.html
# PyTorch 2.1.0: https://data.pyg.org/whl/torch-2.1.0+cu118.html
```

### **Error: "CUDA version mismatch"**

**Solution:**
```bash
# Check CUDA version
nvcc --version

# Install matching PyTorch
pip3 uninstall torch
pip3 install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## ✅ Verification Checklist

After installation, run these commands:

```bash
# 1. Check PyTorch
python3 -c "import torch; print(f'✅ PyTorch: {torch.__version__}')"

# 2. Check torch-geometric
python3 -c "import torch_geometric; print(f'✅ torch-geometric: {torch_geometric.__version__}')"

# 3. Check optional components
python3 -c "import torch_scatter; print('✅ torch-scatter installed')"
python3 -c "import torch_sparse; print('✅ torch-sparse installed')"
python3 -c "import torch_cluster; print('✅ torch-cluster installed')"

# 4. Test complete installation
python3 -c "
import torch
import torch_geometric
print(f'✅ All packages installed successfully!')
print(f'   PyTorch: {torch.__version__}')
print(f'   CUDA available: {torch.cuda.is_available()}')
"
```

---

## 🔄 Alternative: Use Without torch-scatter

If you continue to have issues with `torch-scatter`, the Neural Matching Engine can work **without** it for basic functionality:

```python
# NeuralMatchingEngine will use a simplified version without scatter
# It will still work, just with fewer graph operations

from tourista_ai_model.matching.neural_engine import NeuralMatchingEngine

# This will work even without torch-scatter
engine = NeuralMatchingEngine()

# It will use fallback methods if scatter is not available
```

---

## 📋 Minimum Working Installation

If you just want to get started quickly:

```bash
# Install only essential packages
pip3 install torch torchvision torchaudio
pip3 install torch-geometric

# Test
python3 test_neural_matching.py
```

---

## 🎯 Expected Result

After successful installation, you should see:

```
✅ PyTorch: 2.0.1
✅ torch-geometric: 2.5.0
✅ torch-scatter: 2.1.0
✅ torch-sparse: 0.6.17
✅ torch-cluster: 1.6.0
```

---

## 🆘 Still Having Issues?

Try this **nuclear option**:

```bash
# Uninstall everything
pip3 uninstall torch torch-geometric torch-scatter torch-sparse torch-cluster -y

# Clean pip cache
pip3 cache purge

# Fresh install
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install torch-geometric

# Verify
python3 -c "import torch_geometric; print('Success!')"
```

---

## 📞 Need Help?

If you continue to have installation issues, please share:

1. Your PyTorch version: `python3 -c "import torch; print(torch.__version__)"`
2. Your Python version: `python3 --version`
3. Your OS: `uname -a`
4. Full error message

---

## ✅ Recommended Installation Commands (Copy-Paste Ready)

### **For macOS (Apple Silicon/M1/M2/M3):**
```bash
pip3 install torch torchvision torchaudio
pip3 install torch-geometric
```

### **For macOS (Intel):**
```bash
pip3 install torch torchvision torchaudio
pip3 install torch-geometric
```

### **For Linux (CPU):**
```bash
pip3 install torch torchvision torchaudio
pip3 install torch-geometric
```

### **For Linux (NVIDIA GPU):**
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install torch-geometric
```

### **For Windows (NVIDIA GPU):**
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install torch-geometric
```

---

**Try the commands above and let me know if you need further assistance!** 🚀
