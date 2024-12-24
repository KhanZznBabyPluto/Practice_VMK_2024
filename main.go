package main

import (
	"image/color"
	"log"

	"a_star/a_star"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenWidth  = 640
	screenHeight = 480
	cellSize     = 40
	gridWidth    = 16
	gridHeight   = 12
)

type Game struct {
	grid   *a_star.Grid
	path   []*a_star.Node
	startX int
	startY int
	endX   int
	endY   int
}

func NewGame() *Game {
	grid := a_star.NewGrid(gridWidth, gridHeight)

	// Устанавливаем препятствия
	obstacles := [][2]int{
		{2, 2}, {2, 3}, {2, 4},
		{4, 2}, {4, 3}, {4, 4},
		{3, 6}, {4, 6}, {5, 6},
		{7, 7}, {7, 8}, {7, 9},
		{10, 3}, {10, 4}, {10, 5},
	}

	for _, obs := range obstacles {
		grid.Nodes[obs[1]][obs[0]].Walkable = false
	}

	game := &Game{
		grid:   grid,
		startX: 0,
		startY: 0,
		endX:   15,
		endY:   11,
	}

	// Находим путь сразу при создании игры
	game.path = grid.FindPath(game.startX, game.startY, game.endX, game.endY)

	return game
}

func (g *Game) Update() error {
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// Заполняем фон
	screen.Fill(color.RGBA{240, 240, 240, 255})

	// Рисуем сетку
	for y := 0; y < gridHeight; y++ {
		for x := 0; x < gridWidth; x++ {
			node := g.grid.Nodes[y][x]

			// Определяем цвет клетки
			var clr color.Color
			if !node.Walkable {
				clr = color.RGBA{100, 100, 100, 255} // Препятствия
			} else {
				clr = color.RGBA{255, 255, 255, 255} // Проходимые клетки
			}

			// Рисуем клетку
			ebitenutil.DrawRect(screen,
				float64(x*cellSize),
				float64(y*cellSize),
				float64(cellSize-1),
				float64(cellSize-1),
				clr)
		}
	}

	// Рисуем путь
	if g.path != nil {
		for i, node := range g.path {
			if i > 0 {
				// Рисуем линию от предыдущего узла к текущему
				prev := g.path[i-1]
				ebitenutil.DrawLine(screen,
					float64(prev.X*cellSize+cellSize/2),
					float64(prev.Y*cellSize+cellSize/2),
					float64(node.X*cellSize+cellSize/2),
					float64(node.Y*cellSize+cellSize/2),
					color.RGBA{0, 150, 255, 255})
			}
		}
	}

	// Рисуем начальную и конечную точки
	ebitenutil.DrawCircle(screen,
		float64(g.startX*cellSize+cellSize/2),
		float64(g.startY*cellSize+cellSize/2),
		float64(cellSize/4),
		color.RGBA{0, 255, 0, 255})

	ebitenutil.DrawCircle(screen,
		float64(g.endX*cellSize+cellSize/2),
		float64(g.endY*cellSize+cellSize/2),
		float64(cellSize/4),
		color.RGBA{255, 0, 0, 255})
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func main() {
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("A* Pathfinding Visualization")

	if err := ebiten.RunGame(NewGame()); err != nil {
		log.Fatal(err)
	}
}
