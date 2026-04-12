// Package evtx_db provides an event message database.
package evtx_db

import (
	"bytes"
	"encoding/json"
	"io"

	_ "embed"

	"github.com/klauspost/compress/zstd"
)

//go:embed evtx_db.zst
var db []byte

// Provider mapping of event ids and messages.
type Provider map[string]map[int64]string

// Load returns the decompressed embedded provider map.
func Load() (Provider, error) {
	var prv Provider

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
