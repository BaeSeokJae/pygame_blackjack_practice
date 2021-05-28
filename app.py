import time

from includes.common import *
from includes.fsm import *

class BlackJack(object):
    pygame.init()
    pygame.display.set_caption('Black Jack')
    pygame.font.init()
    clock = pygame.time.Clock()

    common_vars = CommenVariables.get_instance()
    button_status = ButtonStatus.get_instance()
    image_db = ImageDB.get_instance()

    common_vars.done = False
    common_vars.screen = pygame.display.set_mode(GAME_BOARD_SIZE)
    common_vars.player_cash = DEFAULT_PLAYER_BALANCE
    common_vars.game_rounds = 0
    common_vars.pause_time = 0
    common_vars.dealer_last_hand = 0
    common_vars.player_hands = []
    common_vars.button_image_width = image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON).get_width()
    common_vars.button_image_height = image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON).get_height()
    common_vars.chips_image_width = image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON).get_width()
    common_vars.chips_image_height = image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON).get_height()

    common_vars.text_font = pygame.font.SysFont('Arial', 18)
    value_of_players_hand_font = pygame.font.SysFont('Arial', 16)

    current_state = InitialState()

    while not common_vars.done:
        # Plot the base table
        common_vars.screen.fill(GAME_BOARD_COLOR)
        # Can handle scaling much better to be prepared for other board sizes.
        x_pos = int(GAME_BOARD_X_SIZE * 0.12)
        y_pos = GAME_BOARD_Y_SIZE - 240
        common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'yellow_box_179_120.png'), (x_pos, y_pos))
        x_pos = int((GAME_BOARD_X_SIZE - image_db.get_image(IMAGE_PATH + "bj_banner_yellow2.png").get_width()) / 2)
        y_pos = GAME_BOARD_Y_SIZE - 500
        common_vars.screen.blit(image_db.get_image(IMAGE_PATH + "bj_banner_yellow2.png"), (x_pos, y_pos))

        if COUNTING_HELP:
            # Plot the value of the current hand
            x_pos = 22
            for hand in common_vars.player_hands:
                count = get_value_of_players_hand(hand)
                if count:
                    message = value_of_players_hand_font.render('{0}'.format(count), False, YELLOW_COLOR)
                    common_vars.screen.blit(message, (x_pos, GAME_BOARD_Y_SIZE - 270))
                x_pos += GAP_BETWEEN_SPLIT
        
        x_pos, y_pos = STATUS_START_POS
        message1 = common_vars.text_font.render('[ Credits: $ {0}]   [Hands played: {1} ]'.format(
            common_vars.player_cash, common_vars.game_rounds), False, YELLOW_COLOR)
        common_vars.screen.blit(message1, (x_pos, y_pos))
        message2 = common_vars.text_font.render('[ Dealers last hand: {0} ]'.format(
            common_vars.dealer_last_hand), False, YELLOW_COLOR)
        common_vars.screen.blit(message2, (x_pos, y_pos + 25))

        current_state(common_vars, button_status)

        pygame.display.flip()

        if common_vars.pause_time:
            time.sleep(common_vars.pause_time)
            common_vars.pause_time = 0
        
        clock.tick(10)

if __name__ == '__main__':
    MY_GAME = BlackJack()