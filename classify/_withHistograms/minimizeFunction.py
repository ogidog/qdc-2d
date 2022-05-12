import numpy as np


def minimizeFunction(w):
    theta_vector = np.arange(0, 179, 2)

    NBjointSet = np.floor(len(w)/3)
    histo_distribution_joint = np.zeros((90, NBjointSet))
    for joint in range(len(NBjointSet)):
        H = np.zeros(90)
        histo1  = w(1+2*NBjointSet+joint)* normpdf(theta_vector    , w(1+joint), w(1+NBjointSet+joint));
        histo2  = w(1+2*NBjointSet+joint)* normpdf(theta_vector-180, w(1+joint), w(1+NBjointSet+joint));
        histo3  = w(1+2*NBjointSet+joint)* normpdf(theta_vector+180, w(1+joint), w(1+NBjointSet+joint));
        indice1 = find(histo1>0.0001);
        indice2 = find(histo2>0.0001);
        indice3 = find(histo3>0.0001);
        H(indice1) = histo1(indice1);
        H(indice2) = histo2(indice2);
        H(indice3) = histo3(indice3);
        H(isnan(H))=0;
        histo_distribution_joint(:,joint) = H;
        end
        gaussian_sum     = sum(histo_distribution_joint,2) + w(1);
        gaussian_std     = (theta_histogram - gaussian_sum).^2;
        value2minimize = sum(gaussian_std)/100000; %value to minimize

    return value2minimize