package a_star

// Node представляет узел в сетке
type Node struct {
	X, Y     int     // Координаты
	F, G, H  float64 // F = G + H, где G - стоимость пути от старта, H - эвристическая оценка до цели
	Parent   *Node   // Ссылка на родительский узел
	Walkable bool    // Проходимость узла
}

// Grid представляет сетку для поиска пути
type Grid struct {
	Nodes  [][]*Node
	Width  int
	Height int
}

// NewGrid создает новую сетку заданного размера
func NewGrid(width, height int) *Grid {
	grid := &Grid{
		Width:  width,
		Height: height,
		Nodes:  make([][]*Node, height),
	}

	// Инициализация узлов
	for y := 0; y < height; y++ {
		grid.Nodes[y] = make([]*Node, width)
		for x := 0; x < width; x++ {
			grid.Nodes[y][x] = &Node{
				X:        x,
				Y:        y,
				Walkable: true,
			}
		}
	}

	return grid
}

// manhattanDistance вычисляет манхэттенское расстояние между двумя точками
func manhattanDistance(a, b *Node) float64 {
	dx := float64(abs(a.X - b.X))
	dy := float64(abs(a.Y - b.Y))
	return dx + dy
}

// abs возвращает абсолютное значение числа
func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

// getNeighbors возвращает список соседних узлов
func (g *Grid) getNeighbors(node *Node) []*Node {
	neighbors := make([]*Node, 0, 8)

	// Проверяем все 8 направлений
	directions := [][2]int{
		{-1, -1}, {0, -1}, {1, -1},
		{-1, 0}, {1, 0},
		{-1, 1}, {0, 1}, {1, 1},
	}

	for _, dir := range directions {
		newX := node.X + dir[0]
		newY := node.Y + dir[1]

		// Проверяем границы сетки
		if newX >= 0 && newX < g.Width && newY >= 0 && newY < g.Height {
			neighbor := g.Nodes[newY][newX]
			if neighbor.Walkable {
				neighbors = append(neighbors, neighbor)
			}
		}
	}

	return neighbors
}

// FindPath находит путь между двумя точками используя алгоритм A*
func (g *Grid) FindPath(startX, startY, endX, endY int) []*Node {
	start := g.Nodes[startY][startX]
	end := g.Nodes[endY][endX]

	openSet := make(map[*Node]bool)
	closedSet := make(map[*Node]bool)
	openSet[start] = true

	// Инициализация начального узла
	start.G = 0
	start.H = manhattanDistance(start, end)
	start.F = start.G + start.H

	for len(openSet) > 0 {
		// Находим узел с наименьшим значением F в открытом множестве
		current := findLowestF(openSet)

		// Если достигли конечной точки
		if current == end {
			return reconstructPath(current)
		}

		// Перемещаем текущий узел из открытого множества в закрытое
		delete(openSet, current)
		closedSet[current] = true

		// Обрабатываем соседей
		for _, neighbor := range g.getNeighbors(current) {
			if closedSet[neighbor] {
				continue
			}

			// Вычисляем новую стоимость пути через текущий узел
			tentativeG := current.G + 1 // Предполагаем, что все шаги имеют стоимость 1

			if !openSet[neighbor] {
				openSet[neighbor] = true
			} else if tentativeG >= neighbor.G {
				continue
			}

			// Этот путь лучше. Запоминаем его.
			neighbor.Parent = current
			neighbor.G = tentativeG
			neighbor.H = manhattanDistance(neighbor, end)
			neighbor.F = neighbor.G + neighbor.H
		}
	}

	return nil // Путь не найден
}

// findLowestF находит узел с наименьшим значением F в открытом множестве
func findLowestF(openSet map[*Node]bool) *Node {
	var lowest *Node
	lowestF := float64(^uint(0) >> 1) // Maximum float64 value

	for node := range openSet {
		if node.F < lowestF {
			lowestF = node.F
			lowest = node
		}
	}

	return lowest
}

// reconstructPath восстанавливает путь от конечной точки до начальной
func reconstructPath(node *Node) []*Node {
	path := make([]*Node, 0)
	current := node

	for current != nil {
		path = append([]*Node{current}, path...)
		current = current.Parent
	}

	return path
}
