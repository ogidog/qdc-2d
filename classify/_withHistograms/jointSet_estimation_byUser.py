import sys
import numpy as np

def jointSet_estimation_byUser():
    confirm = 'N'
    jointsets = {'G_mean': [], 'G_std': [], 'G_N': []}

    # ---------Input
    question_NBjointSet = 'Number of joint sets you estimate ? : '
    NBjointSet = 2  # NBjointSet = input(question_NBjointSet)

    # Jointset structure with parameters
    jointsets['NBjointSet'] = NBjointSet

    # for each jointset, estimation of gaussians parameters
    for joint in range(NBjointSet):
        # print('Joint set {} : '.format(joint))
        # question_mean = 'Gaussian mean you estimate ? : '
        # mean = input(question_mean)
        mean = 2
        # question_std = 'Gaussian std you estimate ? : '
        # std = input(question_std)
        std = 3
        # question_N = 'Gaussian amplitude you estimate ? : '
        # N = input(question_N)
        N = 150

        jointsets['G_mean'].append(mean)
        jointsets['G_std'].append(std)
        jointsets['G_N'].append(N)

    # Noise estimation
    # question_noise = 'Noise you estimate ? : ';
    # jointsets['noise'] = input(question_noise);
    jointsets['noise'] = 200

    # resume estimation :
    print('---------------------------------------')
    print('Confirm your estimation : ');
    print('{} join sets'.format(NBjointSet))
    print('Mean -- std -- N')
    resume = np.array([jointsets['G_mean'], jointsets['G_std'], jointsets['G_N']]).T
    print(resume)
    print('Noise your estimate : {}'.format(jointsets['noise']))
    print('---------------------------------------')

    # User confirmation
    question_comfirm = 'Confirm ? Y/N   ';
    # confirm = input(question_comfirm, 's');
    confirm = "Y"

    if confirm == "N":
        sys.exit(-1)
    else:
        return jointsets
