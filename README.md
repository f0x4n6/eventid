# EventID

[![Go Report](https://goreportcard.com/badge/github.com/f0x4n6/eventid?style=for-the-badge)](https://goreportcard.com/report/github.com/f0x4n6/eventid)
[![Build](https://img.shields.io/github/actions/workflow/status/f0x4n6/eventid/goreleaser.yml?style=for-the-badge&label=build)](https://github.com/f0x4n6/eventid/actions)
[![Release](https://img.shields.io/github/release/f0x4n6/eventid.svg?style=for-the-badge&label=release)](https://github.com/f0x4n6/eventid/releases)

Lookup Windows event messages by id and provider (up to Windows 10).

```console
go install go.foxforensics.dev/eventid@latest
```

## Usage
```console
$ eventid [PROVIDER:]ID ...
```

## Acknowledgments
* Based on the [evtx-data](https://github.com/Velocidex/evtx-data/tree/master/welm) by [Velocidex](https://github.com/Velocidex).
* Based on the [WELM project](https://github.com/nsacyber/Windows-Event-Log-Messages) by [NSACyber](https://github.com/nsacyber).

## License
Released under the [MIT License](LICENSE.md).