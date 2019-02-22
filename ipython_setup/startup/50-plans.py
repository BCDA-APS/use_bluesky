print(__file__)

"""local, custom Bluesky plans (scans)"""


# example using an Excel file to provide a list of samples to scan

def run_Excel_file(xl_file):
    """
    example of reading a list of samples from Excel spreadsheet
    
    USAGE::
    
        summarize_plan(run_Excel_file("sample_example.xlsx"))
        RE(run_Excel_file("sample_example.xlsx"))
    """
    assert os.path.exists(xl_file)
    xl = APS_utils.ExcelDatabaseFileGeneric(os.path.abspath(xl_file))
    yield from beforePlan()
    for row in xl.db.values():
        scan_command = row["Scan Type"].lower()
        if scan_command == "step_scan":
            yield from step_scan(
                row["sx"],  # label must match cell string EXACTLY
                row["sy"], 
                row["Thickness"], 
                row["Sample Name"],
                # add all input as scan metadata, ensure the keys are clean
                #md={APS_utils.cleanupText(k): v for k, v in row.items()},
                md={cleanupText(k): v for k, v in row.items()},
                ) 
    yield from afterPlan()


def step_scan(pos_X, pos_Y, thickness, scan_title, md={}):
    """
    collect SAXS data
    """
    yield from bps.mv(
        m2, pos_X,
        m3, pos_Y,
    )
    print(f"scan: {scan_title}")
    yield from bp.scan([scaler], m1, -5, 5, 8, md=md)


def beforePlan():
    """things to be done before every data collection plan"""
    yield from bps.mv(
        shutter, "open",    # for example
    )

    
def afterPlan():
    """things to be done after every data collection plan"""
    yield from bps.mv(
        shutter, "close",   # for example
        m1, 0,              # park the motors
        m2, 0,
        m3, 0,
    )
