# EDDN EventListener Module
The EventListener Module exposes CMDR data via EDDN FSDJump logs to a Notification object (eg: factionStatusNotification).

A Notification object compares every reported FSDJump data against its own set of (desireable) parameters, and reports matches to a txt file.

This module currently provides such reports on Faction's Active Statuses, filtered by a number of other variables: system population, faction influence%, distance from Sol, comparison against a premade list of systems, and so on.

This program would be currently useful for inferring stations that may have high (or low) commodity prices by their active faction statuses and overall influence%.