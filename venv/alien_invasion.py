import sys
import pygame
from pygame.sprite import Group

from  scoreboard import Scoreboard
from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship
import game_functions as gf
def run_game():
# 初始化游戏并创建一个屏幕对象 
    pygame.init()

    ai_settings=Settings()
    stats= GameStats(ai_settings)
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button= Button(ai_settings,screen,"Play")
    sb=Scoreboard(ai_settings,screen,stats)
# 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)
# 开始游戏的主循环 
    while True:
# 监视键盘和鼠标事件 
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
# 让最近绘制的屏幕可见
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,bullets)
        gf.update_screen(ai_settings,stats,screen,sb,ship,aliens,bullets,play_button)


run_game()