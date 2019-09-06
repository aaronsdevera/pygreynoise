"""CLI subcommands."""

import platform

import click

from greynoise.__version__ import __version__
from greynoise.cli.decorator import gnql_command, ip_lookup_command
from greynoise.cli.helper import get_ip_addresses, get_queries
from greynoise.util import CONFIG_FILE, DEFAULT_CONFIG, save_config


class SubcommandNotImplemented(click.ClickException):
    """Exception used temporarily for subcommands that have not been implemented.

    :param subcommand_name: Name of the subcommand to display in the error message.
    :type subcommand_function: str

    """

    def __init__(self, subcommand_name):
        message = "{!r} subcommand is not implemented yet.".format(subcommand_name)
        super(SubcommandNotImplemented, self).__init__(message)


@click.command()
def account():
    """View information about your GreyNoise account."""
    raise SubcommandNotImplemented("account")


@click.command()
def alerts():
    """List, create, delete, and manage your GreyNoise alerts."""
    raise SubcommandNotImplemented("alerts")


@click.command()
def analyze():
    """Analyze the IP addresses in a log file, stdin, etc."""
    raise SubcommandNotImplemented("analyze")


@click.command()
def feedback():
    """Send feedback directly to the GreyNoise team."""
    raise SubcommandNotImplemented("feedback")


@click.command(name="filter")
def filter_():
    """"Filter the noise from a log file, stdin, etc."""
    raise SubcommandNotImplemented("filter")


@click.command(name="help")
@click.pass_context
def help_(context):
    """Show this message and exit."""
    click.echo(context.parent.get_help())


@click.command()
def interesting():
    """Report an IP as "interesting"."""
    raise SubcommandNotImplemented("interesting")


@ip_lookup_command
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def ip(
    context,
    api_client,
    api_key,
    input_file,
    output_file,
    output_format,
    verbose,
    ip_address,
):
    """Query GreyNoise for all information on a given IP."""
    ip_addresses = get_ip_addresses(context, input_file, ip_address)
    results = [api_client.ip(ip_address=ip_address) for ip_address in ip_addresses]
    return results


@click.command()
def pcap():
    """Get PCAP for a given IP address."""
    raise SubcommandNotImplemented("pcap")


@gnql_command
def query(
    context, api_client, api_key, input_file, output_file, output_format, verbose, query
):
    """Run a GNQL (GreyNoise Query Language) query."""
    queries = get_queries(context, input_file, query)
    results = [api_client.query(query=query) for query in queries]
    return results


@ip_lookup_command
def quick(
    context, api_client, api_key, input_file, output_file, output_format, ip_address
):
    """Quickly check whether or not one or many IPs are "noise"."""
    ip_addresses = get_ip_addresses(context, input_file, ip_address)
    results = []
    if ip_addresses:
        results.extend(api_client.quick(ip_addresses=ip_addresses))
    return results


@click.command()
@click.option("-k", "--api-key", required=True, help="Key to include in API requests")
@click.option("-t", "--timeout", type=click.INT, help="API client request timeout")
def setup(api_key, timeout):
    """Configure API key."""
    config = {"api_key": api_key}
    if timeout is None:
        config["timeout"] = DEFAULT_CONFIG["timeout"]
    else:
        config["timeout"] = timeout
    save_config(config)
    click.echo("Configuration saved to {!r}".format(CONFIG_FILE))


@click.command()
def signature():
    """Submit an IDS signature to GreyNoise to be deployed to all GreyNoise nodes."""
    raise SubcommandNotImplemented("signature")


@gnql_command
def stats(
    context, api_client, api_key, input_file, output_file, output_format, verbose, query
):
    """Get aggregate stats from a given GNQL query."""
    queries = get_queries(context, input_file, query)
    results = [api_client.stats(query=query) for query in queries]
    return results


@click.command()
def version():
    """Get version and OS information for your GreyNoise commandline installation."""
    click.echo(
        "greynoise {}\n"
        "  Python {}\n"
        "  {}\n".format(__version__, platform.python_version(), platform.platform())
    )
