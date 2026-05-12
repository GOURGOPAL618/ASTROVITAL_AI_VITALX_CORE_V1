# Security Policy
## ASTROVITAL AI — VITALX CORE V1
**Maintained by:** Gouragopal Mohapatra — Independent Researcher  
**Contact:** GitHub [@GOURGOPAL618](https://github.com/GOURGOPAL618)  
**Effective Date:** May 2026

---

## Supported Versions

| Version | Status | Security Support |
|---|---|---|
| V1 — VITALX CORE | 🟢 Current | ✅ Actively Maintained |
| V1.5 — AEREXIS OMEGA | 🔵 In Development | ✅ Pre-release Security Review |
| V2.0 and above | ⏳ Planned | ⏳ Future |

Only the most current stable release receives active security patches and vulnerability responses.

---

## Scope of This Security Policy

This policy applies to all components of the ASTROVITAL AI — VITALX CORE V1 repository, including:

- All Python source files under `AI_CORE/src/`
- All Jupyter Notebooks under `VITALX_LAB/`
- All serialized model artifacts (`.pkl`, `.json`) under `MODEL_HANGAR/`
- All dataset files under `DATA_VAULT/`
- All pipeline configuration and environment files

This policy does **not** cover third-party dependencies (scikit-learn, Pandas, NumPy, etc.). Vulnerabilities in those libraries should be reported directly to their respective maintainers.

---

## Reporting a Vulnerability

ASTROVITAL AI takes the security and integrity of its research artifacts seriously. If you have discovered a vulnerability, a security concern, or a misuse risk within this repository, please follow the responsible disclosure process described below.

### How to Report

**Do not open a public GitHub Issue for security vulnerabilities.**

Report all security concerns privately via one of the following channels:

- **GitHub Private Security Advisory:** Use the "Report a Vulnerability" option under the Security tab of this repository.
- **Direct Contact:** Reach out via GitHub profile [@GOURGOPAL618](https://github.com/GOURGOPAL618) with the subject line: `[SECURITY] ASTROVITAL VITALX CORE V1 — Vulnerability Report`

### What to Include in Your Report

Please provide the following information to enable a thorough and timely assessment:

1. A clear description of the vulnerability or security concern
2. The specific file(s), component(s), or module(s) affected
3. Steps to reproduce the issue or a proof-of-concept demonstration
4. The potential impact or exploit scenario you have identified
5. Your recommended remediation approach, if available

### Response Timeline

| Stage | Target Timeframe |
|---|---|
| Acknowledgement of report received | Within 72 hours |
| Initial assessment and severity classification | Within 7 days |
| Remediation or mitigation patch | Within 30 days (critical), 60 days (moderate) |
| Public disclosure (coordinated) | After patch is released |

The researcher commits to coordinated disclosure — no vulnerability will be made public before a patch or official response has been prepared and communicated to the reporter.

---

## Security Considerations for Research Use

### Model Artifacts

The serialized `.pkl` model files in `MODEL_HANGAR/` are Python pickle objects. **Do not deserialize pickle files from untrusted or unverified sources.** Only load model artifacts directly from this official repository. Maliciously crafted pickle files can execute arbitrary code upon loading.

### Synthetic Dataset

All datasets in `DATA_VAULT/` are entirely synthetic — they contain no real astronaut physiological data, no personally identifiable information (PII), and no protected health information (PHI). There is no privacy risk associated with the dataset files in this repository.

### Jupyter Notebooks

Jupyter Notebooks may execute arbitrary Python code. Always review notebook cell contents before execution, particularly if you have received a copy of this repository from a secondary or unverified source. The canonical, trusted version of all notebooks is the one hosted at the official repository: `github.com/GOURGOPAL618/ASTROVITAL_AI_VITALX_CORE_V1`.

### Clinical Use Restriction

**VITALX CORE V1 is a research prototype. It is not certified, validated, or approved for clinical use, operational deployment, or any application involving real human patients or crew members.** Any deployment of this system in a real medical or mission-critical context without appropriate clinical validation, regulatory approval, and expert medical oversight would constitute a serious and potentially life-threatening misuse of this research artifact. The developer assumes no liability for any such misuse.

---

## Integrity Verification

To verify the integrity of files downloaded from this repository, SHA-256 checksums for all model artifacts and critical source files will be published in the `CHANGELOG.md` with each release. Always verify checksums before use in any research replication or derivative work.

---

## Acknowledgements

Responsible disclosure of genuine security concerns in research software serves the scientific community. The researcher sincerely thanks anyone who takes the time to identify and responsibly report a security issue in this project.

---

*© 2026 Gouragopal Mohapatra — ASTROVITAL AI — All Rights Reserved*