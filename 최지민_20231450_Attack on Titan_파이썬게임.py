import pygame
import random

# 초기화
pygame.init()

# 화면 설정
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Subway Surfer Clone")

# 색깔 정의
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# 효과음 및 배경 음악 로드
try:
    pygame.mixer.music.load('y2mate.com - 진격의 거인 1기 op.mp3')  # 배경 음악 파일 경로
    pygame.mixer.music.play(-1)  # 반복 재생
    hit_sound = pygame.mixer.Sound('칼 소리1.wav')  # 효과음 파일 경로
except pygame.error as e:
    print(f"음악 파일 로드 오류: {e}")
    pygame.quit()

# 이미지 불러오기 및 크기 조정
try:
    player_img = pygame.image.load('player.png')
    player_img = pygame.transform.scale(player_img, (120, 120))  # 플레이어 이미지 크기 조정
except pygame.error as e:
    print(f"플레이어 이미지 로드 오류: {e}")
    pygame.quit()

try:
    wall_img = pygame.image.load('normal.png')
    wall_img = pygame.transform.scale(wall_img, (100, 200))  # 벽 이미지 크기 조정
except pygame.error as e:
    print(f"벽 이미지 로드 오류: {e}")
    pygame.quit()

try:
    background_img = pygame.image.load('back.JPG')
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))  # 배경 이미지 크기 조정
except pygame.error as e:
    print(f"배경 이미지 로드 오류: {e}")
    pygame.quit()

try:
    boss_img = pygame.image.load('boss.png')
    boss_img = pygame.transform.scale(boss_img, (250, 350))  # 보스 이미지 크기 조정
except pygame.error as e:
    print(f"보스 이미지 로드 오류: {e}")
    pygame.quit()

try:
    mid_boss_img1 = pygame.image.load('mid 1.png')
    mid_boss_img1 = pygame.transform.scale(mid_boss_img1, (200, 200))  # 중간 보스1 이미지 크기 조정
    mid_boss_img2 = pygame.image.load('mid 2.png')
    mid_boss_img2 = pygame.transform.scale(mid_boss_img2, (150, 300))  # 중간 보스2 이미지 크기 조정
    mid_boss_img3 = pygame.image.load('mid 3.png')
    mid_boss_img3 = pygame.transform.scale(mid_boss_img3, (300, 400))  # 중간 보스3 이미지 크기 조정
except pygame.error as e:
    print(f"중간 보스 이미지 로드 오류: {e}")
    pygame.quit()

# 파티클 클래스
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = [random.uniform(-1, 1) * 5, random.uniform(-1, 1) * 5]
        self.lifetime = random.randint(20, 50)
    
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 50
        self.speed = 20  # 플레이어의 이동 속도
        self.health = 100  # 플레이어의 체력
        self.attack_power = 10  # 플레이어의 공격력

    def update(self):
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 화면을 벗어나지 않도록 제한
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw_health_bar(self, screen):
        # 체력 바의 배경
        pygame.draw.rect(screen, red, (self.rect.x, self.rect.y - 20, 100, 10))
        # 체력 바의 현재 체력
        pygame.draw.rect(screen, green, (self.rect.x, self.rect.y - 20, self.health, 10))

# 장애물 클래스
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, health):
        super().__init__()
        self.image = wall_img  # 벽 이미지로 설정
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randrange(screen_height - self.rect.height)
        self.speed = speed
        self.health = health

    def update(self):
        self.rect.x -= self.speed
        # 화면 밖으로 나가면 제거
        if self.rect.right < 0:
            self.kill()

# 돌 클래스 추가
class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(black)  # 돌의 색깔 설정
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 15  # 돌의 속도를 빠르게 설정

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# 보스 클래스
class BossObstacle(pygame.sprite.Sprite):  # 보스가 Obstacle을 상속받지 않도록 변경
    def __init__(self, speed, health):
        super().__init__()
        self.image = boss_img  # 보스 이미지로 설정
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = (screen_height // 2) - (self.rect.height // 2)
        self.speed = speed
        self.health = health
        self.last_attack_time = pygame.time.get_ticks()  # 마지막 공격 시간을 저장
        self.attacking = False  # 보스가 공격 중인지 여부

    def update(self):
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > 500:  # 0.5초 후에 다시 움직이기
                self.attacking = False
        else:
            self.rect.x -= self.speed
            # 1.5초마다 돌 던지기
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time > 1500:  # 1.5초마다
                self.last_attack_time = current_time
                self.attacking = True
                rock = Rock(self.rect.centerx, self.rect.centery)
                all_sprites.add(rock)
                rocks.add(rock)
        # 화면 밖으로 나가면 제거
        if self.rect.right < 0:
            self.kill()

# 중간 보스 클래스
class MidBossObstacle(Obstacle):
    def __init__(self, image, speed, health):
        super().__init__(speed, health)
        self.image = image  # 중간 보스 이미지로 설정
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randrange(screen_height - self.rect.height)

    def update(self):
        super().update()

# 그룹 생성
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
rocks = pygame.sprite.Group()  # 돌 그룹 추가
bosses = pygame.sprite.Group()  # 보스 그룹 추가
particles = pygame.sprite.Group()  # 파티클 그룹 추가

# 플레이어 추가
player = Player()
all_sprites.add(player)

def create_obstacle(speed, health):
    obstacle = Obstacle(speed, health)
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

def create_mid_boss_obstacle(image, speed, health):
    mid_boss = MidBossObstacle(image, speed, health)
    all_sprites.add(mid_boss)
    obstacles.add(mid_boss)

def create_boss_obstacle(speed, health):
    boss = BossObstacle(speed, health)
    all_sprites.add(boss)
    bosses.add(boss)  # 보스를 bosses 그룹에 추가

def create_particles(x, y, color, num_particles=30):
    for _ in range(num_particles):
        particle = Particle(x, y, color)
        all_sprites.add(particle)
        particles.add(particle)

# 게임 변수 설정
stage = 1
obstacle_timer = 0
boss_timer = 0
obstacles_destroyed = 0
boss_created = False
mid_boss_created = [False, False, False]  # 중간 보스 생성 여부
game_clear = False  # 게임 클리어 상태 변수
clear_start_time = 0  # 클리어 시작 시간
game_fail = False  # 게임 실패 상태 변수
fail_start_time = 0  # 실패 시작 시간

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 스페이스바를 누르면 장애물 공격
                hits = pygame.sprite.spritecollide(player, obstacles, False, collided=pygame.sprite.collide_rect_ratio(1.3))  # 조정된 충돌 범위로 충돌 감지
                for hit in hits:
                    hit.health -= player.attack_power
                    create_particles(hit.rect.centerx, hit.rect.centery, red)  # 장애물에 파티클 효과 추가
                    hit_sound.play()  # 효과음 재생
                    if hit.health <= 0:
                        hit.kill()
                        obstacles_destroyed += 1  # 제거한 장애물 수 추가

    # 게임 로직
    if not game_clear and not game_fail:
        all_sprites.update()

        # 장애물 생성 및 난이도 증가
        if stage == 1:
            if random.randrange(100) < 2:
                create_obstacle(5, 1)
            if obstacles_destroyed >= 15:
                stage = 2
                obstacles_destroyed = 0  # 다음 스테이지를 위해 초기화

        elif stage == 2:
            if random.randrange(100) < 2:
                create_obstacle(8, 2)  # 일반 장애물
            if not mid_boss_created[0] and random.randrange(1000) < 1:
                create_mid_boss_obstacle(mid_boss_img1, 5, 20)  # 중간 보스1
                mid_boss_created[0] = True
            if not mid_boss_created[1] and random.randrange(1000) < 1:
                create_mid_boss_obstacle(mid_boss_img2, 5, 20)  # 중간 보스2
                mid_boss_created[1] = True
            if not mid_boss_created[2] and random.randrange(1000) < 1:
                create_mid_boss_obstacle(mid_boss_img3, 5, 20)  # 중간 보스3
                mid_boss_created[2] = True
            if obstacles_destroyed >= 30:
                stage = 3
                obstacles_destroyed = 0  # 다음 스테이지를 위해 초기화

        elif stage == 3:
            if not boss_created:
                create_boss_obstacle(5, 30)  # 보스 체력을 30으로 설정하여 플레이어가 세 번 때려야 없앰
                boss_created = True
            # 보스를 처치하면 게임 클리어
            boss_hits = pygame.sprite.spritecollide(player, bosses, False)  # bosses 그룹에서 보스와 충돌 확인
            for boss_hit in boss_hits:
                boss_hit.health -= player.attack_power
                create_particles(boss_hit.rect.centerx, boss_hit.rect.centery, red)  # 보스에 파티클 효과 추가
                hit_sound.play()  # 효과음 재생
                if boss_hit.health <= 0:
                    boss_hit.kill()
                    game_clear = True  # 게임 클리어 상태로 전환
                    clear_start_time = pygame.time.get_ticks()  # 클리어 시작 시간 기록

        # 플레이어와 돌의 충돌 체크
        rock_hits = pygame.sprite.spritecollide(player, rocks, True)
        for hit in rock_hits:
            player.health -= 10  # 돌에 맞으면 체력 감소
            create_particles(hit.rect.centerx, hit.rect.centery, black)  # 돌 충돌 시 파티클 효과 추가
            if player.health <= 0:
                game_fail = True  # 체력이 0 이하가 되면 게임 실패 상태로 전환
                fail_start_time = pygame.time.get_ticks()  # 실패 시작 시간 기록

        # 충돌 체크
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        for hit in hits:
            player.health -= 10  # 충돌 시 체력 감소
            hit.health -= player.attack_power
            create_particles(hit.rect.centerx, hit.rect.centery, red)  # 충돌 시 파티클 효과 추가
            if hit.health <= 0:
                hit.kill()  # 충돌한 장애물 제거
                obstacles_destroyed += 1
            if player.health <= 0:
                game_fail = True  # 체력이 0 이하가 되면 게임 실패 상태로 전환
                fail_start_time = pygame.time.get_ticks()  # 실패 시작 시간 기록

    # 그리기
    screen.blit(background_img, (0, 0))  # 배경 이미지 그리기
    all_sprites.draw(screen)
    player.draw_health_bar(screen)  # 체력 바 그리기

    # 스테이지 표시
    font = pygame.font.Font(None, 36)
    stage_text = font.render(f"Stage: {stage}", True, black)
    screen.blit(stage_text, (10, 10))

    # 클리어 상태인 경우 "Clear" 메시지 표시
    if game_clear:
        font = pygame.font.Font(None, 74)
        clear_text = font.render("Clear", True, black)
        screen.blit(clear_text, (screen_width // 2 - clear_text.get_width() // 2, screen_height // 2 - clear_text.get_height() // 2))
        if pygame.time.get_ticks() - clear_start_time > 3000:  # 3초 대기 후 게임 종료
            running = False

    # 실패 상태인 경우 "Fail" 메시지 표시
    if game_fail:
        font = pygame.font.Font(None, 74)
        fail_text = font.render("Fail", True, red)
        screen.blit(fail_text, (screen_width // 2 - fail_text.get_width() // 2, screen_height // 2 - fail_text.get_height() // 2))
        if pygame.time.get_ticks() - fail_start_time > 3000:  # 3초 대기 후 게임 종료
            running = False

    # 화면 업데이트
    pygame.display.flip()

    # FPS 설정
    clock.tick(30)

# 게임 종료
pygame.quit()






