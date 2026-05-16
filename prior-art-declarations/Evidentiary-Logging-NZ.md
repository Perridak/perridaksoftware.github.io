
# **Defensive Publication:  
A Simple Local Hash‑Chained Append‑Only Log for Evidentiary Data Integrity (New Zealand)**

## **Abstract**

This document describes a minimal, local, append‑only logging mechanism intended to preserve the evidentiary integrity of application data. Each log entry contains a cryptographic hash of the previous entry, forming a hash chain. The design is based on long‑established cryptographic timestamping techniques and decades of prior art in secure audit trails, WORM storage, and forensic logging. The system uses a single local file, optional backups, and a separate verification tool to detect tampering. It does not employ distributed consensus, remote attestation, multi‑datastore architectures, or hardware trust anchors. This publication establishes prior art for this design and clarifies its non‑infringing scope under New Zealand law.

---

# **1. Background**

Many software systems require a verifiable record of changes to data for operational, compliance, or evidentiary purposes. A tamper‑evident log provides a chronological chain of events that can support forensic analysis and legal review under the *Evidence Act 2006 (NZ)* and relevant common‑law principles governing digital evidence. This document defines a minimal implementation that relies on established public techniques and avoids patented architectural elements.

---

# **2. Prior Art Foundations**

The design is based on the following established techniques:

- Cryptographic timestamping and hash‑chaining methods introduced in the early 1990s  
- Write‑Once‑Read‑Many (WORM) audit logs used in financial and compliance systems  
- Forensic audit trails employing hash‑linked entries  
- Public cryptographic hash functions such as SHA‑1 and SHA‑256  
- Append‑only logging mechanisms used in early operating systems  

These references demonstrate that the core mechanism is not novel and is widely known.

---

# **3. System Overview**

The system consists of:

- A single local log file  
- An append‑only write process  
- A hash chain linking entries  
- An optional backup mechanism  
- A verification tool that recomputes the chain  

The system operates entirely on a local device and does not require networked components.

---

# **4. Architecture Diagram**

```
+---------------------------+
| Application Data Changes  |
+-------------+-------------+
              |
              v
+---------------------------+
| Append-Only Log Writer    |
+-------------+-------------+
              |
              v
+---------------------------+
| Local Log File            |
| [Entry N]                 |
|   - Timestamp             |
|   - Data Delta            |
|   - Hash(prev entry)     |
+-------------+-------------+
              |
              v
+---------------------------+
| Optional Backup Copy      |
+---------------------------+

Verification Tool:
- Reads log file
- Recomputes hash chain
- Reports tampering if mismatch
```

---

# **5. Log Entry Format**

Each log entry contains:

- Timestamp  
- Data change  
- Hash of the previous entry  
- Optional metadata  

Example:

```
{
  "timestamp": "2026-05-14T10:15:00+12:00",
  "change": "Data modification",
  "prev_hash": "a3f9c1...",
  "hash": "b7d4e2..."
}
```

---

# **6. Verification Process**

A verification tool performs the following steps:

1. Reads the log sequentially  
2. Recomputes each entry’s hash  
3. Confirms that each `prev_hash` matches the previous entry’s computed hash  
4. Reports any mismatch as evidence of tampering  

This process is deterministic and requires no external services.

---

# **7. Non‑Infringing Scope**

The system does not include:

- Multi‑datastore architectures  
- Remote attestation  
- Cloud‑based verification  
- Distributed consensus  
- Blockchain replication  
- Hardware trust anchors  
- Behavioural analytics  
- Automated tamper reconstruction  
- Intrusion detection  
- Server‑side log correlation  

The design is limited to classical, well‑known techniques.

---

# **8. New Zealand Evidentiary Context**

The system is designed to support evidentiary use under New Zealand law, including:

### **8.1. Admissibility**
Under the *Evidence Act 2006 (NZ)*, electronic records may be admissible if they are relevant and not excluded by other rules. A hash‑chained log supports admissibility by demonstrating that records have not been altered.

### **8.2. Reliability**
Section 7 and Section 8 require that evidence be reliable and not unduly prejudicial. A deterministic hash‑chain verification process supports reliability by providing a clear method for detecting tampering.

### **8.3. Authentication**
Section 9 requires evidence to be authenticated. A verifiable hash chain provides a transparent mechanism for demonstrating authenticity.

### **8.4. Weight of Evidence**
Courts may consider the integrity and provenance of digital records when determining their evidential weight. A verifiable chain of changes may assist in disputes involving data integrity or contested actions.

### **8.5. Forensic Analysis**
The verification process allows forensic examiners to confirm whether the log has been altered, supporting expert testimony where required.

---

# **9. Defensive Purpose**

Publication of this document:

- Establishes public prior art  
- Prevents others from patenting this design  
- Provides a clear non‑infringing scope  
- Documents reliance on long‑established techniques  
- Supports evidentiary use in New Zealand legal contexts  

This serves as a defensive intellectual‑property measure.

---

# **10. Conclusion**

This document defines a simple, local, hash‑chained append‑only log suitable for evidentiary use across a wide range of applications. The design is grounded in decades of prior art and avoids patented architectural elements. Publication establishes a defensive position and protects the design from future patent claims.

