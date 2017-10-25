print(__file__)

from collections import OrderedDict
from ophyd.device import (
    DynamicDeviceComponent as DDC,
    FormattedComponent as FC)


class swaitRecordChannel(Device):
    """channel of a synApps swait record: A-L"""

    value = FC(EpicsSignal, '{self.prefix}.{self._ch_letter}')
    input_pv = FC(EpicsSignal, '{self.prefix}.IN{self._ch_letter}N')
    input_trigger = FC(EpicsSignal, '{self.prefix}.IN{self._ch_letter}P')
    
    def __init__(self, prefix, letter, **kwargs):
        self._ch_letter = letter
        super().__init__(prefix, **kwargs)


def _swait_channels(attr_fix, id_range):
    defn = OrderedDict()
    for k in id_range:
        #key = '{letter}'.format(letter=k)
        defn[k] = (swaitRecordChannel, '', {'letter': k})
    return defn


class swaitRecord(Device):
    """synApps swait record: used as $(P):userCalc$(N)"""
    desc = Cpt(EpicsSignal, '.DESC')
    scan = Cpt(EpicsSignal, '.SCAN')
    calc = Cpt(EpicsSignal, '.CALC')
    val = Cpt(EpicsSignalRO, '.VAL')
    prec = Cpt(EpicsSignal, '.PREC')
    oevt = Cpt(EpicsSignal, '.OEVT')
    outn = Cpt(EpicsSignal, '.OUTN')
    odly = Cpt(EpicsSignal, '.ODLY')
    doln = Cpt(EpicsSignal, '.DOLN')
    dold = Cpt(EpicsSignal, '.DOLD')
    dopt = Cpt(EpicsSignal, '.DOPT')
    oopt = Cpt(EpicsSignal, '.OOPT')
    flnk = Cpt(EpicsSignal, '.FLNK')
    
    _channel_letters = "A B C D E F G H I J K L".split()
    # TODO: eliminate the ".channels"
    # Note that the scaler support has this also.
    channels = DDC(_swait_channels('chan', _channel_letters))
    
    def reset(self):
        """set all fields to default values"""
        self.scan.put("Passive")
        self.calc.put("0")
        self.prec.put("5")
        self.dold.put(0)
        self.doln.put("")
        self.dopt.put("Use VAL")
        self.flnk.put("0")
        self.odly.put(0)
        self.oopt.put("Every Time")
        self.outn.put("")
        for letter in self.channels.read_attrs:
            channel = self.channels.__getattr__(letter)
            channel.value.put(0)
            channel.input_pv.put("")
            channel.input_trigger.put("Yes")


def swait_setup_random_number(swait, **kw):
    """setup swait record to generate random numbers"""
    swait.reset()
    swait.scan.put("Passive")
    swait.calc.put("RNDM")
    swait.scan.put(".1 second")


def swait_setup_gaussian(swait, motor, center=0, width=1, scale=1, noise=0.05):
    """setup swait for noisy Gaussian"""
    # consider a noisy background, as well (needs a couple calcs)
    assert(isinstance(motor, EpicsMotor))
    assert(width > 0)
    assert(0.0 <= noise <= 1.0)
    swait.reset()
    swait.scan.put("Passive")
    swait.channels.A.input_pv.put(motor.user_readback.pvname)
    swait.channels.B.value.put(center)
    swait.channels.C.value.put(width)
    swait.channels.D.value.put(scale)
    swait.channels.E.value.put(noise)
    swait.calc.put("D*(0.95+E*RNDM)/exp(((A-b)/c)^2)")
    swait.scan.put("I/O Intr")


def swait_setup_lorentzian(swait, motor, center=0, width=1, scale=1, noise=0.05):
    """setup swait record for noisy Lorentzian"""
    # consider a noisy background, as well (needs a couple calcs)
    assert(isinstance(motor, EpicsMotor))
    assert(width > 0)
    assert(0.0 <= noise <= 1.0)
    swait.reset()
    swait.scan.put("Passive")
    swait.channels.A.input_pv.put(motor.user_readback.pvname)
    swait.channels.B.value.put(center)
    swait.channels.C.value.put(width)
    swait.channels.D.value.put(scale)
    swait.channels.E.value.put(noise)
    swait.calc.put("D*(0.95+E*RNDM)/(1+((A-b)/c)^2)")
    swait.scan.put("I/O Intr")


if False:       # demo & testing code
    
    epics.caput("xxx:userCalcEnable", "Enable")
    calc1 = swaitRecord("xxx:userCalc1")

    def simulate_peak(swait, motor, profile=None, start=-1.5, stop=-0.5):
        if profile is not None:
            simulator = dict(
                gaussian = swait_setup_gaussian,
                lorentzian = swait_setup_lorentzian,
            )[profile]
            kw = dict(
                center = start + np.random.uniform()*(stop-start), 
                width = 0.002 + 0.1*np.random.uniform(), 
                scale = 100000 * np.random.uniform(), 
                noise = 0.05 + 0.1*np.random.uniform())
            simulator(swait, motor, **kw)
        else:
            swait_setup_random_number(swait)

    def both_peaks():
        simulate_peak(calc1, m1, profile="gaussian")
        yield from bp.scan([noisy,], m1, start, stop, 219)
        simulate_peak(calc1, m1, profile="lorentzian")
        yield from bp.scan([noisy,], m1, start, stop, 219)
    
    RE(both_peaks())
