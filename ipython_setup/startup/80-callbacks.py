print(__file__)

# custom callbacks

# write scans to SPEC data file
specwriter = APS_filewriters.SpecWriterCallback()
#_path = "/tmp"      # make the SPEC file in /tmp (assumes OS is Linux)
_path = os.getcwd() # make the SPEC file in current working directory (assumes is writable)
specwriter.newfile(os.path.join(_path, specwriter.spec_filename))
callback_db['specwriter'] = RE.subscribe(specwriter.receiver)
print(f"""
  writing to SPEC file: {specwriter.spec_filename}
  >>>>   Using default SPEC file name   <<<<
  file will be created when bluesky ends its next scan
  to change SPEC file, use command:   newSpecFile('title')
""")
