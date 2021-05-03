package conf

import (
	"paper/libs/mysqldb"
)

var Conf = &struct {
	PaperDB mysqldb.DBConf `json:"paper_db"`
}{}
