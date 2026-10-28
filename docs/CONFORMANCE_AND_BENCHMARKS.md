# PIIS — Conformance and Comparative Evaluation

*Exploratory discussion notes; not normative test procedures.*

## 1. Functional conformance first

A claim of compatibility must identify the contract and supported capabilities, explain any unsupported behavior, and provide evidence that the stated observable outcomes and effects are preserved. Reading the file or importing a configuration is insufficient.

## 2. Compare observable results

Once conforming, implementations may be evaluated under equivalent inputs, initial states, workload and external dependencies. Internal architectures, queueing mechanisms, concurrency strategies and programming methods may differ completely.

**Do not subtract internal queues, scheduling, waiting or other architecture-dependent time from the primary end-to-end measurement.** If a compliant implementation delivers the full contracted outcome faster, that is a real advantage in that tested scenario.

## 3. Preliminary metrics

| Metric | Intent |
|---|---|
| End-to-end time | Full elapsed time until the specified functional outcome is observably complete |
| P50/P95/P99 | Distribution of end-to-end completion times |
| Conforming throughput | Correct contract-compliant outcomes per second |
| CPU | Resource usage and CPU time per completed outcome |
| RAM | Sustained and peak resident memory |
| Scalability | Outcomes and resource demand as load and concurrency grow |
| Recovery | Time required to regain the contracted functional behavior after failure |
| Integrity | Missing, duplicate, inconsistent, or otherwise nonconforming effects |
| Operational cost | Documented cost of the entire solution under test |
| Migration effort | Person-hours and interventions to reach verified conformance |

## 4. Fairness is not identical implementation

The purpose of a benchmark is to reveal technological differences, not suppress them. Record workload, test data, hardware, resource ceilings, dependency conditions, measurement boundaries and exceptions. Distinguish conformance from performance. Do not call one implementation universally superior based on one workload.

## 5. Open work

Precise measurement boundaries, state models, evidence formats, benchmark profiles and inter-run reproducibility remain to be specified.
