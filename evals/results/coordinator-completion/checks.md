# Bounded discovery and completion evidence

The installed Harness 0.12.0 candidate at `3d9c199d06b8d0c6828d232548ef76b9be51196b` ran three fixture-backed execution-matrix cases with Codex CLI 0.171.0, gpt-6-astra and medium reasoning effort. Each case used one fresh Harness-arm trial. All three exited successfully and their responses met the case expectations on inspection.

| Case | Decision required | Observed response |
| --- | --- | --- |
| `execution-review-delayed-fix` | Use the remaining allowance on frozen A while the correction is outstanding. Reserve B for verification. | Reported the blocker at 09:02, scheduled retry and cancellation checks on A through 09:06, and called for one consolidated handback with unfinished scope identified. It reserved the 09:17 revision B for focused verification. |
| `execution-clean-partial-audit` | Account for a request covering native and web when the receipt covers only native. | Accepted the native evidence and assigned the outstanding web caller audit before overall signoff. |
| `execution-clean-complete-audit` | Close a native-only request when that same receipt and its preflight evidence suffice. | Marked the request complete with no further review. |

The first invocation stopped at runner preflight because its output directory was inaccessible to the browser sandbox. Repeating with a sandbox-visible evidence directory produced all three responses. These synthetic prompts exercise policy interpretation. They simulate the review clock and provide no estimate of live-review reliability.
