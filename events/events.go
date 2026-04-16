// Package events provides an event message database.
package events

import (
	"bytes"
	"encoding/json"
	"io"

	_ "embed"

	"github.com/klauspost/compress/zstd"
)

//go:embed events_db.zst
var db []byte

// Providers mapping of event ids and messages.
type Providers map[string]map[int64]string

// Load returns the decompressed embedded providers.
func Load() (Providers, error) {
	var prv Providers

	r, err := zstd.NewReader(bytes.NewReader(db))

	if err != nil {
		return nil, err
	}

	defer r.Close()

	b, err := io.ReadAll(r)

	if err != nil {
		return nil, err
	}

	err = json.Unmarshal(b, &prv)

	return prv, err
}
