try:
    import pandas as pd
    import numpy as np
    import requests
    print("✅ All basic packages installed successfully!")
    print(f"Pandas version: {pd.__version__}")
    print(f"Numpy version: {np.__version__}")
except ImportError as e:
    print(f"❌ Error importing packages: {e}")
