# Open-source space software: SBOM + security-policy inventory (2026-10-15)

Paper 1's original number. Public GitHub data, read by `scripts/space_sbom_inventory.py`. Definitions live in the script header. A dated snapshot: bound every sentence to these repos on this date.

**Of 9 repositories: 1 publish an SBOM; 6 publish a security policy; 4 accept private vulnerability reports through GitHub; 4 have published a security advisory.** (1 rows have an unknown cell, see errors.)

| Project | Repo | Security policy | Private reporting | Advisories published | Maintainer SBOM | Last push | Latest release |
|---|---|---|---|---|---|---|---|
| cFS | [nasa/cFS](https://github.com/nasa/cFS) | [yes](https://github.com/nasa/cFS/security/policy) | no | 0 | no | 2026-10-15 | v7.0.1 2026-05-14 |
| cFS | [nasa/cFE](https://github.com/nasa/cFE) | [yes](https://github.com/nasa/cFE/security/policy) | no | 0 | no | 2026-10-09 | v7.0.1 2026-05-14 |
| cFS | [nasa/osal](https://github.com/nasa/osal) | [yes](https://github.com/nasa/osal/security/policy) | no | 0 | no | 2026-10-08 | v7.0.1 2026-05-14 |
| F Prime | [nasa/fprime](https://github.com/nasa/fprime) | [yes](https://github.com/nasa/fprime/security/policy) | yes | 36 | at build only: cmake/target/sbom.cmake | 2026-10-14 | v4.4.1 2026-10-07 |
| Yamcs | [yamcs/yamcs](https://github.com/yamcs/yamcs) | [yes](https://github.com/yamcs/yamcs/security/policy) | yes | 23 | no | 2026-10-05 | yamcs-5.13.6 2026-10-01 |
| OpenC3 COSMOS | [OpenC3/cosmos](https://github.com/OpenC3/cosmos) | [yes](https://github.com/OpenC3/cosmos/security/policy) | yes | 17 | yes: v7.4.1/09_24_26_14_44_25_sbom_ubi_v7.4.1.zip, v7.4.1/09_24_26_14_44_25_sbom_v7.4.1.zip | 2026-10-15 | v7.4.1 2026-09-24 |
| CryptoLib | [nasa/CryptoLib](https://github.com/nasa/CryptoLib) | no | yes | 20 | no | 2026-10-14 | v1.5.1 2026-09-23 |
| SLE tools | [yamcs/jsle](https://github.com/yamcs/jsle) | no | no | 0 | no | 2026-10-01 | jsle-1.1.0 2024-07-09 |
| SLE tools | [visionspacetec/sle-provider](https://github.com/visionspacetec/sle-provider) | no | unknown | 0 | no | 2025-06-30 (archived) | none  |

## Unknown cells (could not look, which is not the same as no)
- visionspacetec/sle-provider: private-reporting: gh: Repository must be public and not archived (HTTP 422)
