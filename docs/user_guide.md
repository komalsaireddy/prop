# User Guide – Governed Drone Platform

## How to Program Behavior
1. Open rule.txt
2. Write ONE behavior rule
3. Save and start mission

## What You Can Control
- High-level behavior intent only

## What You Cannot Control
- Motors
- Speed
- Altitude
- Navigation
- Safety rules

## What Happens at Runtime
1. AI produces signals
2. Rule produces intent
3. Safety kernel decides final action
4. Decision is logged

## If Your Rule Is Unsafe
The compiler will reject it with a clear error.
