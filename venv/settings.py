class Settings():
    def __init__(self):
        #初始化游戏的设置
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #玩家几条命
        self.ship_limit=1
        # 子弹设置

        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
        self.bullets_allowed=10
        #外星人移动速度
        self.fleet_drop_speed=50
        self.fleet_direction=1  #表示向右
        self.alien_num_allowed=16
        #每个外星人得分
        self.alien_points=50
        #得分递增规模
        self.score_scale=1.5

        self.speedup_scale=1.1
        self.initialize_dynamic_settings()
        #初始最高分
        self.high_score=0

    def initialize_dynamic_settings(self):
        #初始化随时间变化的设置
        self.ship_speed_factor =1
        self.alien_speed_factor =1
        self.bullet_speed_factor = 1
        #默认向右移
        self.fleet_direction=1

    def increase_speed(self):
        ##提高速度设置
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points*=self.score_scale



