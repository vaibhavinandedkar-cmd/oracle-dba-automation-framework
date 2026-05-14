#!/bin/bash
# ================================================
# Central Oracle DBA Automation Framework
# Author: Vaibhavi Nandedkar
# ================================================

echo "================================================"
echo "🚀 Starting Oracle DBA Automation Framework"
echo "Start Time: $(date)"
echo "================================================"

cd /home/oracle/oracle-dba-automation-framework

python3 src/health_check.py
python3 src/tablespace_monitor.py

echo "================================================"
echo "✅ Framework Execution Completed Successfully - $(date)"
echo "================================================"
