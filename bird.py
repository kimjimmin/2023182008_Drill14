from pico2d import get_canvas_height, get_canvas_width, load_image

import game_framework
from boy import PIXEL_PER_METER


# 집참새의 평균 수평 비행 속도인 시속 45.5 km를 사용한다.
# Boy와 같은 축척(10 pixel = 0.3 m)으로 환산하면 약 421.30 pixel/s이다.
HOUSE_SPARROW_SPEED_KMPH = 45.5
HOUSE_SPARROW_SPEED_MPS = HOUSE_SPARROW_SPEED_KMPH * 1000.0 / 3600.0
HOUSE_SPARROW_SPEED_PPS = HOUSE_SPARROW_SPEED_MPS * PIXEL_PER_METER

# 참새가 사람 머리 위의 낮은 하늘을 지나는 장면으로 보고 비행 고도를 12 m로 둔다.
# 화면 높이가 부족한 경우에도 새 전체가 보이도록 실제 캔버스 영역 안으로 제한한다.
HOUSE_SPARROW_FLIGHT_HEIGHT_M = 12.0

SHEET_HEIGHT = 506
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
FRAME_COLUMNS = 5
FRAME_COUNT = 14
ANIMATION_FRAMES_PER_SECOND = 12.0


class Bird:
    def __init__(self):
        self.image = load_image('bird_animation.png')
        self.draw_width = 110
        self.draw_height = 101
        self.x = get_canvas_width() / 4
        self.y = min(
            HOUSE_SPARROW_FLIGHT_HEIGHT_M * PIXEL_PER_METER,
            get_canvas_height() - self.draw_height / 2,
        )
        self.y = max(self.draw_height / 2, self.y)
        self.direction = 1
        self.frame = 0.0

    def update(self):
        frame_time = game_framework.frame_time
        self.frame = (
            self.frame + ANIMATION_FRAMES_PER_SECOND * frame_time
        ) % FRAME_COUNT

        left_edge = self.draw_width / 2
        right_edge = max(left_edge, get_canvas_width() - left_edge)
        if right_edge == left_edge:
            self.x = left_edge
            return

        # 초당 이동 거리와 실제 경과 시간을 곱하므로 CPU/FPS가 달라도
        # 같은 시간 동안 이동하는 물리적 거리는 항상 같다.
        self.x += self.direction * HOUSE_SPARROW_SPEED_PPS * frame_time

        # 프레임이 길어 경계를 여러 번 넘은 경우에도 초과 거리를 보존해 반사한다.
        while self.x < left_edge or self.x > right_edge:
            if self.x > right_edge:
                self.x = right_edge - (self.x - right_edge)
                self.direction = -1
            else:
                self.x = left_edge + (left_edge - self.x)
                self.direction = 1

    def draw(self):
        frame_index = int(self.frame)
        column = frame_index % FRAME_COLUMNS
        row = frame_index // FRAME_COLUMNS
        source_x = column * FRAME_WIDTH
        source_y = SHEET_HEIGHT - (row + 1) * FRAME_HEIGHT
        flip = 'h' if self.direction < 0 else ''

        self.image.clip_composite_draw(
            source_x, source_y, FRAME_WIDTH, FRAME_HEIGHT,
            0, flip, self.x, self.y, self.draw_width, self.draw_height
        )
