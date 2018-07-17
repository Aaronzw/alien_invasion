import sys
import pygame
from time import sleep
from bullet import Bullet
from  alien import  Alien

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key==pygame.K_a:
        ship.moving_left = False

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #按键按下
    if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key==pygame.K_a :
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_events(ai_settings, screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN :
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP :
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def update_screen(ai_settings,stats,screen,sb,ship,aliens,bullets,play_button):
    #刷新屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites() :
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    for bullet in bullets.copy() :
        #超出屏幕的子弹清除
        if bullet.rect.bottom<0 :
            bullets.remove(bullet)
    check_bullets_aliens_collision(ai_settings, screen,stats,sb, ship, aliens, bullets)

def check_bullets_aliens_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #处理外星人和子弹碰撞检测
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if(collisions):
        for aliens in collisions.values():
            stats.score+=(ai_settings.alien_points*len(aliens))
            sb.prep_score()
        check_high_score(stats, sb)
    if (len(aliens) == 0):
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)



def fire_bullet(ai_settings, screen, ship, bullets):
   #开火发射子弹，现存子弹数目有限
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen,ship, aliens):
    #创建外星人群
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x=get_number_aliens_x(ai_settings,alien_width)
    number_rows=get_number_row(ai_settings,ship.rect.height,alien.rect.height)
    i=0
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
    # 创建一个外星人并将其加入当前行
            if i<ai_settings.alien_num_allowed :
                create_alien(ai_settings,screen,aliens,alien_number,row_number)
                i+=1

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return  number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    #根据行数和列数生成外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def get_number_row(ai_settings,ship_height,alien_hight):
    #获取行数
    available_space_y=ai_settings.screen_height-3*alien_hight-ship_height
    numbers_rows=int(available_space_y/(2*alien_hight))
    return numbers_rows

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
    #有外星人到达边缘时采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    #将整群外星人下移，并改变它们的方向
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #响应飞船和外星人碰撞
    if stats.ships_left > 0:
        stats.ships_left-=1
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    # 清空屏幕的子弹和外星人
    aliens.empty()
    bullets.empty()
    #重新生成
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,bullets):
    #检测外星人是否到达底部
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            #检测是否触底，坐标系左上角为0,0
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    #单击play开始游戏
    button_clicked=play_button.rect.collidepoint(mouse_x, mouse_y)
    if  button_clicked and not stats.game_active:
        #隐藏鼠标
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        #开始时重置统计信息
        stats.reset_stats()
        stats.game_active=True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def check_high_score(stats, sb):
#检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
