import pyxel
import random

class BitroadAlchemyStable:
    def __init__(self):
        pyxel.init(240, 400, title="BITROAD ALCHEMY")
        pyxel.mouse(True) 
        
        self.C_GOLD = 10     
        self.C_BG = 0        
        self.C_BLUE = 12     
        self.music_on = True
        
        self.nickname = ""
        self.reset_game_data()
        self.setup_audio()
        pyxel.run(self.update, self.draw)

    def reset_game_data(self):
        self.state = "NICKNAME"
        self.elixirs = 35 # Kapanma hatası şerefine 5 tane benden!
        self.weapons = [[i, 0] for i in range(6)]
        self.weapon_names = ["SWORD", "BLADE", "SPEAR", "GLAVIE", "BOW", "STAFF"]
        self.rates = [0.90, 0.85, 0.75, 0.65, 0.50, 0.35, 0.20, 0.10, 0.05, 0.02]
        self.sell_rewards = {3:10, 4:25, 5:60, 6:150, 7:400, 8:1000, 9:3000, 10:10000}
        
        self.fuse_timer = 0
        self.max_fuse_time = 15 
        self.success_stamp_timer = 0
        self.fail_flash_timer = 0
        self.shake = 0
        self.selected_weapon = 0

    def setup_audio(self):
        pyxel.sounds[0].set("a1 r a1 r e1 r e1 r", "p", "2", "v", 10 if self.music_on else 0) 
        pyxel.sounds[1].set("c3e3g3c4", "p", "5", "v", 15)
        pyxel.sounds[2].set("g1g1", "n", "2", "f", 20)      
        pyxel.play(0, 0, loop=True)

    def update(self):
        if self.music_on:
            if pyxel.play_pos(0) == -1: pyxel.play(0, 0, loop=True)
        else:
            pyxel.stop(0)

        if self.shake > 0: self.shake -= 1
        if self.success_stamp_timer > 0: self.success_stamp_timer -= 1
        if self.fail_flash_timer > 0: self.fail_flash_timer -= 1
        
        # Müzik Butonu Kontrolü
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if 160 < pyxel.mouse_x < 235 and 40 < pyxel.mouse_y < 65: 
                self.music_on = not self.music_on

        if self.state == "NICKNAME":
            for i in range(32, 126):
                if pyxel.btnp(i) and len(self.nickname) < 8: self.nickname += chr(i).upper()
            if pyxel.btnp(pyxel.KEY_BACKSPACE): self.nickname = self.nickname[:-1]
            if pyxel.btnp(pyxel.KEY_RETURN) and self.nickname: self.state = "SELECT"
        
        elif self.state == "SELECT":
            self.handle_selection() # Çöken yer burasıydı, düzeldi!
        elif self.state == "INFO":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): self.state = "SELECT"
        elif self.state == "ALCHEMY":
            self.handle_alchemy()
        elif self.state == "GAMEOVER":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): self.reset_game_data()

    def handle_selection(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if 180 < mx < 230 and 10 < my < 30: 
                self.state = "INFO"
                return # Info'ya gidince döngüden çık
            
            for i in range(6):
                y = 100 + (i * 45)
                if 20 < mx < 220 and y < my < y + 35:
                    self.selected_weapon = i
                    self.state = "ALCHEMY"
                    break

    def handle_alchemy(self):
        if self.fuse_timer > 0:
            self.fuse_timer -= 1
            if self.fuse_timer == 0:
                w = self.weapons[self.selected_weapon]
                if random.random() < self.rates[w[1]]:
                    w[1] += 1; self.elixirs += 1; self.success_stamp_timer = 20
                    pyxel.play(1, 1)
                else:
                    w[1] = 0; self.shake = 15; self.fail_flash_timer = 10
                    pyxel.play(1, 2)
                if self.elixirs <= 0: self.state = "GAMEOVER"
            return
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if 180 < mx < 230 and 10 < my < 30: self.state = "SELECT"
            elif 40 < mx < 200 and 280 < my < 320 and self.elixirs > 0:
                self.fuse_timer = self.max_fuse_time; self.elixirs -= 1
            elif 40 < mx < 200 and 340 < my < 370:
                w = self.weapons[self.selected_weapon]
                if w[1] >= 3: self.elixirs += self.sell_rewards[w[1]]; w[1] = 0; self.state = "SELECT"

    def draw_golden_elixir_bottle(self, x, y):
        pyxel.pset(x+3, y, 9); pyxel.pset(x+4, y, 9)
        pyxel.rect(x+3, y+1, 2, 2, 13)
        pyxel.circ(x+4, y+6, 3, self.C_GOLD)
        pyxel.rect(x+2, y+4, 5, 5, self.C_GOLD)
        pyxel.pset(x+2, y+4, 7); pyxel.pset(x+6, y+7, 7)

    def draw(self):
        if self.fail_flash_timer > 0 and (self.fail_flash_timer // 2) % 2 == 0: pyxel.cls(8)
        else: pyxel.cls(0)
        
        # ANA ÇERÇEVE
        pyxel.rectb(0, 0, 240, 400, self.C_GOLD)
        
        # MÜZİK BUTONU
        m_txt = "MUSIC: ON" if self.music_on else "MUSIC: OFF"
        col = 11 if self.music_on else 5
        pyxel.rectb(165, 42, 65, 15, col); pyxel.text(172, 47, m_txt, col)

        if self.state == "INFO": self.draw_info_screen()
        elif self.state == "SELECT": self.draw_selection_screen()
        elif self.state == "ALCHEMY": self.draw_alchemy_ui()
        elif self.state == "NICKNAME":
            pyxel.text(80, 180, "ENTER NICKNAME", 10); pyxel.text(100, 200, "> " + self.nickname, 7)
        elif self.state == "GAMEOVER":
            pyxel.text(85, 180, "OUT OF ELIXIRS", 8); pyxel.text(80, 210, "TAP TO RESTART", 10)

    def draw_info_screen(self):
        pyxel.rectb(15, 30, 210, 355, 10)
        pyxel.rect(20, 35, 200, 18, 12); pyxel.text(85, 41, "ALCHEMY HANDBOOK", 7)
        pyxel.text(30, 65, "[ SUCCESS RATES ]", 10)
        for i in range(10):
            col = 30 if i < 5 else 130
            row = 78 + (i % 5) * 12
            pyxel.text(col, row, f"+{i+1}: {int(self.rates[i]*100)}%", 7)
        pyxel.text(30, 145, "[ SELL REWARDS ]", 10)
        rewards = list(self.sell_rewards.items())
        for i, (lvl, val) in enumerate(rewards):
            col = 30 if i < 4 else 130
            row = 158 + (i % 4) * 12
            pyxel.text(col, row, f"+{lvl}: {val} ELX", 12)
        pyxel.text(30, 215, "[ HOW TO PLAY ]", 10)
        pyxel.text(30, 228, "- Click item to select.", 7)
        pyxel.text(30, 240, "- FUSE costs 1 Elixir.", 7)
        pyxel.text(45, 365, "--- TAP ANYWHERE TO CLOSE ---", 5)

    def draw_selection_screen(self):
        pyxel.text(75, 75, "BITROAD ALCHEMY", 10)
        self.draw_golden_elixir_bottle(15, 15)
        pyxel.text(30, 20, f"ELIXIRS: {self.elixirs}", 10)
        pyxel.rectb(180, 10, 50, 20, 12); pyxel.text(195, 17, "INFO", 12)
        for i in range(6):
            y = 100 + (i * 45)
            lvl = self.weapons[i][1]
            pyxel.rectb(20, y, 200, 35, 10)
            self.draw_detailed_icon(40, y+17, i, 2, lvl)
            pyxel.text(75, y+15, self.weapon_names[i], 7); pyxel.text(205, y+15, f"+{lvl}", 12 if lvl > 0 else 5)

    def draw_alchemy_ui(self):
        w = self.weapons[self.selected_weapon]
        self.draw_golden_elixir_bottle(15, 15)
        pyxel.text(30, 20, f"ELIXIRS: {self.elixirs}", 10)
        pyxel.rectb(180, 10, 50, 20, 10); pyxel.text(192, 17, "BACK", 10)
        pyxel.rectb(70, 120, 100, 130, 12); self.draw_detailed_icon(120, 185, self.selected_weapon, 6, w[1])
        if self.fuse_timer > 0:
            p = (self.max_fuse_time - self.fuse_timer) / self.max_fuse_time
            pyxel.rectb(70, 260, 100, 8, 10); pyxel.rect(70, 260, 100 * p, 8, 12)
        else:
            pyxel.text(90, 105, f"+{w[1]} {self.weapon_names[self.selected_weapon]}", 7)
            pyxel.rectb(40, 280, 160, 40, 10); pyxel.text(110, 297, "FUSE", 10)
            if w[1] >= 3: 
                pyxel.rectb(40, 340, 160, 30, 13)
                txt = f"SELL FOR {self.sell_rewards[w[1]]}"
                pyxel.text(80, 352, txt, 13)
                self.draw_golden_elixir_bottle(80 + len(txt)*4, 348)
        if self.success_stamp_timer > 0:
            pyxel.rect(60, 170, 120, 35, 12); pyxel.text(98, 185, "SUCCESS!", 7)

    def draw_detailed_icon(self, x, y, tid, s, lvl):
        c = 7 if lvl < 7 else 10
        if tid == 0: pyxel.rect(x-1, y-8, 2, 12, c); pyxel.rect(x-3, y+2, 6, 1, c)
        elif tid == 1: pyxel.line(x, y-8, x+3, y+4, c); pyxel.line(x-1, y-8, x+2, y+4, c)
        elif tid == 2: pyxel.line(x, y-10, x, y+10, 4); pyxel.tri(x, y-11, x-2, y-7, x+2, y-7, c)
        elif tid == 3: pyxel.line(x, y-10, x, y+10, 4); pyxel.rect(x-2, y-9, 4, 3, c)
        elif tid == 4: pyxel.line(x-2, y-6, x-4, y, c); pyxel.line(x-4, y, x-2, y+6, c); pyxel.line(x-6, y, x, y, 6)
        elif tid == 5: pyxel.line(x, y-10, x, y+10, 4); pyxel.circb(x, y-9, 2, 12)
        if lvl >= 5:
            for _ in range(lvl * 2):
                pyxel.pset(x + random.randint(-5, 5), y + random.randint(-8, 8), 12 if lvl < 9 else 8)

BitroadAlchemyStable()
