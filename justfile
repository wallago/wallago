import 'just/nix.just'
import 'just/editorconfig.just'
import 'just/typos.just'
import 'just/lychee.just'
import 'just/git.just'
import 'just/github.just'
import 'just/gif.just'

# List all commands
default:
    @just --list

# Run every check before pushing
[group('ci')]
ci:
    @just nix-lint
    @just editorconfig
    @just typos
    @just links
    @just workflows
