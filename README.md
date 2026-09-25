# GraphSentinel

An open, multimodal graph neural network framework for lateral movement
detection in enterprise networks.

## Research Question

Does combining behavioral anomaly detection with relational graph-based
learning over multimodal enterprise telemetry improve the detection and
early identification of lateral movement?

## Core Telemetry

GraphSentinel integrates three telemetry modalities:

- Identity / authentication
- Network flow
- Endpoint / process activity

## Detection Stack

### Behavioral baselines
- Isolation Forest
- One-Class SVM

### Graph models
- GraphSAGE
- Graph Attention Network (GAT)

### Temporal analysis
- Sliding-window temporal graph analysis
- TGN-style temporal modeling as an advanced extension

### Detection
Calibrated behavioral, graph, and temporal evidence is combined into a
hybrid risk signal.

## Key Research Outputs

- Lateral movement detection
- Attack-chain reconstruction
- Hop-index early detection metric
- Detection latency
- MITRE ATT&CK mapping
- GAT-based explainability
- Multimodal ablation studies
- Analyst-facing dashboard

## Primary Dataset

LANL Comprehensive Multi-Source Cyber-Security Events Dataset.

DARPA OpTC is a secondary validation dataset where practical.

## Project Status

Early development.

## Repository Structure

```text
GraphSentinel/
├── data/
├── configs/
├── docs/
├── models/
├── notebooks/
├── scripts/
├── src/
│   └── graphsentinel/
│       ├── ingestion/
│       ├── schema/
│       ├── features/
│       ├── graph/
│       ├── models/
│       ├── detection/
│       ├── evaluation/
│       ├── attack_chain/
│       ├── explainability/
│       └── dashboard/
├── tests/
├── logs/
├── artifacts/
├── README.md
├── pyproject.toml
└── requirements.txt
