# OCCID-only closed-loop demonstration

`end_to_end_ooda.py` exercises the Control contract without Sigma, HiveLink, MPFC, a broker, a flight controller, or network services.

The scenario creates one objective and a `TaskInformation` with `InformationIntent.SEARCH`. `TaskInformation` is a practical schema specialization of the ontological `Task` class: it inherits the common Task record and adds only its controlled information-intent vocabulary. The Task contains the operator instruction and location reference but no assignee. A separate `Authority` record is issued, then an `Assignment` binds the Task to an executor under that authority. A `Plan` correlates the objective, task, actor, and assignment. An `Execution` records one runtime attempt.

Dispatch uses `ExecutionCommand(EXECUTE)` inside `CommandMessage`. The executor returns `ExecutionAcceptance`, then runtime progress through `Execution`, `TaskDelta`, and `ExecutionStatusReport`. Completion revises the Assignment and Objective without changing their stable logical IDs.

The demonstration asserts these boundaries:

- Task intent is preserved by the practical Task schema independently of assignment.
- Assignment references both Task and Authority.
- Execution references Assignment and remains runtime State.
- `task_id`, `assignment_id`, and `execution_id` are distinct correlation identities.
- dispatch identity is preserved through command, acceptance, and status report.
- every trace entry crosses a real OCCID MsgPack encode/decode boundary.

Run it with:

```bash
python end_to_end_ooda.py
python end_to_end_ooda.py --json
python -m unittest tests.test_end_to_end_ooda
```
