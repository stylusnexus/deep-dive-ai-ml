# OPS-STD-04 — Standard Operating Envelope

## Scope and authority

This standard defines the operating envelope for every turbine in the
fleet. It is the single authority for the limits below. Site profiles and
local procedures reference it and must not restate its numbers, because a
restated limit becomes a second source that drifts silently once one copy
is revised. Where a site requires a different limit, the difference is
recorded as a site variance against the specific parameter, with an owner
and an expiry date, and the variance is listed in the site profile rather
than written into a local copy of this document.

## Gearbox temperature

The gearbox oil temperature must not exceed 82 degrees Celsius during
continuous operation. Between 82 and 90 degrees the turbine enters derated
operation automatically, reducing output until the temperature returns
below the continuous limit. Above 90 degrees the turbine performs a
controlled shutdown. Derated operation is a normal control response and is
not a fault in itself, but sustained derating indicates a developing
problem: a turbine that derates on temperature for more than four hours in
any twenty-four is raised to the regional desk for review even where it
never approaches the shutdown threshold.

## Vibration

Nacelle vibration above 0.55 mm/s RMS sustained for more than thirty
minutes triggers a Level 2 alert. Above 0.80 mm/s the turbine shuts down
immediately and requires physical inspection before restart. The
thirty-minute qualifier matters: transient excursions above the Level 2
threshold are common in turbulent inflow and do not indicate a developing
fault, so alerting on instantaneous readings produces noise that trains
operators to ignore the alert. The immediate-shutdown threshold has no
such qualifier because the failure modes it guards against develop faster
than any averaging window would tolerate.

## Rotor speed and overspeed protection

Rated rotor speed is 14.6 rpm. The overspeed trip is set at 17.2 rpm and
is implemented independently of the main controller, so that a controller
fault cannot disable it. The trip is tested at every routine inspection
and the test result is recorded against the turbine rather than against
the inspection, which allows a history to be read per machine. A failed
overspeed test takes the turbine out of service immediately and is not
subject to any deferral provision.

## Environmental limits

Turbines shut down automatically above 25 m/s mean wind speed measured
over ten minutes, and resume when the mean falls below 20 m/s for a
sustained period. The gap between the two thresholds prevents repeated
stop-start cycling in gusty conditions, which imposes more fatigue on the
drivetrain than either continuous operation or a clean shutdown would.
Icing detection triggers a shutdown independently of wind speed.
