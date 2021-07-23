import random
import itertools
import time


def hand_to_numeric(hand):
    # Converts alphanumeric hand to numeric values for easier comparisons
    # Also sorts cards based on rank
    card_rank = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "T": 8, "J": 9, "Q": 10, "K": 11,
                 "A": 12}

    card_suit = {"c": 0, "d": 1, "h": 2, "s": 3}
    result = []
    for i in range(len(hand) // 2 + len(hand) % 2):
        result.append([card_rank[hand[i * 2]], card_suit[hand[i * 2 + 1]]])
    result.sort(reverse=True)
    return result


def readable_hand(hand):
    # Returns a readable version of a set of cards
    card_rank = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 7: "9", 8: "T", 9: "J", 10: "Q", 11: "K",
                 12: "A"}
    card_suit = {0: "c", 1: "d", 2: "h", 3: "s"}
    return_string = ""
    for i in hand:
        return_string += card_rank[i[0]] + card_suit[i[1]]
    return return_string


def check_flush(hand):
    # Returns True if hand is a Flush, otherwise returns False
    hand_suit = [hand[0][1], hand[1][1], hand[2][1], hand[3][1], hand[4][1]]
    for i in range(4):
        if hand_suit.count(i) == 5:
            return True
    return False


def check_quads(hand):
    # Return True if hand is Four-of-a-Kind, otherwise returns False
    # Also returns rank of four of a kind card and rank of fifth card (in case 2 ppl have quads)
    rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for i in range(13):
        if rank.count(i) == 4:
            quads_rank = i
            for j in range(13):
                if rank.count(j) == 1:
                    kicker = j
            return True, quads_rank, kicker
    return False, 99, 99


def check_straight(hand):
    # Return True if hand is a Straight, otherwise returns False
    # Also returns rank of the straight
    if hand[0][0] == hand[1][0] + 1 == hand[2][0] + 2 == hand[3][0] + 3 == hand[4][0] + 4:
        return True, hand[0][0]
    elif (hand[0][0] == 12) & (hand[1][0] == 3) & (hand[2][0] == 2) & (hand[3][0] == 1) & (hand[4][0] == 0):
        return True, 3
    else:
        return False, 99


def check_straight_flush(hand):
    # Return True if hand is a Straight Flush, otherwise returns False
    # Also returns rank of the Straight
    if check_flush(hand) & check_straight(hand)[0]:
        return True, check_straight(hand)[1]
    else:
        return False, 99


def check_full_house(hand):
    # Return True if hand is a Full House, otherwise returns False
    # Also returns rank of the trips and the pair
    rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for i in range(13):
        if rank.count(i) == 3:
            trips = i
            for j in range(13):
                if rank.count(j) == 2:
                    pair = j
                    return True, trips, pair
    return False, 99, 99


def check_trips(hand):
    # Return True if hand is a triple, otherwise returns False
    # Also returns rank of the trips and the two kickers
    rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for i in range(13):
        if rank.count(i) == 3:
            trips = i
            for j in range(13):
                if rank.count(j) == 1:
                    kicker1 = j
                    for k in range(j + 1, 13):
                        if rank.count(k) == 1:
                            kicker2 = k
                            return True, trips, [kicker2, kicker1]
    return False, 99, [99, 99]


def check_two_pair(hand):
    # Return True if hand is a Two Pair, otherwise returns False
    # Also returns rank of the Pairs and the kicker
    rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for i in range(13):
        if rank.count(i) == 2:
            pair1 = i
            for j in range(i + 1, 13):
                if rank.count(j) == 2:
                    pair2 = j
                    for k in range(13):
                        if rank.count(k) == 1:
                            kicker = k
                            return True, [pair2, pair1], kicker
    return False, [99, 99], 99


def check_pair(hand):
    # Return True if hand is a Pair, otherwise returns False
    # Also returns ranks of paired cards and kickers
    rank = [hand[0][0], hand[1][0], hand[2][0], hand[3][0], hand[4][0]]
    for i in range(13):
        if rank.count(i) == 2:
            pair = i
            for j in range(13):
                if rank.count(j) == 1:
                    kicker1 = j
                    for k in range(j + 1, 13):
                        if rank.count(k) == 1:
                            kicker2 = k
                            for l in range(k + 1, 13):
                                if rank.count(l) == 1:
                                    kicker3 = l
                                    return True, pair, kicker3, kicker2, kicker1
    return False, 99, [99, 99, 99]


def what_hand(hand):
    # Returns the rank of the hand and its kickers
    if check_straight_flush(hand)[0]:
        return 8, check_straight_flush(hand)[1]
    elif check_quads(hand)[0]:
        return 7, check_quads(hand)[1], check_quads(hand)[2]
    elif check_full_house(hand)[0]:
        return 6, check_full_house(hand)[1], check_full_house(hand)[2]
    elif check_flush(hand):
        return 5,
    elif check_straight(hand)[0]:
        return 4, check_straight(hand)[1]
    elif check_trips(hand)[0]:
        return 3, check_trips(hand)[1], check_trips(hand)[2]
    elif check_two_pair(hand)[0]:
        return 2, check_two_pair(hand)[1], check_two_pair(hand)[2]
    elif check_pair(hand)[0]:
        return 1, check_pair(hand)[1], check_pair(hand)[2]
    else:
        return 0, hand[0][0]


def what_final_hand(player_hand, community_hand):
    # Goes through all the 60 possible hands and returns the best possible combination of them
    player_cards = ([player_hand[i:i + 2] for i in range(0, len(player_hand), 2)])
    community_cards = ([community_hand[i:i + 2] for i in range(0, len(community_hand), 2)])
    all_player_cards = list(itertools.combinations(player_cards, 2))
    all_community_cards = list(itertools.combinations(community_cards, 3))
    all_hands = (list(itertools.product(all_player_cards, all_community_cards)))
    result_list = []
    for i in range(len(all_hands)):
        hand = "".join(str(item) for item in (all_hands[i][0] + all_hands[i][1]))
        result = what_hand(hand_to_numeric(hand))
        result_list.append(result)
    return max(result_list)


def categorize_hand(result):
    # Puts the hand in its category
    global rank_list
    rank = result[0]
    if rank == 0:
        rank_list[0] += 1
    elif rank == 1:
        rank_list[1] += 1
    elif rank == 2:
        rank_list[2] += 1
    elif rank == 3:
        rank_list[3] += 1
    elif rank == 4:
        rank_list[4] += 1
    elif rank == 5:
        rank_list[5] += 1
    elif rank == 6:
        rank_list[6] += 1
    elif rank == 7:
        rank_list[7] += 1
    elif result[1] == 12:
        rank_list[9] += 1
    else:
        rank_list[8] += 1


def generate_hand():
    # Generates a set of community cards and a player hand and returns them
    player_hand = []
    community_hand = []
    i = 0
    j = 0
    while i < 4:
        player_card = []
        rank = random.randint(0, 12)
        suit = random.randint(0, 3)
        player_card.append(rank)
        player_card.append(suit)
        if player_card in player_hand:
            pass
        else:
            i += 1
            player_hand.append(player_card)
    while j < 5:
        community_card = []
        rank = random.randint(0, 12)
        suit = random.randint(0, 3)
        community_card.append(rank)
        community_card.append(suit)
        if community_card in player_hand or community_card in community_hand:
            pass
        else:
            j += 1
            community_hand.append(community_card)
    return player_hand, community_hand


def main():
    global rank_list
    rank_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0
    iterations = 1000000
    start = time.time()
    for i in range(iterations):
        random_hand = generate_hand()
        player_hand = readable_hand(random_hand[0])
        community_hand = readable_hand(random_hand[1])
        result = what_final_hand(player_hand, community_hand)
        categorize_hand(result)
        total += 1
    end = time.time()
    print("High Cards: " + str(rank_list[0]))
    print("One Pairs: " + str(rank_list[1]))
    print("Two Pairs: " + str(rank_list[2]))
    print("Three of a kind: " + str(rank_list[3]))
    print("Straights: " + str(rank_list[4]))
    print("Flushes: " + str(rank_list[5]))
    print("Full Houses: " + str(rank_list[6]))
    print("Four of a kind: " + str(rank_list[7]))
    print("Straight Flushes: " + str(rank_list[8]))
    print("Royal Flushes: " + str(rank_list[9]))
    print("Total: " + str(total))
    print("Elapsed time: " + str(end - start) + "s")


if __name__ == '__main__':
    main()
