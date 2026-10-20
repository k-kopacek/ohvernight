"""Habitat data is not legal closure geometry."""
from lib.common import source

def main():
    src = source("wildlife")
    raise RuntimeError(src["reason"] if not src.get("enabled") else
                       "A reviewed replacement habitat adapter has not been configured")

if __name__ == "__main__":
    main()
