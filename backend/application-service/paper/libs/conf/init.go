package conf

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
	"paper/libs/errors"
	"path/filepath"
	"reflect"
	"time"
)

var jsonConfPath = "./service-conf.json"

func InitJsonConfPeriod(conf interface{}, timeIntervalSec int) {
	if err := InitJsonConf(conf); err != nil {
		panic(err)
	}
	tk := time.NewTicker(time.Second * time.Duration(timeIntervalSec))
	for range tk.C {
		if err := InitJsonConf(conf); err != nil {
			log.Printf("[ERROR LOG] InitJsonConf failed, err: %s", err)
		}
	}
}

func InitJsonConf(conf interface{}) *errors.Error {
	if reflect.TypeOf(conf).Kind() != reflect.Ptr || conf == nil {
		return errors.New("conf is not a pointer or it's a nil pointer")
	}
	if jsonConfPath == "" {
		return errors.New("empty jsonConfPath")
	}
	confPath, _ := filepath.Abs(jsonConfPath)
	f, err := os.Open(confPath)
	if err != nil {
		return errors.Errorf(err, "file doesn't exist, confPath: %s", confPath)
	}
	defer f.Close()
	bs, err := ioutil.ReadAll(f)
	if err != nil {
		return errors.Errorf(err, "read file failed, confPath: %s", confPath)
	}
	if err = json.Unmarshal(bs, &conf); err != nil {
		return errors.Errorf(err, "unmarshal conf failed")
	}
	return nil
}
