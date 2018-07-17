import  pygame
class Button():
    def __init__(self,ai_settings,screen,msg):
        #关联窗口信息
        self.screen=screen
        self.screen_rect=self.screen.get_rect()
        #按钮大小颜色字体信息
        self.width,self.height=200,100
        self.text_color=(0,255,255)
        self.button_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center
        #准备文本信息
        self.prep_msg(msg)

    def prep_msg(self,msg):
        #将文字渲染成图像
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        #渲染按钮背景
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

