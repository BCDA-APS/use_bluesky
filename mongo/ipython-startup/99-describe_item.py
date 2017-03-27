
import pyRestTable
from ophyd.epics_motor import EpicsMotor

# example user function

def describe_item(item):
    '''
    describe an EPICS item from its configuration in a table

	example usage::

		In [54]: print(describe_motor(m1))
		================ =============== ============= ============== ================== ==============
		field            m1_acceleration m1_motor_egu  m1_user_offset m1_user_offset_dir m1_velocity   
		================ =============== ============= ============== ================== ==============
		dtype            number          string        number         integer            number        
		enum_strs                                                     ['Pos', 'Neg']                   
		lower_ctrl_limit -1e+300         None          -1e+300        None               0.1           
		precision        5                             5                                 5             
		shape            []              []            []             []                 []            
		source           PV:xxx:m1.ACCL  PV:xxx:m1.EGU PV:xxx:m1.OFF  PV:xxx:m1.DIR      PV:xxx:m1.VELO
		units            sec             None          degrees        None               degrees       
		upper_ctrl_limit 1e+300          None          1e+300         None               0.0           
		================ =============== ============= ============== ================== ==============


    '''
    #assert(isinstance(item, EpicsMotor))
    _d = item.describe_configuration()
    column_names = _d.keys()

    rd = {}
    for v in _d.values():
        for k in v.keys():
            rd[k] = k
    row_names = list(rd.keys())
    del rd

    t = pyRestTable.Table()
    t.labels = sorted(column_names)
    for r in sorted(row_names):
        row = [r,]
        for c in t.labels:
            row.append(_d[c].get(r, ''))
        t.rows.append(row)
    t.labels.insert(0, 'field')
    return t.reST()

