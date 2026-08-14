#!/usr/bin/env python3
"""
Format and verification script for short-url list.txt.

Checks & Formatting Rules:
  - Valid section headers (e.g. // === START PUBLIC ===)
  - Standard section spacing:
      - 1 blank line after section description
      - Exactly 1 blank line between entry blocks inside a section
      - Exactly 2 blank lines between sections
      - Max 2 consecutive blank lines anywhere (no 3+ empty lines)
  - Duplicate domain entries across sections (case-insensitive)
  - Domain syntax validity (lowercase, valid hostname syntax)
  - Entity / Company grouping in BRANDED / PLATFORM OWNED sections:
      - Groups are sorted alphabetically by Company/Entity Name (e.g. Amazon, Apple, Microsoft)
      - Short domains within each company group are sorted alphabetically (e.g. a.co, amzn.to)
  - Alphabetical domain sorting in PUBLIC and DEFUNCT sections
  - Clean spacing and LF line endings

Usage:
  python3 fmt.py           Check if list.txt passes validation
  python3 fmt.py --check   Check if list.txt passes validation
  python3 fmt.py --fix     Automatically sort and reformat list.txt in place
"""

import sys
import re
from pathlib import Path

SECTION_HEADER_RE = re.compile(r"^//\s*===\s*START\s+([A-Z0-9_\s]+)\s*===$")
DOMAIN_RE = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")
COMPANY_COMMENT_RE = re.compile(r"^//\s*([^()\n]+)(?:\s*\(([^()\n]+)\))?")

LIST_FILE = Path(__file__).parent / "list.txt"


class EntityGroup:
    def __init__(self, comments: list[str] = None):
        self.comments = list(comments) if comments else []
        self.domains = []

    @property
    def sort_key(self) -> str:
        if self.comments:
            first_comment = self.comments[0]
            cleaned = re.sub(r"^//\s*", "", first_comment).strip()
            match = COMPANY_COMMENT_RE.match(first_comment)
            if match and match.group(1):
                name = match.group(1).strip()
                if name.lower().startswith("the "):
                    name = name[4:].strip()
                return name.lower()
            return cleaned.lower()
        elif self.domains:
            return self.domains[0].lower()
        return ""


class Section:
    def __init__(self, name: str, description_comments: list[str] = None):
        self.name = name
        self.description_comments = list(description_comments) if description_comments else []
        self.groups = []


def parse_structure(filepath: Path) -> list[Section]:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\r\n") for l in f]

    sections = []
    current_section = None
    pending_comments = []
    current_group = None

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if current_section and not current_section.groups and pending_comments and not current_section.description_comments:
                current_section.description_comments = pending_comments
                pending_comments = []
            elif current_group:
                current_group = None
            continue

        header_match = SECTION_HEADER_RE.match(stripped)
        if header_match:
            sec_name = header_match.group(1).strip()
            current_section = Section(sec_name)
            sections.append(current_section)
            pending_comments = []
            current_group = None
            continue

        if stripped.startswith("//"):
            pending_comments.append(stripped)
            continue

        domain = stripped.lower()
        if current_section is not None:
            if current_group is None or pending_comments:
                current_group = EntityGroup(pending_comments)
                current_section.groups.append(current_group)
                pending_comments = []
            
            current_group.domains.append(domain)

    return sections


def build_formatted_content(sections: list[Section]) -> str:
    output = []
    for s_idx, section in enumerate(sections):
        output.append(f"// === START {section.name} ===\n\n")

        if section.description_comments:
            for c in section.description_comments:
                output.append(f"{c}\n")
            output.append("\n")

        # Sort entity groups alphabetically by company/entity name
        section.groups.sort(key=lambda g: g.sort_key)

        for g_idx, group in enumerate(section.groups):
            if group.comments:
                for c in group.comments:
                    output.append(f"{c}\n")
            
            # Sort domains within group
            group.domains.sort()

            for d in group.domains:
                output.append(f"{d}\n")
            
            output.append("\n")

        output.append("\n")

    result = "".join(output)
    # Ensure standard 2 newlines between sections, 1 newline between entry blocks
    result = re.sub(r"\n{4,}", "\n\n\n", result)
    result = result.strip() + "\n"
    return result


def check_file(filepath: Path) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []

    if not filepath.exists():
        return [f"File not found: {filepath}"], []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    # Check Windows CRLF
    if "\r\n" in content:
        warnings.append("Windows CRLF line endings detected. Use LF.")

    # Check trailing whitespace & consecutive blank lines
    consecutive_blank = 0
    all_domains = {}  # lower_domain -> line_num

    for idx, line in enumerate(lines):
        line_num = idx + 1
        if line != line.rstrip():
            errors.append(f"Line {line_num}: Trailing whitespace detected.")

        stripped = line.strip()
        if not stripped:
            consecutive_blank += 1
            if consecutive_blank > 2:
                errors.append(f"Line {line_num}: Excessive blank lines (found {consecutive_blank} empty lines in a row, max allowed is 2).")
        else:
            consecutive_blank = 0

        if not stripped or stripped.startswith("//"):
            continue

        if SECTION_HEADER_RE.match(stripped):
            continue

        domain = stripped
        if domain != domain.lower():
            errors.append(f"Line {line_num}: Domain '{domain}' must be lowercase ('{domain.lower()}').")

        if not DOMAIN_RE.match(domain.lower()):
            errors.append(f"Line {line_num}: Invalid domain format '{domain}'.")

        lower_domain = domain.lower()
        if lower_domain in all_domains:
            prev_line = all_domains[lower_domain]
            errors.append(f"Line {line_num}: Duplicate domain '{lower_domain}' (previously seen at line {prev_line}).")
        else:
            all_domains[lower_domain] = line_num

    # Check structural parsing & spacing consistency
    sections = parse_structure(filepath)

    for section in sections:
        group_keys = [g.sort_key for g in section.groups]
        sorted_group_keys = sorted(group_keys)
        if group_keys != sorted_group_keys:
            errors.append(f"Section '{section.name}': Company/Entity groups are not in alphabetical order.")
            for i in range(len(group_keys) - 1):
                if group_keys[i] > group_keys[i + 1]:
                    errors.append(
                        f"  -> Order issue in '{section.name}': Group '{group_keys[i]}' comes before '{group_keys[i+1]}'."
                    )

        for group in section.groups:
            sorted_domains = sorted(group.domains)
            if group.domains != sorted_domains:
                group_label = group.comments[0] if group.comments else group.domains[0]
                errors.append(f"Section '{section.name}' ({group_label}): Short domains within group are not sorted alphabetically.")

    # Compare actual content with canonical formatted content to enforce exact spacing
    canonical = build_formatted_content(sections)
    if content != canonical:
        errors.append("File formatting and line spacing does not match canonical style (e.g. missing blank lines between entries or extra spacing).")

    return errors, warnings


def format_and_fix(filepath: Path):
    sections = parse_structure(filepath)
    formatted = build_formatted_content(sections)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(formatted)

    print(f"Successfully formatted and sorted {filepath}")


def main():
    fix_mode = "--fix" in sys.argv

    if fix_mode:
        format_and_fix(LIST_FILE)

    errors, warnings = check_file(LIST_FILE)

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  [WARN] {w}")

    if errors:
        print("Verification Failed with errors:")
        for e in errors:
            print(f"  [ERROR] {e}")
        if not fix_mode:
            print("\nRun 'python3 fmt.py --fix' to automatically resolve ordering and formatting issues.")
        sys.exit(1)
    else:
        print("Verification Succeeded! All checks passed for list.txt.")
        sys.exit(0)


if __name__ == "__main__":
    main()
