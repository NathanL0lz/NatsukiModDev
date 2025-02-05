default persistent.jn_natsuki_current_pose = "sitting"
default persistent.jn_natsuki_current_outfit = "uniform"
default persistent.jn_natsuki_current_hairstyle = "default"
default persistent.jn_natsuki_current_accessory = "hairbands/red"
default persistent.jn_natsuki_current_eyewear = None
default persistent.jn_natsuki_current_headgear = None
default persistent.jn_natsuki_current_necklace = None
default persistent.jn_natsuki_saved_outfits = {}
default persistent.jn_natsuki_auto_outfit_change_enabled = True

init python in jn_outfits:
    import random
    import store
    import store.jn_affinity as jn_affinity
    import store.jn_utils as jn_utils

    current_outfit_name = None
    _use_alt_outfit = random.choice(range(1, 3)) == 1

    class JNOutfitPreset():
        """
        Describes a complete outfit for Natsuki to wear; including clothing, hairstyle, etc.
        At minimum, an outfit must consist of clothes and a hairstyle
        """
        def __init__(
            self,
            display_name,
            reference_name,
            unlocked,
            clothes,
            hairstyle,
            accessory=None,
            eyewear=None,
            headgear=None,
            necklace=None
        ):
            if clothes is None:
                raise TypeError("Outfit clothing cannot be None")
                return

            if hairstyle is None:
                raise TypeError("Outfit hairstyle cannot be None")
                return

            self.display_name = display_name
            self.reference_name = reference_name
            self.unlocked = unlocked
            self.clothes = clothes
            self.hairstyle = hairstyle
            self.accessory = accessory
            self.eyewear = eyewear
            self.headgear = headgear
            self.necklace = necklace

    #TODO: We need a means of storing and recalling user-defined outfit combos, as well as creating them.
    # For now, we'll settle with presets.

    # Default outfits
    DEFAULT_OUTFIT_UNIFORM = JNOutfitPreset(
        display_name="School uniform",
        reference_name="jn_school_uniform",
        unlocked=True,
        clothes="uniform",
        hairstyle="default",
        accessory="hairbands/red"
    )

    DEFAULT_OUTFIT_CASUAL_WEEKDAY = JNOutfitPreset(
        display_name="Casual clothes",
        reference_name="jn_casual_weekday",
        unlocked=True,
        clothes="casual",
        hairstyle="default",
        accessory="hairbands/red"
    )

    DEFAULT_OUTFIT_CASUAL_WEEKDAY_ALT = JNOutfitPreset(
        display_name="Casual clothes",
        reference_name="jn_casual_weekday_alt",
        unlocked=True,
        clothes="casual",
        hairstyle="ponytail",
        accessory="hairbands/white"
    )

    DEFAULT_OUTFIT_CASUAL_WEEKEND = JNOutfitPreset(
        display_name="Casual clothes",
        reference_name="jn_casual_weekend",
        unlocked=True,
        clothes="casual",
        hairstyle="bun",
        accessory="hairbands/red"
    )

    DEFAULT_OUTFIT_CASUAL_WEEKEND_ALT = JNOutfitPreset(
        display_name="Casual clothes",
        reference_name="jn_casual_weekend_alt",
        unlocked=True,
        clothes="casual",
        hairstyle="messy_bun",
        accessory="hairbands/white"
    )

    DEFAULT_OUTFIT_NIGHT = JNOutfitPreset(
        display_name="Pyjamas",
        reference_name="jn_pajamas_night",
        unlocked=True,
        clothes="star_pajamas",
        hairstyle="down",
        accessory="hairbands/red"
    )

    DEFAULT_OUTFIT_MORNING = JNOutfitPreset(
        display_name="Pyjamas",
        reference_name="jn_pajamas_morning",
        unlocked=True,
        clothes="star_pajamas",
        hairstyle="bedhead",
        accessory="hairbands/red"
    )

    DEFAULT_OUTFIT_MORNING_ALT = JNOutfitPreset(
        display_name="Pyjamas",
        reference_name="jn_pajamas_morning_alt",
        unlocked=True,
        clothes="star_pajamas",
        hairstyle="bedhead",
        accessory="hairbands/green"
    )

    DEFAULT_OUTFIT_CHRISTMAS = JNOutfitPreset(
        display_name="Natsu Claus",
        reference_name="jn_natsu_claus",
        unlocked=True,
        clothes="casual",
        hairstyle="down",
        accessory="hairbands/green",
        headgear="natsu_claus_hat"
    )

    DEFAULT_OUTFIT_VALENTINE = JNOutfitPreset(
        display_name="Valentine Dress",
        reference_name="jn_valentine",
        unlocked=True,
        clothes="red_rose_lace_dress",
        hairstyle="messy_bun",
        accessory="hairbands/white"
    )

    # Default outfit schedules
    DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_HIGH_AFFINITY = {
        store.JNTimeBlocks.early_morning: DEFAULT_OUTFIT_MORNING_ALT if _use_alt_outfit else DEFAULT_OUTFIT_MORNING,
        store.JNTimeBlocks.mid_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.late_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.afternoon: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.evening: DEFAULT_OUTFIT_CASUAL_WEEKDAY_ALT if _use_alt_outfit else DEFAULT_OUTFIT_CASUAL_WEEKDAY,
        store.JNTimeBlocks.night: DEFAULT_OUTFIT_NIGHT
    }

    DEFAULT_OUTFIT_SCHEDULE_WEEKEND_HIGH_AFFINITY = {
        store.JNTimeBlocks.early_morning: DEFAULT_OUTFIT_MORNING_ALT if _use_alt_outfit else DEFAULT_OUTFIT_MORNING,
        store.JNTimeBlocks.mid_morning: DEFAULT_OUTFIT_MORNING_ALT if _use_alt_outfit else DEFAULT_OUTFIT_MORNING,
        store.JNTimeBlocks.late_morning: DEFAULT_OUTFIT_MORNING_ALT if _use_alt_outfit else DEFAULT_OUTFIT_MORNING,
        store.JNTimeBlocks.afternoon: DEFAULT_OUTFIT_CASUAL_WEEKEND_ALT if _use_alt_outfit else DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.evening: DEFAULT_OUTFIT_CASUAL_WEEKEND_ALT if _use_alt_outfit else DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.night:DEFAULT_OUTFIT_NIGHT
    }

    DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_MEDIUM_AFFINITY = {
        store.JNTimeBlocks.early_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.mid_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.late_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.afternoon: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.evening: DEFAULT_OUTFIT_CASUAL_WEEKDAY,
        store.JNTimeBlocks.night: DEFAULT_OUTFIT_CASUAL_WEEKDAY
    }

    DEFAULT_OUTFIT_SCHEDULE_WEEKEND_MEDIUM_AFFINITY = {
        store.JNTimeBlocks.early_morning: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.mid_morning: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.late_morning: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.afternoon: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.evening: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.night: DEFAULT_OUTFIT_CASUAL_WEEKEND
    }

    DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_LOW_AFFINITY = {
        store.JNTimeBlocks.early_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.mid_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.late_morning: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.afternoon: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.evening: DEFAULT_OUTFIT_UNIFORM,
        store.JNTimeBlocks.night: DEFAULT_OUTFIT_UNIFORM
    }

    DEFAULT_OUTFIT_SCHEDULE_WEEKEND_LOW_AFFINITY = {
        store.JNTimeBlocks.early_morning: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.mid_morning: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.late_morning: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.afternoon: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.evening: DEFAULT_OUTFIT_CASUAL_WEEKEND,
        store.JNTimeBlocks.night: DEFAULT_OUTFIT_CASUAL_WEEKEND
    }

    def set_outfit(outfit):
        """
        Sets Natsuki's appearance using the given outfit.

        IN:
            - outfit - JNOutfitPreset outfit for Natsuki to wear
        """
        global current_outfit_name
        
        if outfit.unlocked:
            store.persistent.jn_natsuki_current_outfit = outfit.clothes
            store.persistent.jn_natsuki_current_hairstyle = outfit.hairstyle
            store.persistent.jn_natsuki_current_accessory = outfit.accessory
            store.persistent.jn_natsuki_current_eyewear = outfit.eyewear
            store.persistent.jn_natsuki_current_headgear = outfit.headgear
            store.persistent.jn_natsuki_current_necklace = outfit.necklace
            current_outfit_name = outfit.reference_name

        else:
            jn_utils.log("Cannot dress Natsuki in outfit {0}; outfit is locked".format(outfit.name))

    def get_outfit_for_time_block():
        """
        Returns the outfit corresponding to affinity, the current time block and whether or not is is a weekday.
        """
        if jn_affinity.get_affinity_state() >= jn_affinity.AFFECTIONATE:
            if store.jn_is_weekday():
                return DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_HIGH_AFFINITY.get(store.jn_get_current_time_block())

            else:
                return DEFAULT_OUTFIT_SCHEDULE_WEEKEND_HIGH_AFFINITY.get(store.jn_get_current_time_block())
        
        elif jn_affinity.get_affinity_state() >= jn_affinity.UPSET:
            if store.jn_is_weekday():
                return DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_MEDIUM_AFFINITY.get(store.jn_get_current_time_block())

            else:
                return DEFAULT_OUTFIT_SCHEDULE_WEEKEND_MEDIUM_AFFINITY.get(store.jn_get_current_time_block())
        
        else:
            if store.jn_is_weekday():
                return DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_LOW_AFFINITY.get(store.jn_get_current_time_block())

            else:
                return DEFAULT_OUTFIT_SCHEDULE_WEEKEND_LOW_AFFINITY.get(store.jn_get_current_time_block())

    def set_outfit_for_time_block():
        """
        Sets Natsuki's outfit based on the time of day, whether it is a weekday/weekend, and affinity.
        """
        if jn_affinity.get_affinity_state() >= jn_affinity.AFFECTIONATE:
            if store.jn_is_weekday():
                set_outfit(DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_HIGH_AFFINITY.get(store.jn_get_current_time_block()))

            else:
                set_outfit(DEFAULT_OUTFIT_SCHEDULE_WEEKEND_HIGH_AFFINITY.get(store.jn_get_current_time_block()))
        
        elif jn_affinity.get_affinity_state() >= jn_affinity.UPSET:
            if store.jn_is_weekday():
                set_outfit(DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_MEDIUM_AFFINITY.get(store.jn_get_current_time_block()))

            else:
                set_outfit(DEFAULT_OUTFIT_SCHEDULE_WEEKEND_MEDIUM_AFFINITY.get(store.jn_get_current_time_block()))
        
        else:
            if store.jn_is_weekday():
                set_outfit(DEFAULT_OUTFIT_SCHEDULE_WEEKDAY_LOW_AFFINITY.get(store.jn_get_current_time_block()))

            else:
                set_outfit(DEFAULT_OUTFIT_SCHEDULE_WEEKEND_LOW_AFFINITY.get(store.jn_get_current_time_block()))
            
label outfits_time_of_day_change:
    if jn_affinity.get_affinity_state() >= jn_affinity.ENAMORED:
        n 1uchbg "Oh!{w=0.2} I gotta change,{w=0.1} just give me a sec...{w=0.75}{nw}"

    elif jn_affinity.get_affinity_state() >= jn_affinity.HAPPY:
        n 1unmpu "Oh!{w=0.2} I should probably change,{w=0.1} one second..."
        n 1flrpol "A-{w=0.1}and no peeking,{w=0.1} got it?!{w=0.75}{nw}"

    elif jn_affinity.get_affinity_state() >= jn_affinity.NORMAL:
        n 1unmpu "Oh -{w=0.1} I gotta get changed.{w=0.2} I'll be back in a sec.{w=0.75}{nw}"

    elif jn_affinity.get_affinity_state() >= jn_affinity.DISTRESSED:
        n 1nnmsl "Back in a second.{w=0.75}{nw}"

    else:
        n 1fsqsl "I'm changing.{w=0.75}{nw}"

    play audio clothing_ruffle
    $ jn_outfits.set_outfit_for_time_block()
    with Fade(out_time=0.1, hold_time=1, in_time=0.5, color="#181212")
    
    if jn_affinity.get_affinity_state() >= jn_affinity.ENAMORED:
        n 1uchgn "Ta-da!{w=0.2} There we go!{w=0.2} Ehehe.{w=0.75}{nw}"

    elif jn_affinity.get_affinity_state() >= jn_affinity.HAPPY:
        n 1nchbg "Okaaay!{w=0.2} I'm back!{w=0.75}{nw}"

    elif jn_affinity.get_affinity_state() >= jn_affinity.NORMAL:
        n 1nnmsm "And...{w=0.3} all done.{w=0.75}{nw}"

    elif jn_affinity.get_affinity_state() >= jn_affinity.DISTRESSED:
        n 1nllsl "I'm back.{w=0.75}{nw}"

    else:
        n 1fsqsl "...{w=0.75}{nw}"

    show natsuki idle
    return
