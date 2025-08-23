from ..string_utilities import string_cleaner
import regex

class CommandDispatcher:
    def __init__(self, command_handler):
        self.command_handler = command_handler
        self.keyword_handlers = {
            'help': self.command_handler.handle_help,
            'end': self.command_handler.handle_terminate,
            'refresh': self.command_handler.handle_refresh,
            'clear': self.command_handler.handle_clear,
            'cls': self.command_handler.handle_clear,
        }

    def dispatch(self, keyword):
        keyword = string_cleaner(keyword)

        if keyword in self.keyword_handlers:
            self.keyword_handlers[keyword]()
            return

        if keyword.endswith('rf'):
            self.command_handler.handle_reference(keyword)
        elif keyword.endswith('code'):
            self.command_handler.handle_check(keyword)
        elif keyword.startswith('inch'):
            self.command_handler.handle_inch(keyword)
        elif keyword.startswith('replace'):
            self.command_handler.handle_replace(keyword)
        elif keyword.startswith('load'):
            self.command_handler.handle_load(keyword)
        elif keyword.startswith('get'):
            self.command_handler.handle_pick(keyword)
        elif keyword.startswith('sculap'):
            self.command_handler.handle_sculap(keyword)
        elif keyword.startswith('integra'):
            self.command_handler.handle_integra(keyword)
        elif regex.fullmatch(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword):
            if self.command_handler.handle_search_by_code(keyword):
                return
        else:
            self.command_handler.handle_search(keyword)
