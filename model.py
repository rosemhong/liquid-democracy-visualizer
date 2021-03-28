class Model:
    def __init__(self, model_args):
        '''
        if parameter not in model_args, is set to None

        total_voters: total number of nodes in graph
        competence_mean: mean of distribution to sample voter's competence
            (competence = probability of voting correctly)
        competence_sd: standard deviation of distribution to sample voter's competence
            (competence ~ N(competence_mean, competence_sd))
        connect_probability: chance that any edge in social network exists
        delegate_probability: chance that node above competence threshold (see below)
            is included in eligible delegates list
        threshold_diff: voter's competence must be above threshold_diff + own competence
            to be considered eligible delegate
        weight_limit: limit of number of votes of a delegate
        delegation_degrees: limit of degrees of delegation
            degree 1 = I delegate to voter x unless they delegate to someone else
        '''
        self.total_voters = model_args.get('total_voters')
        self.competence_mean = model_args.get('competence_mean')
        self.competence_sd = model_args.get('competence_sd')
        self.connect_probability = model_args.get('connect_probability')
        self.delegate_probability = model_args.get('delegate_probability')
        self.threshold_diff = model_args.get('threshold_diff')
        self.weight_limit = model_args.get('weight_limit')
        self.delegation_degrees = model_args.get('delegation_degrees')
        # TODO: splitting vote among different delegates