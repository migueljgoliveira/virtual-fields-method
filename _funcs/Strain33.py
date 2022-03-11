def strain33(strain,pstrain,nu):
    """
    Compute the thickness strain in plane stress problems.

    Parameters
    ----------
    strain : (nf,ne,ntens) , float
        Total strain in corotational material csys.
    pstrain : (nf,ne,ntens) , float
        Plastic strain in corotational material csys.
    nu : float
        Poisson ration

    Returns
    -------
    d33 : (nf,ne) , float
        Strain in thickness direction.

    Theory
    ------
    """

    # Sum of normal strain components
    strain12 = strain[...,0] + strain[...,1]
    pstrain12 = pstrain[...,0] + pstrain[...,1]

    # Strain in thickness direction
    d33 = -(nu/(1-nu)) * (strain12 - pstrain12) - pstrain12

    return d33