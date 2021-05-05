package conf

import (
	"paper/libs/testutil"
	"testing"
)

var Conf = &struct {
	DBConf *testDBConf `json:"db_conf"`
}{}

type testDBConf struct {
	Host              string `json:"host"`
	Name              string `json:"name"`
	User              string `json:"user"`
	Pwd               string `json:"pwd"`
	MaxOpenConnection int    `json:"max_open_connection"`
}

func TestInitJsonConf(t *testing.T) {
	jsonConfPath = "./test-conf.json"
	if err := InitJsonConf(Conf); err != nil {
		t.Fatal(err)
	}
	testutil.LogJson(t, Conf)
}
