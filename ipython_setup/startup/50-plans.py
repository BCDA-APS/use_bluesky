print(__file__)

"""local, custom Bluesky plans (scans)"""

# example using an Excel file to provide a list of samples to scan

def run_Excel_file(xl_file):
    """
    example of reading a list of samples from Excel spreadsheet
    
    TEXT view of spreadsheet (Excel file line numbers shown)::
    
        [1] List of sample scans to be run              
        [2]                 
        [3]                 
        [4] scan    sx  sy  thickness   sample name
        [5] FlyScan 0   0   0   blank
        [6] FlyScan 5   2   0   blank
    """
    assert os.path.exists(xl_file)
    xl = APS_utils.ExcelDatabaseFileGeneric(os.path.abspath(xl_file))
    yield from beforePlan()
    for row in xl.db.values():
        scan_command = row["scan"].lower()
        if scan_command == "step_scan":
            yield from step_scan(row["sx"], row["sy"], row["thickness"], row["sample name"]) 
    yield from afterPlan()


def step_scan(pos_X, pos_Y, thickness, scan_title):
    """
    collect SAXS data
    """
    yield from bps.mv(
        m2, pos_X,
        m3, pos_Y,
    )
    scan_metadata = dict(
        sx = pos_X,
        sy = pos_Y,
        thickness = thickness,
        title = scan_title,
    )
    yield from bp.scan([scaler], m1, -5, 5, 25, md=scan_metadata)

def beforePlan():
    """things to be done before every data collection plan"""
    yield from bps.mv(
        shutter, "open",  # for example
    )

    
def afterPlan():
    """things to be done after every data collection plan"""
    yield from bps.mv(
        shutter, "close",  # for example
    )
