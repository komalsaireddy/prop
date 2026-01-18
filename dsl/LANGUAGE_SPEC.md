# Governed Drone Behavior Language (GDBL) – v1.0

## Purpose
GDBL allows users to define **high-level drone behavior intent**
without any access to flight control, motors, speed, or navigation.

## Design Principle
Users define **WHAT** the drone should do,
never **HOW** it flies.

## Grammar
Each file contains exactly ONE rule.

RULE <rule_name>
WHEN <event>
IF <signal> <operator> <value>   (optional)
DO <action>

## Supported Events
- anomaly_detected
- obstacle_detected
- battery_low
- gps_lost

## Supported Signals
- confidence (0.0 – 1.0)
- risk_level (future)

## Supported Actions
- HOVER
- STOP
- RETURN_HOME
- ABORT

## Forbidden
- Motor control
- Speed / altitude / direction
- Timing loops
- Hardware access
- User-defined actions

## Safety
All actions are subject to a non-bypassable safety kernel.
The system may override or reject user intent at runtime.

## Example
RULE avoid_risk
WHEN anomaly_detected
IF confidence > 0.7
DO HOVER
