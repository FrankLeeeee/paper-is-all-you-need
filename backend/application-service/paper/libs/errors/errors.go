package errors

import (
	"errors"
	"fmt"
	"runtime/debug"
)

type Error struct {
	innErr error
	msg    string
}

func (e *Error) Error() string {
	return fmt.Sprintf("stack: %s, err: %s", debug.Stack(), e.msg)
}

func (e *Error) Unwrap() error {
	return e.innErr
}

func New(text string) *Error {
	return &Error{
		innErr: errors.New(text),
		msg:    text,
	}
}

func Errorf(err error, format string, args ...interface{}) *Error {
	e, ok := err.(*Error)
	if !ok {
		return New(fmt.Sprintf(format, args...) + "err: " + err.Error())
	}
	e.msg = fmt.Sprintf(format, args...) + "err: " + err.Error()
	return e
}
