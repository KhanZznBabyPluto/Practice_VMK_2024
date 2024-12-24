# A* Pathfinding Visualization

Визуализация алгоритма поиска пути A* с использованием Go и библиотеки Ebiten.

## Требования

### Windows
1. Установить [Go](https://golang.org/dl/)
2. Установить [MinGW-w64](https://sourceforge.net/projects/mingw-w64/) или [TDM-GCC](https://jmeubank.github.io/tdm-gcc/)

### Linux (Ubuntu/Debian)
```bash
# Установка Go
sudo apt-get update
sudo apt-get install golang-go

# Установка необходимых зависимостей для Ebiten
sudo apt-get install -y libgl1-mesa-dev xorg-dev libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev
```

### Linux (Fedora)
```bash
sudo dnf install golang
sudo dnf install libX11-devel libXcursor-devel libXrandr-devel libXinerama-devel libXi-devel mesa-libGL-devel
```

### MacOS
```bash
# Установка через Homebrew
brew install go
```

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com//a_star
cd a_star
```

2. Инициализируйте модуль и установите зависимости:
```bash
go mod init a_star
go get github.com/hajimehoshi/ebiten/v2
go mod tidy
```

3. Запустите программу:
```bash
go run main.go
```

## Структура проекта
```
directoy/
├── a_star/
│   └── a_star.go    # Реализация алгоритма A*
├── main.go         # Визуализация с использованием Ebiten
├── go.mod
├── go.sum
└── README.md
```

## Использование

В визуализации:
- Зеленая точка - начальная позиция
- Красная точка - конечная позиция
- Серые клетки - препятствия
- Синяя линия - найденный путь

## Возможные проблемы и их решение

### Windows
- Если возникает ошибка компиляции, убедитесь, что gcc добавлен в PATH
- Для Visual Studio Code может потребоваться установка расширения "Go"

### Linux
- Если возникает ошибка "package github.com/hajimehoshi/ebiten/v2 is not in GOROOT", выполните:
```bash
go env -w GO111MODULE=on
go mod tidy
```

- Если возникает ошибка с X11, убедитесь, что установлены все необходимые зависимости:
```bash
# Ubuntu/Debian
sudo apt-get install -y libgl1-mesa-dev xorg-dev libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev

# Fedora
sudo dnf install libX11-devel libXcursor-devel libXrandr-devel libXinerama-devel libXi-devel mesa-libGL-devel
```

### MacOS
- Если возникает ошибка при компиляции, установите инструменты командной строки Xcode:
```bash
xcode-select --install
```
