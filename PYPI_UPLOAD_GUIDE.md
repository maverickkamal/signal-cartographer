# 📦 PyPI Upload Guide for Signal Cartographer

## Prerequisites

1. **Create PyPI Account**: Register at https://pypi.org/account/register/
2. **Create TestPyPI Account**: Register at https://test.pypi.org/account/register/
3. **Generate API Tokens**:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

## Upload Process

### Step 1: Test Upload (Recommended)
```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*
```

### Step 2: Test Installation
```bash
# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ signal-cartographer
```

### Step 3: Production Upload
```bash
# Upload to real PyPI
twine upload dist/*
```

### Step 4: Verify Installation
```bash
# Install from PyPI
pip install signal-cartographer

# Test the command-line tools
signal-cartographer
aethertap
```

## Package Information

- **Name**: signal-cartographer
- **Version**: 1.0.0
- **Entry Points**:
  - `signal-cartographer` - Main game entry
  - `aethertap` - Alternative entry point
- **Dependencies**:
  - textual>=0.20.0
  - rich>=13.0.0
  - click>=8.0.0

## Built Distributions

The following files are ready for upload in `dist/`:
- `signal_cartographer-1.0.0-py3-none-any.whl` (wheel)
- `signal_cartographer-1.0.0.tar.gz` (source distribution)

Both packages have been validated with `twine check` ✅

## Usage After Installation

```bash
# Users can install with:
pip install signal-cartographer

# Then run with:
signal-cartographer
# or
aethertap
```

## Notes

- Package structure follows PyPI best practices
- Modern pyproject.toml configuration
- Cross-platform compatibility
- Complete documentation included
- All dependencies properly specified

Ready for publication! 🚀 