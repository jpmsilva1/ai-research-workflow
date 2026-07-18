### Known Deprecation Lookup (Python)
If you encounter these packages in older code, use the modern alternative:

| Old Package | Issue | Modern Fix |
|-------------|-------|------------|
| `tensorflow-addons` | Deprecated (TF 2.13+) | Re-implement needed function using core TF/Keras |
| `keras` (standalone) | Merged into TF | Change `import keras` to `from tensorflow import keras` |
| `sklearn.externals.joblib` | Removed | `pip install joblib`; change import to `import joblib` |
| `torchvision.models` (old API) | Deprecated `pretrained=True` | Use `weights=ResNet50_Weights.DEFAULT` |
| `scipy.misc.imresize` | Removed (SciPy 1.3.0) | Use `PIL.Image.resize` or `cv2.resize` |
| `numpy.float` | Removed (NumPy 1.24) | Change `np.float` to `float` (built-in) |
| `numpy.int` | Removed (NumPy 1.24) | Change `np.int` to `int` (built-in) |

### Common Python Replication Traps
1. **Implicit relative imports**: Python 2 allowed `import my_module` for local files. Python 3 requires `from . import my_module` or `import my_module` if running as a script (but fails if run as a module).
   *Fix*: Run the script from the directory containing the modules, or add the dir to `sys.path`.
2. **Dict ordering**: Pre-Python 3.7 dicts did not preserve insertion order. If code relies on `dict.keys()` order for reproducibility, you may get different results.
   *Fix*: Sort keys if deterministic order is required.
3. **Pickle versions**: `pd.read_pickle` might fail if saved with an older pandas/pickle protocol.
   *Fix*: Might need to create a temporary older environment just to load and re-save as CSV.
