package logger

import (
	"os"
	"path/filepath"

	"github.com/sirupsen/logrus"
)

// Init 初始化日志
func Init(level, file string) error {
	// 设置日志级别
	logLevel, err := logrus.ParseLevel(level)
	if err != nil {
		logLevel = logrus.InfoLevel
	}
	logrus.SetLevel(logLevel)

	// 设置日志格式
	logrus.SetFormatter(&logrus.JSONFormatter{
		TimestampFormat: "2006-01-02 15:04:05",
		FieldMap: logrus.FieldMap{
			logrus.FieldKeyTime:  "timestamp",
			logrus.FieldKeyLevel: "level",
			logrus.FieldKeyMsg:   "message",
		},
	})

	// 如果指定了日志文件，则输出到文件
	if file != "" {
		// 确保日志目录存在
		logDir := filepath.Dir(file)
		if err := os.MkdirAll(logDir, 0755); err != nil {
			return err
		}

		// 打开日志文件
		logFile, err := os.OpenFile(file, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
		if err != nil {
			return err
		}

		// 同时输出到控制台和文件
		logrus.SetOutput(os.Stdout)
		logrus.AddHook(&FileHook{logFile})
	}

	return nil
}

// FileHook 文件钩子
type FileHook struct {
	file *os.File
}

// Levels 返回钩子处理的日志级别
func (hook *FileHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

// Fire 处理日志事件
func (hook *FileHook) Fire(entry *logrus.Entry) error {
	line, err := entry.Bytes()
	if err != nil {
		return err
	}
	_, err = hook.file.Write(line)
	return err
}
