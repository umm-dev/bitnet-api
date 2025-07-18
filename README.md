# BitNet API

A Python client for interacting with the [Microsoft BitNet Demo API](https://bitnet-demo.azurewebsites.net).  
Built for developers, researchers, and tinkerers who want fast and simple access to a GPU/CPU-based large language model.

[![PyPI version](https://badge.fury.io/py/bitnet-api.svg)](https://pypi.org/project/bitnet-api/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

## 🚀 Features

- ✅ Unified GPU/CPU interface
- ✅ Streaming and non-streaming support
- ✅ Custom chat history tracking
- ✅ Lightweight and dependency-free (just `requests`)
- ✅ Fully open source under GPL-3.0

---

## 📦 Installation

```bash
pip install bitnet-api
````

Or for testing:

```bash
pip install --index-url https://test.pypi.org/simple/ bitnet-api
```

---

## 🧠 Usage

```python
from bitnet_api import BitNetClient

# Use GPU (non-streaming)
client = BitNetClient(device="gpu")
response = client.send("Hello from GPU!")
print(response)

# Use CPU (non-streaming)
client = BitNetClient(device="cpu")
response = client.send("Hello from CPU!")
print(response)

# Use CPU (streaming)
client = BitNetClient(device="cpu")
for token in client.send("Stream me!", stream=True):
    print(token, end="", flush=True)
```

---

## ⚠️ Notes

* `device="gpu"` supports only non-streaming mode due to API limitations.
* Streaming is available **only** on CPU mode.
* API is backed by Microsoft's BitNet demo deployment (usage may vary depending on availability and load).

---

## 🪪 License

Licensed under the GNU General Public License v3.0 (GPL-3.0).
See the [LICENSE](./LICENSE) file for more details.

---

## 👤 Author

**Axel Sheire**
Feel free to fork, contribute, or reach out if you build something awesome with this.

---

## 🌐 Links

* [TestPyPI](https://test.pypi.org/project/bitnet-api/)
* [Official BitNet Demo](https://bitnet-demo.azurewebsites.net/)

