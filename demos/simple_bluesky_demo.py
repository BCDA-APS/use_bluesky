'''
simple bluesky demonstration


start in a terminal with: 
   ipython --profile=bluesky

then execute these lines from the terminal
'''

import epics

IOC = 'prj:'
epics.caput(IOC+'userCalc1.CALC', 'rndm')
epics.caput(IOC+'userCalc1.SCAN', '.2 second')
epics.caput(IOC+'EnableUserCalcs', 1)


wh_pos()
m1.move(2)
mov(m1, 0)
noisy.describe
noisy.describe_configuration()
RE(scan([noisy], m1, 1, 5, 20), LiveTable([noisy, m1]))
RE(scan([noisy], m1, 1, 5, 20), LivePlot('noisy', 'm1'))
!mov
mov(m1, 0)
history


# setup "our detector" that is configured in ophyd as "noisy"
epics.caput(IOC+'userCalc1.INAN', IOC+'m1.RBV')
epics.caput(IOC+'userCalc1.INBN', IOC+'m2.RBV')
epics.caput(IOC+'userCalc1.C', '0.05')
epics.caput(IOC+'userCalc1.D', '10')
# simple noisy signal, proportional to motor m1
epics.caput(IOC+'userCalc1.CALC', 'A+C*(rndm-0.5)')
epics.caput(IOC+'userCalc1.SCAN', '.2 second')
epics.caput(IOC+'EnableUserCalcs', '1')
epics.caput(IOC+'userCalc1.CALC', 'D*cos(A+B+C*rndm)^2')
RE(
    outer_product_scan([noisy], m1, -.5, .5, 10, m2, -.7, .7, 10, True), 
    LiveMesh('m1', 'm2', 'noisy', xlim=(-.5,.5), ylim=(-.7,.7), clim=(0, 10)),
    calc=epics.caget("prj:userCalc1.CALC")
)
