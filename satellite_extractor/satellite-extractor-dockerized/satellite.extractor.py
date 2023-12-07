# satellite.extractor.py
import argparse
import config
import satellite_extractor.extractor_original as sat

if __name__ == "__main__":
 sat.run(
    TIMESTAPS = config.TIMESTAPS,
    CLIENT_ID = config.CLIENT_ID,
    CLIENT_SECRET = config.CLIENT_SECRET
    )