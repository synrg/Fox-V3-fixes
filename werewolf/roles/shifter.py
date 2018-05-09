from werewolf.role import Role


class Shifter(Role):
    """
    Base Role class for werewolf game
    
    Category enrollment guide as follows (category property):
        Town:
        1: Random, 2: Investigative, 3: Protective, 4: Government,
        5: Killing, 6: Power (Special night action)
        
        Werewolf:
        11: Random, 12: Deception, 15: Killing, 16: Support
        
        Neutral:
        21: Benign, 22: Evil, 23: Killing
        
        
        Example category:
        category = [1, 5, 6] Could be Veteran
        category = [1, 5] Could be Bodyguard
        category = [11, 16] Could be Werewolf Silencer
        
    
    Action guide as follows (on_event function):
        _at_night_start
        0. No Action
        1. Detain actions (Jailer/Kidnapper)
        2. Group discussions and choose targets
        
        _at_night_end
        0. No Action
        1. Self actions (Veteran)
        2. Target switching and role blocks (bus driver, witch, escort)
        3. Protection / Preempt actions (bodyguard/framer)
        4. Non-disruptive actions (seer/silencer)
        5. Disruptive actions (Killing)
        6. Role altering actions (Cult / Mason)
    """

    rand_choice = False  # Determines if it can be picked as a random role (False for unusually disruptive roles)
    category = [22]  # List of enrolled categories (listed above)
    alignment = 3  # 1: Town, 2: Werewolf, 3: Neutral
    channel_id = ""  # Empty for no private channel
    unique = False  # Only one of this role per game
    game_start_message = (
        "Your role is **Shifter**\n"
        "You have no win condition (yet)\n"
        "Swap your role with other players during the night using `[p]ww choose <ID>`\n"
        "Lynch players during the day with `[p]ww vote <ID>`"
    )
    description = (
        "A creature of unknown origin seeks to escape it's ethereal nightmare\n"
        "It's curse cannot be broken, but transfers are allowed"
    )
    icon_url = None  # Adding a URL here will enable a thumbnail of the role

    def __init__(self, game):
        super().__init__(game)

        self.shift_target = None
        self.action_list = [
            (self._at_game_start, 1),  # (Action, Priority)
            (self._at_day_start, 0),
            (self._at_voted, 0),
            (self._at_kill, 0),
            (self._at_hang, 0),
            (self._at_day_end, 0),
            (self._at_night_start, 2),  # Chooses targets
            (self._at_night_end, 6),  # Role Swap
            (self._at_visit, 0)
        ]

    async def see_alignment(self, source=None):
        """
        Interaction for investigative roles attempting
        to see alignment (Village, Werewolf, Other)
        """
        return "Other"

    async def get_role(self, source=None):
        """
        Interaction for powerful access of role
        Unlikely to be able to deceive this
        """
        return "Shifter"

    async def see_role(self, source=None):
        """
        Interaction for investigative roles.
        More common to be able to deceive this action
        """
        return "Shifter"

    async def _at_night_start(self, data=None):
        await super()._at_night_start(data)
        self.shift_target = None
        await self.game.generate_targets(self.player.member)
        await self.player.send_dm("**Pick a target to shift into**")

    async def _at_night_end(self, data=None):
        await super()._at_night_end(data)

    async def choose(self, ctx, data):
        """Handle night actions"""
        await super().choose(ctx, data)
