class Model:
    def __init__(self, model_args):
        '''
        if parameter not in model_args, is set to None

        total_voters (int): total number of nodes in graph
        competence_mean (float): mean of distribution to sample voter's competence
            (competence = probability of voting correctly)
        competence_sd (float): standard deviation of distribution to sample voter's competence
            (competence ~ N(competence_mean, competence_sd))
        connect_probability (float): chance that any edge in social network exists
        delegate_probability (float): chance that node above competence threshold (see below)
            is included in eligible delegates list
        threshold_diff (float): voter's competence must be above threshold_diff + own competence
            to be considered eligible delegate
        weight_limit (int): limit of number of votes of a delegate
        delegation_degrees (int): limit of degrees of delegation
            degree 1 = I delegate to voter x unless they delegate to someone else
        '''
        self.total_voters = self._to_int(model_args.get('total_voters'))
        self.competence_mean = self._to_float(model_args.get('competence_mean'))
        self.competence_sd = self._to_float(model_args.get('competence_sd'))
        self.connect_probability = self._to_float(model_args.get('connect_probability'))
        self.delegate_probability = self._to_float(model_args.get('delegate_probability'))
        self.threshold_diff = self._to_float(model_args.get('threshold_diff'))
        self.weight_limit = self._to_int(model_args.get('weight_limit'))
        self.delegation_degree = self._to_int(model_args.get('delegation_degree')) # TODO: make this a mean / sd thing instead of being the same for everyone?
        # TODO: splitting vote among different delegates
    
    def _to_int(self, arg):
        if arg is not None:
            return int(arg)
        else:
            return None
    
    def _to_float(self, arg):
        if arg is not None:
            return float(arg)
        else:
            return None
