"""
# Copyright Nick Cheng, Kaihua Sun, 2017
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

from salboard import SALboard
from salbnode import SALBnode

# Add your functions here.


def salb2salbLL(salb):
    '''(SALboard) -> SALBnode
    given a dict representation of salboard and then make a linked list to
    represent the SALboard whose every node represents a square
    REQ: the index of each SALBnode can only used once as a key and once as
    REQ: a value of a key. it could not happen that there are two same keys
    REQ: or two keys share the same value
    REQ: the number of all the source and destination of all the snadder
    REQ: should be less than the value of numsquare
    REQ: the last node can not be the destionation or source of a snadder
    >>> salb = SALboard(10, {1: 9, 9: 1})
    >>> head = salb2salbLL(salb)
    >>> node9 = head.next.next.next.next.next.next.next.next
    >>> node10 = node9.next
    >>> node10.next == head
    True
    >>> head.snadder == node9
    True
    >>> node9.snadder == head
    True
    >>> salb = SALboard(10, {1: 2, 2: 3, 3: 4, 6: 5})
    >>> head = salb2salbLL(salb)
    >>> node2 = head.next
    >>> node3 = node2.next
    >>> node4 = node3.next
    >>> node5 = node4.next
    >>> node6 = node5.next
    >>> head.snadder == node2
    True
    >>> node2.snadder == node3
    True
    >>> node6.snadder == node5
    True
    '''
    # get the information of the numsquares and snadders
    numsquares = salb.numSquares
    snadders = salb.snadders
    # create a new_dict to make a copy of the given snadder
    new_dict = {}
    for key in snadders:
        new_dict[key] = snadders[key]
    # create the same number of SALBnode according to the value of numsqures
    head = None
    for num in range(numsquares):
        # create a SALBnode class object and add it to the end of the linked
        # list
        new_node = SALBnode()
        # if the head is none, then head is equal to the new node
        if head is None:
            head = new_node
            curr = head
        # if head is not empty, then link it to the end
        else:
            curr.next = new_node
            curr = curr.next
    # link the last node to the first node
    curr.next = head
    # set the curr as the head
    curr = head
    # loop through each node, and use a index to represents the index ofw
    # this node
    for index in range(1, numsquares+1):
        # if the node at the index is one source of a snadder, then
        # replace the key in the dict with this node and delete the
        # original key_value pair
        if index in new_dict:
            new_dict[curr] = new_dict[index]
            del new_dict[index]
        # get to the next node
        curr = curr.next
    # change the order of the key and value
    changed_dict = {}
    for key in new_dict:
        changed_dict[new_dict[key]] = key
    curr = head
    # like what I have done before, this time I also use node to replace the
    # the key
    for index in range(1, numsquares+1):
        # use key to represents the node at the index
        if index in changed_dict:
            changed_dict[curr] = changed_dict[index]
            del changed_dict[index]
        # get to the next node
        curr = curr.next
    # link the snadders
    for source_node in changed_dict:
        changed_dict[source_node].snadder = source_node
    # return the head of the linked list representation of the SALboard
    return head


def willfinish(first, stepsize):
    '''
    (SALBnode, int) -> bool
    given a snakes and ladder board and a stepsize, then find out whether
    the person will land on the last square. If yes, then return True. If
    there is a loop, and the player will not reach the end, then return
    False
    REQ: the first should not be None and must be a SALBnode
    REQ: the stepsize should be a positive integer
    >>> salb = SALboard(10, {1: 2, 2: 3, 3: 5, 7: 6})
    >>> head = salb2salbLL(salb)
    >>> willfinish(head, 1)
    False
    >>> willfinish(head, 2)
    True
    >>> willfinish(head, 3)
    False
    >>> willfinish(head, 4)
    True
    >>> willfinish(head, 5)
    True
    >>> willfinish(head, 6)
    True
    >>> willfinish(head, 7)
    True
    >>> willfinish(head, 8)
    True
    >>> willfinish(head, 9)
    False
    >>> willfinish(head, 10)
    True
    '''
    # if one player step into one square twice, then it means there is a loop
    # so I just need to count the number of moves, if the number of moves is
    # greater than that of the squares. Then there must be a loop
    # firstlly,find the end SALBnode and the total number of squares
    curr = first
    square_counter = 1
    while(curr.next != first):
        # find the last SALBnode and do the square counting
        curr = curr.next
        square_counter += 1
    # noew curr stop at the last square and store the address of this node
    end_SALBnode = curr
    # create a move_counter to count the number of moves
    move_counter = 0
    # firstly, we do not finish, so we set finish as False
    finish = False
    # set curr as the start_point and start running
    curr = first
    curr = move_certain_step(curr, stepsize - 1)
    # set the move_counter to store the total number of moves
    move_counter = 1
    # if does not stop at the end and the number of move is not greater than
    # the number of squares, then move the curr by stepsize of squares
    while(move_counter < square_counter + 1 and not finish):
        curr = move_certain_step(curr, stepsize)
        move_counter += 1
        # if it has finished, then set finish True
        if(curr == end_SALBnode):
            finish = True
    # return whether the person has finished the game after certain moves
    return finish


def whowins(first, step1, step2):
    '''
    (SALBnode, int, int) -> int
    given a SALboard and two stepsize for two players and return which
    person will win the game. The first person that reached the end
    win the game. If both of two players are in loop and will not reach the
    end, then the winner will the second player.
    REQ: the first should not be None and it must be a SALBnode.
    REQ: both step1 and step2 should be positive integers
    >>> salb = SALboard(10, {1: 2, 2: 3, 3: 5, 7: 6})
    >>> head = salb2salbLL(salb)
    >>> whowins(head, 1, 2)
    2
    >>> whowins(head, 2, 1)
    1
    >>> whowins(head, 1, 3)
    2
    >>> whowins(head, 2, 4)
    1
    >>> whowins(head, 5, 2)
    1
    >>> whowins(head, 2, 5)
    2
    '''
    # check whether fplayer and splayer will finish the game
    fplayer_finish = willfinish(first, step1)
    splayer_finish = willfinish(first, step2)
    # if fplayer will finish and splayer will not finish, then the winner is
    # first player
    if(fplayer_finish is True and splayer_finish is False):
        winner = 1
    # if both player will loop, then the winner is splayer
    elif(fplayer_finish is False):
        winner = 2
    # if both fplayer and splayer will reach the end, then I
    # need to judge who will win the game first
    elif(fplayer_finish is True and splayer_finish is True):
        # find the last SALBnode
        temp = first
        while(temp.next != first):
            temp = temp.next
        end_SALBnode = temp
        # first do not know the winner, so set it as None
        winner = None
        # put the fplayer and splayer at the first
        fplayer = first
        splayer = first
        fplayer = move_certain_step(fplayer, step1 - 1)
        splayer = move_certain_step(splayer, step2 - 1)
        # judge whether it will reach end_SALBnode
        if(fplayer == end_SALBnode):
            winner = 1
        if(splayer == end_SALBnode and winner != 1):
            winner = 2
        # if there do not generate a winner, then fplayer and splayer move
        # by turn
        while(winner != 1 and winner != 2):
            fplayer = move_certain_step(fplayer, step1)
            # if the fplayer has reached the end square and winner has not
            # generated, then winner is fplayer
            if(fplayer == end_SALBnode and winner != 2):
                winner = 1
            # likewise, do the same thing to splayer
            splayer = move_certain_step(splayer, step2)
            # if splayer reached the end and the winner haven't been generated
            if(splayer == end_SALBnode and winner != 1):
                winner = 2
    # finally return the number of the winner
    return winner


def dualboard(first):
    '''
    (SALBnode) -> SALBnode
    given a linked_list representation of board, then replicate it as a
    new linked_list representation of SALboard. But the new SALboard turn
    snake into ladder and turn ladder into snake.

    I will create a dual board in three steps.

    first step is create a temp_node to link the nodes with the same index
    in both original board and dualboard

    The second step is set the new snadders in the dual board which has the
    opposite direction to the snadders in the original board

    The third step is delete all the temp_node and change the original
    linked list back into what it originally looks like
    REQ: the first should not be None and it must be a SALBnode
    >>> salb = SALboard(10, {1: 2, 2: 3, 3: 5, 7: 6, 8: 9, 9: 8})
    >>> head = salb2salbLL(salb)
    >>> dual_head = dualboard(head)
    >>> dual_node2 = dual_head.next
    >>> dual_node3 = dual_node2.next
    >>> dual_node4 = dual_node3.next
    >>> dual_node5 = dual_node4.next
    >>> dual_node6 = dual_node5.next
    >>> dual_node7 = dual_node6.next
    >>> dual_node8 = dual_node7.next
    >>> dual_node9 = dual_node8.next
    >>> dual_node10 = dual_node9.next
    >>> dual_node10.next == dual_head
    True
    >>> dual_node8.snadder == dual_node9
    True
    >>> dual_node9.snadder == dual_node8
    True
    >>> dual_node5.snadder == dual_node3
    True
    >>> dual_node3.snadder == dual_node2
    True
    >>> dual_node2.snadder == dual_head
    True
    '''
    # first set the curr that points to the first and set new_head None
    # new_head is the head of the dual_board
    curr = first
    new_head = None
    # set the new_head with the first new_node and set the dual_curr at
    # the same time
    new_node = SALBnode()
    new_head = new_node
    dual_curr = new_head
    # after seting the value, I will link the first nodes in both linked
    # lists
    create_link_node(curr, dual_curr)
    # for the rest nodes, link nodes at the same index in two linked lists
    while(curr.next != first):
        # every time create a new node and add it to the end of the dual
        # board
        new_node = SALBnode()
        dual_curr.next = new_node
        dual_curr = dual_curr.next
        # find the next node in the original linked list and dual board
        # and link them
        curr = curr.next
        create_link_node(curr, dual_curr)
    # finally I need to link the last node to the new head in the dual board
    dual_curr.next = new_head
    # create all the new_snadders in the dualboard
    curr = first
    dual_curr = new_head
    create_dual_snadder(curr)
    # after dealing with the first node, then deal with the other nodes
    while(curr.next != first):
        # find next nodes in both original linked list and the dual linked
        # list
        curr = curr.next
        dual_curr = dual_curr.next
        create_dual_snadder(curr)
    # after creating dualboard, I will change the original board back to what
    # it was originally
    curr = first
    # I need to delete all temp_node for the first node and reset its snadder
    # attribute
    delete_temp_node(curr)
    # after dealing with the first node, then deal with other nodes in the
    # in the original_list
    while(curr.next != first):
        # loop through every node in the original board and reset its snadder
        # attribute.
        curr = curr.next
        delete_temp_node(curr)
    # return the dualboard head
    return new_head


def move_certain_step(input_node, stepsize):
    '''
    (SALBnode, int) -> SALBnode
    Given a node and a stepsize, then move this player by stepsize of nodes
    If this player stop at a node which is the source of a snadder, then move
    it to the destination fo that snadder
    REQ: stepsize > 0
    REQ: the input_node should not be None
    >>> salb = SALboard(10, {1: 2, 2: 3, 3: 5, 7: 6, 8: 9, 9: 8})
    >>> head = salb2salbLL(salb)
    >>> node2 = head.next
    >>> node3 = node2.next
    >>> node4 = node3.next
    >>> node5 = node4.next
    >>> node6 = node5.next
    >>> node7 = node6.next
    >>> node8 = node7.next
    >>> node9 = node8.next
    >>> node10 = node9.next
    >>> player = head
    >>> move_certain_step(player, 3) == node4
    True
    >>> move_certain_step(player, 6) == node6
    True
    >>> player = move_certain_step(player, 1)
    >>> player == node3
    True
    >>> player = move_certain_step(player, 7)
    >>> player == node10
    True
    '''
    # move stepsize of squares forward
    for count in range(stepsize):
        input_node = input_node.next
    # check whether this node is the source of a snadder
    if input_node.snadder is not None:
        input_node = input_node.snadder
    return input_node


def create_link_node(original_list_node, new_node):
    '''
    (SALBnode, SALBnode) -> None
    Given two node, the first node is the node in the original list, the
    second node is the node in the dual list.
    Everytime, create a temporary node and use its next attibute to link
    the nodes in both the original linked list and dualboard linked.
    If the node in the original linked list is a snadder source, then use
    the new node's snadder attribute to store the snadder destination.
    >>> salb = SALboard(5, {1: 2, 2: 3, 4: 5, 5: 4})
    >>> dual_board = SALboard(5, {})
    >>> head = salb2salbLL(salb)
    >>> dual_head = salb2salbLL(dual_board)
    >>> node2 = head.next
    >>> node3 = node2.next
    >>> node4 = node3.next
    >>> node5 = node4.next
    >>> dual_node2 = dual_head.next
    >>> dual_node3 = dual_node2.next
    >>> dual_node4 = dual_node3.next
    >>> dual_node5 = dual_node4.next
    >>> create_link_node(head, dual_head)
    >>> create_link_node(node2, dual_node2)
    >>> create_link_node(node3, dual_node3)
    >>> create_link_node(node4, dual_node4)
    >>> create_link_node(node5, dual_node5)
    >>> node2.snadder.next == dual_node2
    True
    >>> node2.snadder.snadder == node3
    True
    >>> node3.snadder.snadder == None
    True
    >>> node3.snadder.next == dual_node3
    True
    >>> node4.snadder.next == dual_node4
    True
    >>> node4.snadder.snadder == node5
    True
    '''
    # create a temp_node and link its next to the node in the dualboard
    temp_node = SALBnode(new_node)
    # if the original_list_node has a nonempty snadder attribute
    # then store it in the temp_node's snadder
    if(original_list_node.snadder is not None):
        temp_node.snadder = original_list_node.snadder
    # change the original_list_node.snadder attribute to the temp_node
    original_list_node.snadder = temp_node
    # it should return None
    return None


def create_dual_snadder(original_list_node):
    '''
    (SALBnode, SALbnode) -> None
    Given one node which is the node in the original list. Check
    whether the original_list_node is one source of a snadder. Then create
    the new snadder in the dualboard linked list. If not, then do nothing.
    REQ: the original_list_node and new_node should not be None.
    >>> salb = SALboard(5, {1: 2, 2: 3, 4: 5, 5: 4})
    >>> dual_board = SALboard(5, {})
    >>> head = salb2salbLL(salb)
    >>> dual_head = salb2salbLL(dual_board)
    >>> node2 = head.next
    >>> node3 = node2.next
    >>> node4 = node3.next
    >>> node5 = node4.next
    >>> dual_node2 = dual_head.next
    >>> dual_node3 = dual_node2.next
    >>> dual_node4 = dual_node3.next
    >>> dual_node5 = dual_node4.next
    >>> create_link_node(head, dual_head)
    >>> create_link_node(node2, dual_node2)
    >>> create_link_node(node3, dual_node3)
    >>> create_link_node(node4, dual_node4)
    >>> create_link_node(node5, dual_node5)
    >>> create_dual_snadder(head)
    >>> create_dual_snadder(node2)
    >>> create_dual_snadder(node3)
    >>> create_dual_snadder(node4)
    >>> create_dual_snadder(node5)
    >>> dual_node2.snadder == dual_head
    True
    >>> dual_node3.snadder == dual_node2
    True
    >>> dual_node4.snadder == dual_node5
    True
    >>> dual_node5.snadder == dual_node4
    True
    >>> dual_head.snadder == None
    True
    '''
    # find out whether the original_list_node is a source of a snadder
    if(original_list_node.snadder.snadder is not None):
        # if the original_ist_node is a snadder source, then create new
        # snadder in the dualboard linked list
        original_list_node.snadder.snadder.snadder.next.snadder =\
            original_list_node.snadder.next
    # it should return None
    return None


def delete_temp_node(original_list_node):
    '''
    (SALBnode) -> None
    Given two node, the first node is the node in the original list. the second
    node is the node in the dual list. Delete all the linked_nodes that were
    created before and change the nodes in the original_linked_list back
    to what it was originally.
    >>> salb = SALboard(5, {1: 2, 2: 3, 4: 5, 5: 4})
    >>> dual_board = SALboard(5, {})
    >>> head = salb2salbLL(salb)
    >>> dual_head = salb2salbLL(dual_board)
    >>> node2 = head.next
    >>> node3 = node2.next
    >>> node4 = node3.next
    >>> node5 = node4.next
    >>> dual_node2 = dual_head.next
    >>> dual_node3 = dual_node2.next
    >>> dual_node4 = dual_node3.next
    >>> dual_node5 = dual_node4.next
    >>> create_link_node(head, dual_head)
    >>> create_link_node(node2, dual_node2)
    >>> create_link_node(node3, dual_node3)
    >>> create_link_node(node4, dual_node4)
    >>> create_link_node(node5, dual_node5)
    >>> create_dual_snadder(head)
    >>> create_dual_snadder(node2)
    >>> create_dual_snadder(node3)
    >>> create_dual_snadder(node4)
    >>> create_dual_snadder(node5)
    >>> delete_temp_node(head)
    >>> delete_temp_node(node2)
    >>> delete_temp_node(node3)
    >>> delete_temp_node(node4)
    >>> delete_temp_node(node5)
    >>> head.snadder == node2
    True
    >>> node2.snadder == node3
    True
    >>> node3.snadder == None
    True
    >>> node4.snadder == node5
    True
    >>> node5.snadder == node4
    True
    '''
    # the third step is delete all the temp_node and change the snadder to
    # its original_snadder
    original_list_node.snadder = original_list_node.snadder.snadder
    # It should return None
    return None