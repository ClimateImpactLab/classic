"""
Regression tests.  Execute via:
    python regression_tests.py
to test, or
    python regression_tests.py True
to create new regression data for archiving.
"""


from clawpack.visclaw import data
import os, sys
import numpy as np
import subprocess

def setup():
    # Create plotdata object for reading in frames in tests below:
    global plotdata
    global olddir

    plotdata = data.ClawPlotData()
    plotdata.outdir = '_output'

    # Now set current working directory to regression_tests.py
    olddir = os.getcwd()
    testdir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(testdir)


def teardown():
    os.chdir(olddir)


def test1():
    """
    Compile and run the code
    """
    subprocess.check_call(['make', 'clean'])
    subprocess.check_call(['make', '.output'])


def test2(save_new_regression_data=False):
    """
    Check sum of all q values in frame 1
    """

    # unique for this test:
    frameno = 1
    fname_data = 'regression_data_test2.txt'

    f = plotdata.getframe(frameno)
    my2 = int(f.state.q.shape[-1] / 2)
    qsum1 = f.state.q[0,:,:my2].sum()
    qsum2 = f.state.q[0,:,my2:].sum()
    
    new_data = np.array([qsum1,qsum2])
    
    if save_new_regression_data:
        np.savetxt(fname_data,new_data)
        print "*** Created new regression_data file ", fname_data
        
    # Read in archived data for comparison:
    regression_data = np.loadtxt(fname_data)

    tol = 1e-14
    assert np.allclose(new_data,regression_data,tol), \
        "\n  new_data: %s, \n  expected: %s"  % (new_data, regression_data)
    print "Frame %i OK" % frameno
    

def test3(save_new_regression_data=False):
    """
    Check sum of all q values in frame 2
    """
    # unique for this test:
    frameno = 2
    fname_data = 'regression_data_test3.txt'

    f = plotdata.getframe(frameno)
    my2 = int(f.state.q.shape[-1] / 2)
    qsum1 = f.state.q[0,:,:my2].sum()
    qsum2 = f.state.q[0,:,my2:].sum()
    
    new_data = np.array([qsum1,qsum2])
    
    if save_new_regression_data:
        np.savetxt(fname_data,new_data)
        print "*** Created new regression_data file ", fname_data
        
    # Read in archived data for comparison:
    regression_data = np.loadtxt(fname_data)

    tol = 1e-14
    assert np.allclose(new_data,regression_data,tol), \
        "\n  new_data: %s, \n  expected: %s"  % (new_data, regression_data)
    print "Frame %i OK" % frameno

    
if __name__=="__main__":
    setup()
    test1()
    save_new_regression_data = (len(sys.argv) > 1) and (sys.argv[1]=='True')
    test2(save_new_regression_data)
    test3(save_new_regression_data)
    teardown()
