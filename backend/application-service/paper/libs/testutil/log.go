package testutil

import (
	"encoding/json"
	"testing"
)

func LogJson(t *testing.T, v interface{}) {
	bs, _ := json.Marshal(v)
	t.Log(string(bs))
}
