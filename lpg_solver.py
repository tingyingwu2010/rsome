import scipy.optimize as opt
import numpy as np
import warnings
import time


def solve(formula, display=True, export=False):

    nv = formula.linear.shape[1]
    vtype = list(formula.vtype)

    indices_eq = (formula.sense == 1)
    indices_ineq = (formula.sense == 0)
    linear_eq = formula.linear[indices_eq, :]
    linear_ineq = formula.linear[indices_ineq, :]
    const_eq = formula.const[indices_eq]
    const_ineq = formula.const[indices_ineq]

    if len(indices_ineq) == 0:
        linear_ineq = None
        const_ineq = None
    if len(indices_eq) == 0:
        linear_eq = None
        const_eq = None

    bounds = [(lb, ub) for lb, ub in zip(formula.lb, formula.ub)]

    default = {'maxiter': 1000000000,
               'sparse': True}

    if display:
        print('Being solved by the default LP solver...')
    t0 = time.process_time()
    res = opt.linprog(formula.obj, A_ub=linear_ineq, b_ub=const_ineq,
                      A_eq=linear_eq, b_eq=const_eq,
                      bounds=bounds, options=default)
    stime = time.process_time() - t0
    if display:
        print('Solution status: {0}'.format(res.status))
        print('Running time: {0:0.4f}s'.format(stime))

    if export:
        warnings.warn('Cannot export model by the linprog() function. ')
    try:
        if formula.qmat:
            warnings.warn('SOC constriants are ignored in the LP solver. ')
    except:
        pass
    if any(np.array(formula.vtype)!='C'):
        warnings.warn('Integrality constraints are ignored in the LP solver. ')

    # x = res.x
    # solution = Solution(x[0], x, res.status)

    return res
