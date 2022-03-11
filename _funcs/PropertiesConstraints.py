def properties_constraints(props,constr):
    """
    Apply identification properties constraints.

    Parameters
    ----------
    props : (nprops,) , float
        Material properties.
    constr : (nprops,2) , float
        Constraints for identification properties.

    Returns
    -------
    props : (nprops,) , float
        Material properties.
    """

    for cprop in constr:
        props[cprop[0]] = eval(cprop[1])

    return props