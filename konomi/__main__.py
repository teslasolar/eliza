"""Allow running as: python -m konomi"""
from konomi.validate import main
import sys
sys.exit(main() or 0)
