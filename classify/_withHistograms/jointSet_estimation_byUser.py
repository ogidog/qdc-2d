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

    # TODO: раскоментировать в продакшене
    # for each jointset, estimation of gaussians parameters
    # for joint in range(NBjointSet):
    #     print('Joint set {} : '.format(joint))
    #     question_mean = 'Gaussian mean you estimate ? : '
    #     mean = int(input(question_mean))
    #     question_std = 'Gaussian std you estimate ? : '
    #     std = int(input(question_std))
    #     question_N = 'Gaussian amplitude you estimate ? : '
    #     N = int(input(question_N))
    #
    #     jointsets['G_mean'].append(mean)
    #     jointsets['G_std'].append(std)
    #     jointsets['G_N'].append(N)
    #
    # # Noise estimation
    # question_noise = 'Noise you estimate ? : ';
    # jointsets['noise'] = int(input(question_noise))

    # TODO: удалить
    jointsets['G_mean'] = [5, 1]
    jointsets['G_std'] = [7, 9]
    jointsets['G_N'] = [69, 22]
    jointsets['noise'] = 2

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
    question_comfirm = 'Confirm ? Y/N   '
    # TODO: раскоментировать в продакшене
    # confirm = input(question_comfirm, 's');

    # TODO: удалить
    confirm = "Y"

    if confirm == "N":
        sys.exit(-1)
    else:
        return jointsets
