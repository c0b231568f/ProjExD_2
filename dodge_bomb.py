import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA={
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5,0),
}  # 移動量辞書
KKT={
    (0, -5): 270,
    (5, -5): 225,
    (5, 0): 180,
    (5, 5): 135,
    (0, 5): 90,
    (-5, 5): 45,
    (-5, 0): 0,
    (-5, -5): -45,
}  # 押下キーに対する移動量の合計値タプルをキー，rotozoomしたSurfaceを値とした辞書
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect)-> tuple[bool, bool]:
    """
    こうかとんRect,又は,爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect,または,爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko=False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate=False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img =  pg.Surface((20,20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct=bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾がぶつかったら
            # 画面をブラックアウト
            GO_img = pg.Surface((WIDTH, HEIGHT))
            GO_img.set_alpha(180)
            pg.draw.rect(GO_img,(0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
            screen.blit(GO_img,[0, 0])
            # 泣いてるこうかとんの表示
            kkn_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
            kkn1_rct = kk_img.get_rect(center = (WIDTH//2-230, HEIGHT//2))
            kkn2_rct = kk_img.get_rect(center = (WIDTH//2+230, HEIGHT//2))
            screen.blit(kkn_img, kkn1_rct)
            screen.blit(kkn_img, kkn2_rct)
            #「Game Over]を表示
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255,255,255))
            txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(txt, txt_rct)
            pg.display.update()  # 画面を更新する
            time.sleep(5)  # 5秒間表示させる
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), KKT[(sum_mv[0], sum_mv[1])], 2.0)
                #飛ぶ方向に従ってこうかとん画像を切り替える
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の移動と表示
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向にはみ出てたら
            vx*=-1
        if not tate:  # 縦方向にはみ出てたら
            vy*=-1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
