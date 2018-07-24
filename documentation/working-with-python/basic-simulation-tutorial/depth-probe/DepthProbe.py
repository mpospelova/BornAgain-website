"""
Basic example of depth-probe simulation with BornAgain.
"""
import bornagain as ba
from bornagain import deg, angstrom, nm


def get_sample():
    """
    Constructs a sample with one resonating Ti/Pt bilayer
    """

    # define materials
    m_Si = ba.HomogeneousMaterial("Si", 3.3009e-05, 0.0)
    m_Ti = ba.HomogeneousMaterial("Ti", -3.0637e-05, 1.5278e-08)
    m_TiO2 = ba.HomogeneousMaterial("TiO2", 4.1921e-05, 8.1293e-09)
    m_Pt = ba.HomogeneousMaterial("Pt", 1.0117e-04, 3.01822e-08)
    m_D2O = ba.HomogeneousMaterial("D2O", 1.0116e-04, 1.8090e-12)

    # create layers
    l_Si = ba.Layer(m_Si)
    l_Ti = ba.Layer(m_Ti, 130.0 * angstrom)
    l_Pt = ba.Layer(m_Pt, 320.0 * angstrom)
    l_Ti_top = ba.Layer(m_Ti, 100.0 * angstrom)
    l_TiO2 = ba.Layer(m_TiO2, 30.0 * angstrom)
    l_D2O = ba.Layer(m_D2O)

    # construct sample from top to bottom
    sample = ba.MultiLayer()
    sample.addLayer(l_Si)

    sample.addLayer(l_Ti)
    sample.addLayer(l_Pt)

    sample.addLayer(l_Ti_top)
    sample.addLayer(l_TiO2)
    sample.addLayer(l_D2O)

    return sample


def get_simulation():
    """
    Returns a depth-probe simulation.
    """
    simulation = ba.DepthProbeSimulation()
    simulation.setBeamParameters(10 * angstrom, 5000, 0.0 * deg, 1.0 * deg)
    simulation.setZSpan(500, -100 * nm, 100 * nm)
    return simulation


def run_simulation():
    """
    Runs simulation and returns its result.
    """
    sample = get_sample()
    simulation = get_simulation()
    simulation.setSample(sample)
    simulation.runSimulation()
    return simulation.result()


if __name__ == '__main__':
    result = run_simulation()
    ba.plot_simulation_result(result)
