from commands.command import Command
from evennia import CmdSet
from evennia import InterruptCommand


simpsocials = ["smile", "frown", "nod", "wave", "point", "grin", "gaze"]

class CmdSocials(Command):
    """
    A social command

    Usage:
      social [<someone>] [<adverb>]

    social to someone in your vicinity or to the room
    in general.
    """

    key = "social_cmd"
    aliases = simpsocials
    locks = "cmd:all()"
    help_category = "Socials"


    def parse(self):
        self.target = None
        self.adverb = None
        args = self.args.strip().split()
        if args:
            target = self.caller.search(args[0], quiet=True)
            if target:
                self.target = target[0]
                self.adverb = " ".join(args[1:])
            elif len(args) > 1:
                raise InterruptCommand(f"Could not find '{args[0]}'.")
            else:
                self.adverb = " ".join(args)

    def func(self):
        caller = self.caller
        if self.cmdstring == self.key:
            caller.msg("Nope.")
            return
        
        social = self.cmdstring
        if self.target and self.adverb:
            self.caller.location.msg_contents(f"$You() $conj({self.cmdstring}) {self.adverb} at $you(target).", mapping={'target': self.target}, from_obj=self.caller)
        elif self.target and not self.adverb:
            self.caller.location.msg_contents(f"$You() $conj({self.cmdstring}) at $you(target).", mapping={'target': self.target}, from_obj=self.caller)
        elif not self.target and self.adverb:
            self.caller.location.msg_contents(f"$You() $conj({self.cmdstring}) {self.adverb}.", from_obj=self.caller)
        else:
            self.caller.location.msg_contents(f"$You() $conj({self.cmdstring}).", from_obj=self.caller)

        

class emoteCmdset(CmdSet):

    def at_cmdset_creation(self):
        self.add(CmdSocials)

