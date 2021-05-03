package mysqldb

type DBConf struct {
	Host              string `json:"host"`
	Name              string `json:"name"`
	User              string `json:"user"`
	Pwd               string `json:"pwd"`
	MaxOpenConnection int    `json:"max_open_connection"`
}
