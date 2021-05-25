import epydoc.cli
epydoc.cli.optparse.sys.argv = [
    'epydoc',
    '--config', 'pyhiewdoc.cfg',
    '-v',
    '--simple-term'
]

# Generate the documentation
epydoc.cli.cli()

