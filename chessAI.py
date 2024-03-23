import random

pieceScores ={"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECHMATE = 1000
STALEMATE = 0
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
    
def scoreMaterial(board):
    "Score the board based on material"
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]

    return score

def findBestMoveMinMax(gs, validMoves):
    """ Helper method to make the first recursive call"""
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove )
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove

    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = - CHECHMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECHMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findBestMoveNegaMax(gs, validMoves):
    """ Helper method to make the first recursive call"""
    global nextMove
    nextMove = None
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECHMATE, CHECHMATE, 1 if gs.whiteToMove else -1)
    return nextMove

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier* scoreBoard(gs)
    maxScore = -CHECHMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = - findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier* scoreBoard(gs)
    
    maxScore = -CHECHMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = - findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: # prunning happens
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return - CHECHMATE
        else:
            return  CHECHMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]

    return score


