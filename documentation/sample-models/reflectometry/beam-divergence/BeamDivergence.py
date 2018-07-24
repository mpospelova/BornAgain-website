"""
Example of taking into account
beam divergence effects in specular simulations
with BornAgain.

"""
from matplotlib import pyplot as plt
import bornagain as ba
from bornagain import deg, angstrom


def get_sample():
    """
    Defines sample and returns it
    """

    # creating materials
    m_ambient = ba.MaterialBySLD("Ambient", 0.0, 0.0)
    m_ti = ba.MaterialBySLD("Ti", -1.9493e-06, 0.0)
    m_ni = ba.MaterialBySLD("Ni", 9.4245e-06, 0.0)
    m_substrate = ba.MaterialBySLD("SiSubstrate", 2.0704e-06, 0.0)

    # creating layers
    ambient_layer = ba.Layer(m_ambient)
    ti_layer = ba.Layer(m_ti, 30 * angstrom)
    ni_layer = ba.Layer(m_ni, 70 * angstrom)
    substrate_layer = ba.Layer(m_substrate)

    # creating multilayer
    multi_layer = ba.MultiLayer()
    multi_layer.addLayer(ambient_layer)
    for i in range(10):
        multi_layer.addLayer(ti_layer)
        multi_layer.addLayer(ni_layer)
    multi_layer.addLayer(substrate_layer)

    return multi_layer


def get_simulation(divergent_beam):
    """
    Defines and returns a specular simulation.
    """

    # simulation parameters definition
    wavelength = 1.54 * angstrom
    n_bins = 500
    alpha_min = 0.0 * deg
    alpha_max = 2.0 * deg

    simulation = ba.SpecularSimulation()
    simulation.setBeamParameters(
        wavelength, n_bins, alpha_min, alpha_max)

    # adding beam divergence
    if divergent_beam is True:
        add_beam_divergence(simulation, wavelength)

    return simulation


def add_beam_divergence(simulation, wavelength):
    """
    Adds beam divergence to the simulation
    """
    # beam divergence parameters
    d_wl = 0.01 * wavelength  # spread width for wavelength
    d_ang = 0.01 * ba.deg  # spread width for incident angle
    n_sig = 3  # number of standard deviations to take into account
    n_points = 25  # number of points to take in parameter distribution

    # creating beam parameter distributions
    alpha_distr = ba.DistributionGaussian(0.0, d_ang)
    wavelength_distr = ba.DistributionGaussian(wavelength, d_wl)

    # adding distributions to the simulation
    simulation.addParameterDistribution("*/Beam/InclinationAngle",
                                        alpha_distr, n_points, n_sig)
    simulation.addParameterDistribution("*/Beam/Wavelength",
                                        wavelength_distr, n_points, n_sig)


def run_simulation(divergent_beam):
    """
    Runs simulation and returns its result.
    """
    sample = get_sample()
    simulation = get_simulation(divergent_beam)
    simulation.setSample(sample)
    simulation.runSimulation()
    return simulation.result()


def get_plot_data(sim_result):
    data = sim_result.data()
    intensity = data.getArray()
    x_axis = data.getAxis(0).getBinCenters()
    return x_axis, intensity


def plot(sim_result_1, sim_result_2):
    """
    Plots results from two different simulations
    """

    plt.semilogy(*get_plot_data(sim_result_1), *get_plot_data(sim_result_2))

    plt.xlabel(r'$\alpha_i \; (deg)$', fontsize=16)
    plt.ylabel(r'Intensity', fontsize=16)

    plt.legend(['Divergent beam',
                'Ideal beam'],
                loc='upper right')

    plt.show()


if __name__ == '__main__':
    result_div_beam = run_simulation(divergent_beam=True)
    result_ideal_beam = run_simulation(divergent_beam=False)
    plot(result_div_beam, result_ideal_beam)
