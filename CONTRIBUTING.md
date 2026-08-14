# Contributing to short-url

Thank you for helping improve the **short-url** database! This repository aims to maintain an accurate, curated, and standardized list of URL shorteners and redirect services.

---

## 📐 Taxonomy & Categorization Guidelines

When proposing a new domain, please place it under the appropriate section in [`list.txt`](list.txt):

1. **`PUBLIC`**
   - General-purpose URL shorteners accessible to the public (e.g. `bit.ly`, `tinyurl.com`, `dub.sh`).
   - Fallback for legitimate public shortener services.

2. **`BRANDED`**
   - Branded short domains associated with a specific established enterprise or brand (e.g. `amzn.to` for Amazon, `apple.co` for Apple, `aka.ms` for Microsoft).

3. **`PLATFORM OWNED`**
   - Native redirect domains belonging to major web/social platforms used for link sharing within or outside the platform (e.g. `t.co` for X/Twitter, `youtu.be` for YouTube, `fb.me` for Facebook).

4. **`DEFUNCT`**
   - Previously active URL shortener services that have ceased operations or shut down (e.g. `goo.gl`).

---

## 📝 Formatting Requirements

Each entry in [`list.txt`](list.txt) must follow these strict rules:

- **Lowercase only**: All domain names must be lowercase (`domain.com`, not `Domain.com`).
- **Domain syntax only**: Do not include protocols (`http://`, `https://`), trailing slashes (`/`), or paths.
- **Company / Entity Comment**: For `BRANDED` and `PLATFORM OWNED` sections, add a comment header line with the company name and main domain:
  ```txt
  // Company Name (maindomain.com)
  short.domain
  ```
- **Multi-Domain Companies**: If a company owns multiple short domains, list all short domains under the single company header, sorted alphabetically:
  ```txt
  // Amazon (amazon.com)
  a.co
  amzn.to
  ```
- **Alphabetical Sorting**:
  - Company groups within `BRANDED` and `PLATFORM OWNED` are sorted alphabetically by company name.
  - Individual short domains within a company group or section are sorted alphabetically.
- **No duplicates**: Domains must not appear more than once anywhere in the dataset.

---

## 🧪 Local Testing & Verification (`fmt.py`)

Before submitting your Pull Request, verify your changes by running `fmt.py`:

```bash
# Verify list.txt formatting and sorting
python3 fmt.py
```

### Auto-sorting & Formatting

You can automatically sort company groups and fix formatting inconsistencies by running:

```bash
python3 fmt.py --fix
```

---

## ✅ Pull Request Checklist

Before opening your PR, ensure:

- [ ] Domain is placed in the correct section in [`list.txt`](list.txt).
- [ ] Domain is validated and lowercase.
- [ ] Ran `python3 fmt.py` and all checks pass without errors.
- [ ] PR description includes context or proof that the domain is a legitimate URL shortener service.
