package mysqldb

import (
	"database/sql"
	"fmt"
	"github.com/jmoiron/sqlx"
)

type MySQL struct {
	User    string
	Pwd     string
	Host    string
	Name    string
	Charset string
}

func (s *MySQL) String() string {
	if s.Charset == "" {
		s.Charset = "utf8"
	}
	return fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?charset=%s&parseTime=true",
		s.User, s.Pwd, s.Host, s.Name, s.Charset)
}

const (
	// MySQLMaxOpenConns 最大连接数
	MySQLMaxOpenConns = 50
	// MySQLMaxIdleConns 最大空闲连接数
	MySQLMaxIdleConns = 10
)

func NewMySQLDBConn(connStr string, maxOpenConns, maxIdleConns int) *sqlx.DB {
	db, err := sql.Open("mysql", connStr)
	if err != nil {
		panic(err)
	}
	db.SetMaxOpenConns(maxOpenConns)
	db.SetMaxIdleConns(maxIdleConns)
	if err = db.Ping(); err != nil {
		panic(err)
	}
	return sqlx.NewDb(db, "mysql")
}
