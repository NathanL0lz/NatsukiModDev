default persistent.trust = 10.0
default persistent.affinity = 25.0

init 0 python:
    def jn_relationship(change, multiplier=1):
        def __affinity_increase(multiplier=1):
            if persistent.trust > 0:
                persistent.affinity += multiplier*(persistent.trust/20)

        def __affinity_decrease(multiplier=1):
            if persistent.trust-50 > 0:
                persistent.affinity -= multiplier*(5 - (persistent.trust-50)/25)
            else:
                persistent.affinity -= multiplier*5

        def __trust_increase(multiplier=1):
            if persistent.trust < 100:
                persistent.trust += multiplier*0.8*(round(math.tanh((persistent.affinity-75)/30)+1, 4)+1)
            if persistent.trust > 100:
                persistent.trust = 100

        def __trust_decrease(multiplier=1):
            if persistent.trust > -100:
                persistent.trust -= multiplier*2*(3 - round(math.tanh((persistent.affinity-75)/30)+1, 4))
            if persistent.trust < -100:
                persistent.trust = -100

        if change == "affinity+":
            __affinity_increase(multiplier)

        elif change == "affinity-":
            __affinity_decrease(multiplier)

        elif change == "trust+":
            __trust_increase(multiplier)

        elif change == "trust-":
            __trust_decrease(multiplier)

        else:
            raise Exception(change+" is not a valid argument!")

init -2 python in jn_trust_affinity_common:
    def _is_state_valid(state, state_order_list):
        """
        Checks if the given state is valid (mapped in the state_order_list)

        IN:
            state - the integer representing the state we wish to check is valid

        OUT:
            True if valid state otherwise False
        """
        return (
            state in state_order_list
            or state is None
        )

    def _compare_thresholds(value, threshold):
        """
        Generic compareto function for values
        """
        if value < threshold:
            return -1
        elif value == threshold:
            return 0
        else:
            return 1

init -1 python in jn_affinity:
    import store
    import random

    # Affinity levels, highest to lowest
    THRESHOLD_LOVE = 1000
    THRESHOLD_ENAMORED = 500
    THRESHOLD_AFFECTIONATE = 250
    THRESHOLD_HAPPY = 100
    THRESHOLD_NORMAL = 0
    THRESHOLD_UPSET = -25
    THRESHOLD_DISTRESSED = -50
    THRESHOLD_BROKEN = -100
    THRESHOLD_RUINED = -125

    # Affinity States (non-prefixed as these are used for affinity_range)
    # RUINED - Natsuki is emotionally exhausted. She barely talks and holds nothing but hopelessness. Things can't get any worse.
    # BROKEN - Natsuki is an obvious state of sadness. She lacks confidence in herself, her player and their future.
    # DISTRESSED - Natsuki is clearly and visibly unhappy. She is distant and impersonal.
    # UPSET - Natsuki isn't particularly happy; generally to the point and somewhat cold.
    # NORMAL - Natsuki is generally cordial, but not particularly affectionate. This is the default state.
    # HAPPY - Natsuki is chipper and friendly, but still not particularly affectionate. Some teasing.
    # AFFECTIONATE - Natsuki is always glad to see her player, and feelings are beginning to obviously stir!
    # ENAMORED - Natsuki clearly has feelings for her player, and she tentatively expresses them.
    # LOVE - Natsuki is completely head-over-heels for her player, and wants nothing more than their love. Things can't get any better!
    RUINED = 1
    BROKEN = 2
    DISTRESSED = 3
    UPSET = 4
    NORMAL = 5
    HAPPY = 6
    AFFECTIONATE = 7
    ENAMORED = 8
    LOVE = 9

    _AFF_STATE_ORDER = [
        RUINED,
        BROKEN,
        DISTRESSED,
        UPSET,
        NORMAL,
        HAPPY,
        AFFECTIONATE,
        ENAMORED,
        LOVE
    ]

    def _is_aff_state_valid(state):
        """
        Checks if the given state is valid (mapped in the _AFF_STATE_ORDER)

        IN:
            state - the integer representing the state we wish to check is valid

        OUT:
            True if valid state otherwise False
        """
        return store.jn_trust_affinity_common._is_state_valid(state, _AFF_STATE_ORDER)

    def _compare_affinity_states(state_1, state_2):
        """
        Internal compareto function which compares two affinity states

        IN:
            state_1 - the first state
            state_2 - the second state

        OUT:
            integer:
                -1 if state_1 is less than state_2
                0 if either state is invalid or both states are the same
                1 if state_1 is greater than state_2
        """
        if state_1 == state_2:
            return 0

        if not _is_aff_state_valid(state_1) or not _is_aff_state_valid(state_2):
            return 0

        #If state 1 is less than state 2, return -1
        if _AFF_STATE_ORDER.index(state_1) < _AFF_STATE_ORDER.index(state_2):
            return -1

        #Else return 1
        return 1

    def is_affinity_range_valid(affinity_range):
        """
        Checks if the given affinity range is valid

        IN:
            affinity_range - The affintiy_range structure used in Topics (a tuple of the format):
                [0] - low bound (Can be None)
                [1] - high bound (Can be None)

        OUT:
            True if affinity_range is valid, False if not
        """
        if affinity_range is None:
            return True

        #deconstruct the tuple
        low_bound, high_bound = affinity_range

        #No low bound and no high bound is equivalent to just no range
        if low_bound is None and high_bound is None:
            return True

        #Now test to see if the individual parts are valid
        if (
            not _is_aff_state_valid(low_bound)
            or not _is_aff_state_valid(high_bound)
        ):
            return False

        #Now if one side is None, and we know the other is valid, this is also valid
        if low_bound is None or high_bound is None:
            return True

        #Finally compare this to make sure we don't have an inversion
        return _compare_affinity_states(low_bound, high_bound) <= 0

    def is_state_within_range(affinity_state, affinity_range):
        """
        Checks if the given affinity_state is within the given affinity_range

        IN:
            affinity_state - the state value to check if is within the affinity_range
                (NOTE: The affinity_range is considered INCLUSIVE)
            affinity_range - a tuple of the form:
                [0] - low_bound
                [1] - high_bound
        """
        #Firstly, make sure the given affinity_state is even valid
        if affinity_state is None or not _is_aff_state_valid(affinity_state):
            return False

        #No affinity_range is a full range, so this is always True
        if affinity_range is None:
            return True

        #Now, deconstruct the tuple
        low_bound, high_bound = affinity_range

        #If low and high are none, it's also a full range, always True
        if low_bound is None and high_bound is None:
            return True

        #Now we run compareTo checks
        #Firstly, single-bounded checks (one side None)
        if low_bound is None:
            #We only care about the high bound
            return _compare_affinity_states(affinity_state, high_bound) <= 0

        if high_bound is None:
            #Only the low bound matters
            return _compare_affinity_states(affinity_state, low_bound) >= 0

        #If the range is only for the single level, so they should just be equal
        if low_bound == high_bound:
            return affinity_state == low_bound

        #With the outlier cases done, simply check if we're within the range
        return (
            _compare_affinity_states(affinity_state, low_bound) >= 0
            and _compare_affinity_states(affinity_state, high_bound) <= 0
        )

    def get_affinity_state():
        """
            returns current affinity state

            states:
                RUINED = 1
                BROKEN = 2
                DISTRESSED = 3
                UPSET = 4
                NORMAL = 5
                HAPPY = 6
                AFFECTIONATE = 7
                ENAMORED = 8
                LOVE = 9

            OUT:
                current affinity state
        """
        #iterate through all thresholds
        i = 1
        for threshold in [
            THRESHOLD_LOVE,
            THRESHOLD_ENAMORED,
            THRESHOLD_AFFECTIONATE,
            THRESHOLD_HAPPY,
            THRESHOLD_NORMAL,
            THRESHOLD_UPSET,
            THRESHOLD_DISTRESSED,
            THRESHOLD_BROKEN,
            THRESHOLD_RUINED
        ]:
            #if affinity is higher than threshold return it's state
            #else check lower threshold
            if store.jn_trust_affinity_common._compare_thresholds(store.persistent.affinity, threshold) >= 0:
                return _AFF_STATE_ORDER[-i]

            # We can't go any further beyond ruined; return it
            if threshold == THRESHOLD_RUINED:
                return _AFF_STATE_ORDER[0]

            i += 1

    def get_affinity_tier_name():

        affinity_state = get_affinity_state()
        if affinity_state == LOVE:
            return "LOVE"

        elif affinity_state == ENAMORED:
            return "ENAMORED"

        elif affinity_state == AFFECTIONATE:
            return "AFFECTIONATE"

        elif affinity_state == HAPPY:
            return "HAPPY"

        elif affinity_state == NORMAL:
            return "NORMAL"

        elif affinity_state == UPSET:
            return "UPSET"

        elif affinity_state == DISTRESSED:
            return "DISTRESSED"

        elif affinity_state == BROKEN:
            return "BROKEN"

        elif affinity_state == RUINED:
            return "RUINED"

        else:
            store.jn_utils.log(
                message="Unable to get tier name for affinity {0}; affinity_state was {1}".format(store.persistent.affinity, get_affinity_state()),
                logseverity=store.jn_utils.SEVERITY_WARN
            )
            return "UNKNOWN"

init -1 python in jn_trust:
    import store
    
    # Trust levels, highest to lowest
    TRUST_ABSOLUTE = 100
    TRUST_COMPLETE = 75
    TRUST_FULL = 50
    TRUST_PARTIAL = 25
    TRUST_NEUTRAL = 0
    TRUST_SCEPTICAL = -25
    TRUST_DIMINISHED = -50
    TRUST_DISBELIEF = -75
    TRUST_SHATTERED = -100

    #Trust States (non-prefixed as these are used for trust_range)
    # SHATTERED - Natsuki doesn't know what to believe any more.
    # DISBELIEF - Natsuki has no reason to believe her player, and doubts that trust can be regained.
    # DIMINISHED - Natsuki has serious doubts about whether she can trust her player at all.
    # SCEPTICAL - Natsuki has some doubts about whether she can trust her player, especially with sensitive topics.
    # NEUTRAL - Natsuki has no particular reason to trust - or distrust - her player.
    # PARTIAL - Natsuki feels more inclined to trust her player, but with considerable caution.
    # FULL - Natsuki generally trusts her player.
    # COMPLETE - Natsuki highly trusts her player, with all but her biggest sensitivities unknown.
    # ABSOLUTE - Natsuki's trust is absolute; her heart is completely open to her player.
    SHATTERED = 1
    DISBELIEF = 2
    DIMINISHED = 3
    SCEPTICAL = 4
    NEUTRAL = 5
    PARTIAL = 6
    FULL = 7
    COMPLETE = 8
    ABSOLUTE = 9

    _TRUST_STATE_ORDER = [
        SHATTERED,
        DISBELIEF,
        DIMINISHED,
        SCEPTICAL,
        NEUTRAL,
        PARTIAL,
        FULL,
        COMPLETE,
        ABSOLUTE
    ]

    def get_trust_state():
        """
            returns current trust state

            states:
                SHATTERED = 1
                DISBELIEF = 2
                DIMINISHED = 3
                SCEPTICAL = 4
                NEUTRAL = 5
                PARTIAL = 6
                FULL = 7
                COMPLETE = 8
                ABSOLUTE = 9

            OUT:
                current trust state
        """
        #iterate through all thresholds
        i = 1
        for threshold in [
            TRUST_ABSOLUTE,
            TRUST_COMPLETE,
            TRUST_FULL,
            TRUST_PARTIAL,
            TRUST_NEUTRAL,
            TRUST_SCEPTICAL,
            TRUST_DIMINISHED,
            TRUST_DISBELIEF,
            TRUST_SHATTERED
        ]:
            #if trust is higher than threshold return it's state
            #else check lower threshold
            if store.jn_trust_affinity_common._compare_thresholds(store.persistent.trust, threshold) >= 0:
                return _TRUST_STATE_ORDER[-i]

            # We can't go any further beyond shattered; return it
            if threshold == TRUST_SHATTERED:
                return _TRUST_STATE_ORDER[0]

            i += 1

    def get_trust_tier_name():
        trust_state = get_trust_state()

        if trust_state == ABSOLUTE:
            return "ABSOLUTE"

        elif trust_state == COMPLETE:
            return "COMPLETE"

        elif trust_state == FULL:
            return "FULL"

        elif trust_state == PARTIAL:
            return "PARTIAL"

        elif trust_state == NEUTRAL:
            return "NEUTRAL"

        elif trust_state == SCEPTICAL:
            return "SCEPTICAL"

        elif trust_state == DIMINISHED:
            return "DIMINISHED"

        elif trust_state == DISBELIEF:
            return "DISBELIEF"

        elif trust_state == SHATTERED:
            return "SHATTERED"

        else:
            store.jn_utils.log(
                message="Unable to get tier name for trust {0}; trust_state was {1}".format(store.persistent.trust, get_trust_state()),
                logseverity=store.jn_utils.SEVERITY_WARN
            )
            return "UNKNOWN"
