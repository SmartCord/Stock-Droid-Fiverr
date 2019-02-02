from imports import * 

class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot
    
    async def on_command_error(self, ctx, exception):
        ignored = (commands.CommandNotFound)
        if isinstance(exception, ignored):
            return 

        errorMsg = exception.with_traceback(exception.__traceback__)
        await error(ctx, errorMsg)
    
def setup(bot):
    bot.add_cog(ErrorHandler(bot))