GOVERNED DRONE PLATFORM – ARCHITECTURE CONTRACT (v1)

--------------------------------------------------
PURPOSE
--------------------------------------------------
This platform enables safe programming of drone BEHAVIOR INTENT
while enforcing non-bypassable safety and human control.

Users never control flight.
Users never bypass safety.
Users never access hardware.

--------------------------------------------------
HIGH-LEVEL PIPELINE
--------------------------------------------------

User (GUI)
  |
  v
Behavior Code (GDBL)
  |
  v
Compiler
  - Syntax validation
  - Safety validation
  - Forbidden action rejection
  |
  v
Intermediate Representation (IR)
  |
  v
Intent Engine
  - Converts IR + AI signals into intent
  |
  v
Safety Kernel (FINAL AUTHORITY)
  - Evaluates intent against safety rules
  - May APPROVE, OVERRIDE, or REJECT
  |
  v
Action Executor (SIMULATED / FUTURE HARDWARE)

--------------------------------------------------
STRICT SEPARATION OF RESPONSIBILITIES
--------------------------------------------------

USER CONTROLS:
- Writes GDBL behavior rules
- Starts / aborts execution
- Views logs and decisions

USER CANNOT:
- Control motors
- Set speed, altitude, or direction
- Define navigation paths
- Disable safety
- Access sensors directly
- Access flight controller

--------------------------------------------------
COMPILER RESPONSIBILITIES
--------------------------------------------------
- Enforce language structure
- Reject forbidden actions at COMPILE TIME
- Produce a safe, minimal IR
- Never execute behavior

--------------------------------------------------
INTENT ENGINE RESPONSIBILITIES
--------------------------------------------------
- Consume IR
- Consume AI / sensor signals (read-only)
- Produce a single high-level intent
- Never bypass safety

--------------------------------------------------
SAFETY KERNEL (NON-BYPASSABLE)
--------------------------------------------------
The safety kernel has FINAL AUTHORITY.

It can:
- Approve intent
- Override intent
- Reject intent

It cannot be bypassed by:
- User code
- GUI
- AI
- Compiler

All decisions are logged with reasons.

--------------------------------------------------
AI ROLE (STRICTLY LIMITED)
--------------------------------------------------
AI:
- Provides signals only (e.g., confidence, anomaly_detected)
- Does NOT control motors
- Does NOT make final decisions
- Does NOT execute actions

AI is advisory, not authoritative.

--------------------------------------------------
LOGGING & EXPLAINABILITY
--------------------------------------------------
Every execution produces logs containing:
- Timestamp
- Intent
- Safety decision
- Final action
- Reason code

Logs are visible in:
- GUI (Action Logs tab)
- Persistent log file

--------------------------------------------------
HARDWARE INTEGRATION (FUTURE)
--------------------------------------------------
Flight controller (PX4 / ArduPilot):
- Remains sealed
- Receives only high-level safe commands
- Never exposed to user code

--------------------------------------------------
KEY GUARANTEE
--------------------------------------------------
This platform can always say NO.
Safety is enforced by architecture, not by trust.
