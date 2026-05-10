// Package events provides an event message database.
package events

import (
	"bytes"
	"encoding/json"
	"io"

	_ "embed"

	"github.com/ulikunitz/xz"
)

//go:embed database.xz
var database []byte

// Providers mapping of event ids and messages.
type Providers map[string]map[int64]string

// Load returns the decompressed embedded providers.
func Load() (Providers, error) {
	var prv Providers

	r, err := xz.NewReader(bytes.NewReader(database))

	if err != nil {
		return nil, err
	}

	b, err := io.ReadAll(r)

	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(b, &prv)

	return prv, err
}
