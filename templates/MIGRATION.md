# Cross-service migrations

Most work is a small change inside one service. A migration is different: a sequence of coordinated small changes across many services, moving the platform toward a shared end state.

Follow this pattern when the work is a migration, not a one-shot fix. Record it in the project's task list, not in `~/.ai`.

## Structure

Record the end state at the top of the migration's section in the project task list:

- The target shape. What every migrated service looks like when done.
- The invariants that hold during the migration. Name what must not be rotated, deleted, or changed.
- The slices, in order.

Each slice is one service's migration to the target shape. When its commits land, that service works under the new pattern and can go to the project's shared non-production environment.

## Slicing rules

- A slice is self-contained. It includes code, config, chart changes, tests, and documentation for one service.
- A slice does not change another service's behavior as a side effect.
- A slice is one batch of related commits, not necessarily one commit. Push the batch together once the service passes its own checks.
- Verify in the project's shared non-production environment before starting the next slice. A failed slice stops the sequence until the failure is understood.
- Standing constraints at the top of the migration stay frozen for the whole run. Do not relax one mid-migration to make a slice easier.

## Recording progress

- Mark a slice done only when it has landed and the acceptance step named in that slice has been verified.
- Do not mark a slice done from a unit test alone when the slice names a shared-environment check.
- When the end state is reached, archive the section the way that project's tracking rules describe.

## Mid-migration handoff

If a session ends mid-migration, write a handoff in the project's handoff location. Name the current slice, what verification already passed, what remains, and any decision that was not in the original plan. See [tool setup](../adapters/README.md#handoff-between-sessions).
