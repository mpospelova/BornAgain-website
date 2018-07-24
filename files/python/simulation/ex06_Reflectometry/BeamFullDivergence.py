"""
An example of taking into account beam angular and wavelength
divergence in reflectometry calculations with BornAgain.

"""
import bornagain as ba

# input parameters
wavelength = 1.54 * ba.angstrom
alpha_i_min = 0.0 * ba.deg  # min incident angle, deg
alpha_i_max = 2.0 * ba.deg  # max incident angle, rad
n_bins = 500  # number of bins in the reflectivity curve

# convolution parameters
d_wl = 0.01 * wavelength  # spread width for wavelength
d_ang = 0.01 * ba.deg  # spread width for incident angle
n_sig = 3  # number of sigmas to convolve over
n_points = 25  # number of points to convolve over

# substrate (Si)
si_sld_real = 2.0704e-06  # \AA^{-2}
# layer parameters
n_repetitions = 10
# Ni
ni_sld_real = 9.4245e-06  # \AA^{-2}
d_ni = 70 * ba.angstrom  # ni layer thickness (nm)
# Ti
ti_sld_real = -1.9493e-06  # \AA^{-2}
d_ti = 30 * ba.angstrom  # ti layer thickness (nm)


def get_sample():
    # defining materials
    # this example implies beam divergence in the wavelength,
    # thus MaterialBySLD must be used to provide correct result
    m_air = ba.MaterialBySLD("Air", 0.0, 0.0)
    m_ni = ba.MaterialBySLD("Ni", ni_sld_real, 0.0)
    m_ti = ba.MaterialBySLD("Ti", ti_sld_real, 0.0)
    m_substrate = ba.MaterialBySLD("SiSubstrate", si_sld_real, 0.0)

    air_layer = ba.Layer(m_air)
    ni_layer = ba.Layer(m_ni, d_ni)
    ti_layer = ba.Layer(m_ti, d_ti)
    substrate_layer = ba.Layer(m_substrate)
    multi_layer = ba.MultiLayer()
    multi_layer.addLayer(air_layer)
    for i in range(n_repetitions):
        multi_layer.addLayer(ti_layer)
        multi_layer.addLayer(ni_layer)
    multi_layer.addLayer(substrate_layer)
    return multi_layer


def get_simulation():
    """
    Returns a specular simulation with beam and detector defined.
    """
    # First argument  of ba.DistributionGaussian is
    # the mean value for distribution.
    # It should be zero in the case of incident angle distribution,
    # otherwise an exception is thrown.
    alpha_distr = ba.DistributionGaussian(0.0, d_ang)
    wavelength_distr = ba.DistributionGaussian(wavelength, d_wl)
    simulation = ba.SpecularSimulation()
    simulation.setBeamParameters(
        wavelength, n_bins, alpha_i_min, alpha_i_max)
    simulation.addParameterDistribution("*/Beam/InclinationAngle",
                                        alpha_distr, n_points, n_sig)
    simulation.addParameterDistribution("*/Beam/Wavelength",
                                        wavelength_distr, n_points, n_sig)
    return simulation


def run_simulation():
    """
    Runs simulation and returns it.
    """
    sample = get_sample()
    simulation = get_simulation()
    simulation.setSample(sample)
    simulation.runSimulation()
    return simulation.result()


if __name__ == '__main__':
    results = run_simulation()
    ba.plot_simulation_result(results)
