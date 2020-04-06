logger.info(__file__)

# custom callbacks

# write scans to SPEC data file
specwriter = APS_filewriters.SpecWriterCallback()
#_path = "/tmp"      # make the SPEC file in /tmp (assumes OS is Linux)
_path = os.getcwd() # make the SPEC file in current working directory (assumes is writable)
specwriter.newfile(os.path.join(_path, specwriter.spec_filename))
callback_db['specwriter'] = RE.subscribe(specwriter.receiver)
logger.info(f"""
  writing to SPEC file: {specwriter.spec_filename}
  >>>>   Using default SPEC file name   <<<<
  file will be created when bluesky ends its next scan
  to change SPEC file, use command:   newSpecFile('title')
""")


def spec_comment(comment, doc=None):
    # supply our specwriter to the standard routine
    APS_filewriters.spec_comment(comment, doc, specwriter)


def newSpecFile(title, scan_id=1):
    """
    user choice of the SPEC file name
    
    Wraps ``apstools.filewriters.SpecWriterCallback().newfile()``
    
    1. cleans up title from user, 
    2. prepends month and day
    3. appends file extension
    """
    global specwriter
    mmdd = str(datetime.now()).split()[0][5:].replace("-", "_")
    clean = APS_utils.cleanupText(title)
    fname = "%s_%s.dat" % (mmdd, clean)
    if os.path.exists(fname):
        logger.warning(f">>> file already exists: {fname} <<<")
        specwriter.newfile(fname, RE=RE)
        handled = "appended"
        
    else:
        specwriter.newfile(fname, scan_id=scan_id, RE=RE)
        handled = "created"

    logger.info(f"SPEC file name : {specwriter.spec_filename}")
    logger.info(f"File will be {handled} at end of next bluesky scan.")
