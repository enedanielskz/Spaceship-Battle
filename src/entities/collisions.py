import pygame.display

from .players_lasers import modify_players_lasers


class Collisions:
    @staticmethod
    def check_space_laser_collision(space_laser_rect, player1, player2):
        if player1.rect.colliderect(space_laser_rect):
            player1.hit()
        if player2.rect.colliderect(space_laser_rect):
            player2.hit()

    @staticmethod
    def players_lasers_collided(player1_rect, player2_rect, player1_laser, player2_laser):
        # check if the lasers passed the players, "False" if they did else "True"
        passed_players = player1_rect.x + player1_rect.width < player2_laser.x and \
                         player2_rect.x > player1_laser.x + player1_laser.width
        # check if the lasers collided at x position
        collided_x = player1_laser.x + player1_laser.width >= player2_laser.x
        # check if the lasers collided at y position
        collided_y = player2_laser.y - player1_laser.height < player1_laser.y < player2_laser.y + player2_laser.height

        return collided_x and collided_y and passed_players

    def check_players_lasers_collision(self, player1, player2, player1_lasers_list, player2_lasers_list):
        # Check if player1_lasers hit the window, player2 or player2_lasers
        for player1_laser in player1_lasers_list:
            if player2.rect.colliderect(player1_laser):
                player2.hit()
                player1_lasers_list.remove(player1_laser)
            elif player1_laser.x + player1_laser.width > pygame.display.get_surface().get_width():
                player1_lasers_list.remove(player1_laser)
            else:
                for player2_laser in player2_lasers_list:
                    if self.players_lasers_collided(player1.rect, player2.rect, player1_laser, player2_laser):
                        # modify the lasers based on how they collided with eachother
                        modify_players_lasers(player1_lasers_list, player2_lasers_list, player1_laser, player2_laser)
                        break

        # Check if player2_lasers hit the window or player1
        for player2_laser in player2_lasers_list:
            if player1.rect.colliderect(player2_laser):
                player1.hit()
                player2_lasers_list.remove(player2_laser)
            elif player2_laser.x < 0:
                player2_lasers_list.remove(player2_laser)

    @staticmethod
    def check_power_up_collision(power_up, player1, player2, player1_lasers, player2_lasers):
        if player1.rect.colliderect(power_up):
            power_up.collect(player1, player1_lasers, player2)
        elif player2.rect.colliderect(power_up):
            power_up.collect(player2, player2_lasers, player1)

    def update(self, player1, player2, player1_lasers, player2_lasers, space_laser_rect, power_up):
        self.check_space_laser_collision(space_laser_rect, player1, player2)
        self.check_players_lasers_collision(player1, player2, player1_lasers.list, player2_lasers.list)
        if power_up.visible:
            self.check_power_up_collision(power_up, player1, player2, player1_lasers, player2_lasers)
