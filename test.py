import numpy as np
import matplotlib.pyplot as plt

def rotMat(angle, axis):
    # Returns the rotation matrix according to http://mathworld.wolfram.com/RotationMatrix.html
    # angle: The rotation angle in radians
    # axis: 1 - x axis, 2 - y axis, 3 - z axis
    c, s = np.cos(angle), np.sin(angle)
    if axis == 1:
        R = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
    elif axis == 2:
        R = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
    elif axis == 3:
        R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
    return R

def transformEuler(phi, theta, psai):
    # Returns the Euler rotational transformation matrix from the three rotation angles in radians
    return np.dot(rotMat(psai, 3), np.dot(rotMat(theta, 2), rotMat(phi, 3)))

def getT_sigma(T):
    # Returns 6*6 T_sigma transition matrix from the input Euler rotational transformation matrix
    # T: Euler rotational transformation matrix
    l1 = T[0, 0]
    m1 = T[0, 1]
    n1 = T[0, 2]
    l2 = T[1, 0]
    m2 = T[1, 1]
    n2 = T[1, 2]
    l3 = T[2, 0]
    m3 = T[2, 1]
    n3 = T[2, 2]
    row1 = np.array([l1*l1, m1*m1, n1*n1, 2*m1*n1, 2*n1*l1, 2*l1*m1])
    row2 = np.array([l2*l2, m2*m2, n2*n2, 2*m2*n2, 2*n2*l2, 2*l2*m2])
    row3 = np.array([l3*l3, m3*m3, n3*n3, 2*m3*n3, 2*n3*l3, 2*l3*m3])
    row4 = np.array([l2*l3, m2*m3, n2*n3, m2*n3+n2*m3, n2*l3+l2*n3, l2*m3+m2*l3])
    row5 = np.array([l3*l1, m3*m1, n3*n1, m3*n1+n3*m1, n3*l1+l3*n1, l3*m1+m3*l1])
    row6 = np.array([l1*l2, m1*m2, n1*n2, m1*n2+n1*m2, n1*l2+l1*n2, l1*m2+m1*l2])
    T_sigma = np.array([row1, row2, row3, row4, row5, row6])
    return T_sigma

def piezoCoeff(type, ratio = 1):
    # Returns 1e11 times the silicon piezoresistive coefficient in Pa-1
    # type: 'p' - p type silicon, 'n' - n type silicon
    if type == 'p':
        pi11 = 6.6
        pi12 = -1.1
        pi44 = 138.1
    elif type == 'n':
        pi11 = -102.2
        pi12 = 53.4
        pi44 = -13.6
    p11 = (pi11 - pi12) * np.identity(3) + pi12 * np.ones((3, 3))
    p12 = np.zeros((3, 3))
    p21 = p12
    p22 = pi44 * np.identity(3)
    return  ratio * np.asarray(np.bmat([[p11, p12], [p21, p22]]))

def piezoCoeffRot(pi, T_sigma):
    # Returns the rotated piezoresistive coefficient matrix
    # Pi: The piezoresistive coefficient matrix before rotation
    # T_sigma: The T_sigma transition matrix obtained from getT_sigma
    return np.dot(np.dot(T_sigma, pi), np.linalg.inv(T_sigma))

def getPiElem(pi, row, col):
    # Returns the Pi(ij) element at row i and column j
    # pi: The piezoresistive coefficient matrix
    return pi[row - 1, col - 1]


def plotPolar(psai_vals, r, color = None, linestyle = '-', label = None):
    # Generate a polar plot with psai_vals as the angle list, and r as the radius list
    # Returns the handle to the plot
    ax = plt.subplot(111, projection = 'polar')
    ax.plot(psai_vals, r, color = color, linestyle = linestyle, label = label)
    # plt.autoscale()
    # ax.set_rlabel_position(0)
    ax.grid(True)
    return ax


def getListPiElem(psai_vals, type, phi, theta, row, col, ratio = 1):
    # Return a list of Pi(ij) elements corresponding to the list of psai_vals
    # phi, theta are the first two Euler rotation angles
    # psai_vals contains a list of the thired Euler rotation angles
    # type: 'p' - p type silicon, 'n' - n type silicon
    # row, col: The (i, j) position of the desired piezoresistive coefficient in the matrix Pi
    T_of_psai = [transformEuler(np.radians(phi), np.radians(theta), np.radians(psai)) for psai in psai_vals]
    T_sigma_of_psai = [getT_sigma(T) for T in T_of_psai]
    pi = piezoCoeff(type, ratio)
    pi_of_psai = [piezoCoeffRot(pi, T_sigma) for T_sigma in T_sigma_of_psai]
    r = [getPiElem(pi, row, col) for pi in pi_of_psai]
    return r

def genPlot(type, phi, theta, row, col, plot_reso, abs = True, linestyle = '-', label = None):
    # Returns the handle to a polar plot of piezoresistive coefficient
    # type: 'p' - p type silicon, 'n' - n type silicon
    # phi, theta: The first two Euler rotation angles, determines the crystalline surface such as (100), (110), etc.
    # row, col: The (i, j) position of the desired piezoresistive coefficient, such as pi11, pi12, etc.
    # plot_reso: Resolution of polar angle in degrees
    # abs: True - plots the magnitude, False - plot will not take the absolute value for negative coefficients
    psai_vals = np.arange(0, 360, plot_reso)
    r = getListPiElem(psai_vals, type, phi, theta, row, col)
    if abs:
        return plotPolar(np.radians(psai_vals), np.abs(r), linestyle = linestyle, label = label)
    else:
        return plotPolar(np.radians(psai_vals), r, linestyle = linestyle, label = label)

def genPlot110(type, plot_reso, abs = True):
    # Plots polar plot for (110) silicon surface
    # See getPlot for meaning of parameters
    psai_vals = np.arange(0, 360, plot_reso)
    r_pi11 = getListPiElem(psai_vals, type, 0, 45, 1, 1)
    r_pi12 = getListPiElem(psai_vals, type, 0, 45, 1, 2)
    r = (np.array(r_pi11) + np.array(r_pi12)).tolist()
    if abs:
        return plotPolar(np.radians(psai_vals), np.abs(r))
    else:
        return plotPolar(np.radians(psai_vals), r)


def getSignalMagnitudeList(psai_vals, stress_XX, stress_YY, r11, r12, r16):
    # Returns a list of signal magnitude w.r.t. psai_vals, for (110) wafer under stress_XX and stress_YY
    # psai_vals: The polar plot angles in degrees, must be the psai_vals used to generate r11 and r12
    # stress_XX and stress YY: The stress level along [110] and [100] direction without coordinate system rotation
    # r11 and r12 are the list of piezoresistive coefficients w.r.t psai_vals after Euler rotation of coordinate system
    psai_radian = np.radians(psai_vals)
    stress_1 = stress_XX * np.square(np.cos(psai_radian)) + stress_YY * np.square(np.sin(psai_radian))
    stress_2 = stress_XX * np.square(np.cos(psai_radian + np.pi / 2)) + stress_YY * np.square(np.sin(psai_radian + np.pi / 2))
    stress_shear = -0.5 * (stress_XX - stress_YY) * np.sin(2 * psai_radian)
    signalMagnitude = r11 * stress_1 + r12 * stress_2 + r16 * stress_shear
    signalMagnitudeList = signalMagnitude.tolist()
    return signalMagnitudeList

def genSignalMagnitudePlot(psai_vals, signalMagnitudeList, abs = True, color = None, linestyle = '-', label = None):
    # Returns the handle to a polar plot of signal magnitude vs. psai_vals
    # psai_vals: List of the third Euler angle as independent variable
    # signalMagnitudeList: List of signal magnitude obtained from getSignalMagnitudeList
    # abs: Same as that in genPlot()
    if abs:
        return plotPolar(np.radians(psai_vals), np.abs(signalMagnitudeList), color, linestyle, label)
    else:
        return plotPolar(np.radians(psai_vals), signalMagnitudeList, color, linestyle, label)

# Example code for generating a polar plot for p-type and n-type 110 wafers
# genPlot110('p', 0.1, abs = False)
# plt.figure()
# ax_n = genPlot110('n', 0.1, abs = False)
# ax_n.set_rmax(100)
# ax_n.set_rmin(-100)
# ax_n.set_rticks([-100, -50, 0, 50, 100])
# plt.show()

# Example code for generating polar plot of signal magnitude for n-type 110 wafers
# plotReso = 0.1
# psai_vals = np.arange(0, 360, plotReso)
# r11 = getListPiElem(psai_vals, 'n', 0, 45, 1, 1)
# r12 = getListPiElem(psai_vals, 'n', 0, 45, 1, 2)
#
# signalMagnitudeList = getSignalMagnitudeList(psai_vals, 1.25, 1, r11, r12)
# ax_n = genSignalMagnitudePlot(psai_vals, signalMagnitudeList, False)
# ax_n.set_rmax(40)
# ax_n.set_rmin(-80)
# ax_n.set_rticks([-80, -40, 0, 40])
# plt.show()


# Codes used to generate Figure 3(a)
# Will generate warning if there're values in signalMagnitudeList between (-1, 0). I believe the warning can be ignored.
#
def shearPlot(psai_vals, stress_XX, stress_YY, piezo_coeff):
    psai_radian = np.radians(psai_vals)
    stress_shear = -0.5 * (stress_XX - stress_YY) * np.sin(2 * psai_radian)
    signalMagnitude = piezo_coeff * stress_shear
    plt.figure()
    ax0 = genSignalMagnitudePlot(psai_vals, stress_shear, False)
    ax0.set_rticks((1e9*np.array([-10, 0, 10, 20])).tolist())
    plt.savefig('stress_shear.png', dpi = 600)
    plt.figure()
    ax1 = genSignalMagnitudePlot(psai_vals, piezo_coeff, False)
    ax1.set_rticks((1e-11*np.array([-120, -60, 0, 60, 120])).tolist())
    plt.savefig('piezo_coeff.png', dpi = 600)
    plt.figure()
    ax2 = genSignalMagnitudePlot(psai_vals, signalMagnitude, False)
    ax2.set_rticks([-5, 0, 5, 10])
    plt.savefig('signalMagnitude.png', dpi = 600)
    plt.show()

plotReso = 0.02
psai_vals = np.arange(0, 360, plotReso)
pi_ratio = 1 # Ratio of reduction in piezo coeff due to e.g. higher doping concentration
pi_ratio *= 1e-11 # Convert to SI unit since piezoCoeff() returns 1e11 times the coefficient in SI unit
stress_ratio = 1.256 # Value obtained from FEA
stress_YY = -100e6 # 100 MPa
stress_YY *= -100 # Convert the r axis into percentage values
stress_XX = stress_ratio * stress_YY

r11 = getListPiElem(psai_vals, 'p', 0, 45, 1, 1, ratio = pi_ratio)
r12 = getListPiElem(psai_vals, 'p', 0, 45, 1, 2, ratio = pi_ratio)
r16 = getListPiElem(psai_vals, 'p', 0, 45, 1, 6, ratio = pi_ratio)
print 'r11=', r11
print 'r12=', r12
# shearPlot(psai_vals, stress_XX, stress_YY, r16) # Plot the shear stress, piezocoeff, and singalMag for check

signalMagnitudeList = getSignalMagnitudeList(psai_vals, stress_XX, stress_YY, r11, r12, r16)
ax_p = genSignalMagnitudePlot(psai_vals, signalMagnitudeList, False, color = 'b', label = 'p-type silicon (110)')
print '110p: ', signalMagnitudeList[psai_vals.tolist().index(0)]
print '100p: ', signalMagnitudeList[psai_vals.tolist().index(90)]
r11 = getListPiElem(psai_vals, 'n', 0, 45, 1, 1, ratio = pi_ratio)
r12 = getListPiElem(psai_vals, 'n', 0, 45, 1, 2, ratio = pi_ratio)
r16 = getListPiElem(psai_vals, 'n', 0, 45, 1, 6, ratio = pi_ratio)

# shearPlot(psai_vals, stress_XX, stress_YY, r16) # Plot the shear stress, piezocoeff, and singalMag for check
#
signalMagnitudeList = getSignalMagnitudeList(psai_vals, stress_XX, stress_YY, r11, r12, r16)
ax_n = genSignalMagnitudePlot(psai_vals, signalMagnitudeList, False, color = 'r', label = 'n-type silicon (110)')
print '110n: ', signalMagnitudeList[psai_vals.tolist().index(0)]
print '100n: ', signalMagnitudeList[psai_vals.tolist().index(90)]
# ax_p.set_xlabel(r'$\psi$')
# ax_p.set_title(r'$\Delta\rho_{11}/\rho \times10^3$', y = 1.1, fontsize = 22)
if stress_YY < 0:
    ax_p.set_rmax(5)
    ax_p.set_rmin(-10)
    ax_p.set_rticks([-10, -5, 0, 5])
else:
    ax_p.set_rmax(10)
    ax_p.set_rmin(-5)
    ax_p.set_rticks([-5, 0, 5, 10])
ax_p.set_rlabel_position(-90)
theta_ticks = np.arange(0,360,45) # Tick locations
ax_p.set_thetagrids(theta_ticks, frac = 1.15) # Set ticklabels location at 1.3 times the axes' radius

font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 20}
plt.rc('font', **font)
# plt.text(0.05*(np.pi/2), 65, '<110>', fontdict = font)
# plt.text(0.95*(np.pi/2), 65, '<100>', fontdict = font)
# plt.text(0.95*(np.pi), 65, '<110>', fontdict = font)
# plt.text(0.95*(3*np.pi/2), 65, '<100>', fontdict = font)
# ax_p.legend(loc = 'upper right', fontsize = 'x-small')
# plt.savefig("Fig3a.png", dpi = 600)
plt.show()


# # Codes to generate Figure 3(b)
# def plotDiffSigVsRatio(type, reso, color = None, linestyle = '-'):
#     psai_vals = [0, 90] # Sensing resistors are along [110], 0 degree, reference resistors are along [100], 90 degree
#     pi_ratio = 1 # Ratio of reduction in piezo coeff due to e.g. higher doping concentration
#     r11 = getListPiElem(psai_vals, type, 0, 45, 1, 1, ratio = pi_ratio)
#     r12 = getListPiElem(psai_vals, type, 0, 45, 1, 2, ratio = pi_ratio)
#     r16 = getListPiElem(psai_vals, type, 0, 45, 1, 6, ratio = pi_ratio)
#     stress_ratio = np.arange(0.5, 1.7 + reso, reso) # The ratio between stress along [110] and [100], i.e. stressXX/stressYY
#     signalMagnitudeList = [getSignalMagnitudeList(psai_vals, str_ratio*100e6, 100e6, r11, r12, r16) for str_ratio in stress_ratio]
#     differentialSignalMagnitude = [(sig[0] - sig[1])* 1e-11 for sig in signalMagnitudeList]
#     label = type + ' type silicon'
#     return plt.plot(stress_ratio, 1e2 * np.array(differentialSignalMagnitude), color = color, linestyle = linestyle, label = label)
#
# plotDiffSigVsRatio('p', 0.01, 'b')
# plotDiffSigVsRatio('n', 0.01, 'r')
# plt.axis([0.6, 1.6, 0.02 * 1e2, 0.12 * 1e2])
# # plt.title(r'Difference of $\Delta\rho_{11}/\rho$ between resistors' + '\n' + r'along <110> and <100>', y = 1.02)
# # plt.xlabel(r'$\eta\ (\sigma_{<100>} = 100$ MPa$)$', size = 30)
# # plt.ylabel(r'$(\Delta\rho_{11}/\rho)_{<110>} - (\Delta\rho_{11}/\rho)_{<100>} $', size = 30)
# # plt.legend(loc = 'center right')
# font = {'weight' : 'normal',
#         'size'   : 20}
# plt.rc('font', **font)
# plt.grid()
# plt.tick_params('x', pad = 10)
# plt.savefig('Fig3b', dpi = 600)
# # plt.show()
