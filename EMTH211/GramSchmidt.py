import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

def GramSchmidt(vecs, normalize=True):
    orthogonal_vecs = [vecs[0]]
    if normalize:
        orthogonal_vecs[0] = orthogonal_vecs[0]/la.norm(orthogonal_vecs[0])
    for i in range(1, len(vecs)):
        proj_vecs = np.zeros(len(vecs[0]))
        for vec in orthogonal_vecs:
            proj_vecs = proj_vecs + np.dot(vec, vecs[i])/np.dot(vec, vec)*vec
        orthogonal_vecs.append(vecs[i] - proj_vecs)

        if normalize:
            orthogonal_vecs[i] = orthogonal_vecs[i]/la.norm(orthogonal_vecs[i])
    return orthogonal_vecs

def main():
    vecs = [np.array([1., 2., 3., 4.]), np.array([-1., 0., 2., 3.]), np.array([0., 1., -1., 2.])]
    orthonormal_vecs = GramSchmidt(vecs)
    for vec in orthonormal_vecs:
        print(vec)

main()