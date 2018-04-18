# WhatshAppened
Analytics tool for WhatsApp chat exports

Under development.

Current version: alpha-04

Recent changes:
alpha-04.1
- WALog datetime parsing now works with strptime() pattern
- WALog timestamp regex bug fixed (missing RTL char lead to false multi line detection)
- WAPanda added preliminary word count

alpha-04
- WALog parse logfile on creation
- regex for removable messages, e.g. placeholder for media-only messages
- message length and message frequency statistics in WAPanda

alpha-03
- added emoji analytics for WAPanda
- added anonymizing for WALog

Works only for German exports, statistics are dull, documentation nonexistent. Come back in a few days.
