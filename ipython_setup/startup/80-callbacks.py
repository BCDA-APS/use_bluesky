print(__file__)

# custom callbacks

import APS_BlueSky_tools.callbacks
import APS_BlueSky_tools.filewriters

# collect last scan's documents into doc_collector.documents
# doc_collector = APS_BlueSky_tools.callbacks.DocumentCollectorCallback()
# callback_db['doc_collector'] = RE.subscribe(doc_collector.receiver)

# write scans to SPEC data file
specwriter = APS_BlueSky_tools.filewriters.SpecWriterCallback()
# make the SPEC file in /tmp (assumes OS is Linux)
specwriter.newfile(os.path.join("/tmp", specwriter.spec_filename))
callback_db['specwriter'] = RE.subscribe(specwriter.receiver)
