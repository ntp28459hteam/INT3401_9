# Bài tập số 2: Tìm kiếm có đối thủ
## Câu 1 + 5:
- Hàm đánh giá được xây dựng theo hai tiêu chí: tham ăn và trốn ma
## Câu 2:
- Tác nhân: MinimaxAgent
- Tổ chức hàm:
  - `getAction(self, gameState)`: xác định hành động cho pacman tại mỗi trạng thái
  - `minimax(self, agentIndex, gameState, depth)`: quyết định giá trị trả về của tác nhân
  - `minimize(self, agentIndex, gameState, depth)`: trả về giá trị minimax nhỏ nhất trong các trạng thái kế tiếp
  - `maximize(self, agentIndex, gameState, depth)`: trả về giá trị minimax lớn nhất trong các trạng thái kế tiếp
## Câu 4:
- Hành vi của pacman tương tự câu số 2
- `minimize(self, agentIndex, gameState, depth)`: trả về giá trị minimax trung bình trong các trạng thái kế tiếp
