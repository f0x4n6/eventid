// Lookup Windows event messages by their event id (up to Windows 10).
//
// Usage:
//
//	eventid [provider:]id ...
//
// The arguments are:
//
//	[provider:]id
//	    The event id with optional provider prefix (required).
package main

import (
	"fmt"
	"maps"
	"os"
	"slices"
	"strconv"
	"strings"

	"github.com/fatih/color"

	"go.foxforensics.dev/eventid/events"
)

func main() {
	if len(os.Args) == 1 || os.Args[1] == "--help" {
		_, _ = fmt.Fprintln(os.Stderr, "usage: eventid [provider:]id ...")
		os.Exit(2)
	}

	db, err := events.Load()

	if err != nil {
		_, _ = fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	all := slices.Sorted(maps.Keys(db))

	for i, id := range os.Args[1:] {
		var tag string
		var found bool

		_, _ = fmt.Println(color.HiWhiteString("=== Windows Event ID: %s ===\n", id))

		if strings.Contains(id, ":") {
			t := strings.SplitN(id, ":", 2)
			tag, id = t[0], t[1]
		}

		n, err := strconv.ParseInt(id, 10, 32)

		if err != nil {
			_, _ = fmt.Fprintf(os.Stderr, "[!] %s\n\n", color.RedString(err.Error()))
			continue
		}

		keys := all

		if len(tag) > 0 {
			keys = keys[:0]

			for _, k := range all {
				if strings.Contains(k, tag) {
					keys = append(keys, k)
				}
			}
		}

		for _, p := range keys {
			if m, ok := db[p][n]; ok {
				_, _ = fmt.Printf("[*] %s\n    %s \n", color.YellowString(p), color.GreenString(m))
				found = true
			}
		}

		if !found {
			_, _ = fmt.Fprintf(os.Stderr, "[!] %s\n", color.RedString("nothing found"))
		}

		if i < len(os.Args[1:])-1 {
			_, _ = fmt.Println()
		}
	}
}
