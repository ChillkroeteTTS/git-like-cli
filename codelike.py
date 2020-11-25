import click

@click.group()
def main():
    click.echo('hello world')

@main.command()
def init():
    click.echo('Init')

if __name__ == '__main__':
    main()
