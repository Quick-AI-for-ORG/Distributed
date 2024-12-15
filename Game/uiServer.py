
"""Import libraries"""
import os
import sys
import asyncio
from flask import Flask, request, jsonify, render_template

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
players = []
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/requestServer', methods=['POST'])
async def requestServer():
    global player, gameServer, players, game
    player = Player(name=request.json.get('playerName'),master='192.168.1.44:7777')
    players.append(player)
    gameSession = int(request.json.get('gameSession')) if request.json.get('gameSession') else None
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
    global player, game
    packs = request.json.get('wordPacks')
    duration = request.json.get('duration')
    result = await player.createGame(packs, duration)
    game = Game.pbToObject(result.game)
    result = Result.pbToObject(result.result)
    return jsonify({'isSuccess': result.isSuccess, 'message': result.message})



@app.route('/lobby')
def lobby():
    global game
    return render_template('lobby.html', game=game, players=game.players)

@app.route('/gameSettings')
def gameSettings():
    global player
    return render_template('settings.html', player=player)


@app.route('/startGame', methods=['GET'])
async def startGame():
    global game, player
    result = await player.startGame(game.id)
    print(result)
    if(isinstance(result,dict) and result['result']):
        game = Game.pbToObject(result['game'])
        return jsonify({'isSuccess': result['result'].isSuccess, 'message': result['result'].message})
        if(isinstance(result,Result)):
            return jsonify({'isSuccess': result.isSuccess, 'message': result.message})
    
       

if __name__ == '__main__':
    app.run(debug=True, port=5000)
