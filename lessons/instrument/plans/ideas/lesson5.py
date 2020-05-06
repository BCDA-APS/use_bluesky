
"""
lesson 5 : lineup scans, with refinement
"""

__all__ = [
    'lineupScans', 
    # 'myCallback',
    ]

from ...session_logs import logger
logger.info(__file__)

import bluesky.plans as bp
import bluesky.plan_stubs as bps
import pyRestTable
from ...framework import bec, RE


def lineupScans(scaler, motor, start, end, numPts=23, numScans=3):
    """
    show simple peak finding by repeated scans with refinement

    basically::

        RE(bp.scan([scaler], motor, start, end, numPts))

        %mov motor peaks["cen"]["scaler"]
        fwhm=peaks["fwhm"]["scaler"]
        RE(bp.rel_scan([scaler], motor, -fwhm, fwhm, numPts))

        %mov motor peaks["cen"]["scaler"]
        fwhm=peaks["fwhm"]["scaler"]
        RE(bp.rel_scan([scaler], motor, -fwhm, fwhm, numPts))
    """
    yield from bps.mv(motor, start)
    yield from bp.rel_scan([scaler], motor, 0, end-start, numPts)
    fwhm = bec.peaks["fwhm"][scaler.name]
    cen = bec.peaks["cen"][scaler.name]
    results = [(RE.md["scan_id"], cen, fwhm)]

    for _again in range(numScans-1):
        logger.info("starting rescan %d", (_again+1))
        yield from bps.mv(motor, cen)
        yield from bp.rel_scan([scaler], motor, -fwhm, fwhm, numPts)
        if scaler.name not in bec.peaks["fwhm"]:
            logger.error("no data in `bec.peaks`, end of these scans")
            break
        fwhm = bec.peaks["fwhm"][scaler.name]
        cen = bec.peaks["cen"][scaler.name]
        results.append((RE.md["scan_id"], cen, fwhm))
    
    tbl = pyRestTable.Table()
    tbl.addLabel("scan_id")
    tbl.addLabel("center")
    tbl.addLabel("FWHM")
    for row in results:
        tbl.addRow(row)
    logger.info("summary results:\n%s", str(tbl))
