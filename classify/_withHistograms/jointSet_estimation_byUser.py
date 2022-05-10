import sys


def jointSet_estimation_byUser():
    confirm = 'N'
    jointsets = {}

    # ---------Input
    question_NBjointSet = 'Number of joint sets you estimate ? : '
    NBjointSet = 2  # NBjointSet = input(question_NBjointSet)

    # Jointset structure with parameters
    jointsets['NBjointSet'] = NBjointSet

    # for each jointset, estimation of gaussians parameters
    for joint in range(NBjointSet):
        print('Joint set %d : ', joint)


    if confirm == "N":
        sys.exit(-1)
    else:
        return jointsets
