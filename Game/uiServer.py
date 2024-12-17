
"""Import libraries"""
import os
import sys
import asyncio
from flask import Flask, request, jsonify, render_template, redirect, url_for

"""Import Folder Paths"""
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

from Entity.Game import Game
from Entity.Player import Player
from Entity.Result import Result
from Entity.GameServer import GameServer

app = Flask(__name__)
player = None
gameServer = None
game = None
words = []
word = None

@app.errorhandler(Exception)
def handle_all_errors(e):
    return redirect(url_for('main'))

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/game')
def game():
    global player, game
    return render_template('game.html',player=player, players=game.players,game=game, round=f"Round {game.round}", role=game.getRole(player))

@app.route('/requestServer', methods=['POST'])
async def requestServer():
    global player, gameServer, players, game
    player = Player(name=request.json.get('playerName'),master='10.3.8.31:7777')
    try:
        gameSession = int(request.json.get('gameSession')) if request.json.get('gameSession') else None
    except ValueError:
        return jsonify({"isSucceeded": False, "message":"Game Session ID has to be an number"})
    result = await player.requestServer(gameSession)
    
    if result.result.isSuccess:
        gameServer = result.gameServerAddress
        if gameSession is None:
            result = await player.connectPlayer(result.gameServerAddress)
            return jsonify({'isSuccess': result.isSuccess, 'message': result.message})
        
        elif gameSession is not None:
            result = await player.connectToGame(request.json.get('playerName'),result.gameServerAddress, gameSession)
            if(isinstance(result,dict) and result['result']):
                if(result['result'].isSuccess): game = Game.pbToObject(result['game'])
                return jsonify({'isSuccess': result['result'].isSuccess, 'message': result['result'].message})
            if(isinstance(result,Result)):
                return jsonify({'isSuccess': result.isSuccess, 'message': result.message})
    else :
        return jsonify({'isSuccess': result.result.isSuccess, 'message': result.result.message})
            

@app.route('/disconnectPlayer', methods=['GET'])
async def disconnectPlayer():
    global player
    result = await player.disconnectPlayer()
    return jsonify({'isSuccess': result.isSuccess, 'message': result.message})


@app.route('/createGame', methods=['POST'])
async def createGame():
    global player, game, words
    packs = request.json.get('wordPacks')
    duration = request.json.get('duration')
    result = await player.createGame(packs, duration)
    game = Game.pbToObject(result.game)
    words = game.words
    result = Result.pbToObject(result.result)
    if(isinstance(result,Result)): return notDict(result)



@app.route('/lobby')
def lobby():
    global game, words
    return render_template('lobby.html', game=game, players=game.players)

@app.route('/gameSettings')
def gameSettings():
    global player
    return render_template('settings.html', player=player)


@app.route('/startGame', methods=['GET'])
async def startGame():
    global game, player
    result = await player.startGame(game.id)
    if(isinstance(result,Result)): return notDict(result)
    if(isinstance(result,dict) and result['result']):
        game = Game.pbToObject(result['game'])
        return jsonify({'isSuccess': result['result'].isSuccess, 'message': result['result'].message})

    
       
@app.route('/sendUpdate', methods=['POST'])
async def addInput():
    global player, game
    input = request.json.get('input')
    badClue = rejectClue(input)  
    badGuess = rejectGuess(input)
    if badClue == False and badGuess == False:
        result = await player.sendUpdate(request.json.get('input'), game.id)
        if(isinstance(result,Result)): return notDict(result)
        if(isinstance(result,dict) and result['result']):
            game = Game.pbToObject(result['game'])    
            player.health = result['health']
            player.score = result['score']        
            return jsonify({
                'isSuccess': result['result'].isSuccess, 
                'message': str(result['result']), 
                'input' :list(game.playersInput),
                'round': f"Round {game.round}",
                'score': player.score,
                'health': player.health
                })

        
    if badClue: return badClue
    if badGuess: return badGuess
  
  
@app.route('/recieveUpdate', methods=['GET'])
async def update():
    global player, game
    result = await player.recieveUpdate(game.id)
    if(isinstance(result,Result)): return notDict(result)
    if(isinstance(result,dict) and result['result']):
        player.health = result['health']
        player.score = result['score']
        game = Game.pbToObject(result['game'])   
        return jsonify({
            'isSuccess': result['result'].isSuccess, 
            'message': str(result['result']), 
            'input' :list(game.playersInput),
            'round': f"Round {game.round}",
            'score': player.score,
            'health': player.health
            })

  




@app.route('/roundStart', methods=['GET'])
async def newRound():
    global player, game, word
    result = await player.recieveUpdate(game.id)
    if(isinstance(result,Result)): return notDict(result)
      
    if(isinstance(result,dict) and result['result']):
        game = Game.pbToObject(result['game']) 
        word = game.getWord()
        role = game.getRole(player)
        if role == 'Clue Giver':
            return jsonify({
                    'isSuccess': result['result'].isSuccess, 
                    'message': str(result['result']), 
                    'round': f"Round {game.round}",
                    'role': role,
                    'word': word,
                    'score': player.score,
                    'health': player.health
                })   
        else:
            return jsonify({
                    'isSuccess': result['result'].isSuccess, 
                    'message': str(result['result']), 
                    'round': f"Round {game.round}",
                    'role': role,
                    'clueGiver': game.getClueGiver().name,
                    'score': player.score,
                    'health': player.health
                })   
    
    
    
def rejectClue(input):
    global game, player, word
    if game.getRole(player) == 'Clue Giver' or game.getClueGiver() == player:
        if not game.validateClue(input):
            return jsonify({
                 'isSuccess': False, 
                 'message': F"Clue cannot be the word itself", 
                 'round': f"Round {game.round}",
            })
    return False


def rejectGuess(input):
    global player, game
    if game.getRole(player) != 'Clue Giver' and game.getClueGiver() != player:
        if player.health == 0:
             return jsonify({
                 'isSuccess': False, 
                 'message': F"No more tries left for this round", 
                 'round': f"Round {game.round}",
            })
    return False
def notDict(result):
      return jsonify({'isSuccess': result.isSuccess, 'message': str(result)})  

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
    
