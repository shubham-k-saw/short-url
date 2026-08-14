# URL Shortener Domain Database (`short-url`)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)
[![Data Verification](https://img.shields.io/badge/verification-passing-brightgreen)](fmt.py)

A public, curated database of known URL shortener domains and redirect services, structured for easy parsing by security tools, adblockers, link expanders, analytics engines, domain classifiers, and threat intelligence pipelines.

---

## 📌 Dataset Structure (`list.txt`)

All entries are stored in [`list.txt`](list.txt) categorized under standardized headers:

| Section Header | Description | Examples |
| :--- | :--- | :--- |
| `// === START PUBLIC ===` | General-purpose public URL shorteners open to anyone. | `bit.ly`, `tinyurl.com`, `dub.sh` |
| `// === START BRANDED ===` | Custom short domains managed by specific organizations for official links. | `amzn.to`, `apple.co`, `aka.ms` |
| `// === START PLATFORM OWNED ===` | Native short/redirect domains owned by major internet platforms. | `t.co`, `youtu.be`, `fb.me`, `redd.it` |
| `// === START DEFUNCT ===` | Formerly active shorteners that are retired or no longer operating. | `goo.gl` |

---

## 🚀 How to Use

### 1. Python Example (Fetching remotely from GitHub or reading `list.txt`)

```python
import urllib.request

RAW_URL = "https://raw.githubusercontent.com/shubham-k-saw/short-url/master/list.txt"

def load_short_url_domains(source=RAW_URL):
    shortener_domains = set()
    
    # Fetch from URL or read local file
    if source.startswith("http://") or source.startswith("https://"):
        req = urllib.request.urlopen(source)
        lines = (line.decode("utf-8") for line in req)
    else:
        lines = open(source, "r", encoding="utf-8")

    for line in lines:
        line = line.strip()
        if line and not line.startswith("//"):
            shortener_domains.add(line.lower())

    return shortener_domains

domains = load_short_url_domains()
print(f"Loaded {len(domains)} URL shortener domains.")
print("Is bit.ly a shortener?", "bit.ly" in domains)
```

### 2. Node.js Example

```javascript
const https = require('https');
const fs = require('fs');

const RAW_URL = 'https://raw.githubusercontent.com/shubham-k-saw/short-url/master/list.txt';

function parseContent(content) {
  return new Set(
    content
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0 && !line.startsWith('//'))
  );
}

// Option A: Parse local list.txt
const localDomains = parseContent(fs.readFileSync('list.txt', 'utf8'));
console.log(`Loaded ${localDomains.size} local shortener domains.`);

// Option B: Fetch remote list from GitHub
https.get(RAW_URL, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const remoteDomains = parseContent(data);
    console.log(`Loaded ${remoteDomains.size} remote domains from GitHub.`);
    console.log(`Is 't.co' a shortener?`, remoteDomains.has('t.co'));
  });
});
```

### 3. Bash / cURL Example

```bash
# Fetch clean list of domains directly from GitHub, ignoring comments and blank lines
curl -sSL https://raw.githubusercontent.com/shubham-k-saw/short-url/master/list.txt \
  | grep -v '^//' \
  | grep -v '^$'
```

---

## 🛠 Formatting & Verification (`fmt.py`)

We enforce strict data integrity, domain formatting, uniqueness, and alphabetical ordering inside [`list.txt`](list.txt) using `fmt.py`.

```bash
# Check if list.txt passes validation
python3 fmt.py

# Automatically sort company groups and format list.txt
python3 fmt.py --fix
```

Verification rules enforced:
- **Valid Hostname Syntax**: Lowercase, valid domain formatting (no schemes `https://`, trailing slashes, or invalid characters).
- **No Duplicates**: Each domain appears at most once across all sections (case-insensitive).
- **Company / Entity Grouping**: In `BRANDED` and `PLATFORM OWNED` sections, company groups (e.g. `// Amazon (amazon.com)`) are sorted alphabetically by company name. Multiple short domains under a company are sorted alphabetically.
- **Section Integrity**: Standard section header format (`// === START <SECTION> ===`).

---

## 🤝 Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on categorizing services, formatting domain entries, and testing your changes before opening a pull request.

---

## 📄 License

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
[![CC BY 4.0](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)
