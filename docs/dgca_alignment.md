# DGCA Safety Alignment (Prototype Level)

This prototype aligns with DGCA safety principles by design.

## Human-in-the-Loop
- Manual override is always respected
- Supervisor controller can abort at any time

## Geofencing
- Mandatory geofence checks
- No user override

## Fail-safe Behavior
- Low battery → RETURN_HOME
- GPS loss → REJECT action

## Non-Weaponization
- No payload control
- No targeting logic
- No flight dynamics exposed

## Explainability
- Every decision is logged
- Overrides are human-readable

## Scope Disclaimer
This is a student prototype demonstrating
software governance concepts, not a certified UAS.
