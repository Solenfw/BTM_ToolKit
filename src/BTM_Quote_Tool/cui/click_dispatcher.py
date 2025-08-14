import click
from .commands import CommandHandler
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """BTM Quote Tool"""
    ctx.obj['command_handler'] = CommandHandler(
        ctx.obj['MartinDataset'],
        ctx.obj['AesculapDataset'],
        ctx.obj['IntegraDataset'],
        ctx.obj['MartinSourceFile'],
        ctx.obj['objects'],
        ctx.obj['MartinCatalog'],
        ctx.obj['IntegraCatalog'],
        ctx.obj['AesculapCatalog']
    )
    if ctx.invoked_subcommand is None:
        ctx.invoke(interactive)

@cli.command()
@click.pass_context
def interactive(ctx):
    """Interactive mode."""
    command_completer = WordCompleter(list(cli.commands.keys()))
    history = FileHistory('history.txt')

    while True:
        try:
            command_with_args = prompt(
                "> ",
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
                completer=command_completer,
            ).strip().split()
            command = command_with_args[0]
            args = command_with_args[1:]

            if command == 'end':
                break
            
            cmd = cli.get_command(ctx, command)
            if cmd:
                if cmd.params:
                    if args:
                        ctx.invoke(cmd, keyword=args[0])
                    else:
                        ctx.invoke(cmd)
                else:
                    ctx.invoke(cmd)
            else:
                # if command is not a click command, assume it is a search keyword
                ctx.invoke(search, keyword=command)

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"Error: {e}")

@cli.command()
@click.pass_context
def help(ctx):
    """Show help message."""
    ctx.obj['command_handler'].handle_help()

@cli.command()
@click.pass_context
def end(ctx):
    """Terminate the program."""
    ctx.obj['command_handler'].handle_terminate()

@cli.command()
@click.pass_context
@click.argument('keyword')
def reference(ctx, keyword):
    """Handle reference."""
    ctx.obj['command_handler'].handle_reference(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def check(ctx, keyword):
    """Check saved codes."""
    ctx.obj['command_handler'].handle_check(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def inch(ctx, keyword):
    """Convert cm to inch."""
    ctx.obj['command_handler'].handle_inch(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def replace(ctx, keyword):
    """Replace a code."""
    ctx.obj['command_handler'].handle_replace(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def load(ctx, keyword):
    """Save a code."""
    ctx.obj['command_handler'].handle_load(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def pick(ctx, keyword):
    """Pick a code."""
    ctx.obj['command_handler'].handle_pick(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def sculap(ctx, keyword):
    """Search for Aesculap code."""
    ctx.obj['command_handler'].handle_sculap(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def integra(ctx, keyword):
    """Search for Integra code."""
    ctx.obj['command_handler'].handle_integra(keyword)

@cli.command()
@click.pass_context
def refresh(ctx):
    """Reload the data."""
    ctx.obj['command_handler'].handle_refresh()

@cli.command()
@click.pass_context
def clear(ctx):
    """Clear the screen."""
    ctx.obj['command_handler'].handle_clear()

@cli.command()
@click.pass_context
@click.argument('keyword')
def search_by_code(ctx, keyword):
    """Search by code."""
    ctx.obj['command_handler'].handle_search_by_code(keyword)

@cli.command()
@click.pass_context
@click.argument('keyword')
def search(ctx, keyword):
    """Search for a product."""
    ctx.obj['command_handler'].handle_search(keyword)
